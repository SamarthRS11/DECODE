import streamlit as st

CSS = """
<style>
#MainMenu, footer, header {visibility: hidden;}

/* Layer 1: page background with soft color glows */
.stApp {
  background:
    radial-gradient(900px 500px at 8% -5%, rgba(124,58,237,0.14), transparent 60%),
    radial-gradient(800px 500px at 100% 10%, rgba(79,70,229,0.12), transparent 60%),
    radial-gradient(700px 400px at 50% 100%, rgba(16,185,129,0.08), transparent 60%),
    #F8FAFC;
}
.block-container {padding-top: 1.2rem; max-width: 1150px;}

/* Layer 2: hero banner with decorative glow circles */
.hero {
  position: relative; overflow: hidden;
  background: linear-gradient(135deg, #4338CA 0%, #7C3AED 55%, #C026D3 100%);
  color: white; padding: 34px 36px; border-radius: 22px; margin-bottom: 16px;
  box-shadow: 0 18px 40px rgba(79,70,229,0.28);
}
.hero::before {
  content: ""; position: absolute; width: 280px; height: 280px; border-radius: 50%;
  right: -70px; top: -90px; background: rgba(255,255,255,0.12);
}
.hero::after {
  content: ""; position: absolute; width: 180px; height: 180px; border-radius: 50%;
  right: 130px; bottom: -100px; background: rgba(255,255,255,0.09);
}
.hero h1 {margin: 0; font-size: 2.2rem; color: white; position: relative; z-index: 1;}
.hero p {margin: 8px 0 16px 0; font-size: 1.08rem; color: white; opacity: 0.93; position: relative; z-index: 1;}
.pill {
  position: relative; z-index: 1; display: inline-block;
  background: rgba(255,255,255,0.18); border: 1px solid rgba(255,255,255,0.28);
  color: white; padding: 5px 13px; border-radius: 999px; font-size: 0.8rem; margin: 3px 6px 3px 0;
  backdrop-filter: blur(4px);
}

/* Layer 3: how-it-works strip */
.steps {display: flex; gap: 12px; margin: 0 0 18px 0; flex-wrap: wrap;}
.step {
  flex: 1; min-width: 200px; background: white; border: 1px solid #E2E8F0;
  border-radius: 16px; padding: 14px 16px; box-shadow: 0 2px 8px rgba(15,23,42,0.05);
  transition: transform .18s ease, box-shadow .18s ease;
}
.step:hover {transform: translateY(-3px); box-shadow: 0 10px 22px rgba(79,70,229,0.15);}
.step b {color: #4F46E5;}
.step span {display: block; color: #475569; font-size: 0.88rem; margin-top: 2px;}

/* Metric cards */
[data-testid="stMetric"] {
  background: linear-gradient(180deg, #FFFFFF 0%, #F5F3FF 100%);
  border: 1px solid #E0E7FF; border-radius: 16px; padding: 14px 18px;
  box-shadow: 0 2px 8px rgba(15,23,42,0.06);
  transition: transform .18s ease, box-shadow .18s ease;
}
[data-testid="stMetric"]:hover {transform: translateY(-3px); box-shadow: 0 10px 22px rgba(79,70,229,0.16);}

/* Clause cards */
[data-testid="stVerticalBlockBorderWrapper"] {
  background: white; border-radius: 16px; border: 1px solid #E2E8F0 !important;
  box-shadow: 0 2px 10px rgba(15,23,42,0.06);
  transition: box-shadow .18s ease, border-color .18s ease;
}
[data-testid="stVerticalBlockBorderWrapper"]:hover {
  box-shadow: 0 10px 26px rgba(79,70,229,0.14); border-color: #C7D2FE !important;
}

/* Buttons */
.stButton > button, .stDownloadButton > button {
  border-radius: 12px; font-weight: 600; padding: 0.6rem 1.3rem;
  transition: transform .15s ease, box-shadow .15s ease;
}
.stButton > button:hover, .stDownloadButton > button:hover {
  transform: translateY(-2px); box-shadow: 0 8px 18px rgba(79,70,229,0.25);
}
.stButton > button[kind="primary"] {
  background: linear-gradient(135deg, #4F46E5, #7C3AED); border: none; color: white;
}

/* Inputs */
.stTextArea textarea, .stTextInput input, .stNumberInput input {
  border-radius: 12px !important; border: 1px solid #CBD5E1 !important; background: white !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
  border-color: #6366F1 !important; box-shadow: 0 0 0 3px rgba(99,102,241,0.18) !important;
}

/* Section headings with an accent bar */
h2, h3 {
  margin-top: 1.4rem; padding-left: 12px; border-left: 5px solid #6366F1; border-radius: 2px;
}

/* Tables and alerts */
[data-testid="stDataFrame"] {border-radius: 14px; overflow: hidden; border: 1px solid #E2E8F0;}
[data-testid="stAlert"] {border-radius: 14px;}
hr {border: none; height: 1px; background: linear-gradient(90deg, transparent, #C7D2FE, transparent);}

/* Smooth fade-in for results */
@keyframes fadeUp {from {opacity: 0; transform: translateY(10px);} to {opacity: 1; transform: none;}}
[data-testid="stVerticalBlockBorderWrapper"], [data-testid="stMetric"] {animation: fadeUp .45s ease both;}
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
        <div class="steps">
          <div class="step"><b>1. Add your contract</b><span>Paste text, upload a PDF, or try a sample.</span></div>
          <div class="step"><b>2. Read it in plain words</b><span>Each clause shown next to its original text, with risk flags.</span></div>
          <div class="step"><b>3. Ask and check</b><span>Ask questions, see the real loan rate, download a report.</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
