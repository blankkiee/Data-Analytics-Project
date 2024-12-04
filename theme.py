import streamlit as st\
    
#COLOR MODE
def set_page_mode(mode):
 
    if mode == "Dark": # Number 1
        st.markdown("""
            <style>
            .stApp {background: linear-gradient(500deg, #152133, #152133); color: #ffffff;}
            .css-1d391kg {background-color: #2B3A67; color: #ffffff;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
        """, unsafe_allow_html=True)
       
    elif mode == "Light":# Number 2
        st.markdown("""
            <style>
            .stApp {background: linear-gradient(135deg, #FFFAF0, #FFFAF0); color: #000000;}
            .css-1d391kg {background-color: #e0e7ff; color: #000000;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
        """, unsafe_allow_html=True)
        
    elif mode == "Gradient White": # Number 3
        st.markdown("""
            <style>
            .stApp {background: linear-gradient(135deg, #f8f9fa, #2F4F4F); color: #ffffff;}
            .css-1d391kg {background-color: #e0e7ff; color: #ffffff;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
        """, unsafe_allow_html=True)
    elif mode == "Gradient Lime Green": # Number 4
        st.markdown("""
            <style>
            .stApp {background: linear-gradient(135deg, #f8f9fa, #3dd07a); color: #ffffff;}
            .css-1d391kg {background-color: #e0e7ff; color: #ffffff;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
        """, unsafe_allow_html=True)
