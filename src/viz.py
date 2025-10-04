import streamlit as st
import pandas as pd
from collections import Counter

# We won't rely on displaCy to render the whole text; we build our own HTML
from .config import (
    DISPLACY_COLORS_DARK,
    DISPLACY_COLORS_LIGHT,
)

def entity_filter(doc):
    labels = sorted({ent.label_ for ent in doc.ents})
    return st.multiselect("Filter Entity Types:", options=labels, default=labels)

def _build_css(theme: str):
    # choose colors for labels
    colors = DISPLACY_COLORS_DARK if theme == "Dark" else DISPLACY_COLORS_LIGHT
    normal = "#ffffff" if theme == "Dark" else "#333333"

    # make CSS rules for each entity label (mark.<LABEL>)
    label_rules = []
    for lbl, bg in colors.items():
        label_rules.append(f"mark.{lbl} {{ background: {bg}; color: #000; padding: 2px 6px; border-radius: 6px; margin: 2px 3px; }}")

    css = f"""
    <style>
      .ner-container {{
        font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, Arial, "Noto Sans", "Apple Color Emoji", "Segoe UI Emoji";
        line-height: 1.7;
        font-size: 1.05rem;
        word-wrap: break-word;
        white-space: pre-wrap; /* keep line breaks & spacing */
      }}
      .normal-text {{ color: {normal}; }}
      mark {{ padding: 2px 6px; border-radius: 6px; margin: 2px 3px; }}
      {' '.join(label_rules)}
    </style>
    """
    return css

def _highlight_entities_html(doc, labels=None):
    """
    Build HTML with:
      - non-entity text wrapped in <span class="normal-text">...</span>
      - entity text wrapped in <mark class="LABEL">...</mark>
    """
    if not doc or not doc.text:
        return "<div class='ner-container'></div>"

    html_parts = []
    last_end = 0

    for ent in doc.ents:
        # normal text before the entity
        if last_end < ent.start_char:
            normal_text = doc.text[last_end:ent.start_char]
            html_parts.append(f"<span class='normal-text'>{_escape(normal_text)}</span>")

        # the entity itself (respect filter if provided)
        if (labels is None) or (ent.label_ in labels):
            html_parts.append(f"<mark class='{ent.label_}'>{_escape(ent.text)}</mark>")
        else:
            html_parts.append(f"<span class='normal-text'>{_escape(ent.text)}</span>")

        last_end = ent.end_char

    # tail text after the last entity
    if last_end < len(doc.text):
        html_parts.append(f"<span class='normal-text'>{_escape(doc.text[last_end:])}</span>")

    return "<div class='ner-container'>" + "".join(html_parts) + "</div>"

def _escape(s: str) -> str:
    """Basic HTML escaping."""
    return (
        s.replace("&", "&amp;")
         .replace("<", "&lt;")
         .replace(">", "&gt;")
    )

def render_entities(doc, theme="Dark", labels=None):
    """Render the full text with entities highlighted AND normal text visible."""
    css = _build_css(theme)
    html = _highlight_entities_html(doc, labels=labels)
    st.components.v1.html(css + html, height=320, scrolling=True)

def stats_and_export(entities):
    st.subheader("📊 Entity Statistics")
    counts = Counter(e.label_ for e in entities)
    df = pd.DataFrame(counts.items(), columns=["Entity Type", "Count"])
    st.table(df)
    st.bar_chart(df.set_index("Entity Type"))

    # Also show unique strings with occurrences (nice touch)
    st.subheader("🧮 Unique Entities (with counts)")
    uniq = _dedup_table(entities)
    st.dataframe(uniq, use_container_width=True)

    st.subheader("⬇️ Export Results")
    out = uniq.rename(columns={"Occurrences": "Count"})[["Entity", "Type", "Count"]]
    st.download_button(
        "Download Entities as CSV",
        data=out.to_csv(index=False).encode("utf-8"),
        file_name="entities.csv",
        mime="text/csv",
    )

def _dedup_table(entities):
    rows = {}
    for e in entities:
        key = (e.text.strip(), e.label_)
        rows[key] = rows.get(key, 0) + 1
    return pd.DataFrame(
        [(k[0], k[1], v) for k, v in rows.items()],
        columns=["Entity", "Type", "Occurrences"]
    ).sort_values(["Occurrences", "Entity"], ascending=[False, True])
