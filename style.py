import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"], .stApp {font-family: 'Inter', sans-serif;}
#MainMenu, footer, header {visibility: hidden;}

/* Page background: soft layered glows */
.stApp {
  background:
    radial-gradient(1000px 520px at 5% -8%, rgba(124,58,237,0.16), transparent 60%),
    radial-gradient(900px 520px at 105% 8%, rgba(236,72,153,0.12), transparent 60%),
    radial-gradient(800px 460px at 50% 105%, rgba(14,165,233,0.10), transparent 60%),
    #F6F7FB;
}
.block-container {padding-top: 1.2rem; max-width: 1150px;}

/* Hero: dark, animated gradient with floating glow blobs */
.hero {
  position: relative; overflow: hidden; color: white;
  padding: 46px 42px 38px 42px; border-radius: 28px; margin-bottom: 18px;
  background: linear-gradient(120deg, #0F172A, #312E81, #6D28D9, #0F172A);
  background-size: 300% 300%; animation: flow 14s ease infinite;
  box-shadow: 0 28px 60px rgba(49,46,129,0.38);
  border: 1px solid rgba(255,255,255,0.10);
}
@keyframes flow {0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%}}
.blob {position: absolute; border-radius: 50%; filter: blur(46px); opacity: .55; animation: float 9s ease-in-out infinite;}
.b1 {width: 260px; height: 260px; background: #8B5CF6; right: -60px; top: -80px;}
.b2 {width: 220px; height: 220px; background: #EC4899; right: 200px; bottom: -120px; animation-delay: -3s;}
.b3 {width: 180px; height: 180px; background: #22D3EE; left: -50px; bottom: -90px; animation-delay: -6s;}
@keyframes float {0%,100%{transform: translateY(0)} 50%{transform: translateY(-22px)}}

.badge {
  position: relative; z-index: 1; display: inline-block; padding: 5px 14px; border-radius: 999px;
  font-size: .75rem; font-weight: 600; letter-spacing: .08em; text-transform: uppercase;
  background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.25); color: #E9D5FF;
}
.hero h1 {
  position: relative; z-index: 1; margin: 14px 0 6px 0; font-size: 2.9rem; line-height: 1.1;
  font-weight: 800; letter-spacing: -0.02em; color: white; padding: 0;
}
.hero h1 .grad {
  background: linear-gradient(90deg, #67E8F9, #C4B5FD, #F9A8D4);
  -webkit-background-clip: text; background-clip: text; color: transparent;
}
.hero p {position: relative; z-index: 1; margin: 0 0 18px 0; font-size: 1.1rem; color: #E2E8F0; max-width: 640px;}
.pill {
  position: relative; z-index: 1; display: inline-block; margin: 3px 6px 3px 0;
  padding: 6px 14px; border-radius: 999px; font-size: .8rem; font-weight: 500; color: white;
  background: rgba(255,255,255,0.10); border: 1px solid rgba(255,255,255,0.22);
  backdrop-filter: blur(6px);
}

/* How-it-works strip: glass cards with a gradient top edge */
.steps {display: flex; gap: 14px; margin: 0 0 22px 0; flex-wrap: wrap;}
.step {
  flex: 1; min-width: 210px; position: relative; overflow: hidden;
  background: rgba(255,255,255,0.75); backdrop-filter: blur(10px);
  border: 1px solid rgba(255,255,255,0.9); border-radius: 18px; padding: 18px 18px 16px 18px;
  box-shadow: 0 6px 20px rgba(15,23,42,0.07);
  transition: transform .2s ease, box-shadow .2s ease;
}
.step::before {content:""; position:absolute; left:0; top:0; right:0; height:4px;
  background: linear-gradient(90deg, #6366F1, #EC4899);}
.step:hover {transform: translateY(-4px); box-shadow: 0 16px 34px rgba(99,102,241,0.22);}
.step b {color: #1E1B4B; font-size: 1rem;}
.step span {display: block; color: #64748B; font-size: .88rem; margin-top: 4px;}

/* Metric cards */
[data-testid="stMetric"] {
  position: relative; overflow: hidden; background: rgba(255,255,255,0.85);
  border: 1px solid #E5E7EB; border-radius: 18px; padding: 16px 20px;
  box-shadow: 0 6px 18px rgba(15,23,42,0.07);
  transition: transform .2s ease, box-shadow .2s ease;
}
[data-testid="stMetric"]::before {content:""; position:absolute; left:0; top:0; bottom:0; width:5px;
  background: linear-gradient(180deg, #6366F1, #EC4899);}
[data-testid="stMetric"]:hover {transform: translateY(-4px); box-shadow: 0 16px 32px rgba(99,102,241,0.2);}
[data-testid="stMetricValue"] {font-weight: 800; letter-spacing: -0.01em;}

/* Clause cards */
[data-testid="stVerticalBlockBorderWrapper"] {
  background: rgba(255,255,255,0.9); border-radius: 18px; border: 1px solid #E5E7EB !important;
  box-shadow: 0 6px 18px rgba(15,23,42,0.06);
  transition: box-shadow .2s ease, border-color .2s ease, transform .2s ease;
}
[data-testid="stVerticalBlockBorderWrapper"]:hover {
  box-shadow: 0 16px 34px rgba(99,102,241,0.16); border-color: #C7D2FE !important; transform: translateY(-2px);
}

/* Buttons */
.stButton > button, .stDownloadButton > button {
  border-radius: 14px; font-weight: 600; padding: 0.65rem 1.5rem; border: 1px solid #C7D2FE;
  transition: transform .15s ease, box-shadow .15s ease;
}
.stButton > button:hover, .stDownloadButton > button:hover {
  transform: translateY(-2px); box-shadow: 0 10px 22px rgba(99,102,241,0.28);
}
.stButton > button[kind="primary"] {
  background: linear-gradient(135deg, #4F46E5, #9333EA 60%, #DB2777); border: none; color: white;
  box-shadow: 0 8px 20px rgba(124,58,237,0.35);
}

/* Inputs */
.stTextArea textarea, .stTextInput input, .stNumberInput input {
  border-radius: 14px !important; border: 1px solid #D1D5DB !important; background: white !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
  border-color: #7C3AED !important; box-shadow: 0 0 0 4px rgba(124,58,237,0.15) !important;
}

/* Headings with gradient accent bar */
h2, h3 {
  margin-top: 1.6rem; padding-left: 14px; font-weight: 700; letter-spacing: -0.01em;
  border-left: 5px solid; border-image: linear-gradient(180deg, #6366F1, #EC4899) 1;
}

/* Tables, alerts, dividers */
[data-testid="stDataFrame"] {border-radius: 16px; overflow: hidden; border: 1px solid #E5E7EB; box-shadow: 0 4px 14px rgba(15,23,42,0.05);}
[data-testid="stAlert"] {border-radius: 16px;}
hr {border: none; height: 2px; background: linear-gradient(90deg, transparent, #C4B5FD, #F9A8D4, transparent);}

/* Fade-in */
@keyframes fadeUp {from {opacity: 0; transform: translateY(12px);} to {opacity: 1; transform: none;}}
[data-testid="stVerticalBlockBorderWrapper"], [data-testid="stMetric"] {animation: fadeUp .5s ease both;}
</style>
"""

def apply_style():
    st.markdown(CSS, unsafe_allow_html=True)

def hero():
    st.markdown(
        """
        <div class="hero">
          <div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div>
          <span class="badge">Financial inclusion · AI-powered</span>
          <h1>Understand any contract in <span class="grad">plain language</span></h1>
          <p>Know what you are signing before you sign it. Risky clauses flagged, real loan cost revealed, every answer quoted from your document.</p>
          <span class="pill">Plain-English summary</span>
          <span class="pill">Risky clauses flagged</span>
          <span class="pill">Real loan cost</span>
          <span class="pill">Hindi &amp; Kannada</span>
          <span class="pill">Quotes verified</span>
        </div>
        <div class="steps">
          <div class="step"><b>1. Add your contract</b><span>Paste text, upload a PDF, or try a sample.</span></div>
          <div class="step"><b>2. Read it in plain words</b><span>Each clause beside its original text, with risk flags.</span></div>
          <div class="step"><b>3. Ask and check</b><span>Ask questions, see the real loan rate, download a report.</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
