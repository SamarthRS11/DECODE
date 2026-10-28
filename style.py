import streamlit as st

CSS = """
<style>
#MainMenu, footer {visibility: hidden;}
.block-container {padding-top: 1.5rem; max-width: 1150px;}

.hero {
  background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
  color: white; padding: 28px 32px; border-radius: 18px; margin-bottom: 18px;
}
.hero h1 {margin: 0; font-size: 2rem; color: white;}
.hero p {margin: 6px 0 14px 0; font-size: 1.05rem; opacity: 0.92; color: white;}
.pill {
  display: inline-block; background: rgba(255,255,255,0.18); color: white;
  padding: 4px 12px; border-radius: 999px; font-size: 0.8rem; margin: 2px 6px 2px 0;
}

[data-testid="stMetric"] {
  background: white; border: 1px solid #E2E8F0; border-radius: 14px;
  padding: 14px 16px; box-shadow: 0 1px 3px rgba(15,23,42,0.06);
}
[data-testid="stVerticalBlockBorderWrapper"] {
  background: white; border-radius: 14px;
  box-shadow: 0 1px 3px rgba(15,23,42,0.06);
}
.stButton > button, .stDownloadButton > button {
  border-radius: 10px; font-weight: 600; padding: 0.55rem 1.2rem;
}
h2, h3 {margin-top: 1.2rem;}
</style>
"""

def apply_style():
    st.markdown(CSS, unsafe_allow_html=True)

def hero():
    st.markdown(
        """
        <div class="hero">
          <h1>📄 AI Contract Explainer</h1>
          <p>Understand any contract in plain language, before you sign it.</p>
          <span class="pill">Plain-English summary</span>
          <span class="pill">Risky clauses flagged</span>
          <span class="pill">Real loan cost</span>
          <span class="pill">Hindi &amp; Kannada</span>
          <span class="pill">Answers quoted from your contract</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
