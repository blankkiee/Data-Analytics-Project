import streamlit as st
import pandas as pd
import plotly.express as px
from sidebar import create_sidebar
from theme import set_page_mode
from header import render_header
from data_utils import clean_data

# Main app
st.set_page_config(layout="wide")

# Sidebar logic
mode, uploaded_file, selected_visualization, num_rows, clean_data_options = create_sidebar()

# page selected mode
set_page_mode(mode)

# Render header
render_header()

# process uploaded file
if uploaded_file:
    try:
        # Load and clean data
        df = pd.read_csv(uploaded_file)
        df = clean_data(df, clean_data_options)

        # Display data preview
        st.write(f"### Data Preview ({num_rows} rows)")
        st.write(df.head(num_rows))

        # Visualization
        if selected_visualization == "Bar Chart":
            x_axis = st.selectbox("Select X-Axis", df.columns)
            y_axis = st.selectbox("Select Y-Axis", df.columns)
            fig = px.bar(df, x=x_axis, y=y_axis, title=f"Bar Chart of {y_axis} vs {x_axis}")
            st.plotly_chart(fig, use_container_width=True)
        elif selected_visualization == "Line Chart":
            x_axis = st.selectbox("Select X-Axis", df.columns)
            y_axis = st.selectbox("Select Y-Axis", df.columns)
            fig = px.line(df, x=x_axis, y=y_axis, title=f"Line Chart of {y_axis} over {x_axis}")
            st.plotly_chart(fig, use_container_width=True)
        elif selected_visualization == "Scatter Plot":
            x_axis = st.selectbox("Select X-Axis", df.columns)
            y_axis = st.selectbox("Select Y-Axis", df.columns)
            # color = st.selectbox("Select Color (Optional)", [None] + list(df.columns))
            fig = px.scatter(df, x=x_axis, y=y_axis, title=f"Scatter Plot of {y_axis} vs {x_axis}")
            st.plotly_chart(fig, use_container_width=True)
        elif selected_visualization == "Table":
            st.write("### Full Data Table")
            st.write(df)
            
    # Add a Textbox Under Visualization
        st.write("### Comments or Observations")
        comments = st.text_area(
            "Add your comments or observations about the visualization here:",
            placeholder="Enter your thoughts...",
            height=200
        )
        
        # Generate Report Button
        st.write("### Generate Report")
        
        # Prepare data for report
        report_data = {
            "Cleaned Data": df,
            "User Comments": comments
        }
# # Wrong Logic
#         # Generate Report Button
#         if st.button("Generate Report"):
#             st.download_button(
#                 label="Download CSV Report",
#                 data=df.to_csv(index=False),
#                 file_name="generated_report.csv",
#                 mime="text/csv",
#             )

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
else:
    st.info("Please upload a CSV file to start.")

