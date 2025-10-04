import streamlit as st
from src.ui import sidebar_settings, header
from src.file_io import read_any
from src.nlp import load_model, run_ner
from src.viz import render_entities, entity_filter, stats_and_export

def main():
    theme, lang = sidebar_settings()
    header()

    uploaded = st.file_uploader("Upload a file (txt, pdf, docx)", type=["txt","pdf","docx"])
    if uploaded:
        text = read_any(uploaded)
        st.text_area("File Content:", text, height=200)
    else:
        text = st.text_area(
            "Enter your text here:",
            "Apple Inc. was founded by Steve Jobs in California. "
            "The company's headquarters are in Cupertino. Tim Cook is the current CEO."
        )

    if st.button("Extract Entities"):
        nlp = load_model(lang)
        doc = run_ner(nlp, text)
        if not doc:
            st.warning("Please enter some text or upload a valid file.")
            return

        selected = entity_filter(doc)
        filtered = [e for e in doc.ents if e.label_ in selected] if selected else list(doc.ents)

        st.subheader("🔎 Detected Entities (Highlighted)")
        render_entities(doc, theme=theme, labels=selected)


        if filtered:
            stats_and_export(filtered)
        else:
            st.info("No entities after filtering.")

if __name__ == "__main__":
    main()
