# Language models you want to support
LANG_MODELS = [
    "en_core_web_sm",
    "fr_core_news_sm",
    "de_core_news_sm",
    "es_core_news_sm",
]

# Minimal CSS for themes
DARK_CSS = """
.main { background-color:#0A1128; color:#FAFAFA; }
.stTextArea textarea { background:#1B263B; color:#FAFAFA; }
.stButton>button { background:#7d3c98; color:#FAFAFA; }
"""

LIGHT_CSS = """
.main { background:#FFFFFF; color:#333; }
.stTextArea textarea { background:#F0F2F6; color:#333; }
.stButton>button { background:#ADD8E6; color:#333; }
"""

# displaCy colors for entity labels
DISPLACY_COLORS_DARK = {
    "ORG": "linear-gradient(90deg, #aa9cfc, #fc9ce7)",
    "PERSON": "linear-gradient(90deg, #a0d468, #1abc9c)",
    "GPE": "#ffd700",
    "LOC": "#ffcc99",
    "DATE": "#c6e2ff",
    "MONEY": "#bfef45",
    "CARDINAL": "#ffbe7d",
}
DISPLACY_COLORS_LIGHT = {
    "ORG": "#d9e2f3",
    "PERSON": "#e6ffe6",
    "GPE": "#fffacd",
    "LOC": "#f5f5dc",
    "DATE": "#f0ffff",
    "MONEY": "#ccffcc",
    "CARDINAL": "#ffe0b2",
}
