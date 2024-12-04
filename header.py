import streamlit as st

def render_header():
    st.markdown("""
        <div class="header-container">
            <h1 class="">Pogi Only Dashboard</h1>
            <p class="">"Make your data handsome with Pogi Only Dashboard"</p>
        </div>
    """, unsafe_allow_html=True)
