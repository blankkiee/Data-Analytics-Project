import base64
from io import BytesIO
import os
from dotenv import load_dotenv, dotenv_values
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")



def generate_comments(image):
    response = model.generate_content(["Using image, can you explain what can be concluded from this chart? Give estimates on each data. simplify words to make it understandable. Take note on what is the highest and lowest if it matters. Do not include asterisks in your response", image])
    return response.text

def suggest_chart(x, x_type, y, y_type):

    if x == y:
        return "Oops, your X and Y axes are the same. Try choosing another column"

    prompt = f'in the selection of Bar Chart, Line Chart, and Scatter Plot, what is the best graph to plot when the X axis is {x} with a type of {x_type} and the Y axis is {y} with a type of {y_type}. Format your answer to "With {x} on the X axis and {y} on the Y axis, the best graph is [graph]"'

    response = model.generate_content(prompt)
    return response.text


