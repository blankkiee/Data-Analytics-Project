import streamlit as st
from aitest import suggest_chart

def create_sidebar(uploaded_file, df):
    # Load the uploaded file into a DataFrame
    chart_type = None
    x_axis = None
    y_axis = None
    x_axis_dtype = None
    y_axis_dtype = None
    with st.sidebar: 
        # LOGO
        st.markdown("""
                    
                    <h1 style="font-size: 3rem; text-align: 'center'">🗿 Pogi Only</h1>
                    """, unsafe_allow_html=True)
        
        # Navigation
        st.markdown("Upload a CSV file, clean your data, and choose visualization options.")

        if df.isnull().values.any():
            st.info("🟡 Data is dirty")
        else:
            st.info("🟢 Data is clean")
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
            #  Revised Layout for X and Y Axis Dropdowns
            col1, col2 = st.columns(2)
            with col1:
                # st.write("X axis")
                x_axis = st.selectbox("X axis", df.columns, key="x_axis")
                x_axis_dtype = df[x_axis].dtype
                if x_axis_dtype == 'object': 
                    sample_value = df[x_axis].iloc[0] 
                    x_axis_dtype = type(sample_value).__name__

            with col2:
                # st.write("Y axis")
                y_axis = st.selectbox("Y axis", df.columns, key="y_axis")
                y_axis_dtype = df[x_axis].dtype
                if y_axis_dtype == 'object': 
                    sample_value = df[y_axis].iloc[0] 
                    y_axis_dtype = type(sample_value).__name__

            # suggestion = suggest_chart(x_axis, x_axis_dtype, y_axis, y_axis_dtype)
            # st.write(suggestion)
            
            # Chart Type Dropdown Below the Axes
            # st.markdown("<label style='font-weight: bold; font-size: 14px;'>Chart Type</label>", unsafe_allow_html=True)
            chart_type = st.selectbox("Chart Type", ["Bar Chart", "Line Chart", "Scatter Plot", "Table"], key="chart_type")
            if st.button("Visualize!"):
                st.session_state.chart_data = chart_type, x_axis, y_axis, x_axis_dtype, y_axis_dtype
                return clean_data_options

        
        return clean_data_options