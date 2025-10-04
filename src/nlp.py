import spacy
import streamlit as st

@st.cache_resource
def load_model(lang_name: str):
    """Load and cache a spaCy model by name."""
    try:
        return spacy.load(lang_name)
    except Exception as e:
        st.error(f"Error loading spaCy model '{lang_name}': {e}")
        st.info(f"Install it with:  python -m spacy download {lang_name}")
        return None

def run_ner(nlp, text: str):
    """Run NER if model and text are available."""
    if not nlp or not text or not text.strip():
        return None
    return nlp(text)
