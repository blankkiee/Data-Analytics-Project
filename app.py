from io import BytesIO
# import pypandoc
import streamlit as st
import pandas as pd
import plotly.express as px
from sidebar import create_sidebar
from bubbles import render_bubbles
from theme import set_page_mode
from header import render_header
from data_utils import clean_data
from aitest import generate_comments, suggest_chart
from PIL import Image
from docx import Document
from docx.shared import Pt, Inches
from docx2pdf import convert 
import tempfile


# Main app
st.set_page_config(layout="wide")
# Add the custom CSS and HTML to Streamlit
render_bubbles()
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


        # Chart Rendering Logic
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


            # Your existing code
            st.write("### Generate Report")
            if st.button("Generate Report"):
                if comments.strip():

                    # Create a Word document
                    doc = Document()
                    doc.add_heading('Report from PogiOnly', 0)
                    

                    # Add image
                    buffer = BytesIO()
                    fig.write_image(buffer, format="png")
                    buffer.seek(0)
                    image = Image.open(buffer)
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
                        image.save(tmp_file.name)
                        doc.add_heading('Generated Image:', level=1)
                        doc.add_picture(tmp_file.name, width=Inches(4.0))
                    

                    # Add comments to the document
                    doc.add_heading('User Comments:', level=1)
                    for line in comments.split('\n'):
                        paragraph = doc.add_paragraph()
                        run = paragraph.add_run(line)
                        run.font.size = Pt(12)

                    # Add some additional text content
                    doc.add_heading('Additional Information:', level=1)
                    doc.add_paragraph("Here you can add any additional information or summaries related to your data and analysis.")


                    # Save the document to a BytesIO object
                    buffer = BytesIO()
                    doc.save(buffer)
                    buffer.seek(0)

                    st.success("Report Generated!")
                    st.download_button( label="Download DOCX Report", data=buffer, file_name="report_with_comments.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document" )
                   
                else:
                    st.warning("Please add comments before generating the report.")

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
    
else:
    st.warning("🔴 Please upload a CSV file to start.")
    pass




