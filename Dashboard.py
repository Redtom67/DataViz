import streamlit as st
import pandas as pd
import base64


# Page configuration
st.set_page_config(
    page_title="Road Safety in France",
    page_icon="🚗",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    return pd.read_csv('./data/df_dataset.csv')

df = load_data()


# Home page
st.title("Road Safety")
st.header("Factors and Victims of Accidents in France")

st.markdown("""
## Welcome to Thomas FISCHER's Road Safety Dashboard

This application analyzes road accident data in France.

### Navigation

Use the sidebar menu to explore different sections:

- **Global Overview**: Evolution and general statistics of accidents
- **Victims**: Analysis of victim profiles
- **Location & Factors**: Mapping and environmental factors

### Data Overview

""")

st.subheader("Sample of the Dataset")
st.dataframe(df.head(10))

st.info("This dataset contains detailed information about road accidents in France, including factors such as location, time, weather conditions, and victim characteristics." \
"It is sourced from the official French road safety database. The dataset used is an aggregated annual version.")

st.markdown("---")

st.markdown("""
### Documentation

For more information, consult the official PDF describing the database:
""")

# Download link for PDF
pdf_path = "./description-des-bases-de-donnees-annuelles.pdf"
with open(pdf_path, "rb") as pdf_file:
    pdf_bytes = pdf_file.read()
    b64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
    href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="description-des-bases-de-donnees-annuelles.pdf">Download PDF Documentation</a>'
    st.markdown(href, unsafe_allow_html=True)

st.markdown("---")