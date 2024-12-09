from io import BytesIO
import streamlit as st
import pandas as pd
import plotly.express as px
from sidebar import create_sidebar
from theme import set_page_mode
from header import render_header
from data_utils import clean_data
from aitest import generate_comments, suggest_chart
from PIL import Image

# CSS for the bubble animation
bubble_css = """
<style>
body {
    background: #0e0e0e;
    overflow: hidden;
}

.bubble {
    position: absolute;
    width: 40px;
    height: 40px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 50%;
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
    animation: float 10s infinite;
}

@keyframes float {
    0% {
        transform: translateY(0) rotate(0deg);
        opacity: 1;
        border-radius: 50%;
    }
    100% {
        transform: translateY(-1000px) rotate(720deg);
        opacity: 0;
        border-radius: 0;
    }
}

.bubble:nth-child(1) {
    left: 10%;
    animation-duration: 8s;
    animation-delay: 1s;
}

.bubble:nth-child(2) {
    left: 20%;
    animation-duration: 10s;
    animation-delay: 3s;
}

.bubble:nth-child(3) {
    left: 30%;
    animation-duration: 12s;
    animation-delay: 5s;
}

.bubble:nth-child(4) {
    left: 40%;
    animation-duration: 7s;
    animation-delay: 2s;
}

.bubble:nth-child(5) {
    left: 50%;
    animation-duration: 9s;
    animation-delay: 4s;
}

.bubble:nth-child(6) {
    left: 60%;
    animation-duration: 11s;
    animation-delay: 6s;
}

.bubble:nth-child(7) {
    left: 70%;
    animation-duration: 13s;
    animation-delay: 8s;
}

.bubble:nth-child(8) {
    left: 80%;
    animation-duration: 10s;
    animation-delay: 1s;
}

.bubble:nth-child(9) {
    left: 90%;
    animation-duration: 14s;
    animation-delay: 3s;
}

.bubble:nth-child(10) {
    left: 95%;
    animation-duration: 16s;
    animation-delay: 5s;
}
</style>
"""

# HTML for the bubbles
bubble_html = """
<div class="bubble"></div>
<div class="bubble"></div>
<div class="bubble"></div>
<div class="bubble"></div>
<div class="bubble"></div>
<div class="bubble"></div>
<div class="bubble"></div>
<div class="bubble"></div>
<div class="bubble"></div>
<div class="bubble"></div>
"""




# Main app
st.set_page_config(layout="wide")
# Add the custom CSS and HTML to Streamlit
st.markdown(bubble_css, unsafe_allow_html=True)
st.markdown(bubble_html, unsafe_allow_html=True)

if "text_area_content" not in st.session_state: 
    st.session_state.text_area_content = ""

if "chart_data" not in st.session_state:
    st.session_state.chart_data = None,None,None,None,None,

# Sidebar logic
uploaded_file = None  # Initialize file
# File upload

# Set page mode
set_page_mode("Dark")

# Render header
render_header()
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])


if uploaded_file:
    
    try:
        # Load uploaded CSV
        df = pd.read_csv(uploaded_file)
        clean_data_options = create_sidebar(uploaded_file, df)
        # Number of rows to display
        # You can change max value to be displayed
        num_rows = st.slider("Number of rows to display in preview", min_value=5, max_value=100, value=10, step=5)

        # Apply cleaning options only after file upload
        if clean_data_options:
            df = clean_data(df, clean_data_options)

        # Display cleaned data preview
        st.write(f"### Cleaned Data Preview ({num_rows} rows)")
        st.write(df.head(num_rows))

        # #  Revised Layout for X and Y Axis Dropdowns
        # col1, col2 = st.columns(2)

        # with col1:
        #     st.markdown("<label style='font-weight: bold; font-size: 14px;'>X-Axis</label>", unsafe_allow_html=True)
        #     x_axis = st.selectbox("", df.columns, key="x_axis")
        #     x_axis_dtype = df[x_axis].dtype
        #     if x_axis_dtype == 'object': 
        #         sample_value = df[x_axis].iloc[0] 
        #         x_axis_dtype = type(sample_value).__name__

        # with col2:
        #     st.markdown("<label style='font-weight: bold; font-size: 14px;'>Y-Axis</label>", unsafe_allow_html=True)
        #     y_axis = st.selectbox("", df.columns, key="y_axis")
        #     y_axis_dtype = df[x_axis].dtype
        #     if y_axis_dtype == 'object': 
        #         sample_value = df[y_axis].iloc[0] 
        #         y_axis_dtype = type(sample_value).__name__

        # print(f'x: {x_axis} = {x_axis_dtype} || y: {y_axis} = {y_axis_dtype}')
        # suggestion = suggest_chart(x_axis, x_axis_dtype, y_axis, y_axis_dtype)
        # st.markdown("<br>", unsafe_allow_html=True)

        # st.write(suggestion)
        # # Chart Type Dropdown Below the Axes
        # st.markdown("<label style='font-weight: bold; font-size: 14px;'>Chart Type</label>", unsafe_allow_html=True)
        # chart_type = st.selectbox("", ["Bar Chart", "Line Chart", "Scatter Plot", "Table"], key="chart_type")

        # # Chart Rendering Logic
        chart_type, x_axis, y_axis, x_axis_dtype, y_axis_dtype = st.session_state.chart_data
        if chart_type:
            if chart_type == "Bar Chart":
                fig = px.bar(df, x=x_axis, y=y_axis, title=f"Bar Chart of {y_axis} vs {x_axis}")
                st.plotly_chart(fig, use_container_width=True)
            elif chart_type == "Line Chart":
                fig = px.line(df, x=x_axis, y=y_axis, title=f"Line Chart of {y_axis} over {x_axis}")
                st.plotly_chart(fig, use_container_width=True)
            elif chart_type == "Scatter Plot":
                fig = px.scatter(df, x=x_axis, y=y_axis, title=f"Scatter Plot of {y_axis} vs {x_axis}")
                st.plotly_chart(fig, use_container_width=True)
            elif chart_type == "Table":
                st.write("### Full Data Table")
                st.write(df)

            # Add comments and download options
            st.write("### Comments or Observations")

            comments = st.text_area(
                "Add your comments or observations about the visualization here:",
                placeholder="Enter your thoughts...",
                height=200,
                value=st.session_state.text_area_content
            )
            if st.button("Use AI") and fig is not None:
                buffer = BytesIO()
                fig.write_image(buffer, format="png")
                buffer.seek(0)
                image = Image.open(buffer)
                response = generate_comments(image)
                st.session_state.text_area_content = f"{response}"
                st.rerun()


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
    st.warning("🔴 Please upload a CSV file to start.")
    pass



