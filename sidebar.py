import streamlit as st

def create_sidebar():
    with st.sidebar:
        #LOGO
        st.image("./img/pogionly.png", 
                 caption="Your data deserves a dash of Pogi style!", width=200)
        
        # Label
        st.title("Navigation")
        st.markdown("Upload a CSV file, clean your data, and choose visualization options.")
        #Color mode
        mode = st.radio("Select Color Mode", 
                        options=["Gradient White", "Gradient Lime Green", "Dark", "Light"])
        
        #UPLOAD fILE
        uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
        
        #Preview No. of Rows to display
        num_rows = st.slider("Number of rows to display in preview", 
                             min_value=5, max_value=100, value=10, step=5)
        
        # CLeaning Operations
        st.header("Data Cleaning Options")
        clean_data_options = {
            "Standardize column names": 
                st.checkbox("Standardize column names (lowercase, no spaces)"),
            "Remove duplicates": 
                st.checkbox("Remove duplicate rows"),
                
        # Dropdown handle missing values
            "Handle missing values": 
                st.selectbox("Handle missing values", 
                             ["None", "Drop rows with missing values", "Fill missing values with 0"]),
        }
        # Graphs
        visualization_options = ["Bar Chart", "Line Chart", "Scatter Plot", "Table"]
        selected_visualization = st.selectbox("Select Visualization", visualization_options)
        
    return mode, uploaded_file, selected_visualization, num_rows, clean_data_options
