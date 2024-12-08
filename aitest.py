import os
from dotenv import load_dotenv, dotenv_values
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))

def generate_comments(prompt, image):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text
