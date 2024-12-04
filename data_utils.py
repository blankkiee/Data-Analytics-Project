import pandas as pd
import streamlit as st

def clean_data(df, options):
    if options["Standardize column names"]:
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
        st.sidebar.write("Column names standardized.")
    if options["Remove duplicates"]:
        df = df.drop_duplicates()
        st.sidebar.write("Duplicate rows removed.")
    if options["Handle missing values"] == "Drop rows with missing values":
        df = df.dropna()
        st.sidebar.write("Rows with missing values dropped.")
    elif options["Handle missing values"] == "Fill missing values with 0":
        df = df.fillna(0)
        st.sidebar.write("Missing values filled with 0.")
    return df
