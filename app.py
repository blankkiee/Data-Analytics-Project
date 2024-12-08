import streamlit as st
import pandas as pd
import plotly.express as px
from sidebar import create_sidebar
from theme import set_page_mode
from header import render_header
from data_utils import clean_data
from aitest import generate_comments

# Main app
st.set_page_config(layout="wide")

# Sidebar logic
uploaded_file = None  # Initialize file
mode, uploaded_file, selected_visualization, num_rows, clean_data_options = create_sidebar(uploaded_file)

# Set page mode
set_page_mode(mode)

# Render header
render_header()

if uploaded_file:
    try:
        # Load uploaded CSV
        df = pd.read_csv(uploaded_file)

        # Apply cleaning options only after file upload
        if clean_data_options:
            df = clean_data(df, clean_data_options)

        # Display cleaned data preview
        st.write(f"### Cleaned Data Preview ({num_rows} rows)")
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
            fig = px.scatter(df, x=x_axis, y=y_axis, title=f"Scatter Plot of {y_axis} vs {x_axis}")
            st.plotly_chart(fig, use_container_width=True)
        elif selected_visualization == "Table":
            st.write("### Full Data Table")
            st.write(df)

        # Add comments and download options
        st.write("### Comments or Observations")
        comments = st.text_area(
            "Add your comments or observations about the visualization here:",
            placeholder="Enter your thoughts...",
            height=200
        )

        st.write("### Generate Report")
        if st.button("Generate Report"):
            if comments.strip():
                csv_data = df.to_csv(index=False)
                full_report = f"User Comments:\n\n{comments}\n\nCleaned Data:\n{csv_data}"
                st.download_button(
                    label="Download CSV Report",
                    data=full_report,
                    file_name="report_with_comments.csv",
                    mime="text/csv"
                )
            else:
                st.warning("Please add comments before generating the report.")
    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
else:
    st.info("Please upload a CSV file to start.")
