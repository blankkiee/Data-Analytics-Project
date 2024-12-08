import streamlit as st

def create_sidebar(uploaded_file, df=None):
    with st.sidebar:
        # LOGO
        st.image("./img/pogionly.png", caption="Your data deserves a dash of Pogi style!", width=200)
        
        # Navigation
        st.title("Navigation")
        st.markdown("Upload a CSV file, clean your data, and choose visualization options.")
        
        # Color mode
        mode = st.radio("Select Color Mode", ["Gradient White", "Gradient Lime Green", "Dark", "Light"])
        
        # File upload
        uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
        
        # If no file is uploaded, return early
        if not uploaded_file:
            return mode, uploaded_file, None, None, None
        
        # Number of rows to display
        num_rows = st.slider("Number of rows to display in preview", min_value=5, max_value=100, value=10, step=5)
        
        # Data Cleaning Options
        st.header("Data Cleaning Options")
        clean_data_options = {
            "Standardize column names": st.checkbox("Standardize column names (lowercase, no spaces)"),
            "Remove duplicates": st.checkbox("Remove duplicate rows"),
            "Handle missing values": st.selectbox(
                "Handle missing values",
                ["None", "Drop rows with missing values", "Fill missing values with 0"]
            ),
            
        }

        # If sorting is enabled, show additional options
        # if clean_data_options["Sort data"] and df is not None:
        #     clean_data_options["Sort column"] = st.selectbox("Select column to sort by:", df.columns)
        #     clean_data_options["Sort order"] = st.radio("Sort order:", ["Ascending", "Descending"])
        
        # Visualization Options
        st.header("Visualization Options")
        visualization_options = ["Bar Chart", "Line Chart", "Scatter Plot", "Table"]
        selected_visualization = st.selectbox("Select Visualization", visualization_options)
        
        return mode, uploaded_file, selected_visualization, num_rows, clean_data_options
