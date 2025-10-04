import streamlit as st
from .config import DARK_CSS, LIGHT_CSS, LANG_MODELS

def sidebar_settings():
    st.sidebar.title("App Settings")
    theme = st.sidebar.radio("Choose Theme:", ("Dark", "Light"), index=0)
    lang  = st.sidebar.selectbox("Choose Language Model", LANG_MODELS, index=0)
    css = DARK_CSS if theme == "Dark" else LIGHT_CSS
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    return theme, lang

def header():
    st.markdown(
        "<h1 style='text-align:center;font-weight:800;text-transform:uppercase;'>SMART ENTITY EXTRACTOR</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<h2 style='text-align:center;font-weight:800;text-transform:uppercase;'>IntelliNER</h2>",
        unsafe_allow_html=True
    )
    st.write("Named Entity Recognition (NER) identifies names, organizations, locations, dates and more.")
    st.write("Enter text or upload a file to analyze named entities.")
