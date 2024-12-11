import base64
from io import BytesIO
import os
from dotenv import load_dotenv, dotenv_values
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")



def generate_comments(json, prediction_json=None):
    graph_response = model.generate_content(["Pretend you're a data analyst. Without using asterisks in your response, pretend this json is a graph (do not mention that this is a json file) and explain what can be concluded from this graph. simplify words to make it understandable but keep it professional. If there are spikes, make an eductaed guess for the reason that is", json]).text
    
    if prediction_json:
        prediction_response = model.generate_content(["Pretend you're a data analyst. Without using asterisks in your response, pretend this json is a prediction chart and explain what can be concluded from this graph. simplify words to make it understandable. If there are spikes, make an eductaed guess for the reason that is", prediction_json]).text
        combined_response = f"Main Graph Analysis:\n\n{graph_response}\n\nPrediction Chart Analysis:\n\n{prediction_response}" 
        return combined_response

    return graph_response

def suggest_chart(x, x_type, y, y_type, agg_method):

    if x == y:
        return "Oops, your X and Y axes are the same. Try choosing another column"

    prompt = f'in the selection of Bar Chart, Line Chart, Grouped Bar Chart and Scatter Plot, Layered Histogram, Pie Chart what is the best graph to plot when the X axis is {x} with a type of {x_type} and the Y axis is the {agg_method} of {y} with a type of {y_type}. Format your answer to "With {x} on the X axis and {agg_method} of {y} on the Y axis, the best graph is _______"'

    response = model.generate_content(prompt)
    return response.text


