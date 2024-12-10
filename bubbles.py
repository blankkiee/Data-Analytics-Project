import streamlit as st

def render_bubbles():
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

    st.markdown(bubble_css, unsafe_allow_html=True)
    st.markdown(bubble_html, unsafe_allow_html=True)



