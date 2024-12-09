import streamlit as st

def create_sidebar(uploaded_file):
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
            return mode, uploaded_file, None, None
        
        # Number of rows to display
        # You can change max value to be displayed
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
        
        return mode, uploaded_file, num_rows, clean_data_options