import numpy as np
import streamlit as st
from aitest import suggest_chart
import altair as alt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

def create_sidebar(uploaded_file, df):
    # Load the uploaded file into a DataFrame
    chart_type = None
    x_axis = None
    y_axis = None
    x_axis_dtype = None
    y_axis_dtype = None
    aggregation_method = None
    
    with st.sidebar: 
        # LOGO
        st.markdown("""
                    
                    <h1 style="font-size: 3rem; text-align: 'center'">🗿 Pogi Only</h1>
                    """, unsafe_allow_html=True)
        
        # Navigation
        st.markdown("Upload a CSV file, clean your data, and choose visualization options.")

        numeric_columns = df.select_dtypes(include=[np.number]).columns
        if not df[numeric_columns].applymap(np.isreal).all().all():
            st.warning("Data contains non-numeric values in numeric columns", icon="🟡")
            st.session_state.is_clean = False

        if df.isnull().values.any():
            st.warning("Data contains missing values", icon="🟡")
            st.session_state.is_clean = False

        elif df.duplicated().any():
            st.warning("Data contains duplicate rows", icon="🟡")
            st.session_state.is_clean = False

        else:
            st.info("Data is clean", icon="🟢")
            st.session_state.is_clean = True
        
        # Data Cleaning Options
        st.divider()
        with st.expander("Clean"):
            st.header("Data Cleaning Options")
            clean_data_options = {
                "Standardize column names": st.checkbox("Standardize column names (lowercase, no spaces)"),
                "Remove duplicates": st.checkbox("Remove duplicate rows"),
                "Handle missing values": st.selectbox(
                    "Handle missing values",
                    ["None", "Drop rows with missing values", "Fill missing values with 0"]
                ),
            }

        with st.expander("Visualize"):
            # Revised Layout for X and Y Axis Dropdowns
            col1, col2 = st.columns(2)
            with col1:
                # x-axis selectbox
                x_axis = st.selectbox("X axis", df.columns, key="x_axis")
                x_axis_dtype = df[x_axis].dtype
                if x_axis_dtype == 'object': 
                    sample_value = df[x_axis].iloc[0] 
                    x_axis_dtype = type(sample_value).__name__

            with col2:
                # y-axis selectbox
                
                y_axis = st.selectbox("Y axis", df.columns, key="y_axis")
                y_axis_dtype = df[y_axis].dtype
                if y_axis_dtype == 'object': 
                    sample_value = df[y_axis].iloc[0] 
                    y_axis_dtype = type(sample_value).__name__

            # Aggregation method dropdown
            aggregation_method = st.selectbox(
                "Aggregation Method", 
                ["Individual", "Count", "Sum", "Average", "Min", "Max", "Median", "Mode"], 
                key="aggregation_method"
            )

            suggestion = suggest_chart(x_axis, x_axis_dtype, y_axis, y_axis_dtype, aggregation_method)
            st.write(suggestion)
            # Chart Type Dropdown Below the Axes
            chart_type = st.selectbox("Chart Type", ["Bar Chart", "Line Chart", "Scatter Plot", "Grouped Bar Chart", "Layered Histogram", "Pie Chart","Table"], key="chart_type")
            if st.button("Visualize!"):
                # Apply aggregation if selected
                if aggregation_method == "Count" or x_axis_dtype == 'object' or y_axis_dtype == 'object': 
                    # Count occurrences for categorical data 
                    df_counts = df.groupby([x_axis, y_axis]).size().reset_index(name='counts')
                elif aggregation_method == "Sum":
                    df_counts = df.groupby(x_axis)[y_axis].sum().reset_index()
                elif aggregation_method == "Average":
                    df_counts = df.groupby(x_axis)[y_axis].mean().reset_index()
                elif aggregation_method == "Min":
                    df_counts = df.groupby(x_axis)[y_axis].min().reset_index()
                elif aggregation_method == "Max":
                    df_counts = df.groupby(x_axis)[y_axis].max().reset_index()
                elif aggregation_method == "Median":
                    df_counts = df.groupby(x_axis)[y_axis].median().reset_index()
                elif aggregation_method == "Mode":
                    df_counts = df.groupby(x_axis)[y_axis].apply(lambda x: x.mode()[0]).reset_index()
                else: 
                    df_counts = df

                st.session_state.chart_data = chart_type, x_axis, y_axis, x_axis_dtype, y_axis_dtype, df_counts
                st.session_state.agg_method = aggregation_method
                return clean_data_options
        
        is_clean = st.session_state.get('is_clean', True)
        chart_type, x_axis, y_axis, x_axis_dtype, y_axis_dtype, df_counts = st.session_state.get('chart_data', (None, None, None, None, None, None))
   
        with st.expander("Predict"):
            st.write("Make a prediction")
            if is_clean:
                col1, col2 = st.columns(2)
                with col1:
                    # x-axis selectbox
                    x_axis = st.selectbox("X", df.columns, key="predict_x")
                    x_axis_dtype = df[x_axis].dtype
                    if x_axis_dtype == 'object': 
                        sample_value = df[x_axis].iloc[0] 
                        x_axis_dtype = type(sample_value).__name__

                with col2:
                    # y-axis selectbox
                    
                    y_axis = st.selectbox("Y", df.columns, key="predict_y")
                    y_axis_dtype = df[y_axis].dtype
                    if y_axis_dtype == 'object': 
                        sample_value = df[y_axis].iloc[0] 
                        y_axis_dtype = type(sample_value).__name__
                
                # Train a linear regression model 
                X = df[[x_axis]] 
                y = df[y_axis] 
                model = LinearRegression() 
                model.fit(X, y)

                # Create scatter plot and regressio n line 
                scatter = alt.Chart(df).mark_circle(size=60).encode( 
                    x=x_axis, 
                    y=y_axis, 
                    tooltip=[x_axis, y_axis]
                ).properties(
                    title=f"Linear Regression Prediction of {y_axis} vs {x_axis}", 
                ).interactive()

                line = scatter.transform_regression( 
                    x_axis, y_axis 
                    ).mark_line(color='red')

                chart = scatter + line
                st.altair_chart(chart, use_container_width=True)

                if st.button("Add to Report"):
                    st.session_state.prediction_chart = chart, x_axis, y_axis
            else:
                st.warning("Clean the data first", icon="🟡")

        if is_clean:
            st.download_button(
                label="Download Clean CSV",
                data=df.to_csv(index=False),
                file_name="clean_data.csv",
                mime="text/csv",
            )
        return clean_data_options