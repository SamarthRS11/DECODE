import os
import streamlit as st
from analyzer import extract_pdf_text, analyze_contract, translate_simple
from qa import answer_question
from extras import show_extras
from finance_engine import audit_contract_with_llm

st.set_page_config(page_title="Contract Explainer", page_icon="📄", layout="wide")

@st.cache_data(show_spinner=False)
def cached_analyze(text):
    return analyze_contract(text)

@st.cache_data(show_spinner=False)
def cached_loan(text):
    return audit_contract_with_llm(text)

st.title("📄 AI Contract Explainer")
st.caption("Understand a contract in plain language before you sign it.")
st.warning(
    "Educational tool, not legal advice. Flags are potential concerns, "
    "not legal conclusions. For important decisions, consult a qualified professional."
)

RISK = {"attention": ("🔴", "Attention"), "review": ("🟠", "Review"), "info": ("🟢", "Info")}
ORDER = {"attention": 0, "review": 1, "info": 2}
SAMPLES = {"Sample rental agreement": "sample_rental_agreement.txt",
           "Sample loan agreement": "sample_loan_agreement.txt"}
available = {k: v for k, v in SAMPLES.items() if os.path.exists(v)}

# ---------- Input ----------
sources = ["Paste text", "Upload PDF"] + (["Use a sample"] if available else [])
source = st.radio("How do you want to add the contract?", sources, horizontal=True)

text = ""
if source == "Paste text":
    text = st.text_area("Paste your contract text here", height=250)
elif source == "Upload PDF":
    pdf = st.file_uploader("Upload a PDF", type=["pdf"])
    if pdf is not None:
        text = extract_pdf_text(pdf)
        if len(text.strip()) < 200:
            st.error("Could not read text from this PDF. It may be a scanned image. Try pasting the text instead.")
            text = ""
else:
    name = st.selectbox("Choose a sample", list(available.keys()))
    text = open(available[name], encoding="utf-8").read()
    st.text_area("Sample text", text, height=200, disabled=True)

if st.button("Analyze contract", type="primary", disabled=not text.strip()):
    with st.spinner("Reading your contract... this takes 10-30 seconds"):
        try:
            st.session_state["result"] = cached_analyze(text)
            st.session_state["text"] = text
            st.session_state.pop("loan", None)
            st.session_state.pop("tr", None)
        except Exception as e:
            st.error(f"Something went wrong: {e}")

# ---------- Results ----------
result = st.session_state.get("result")
if result:
    clauses = result.get("clauses", [])
    st.divider()
    st.subheader(f"📋 {result.get('contract_type', 'Contract')}")

    lang = st.radio("Explanation language", ["English", "Hindi", "Kannada"], horizontal=True)
    tr = None
    if lang != "English":
        cache = st.session_state.setdefault("tr", {})
        if lang not in cache:
            with st.spinner(f"Translating to {lang}..."):
                try:
                    cache[lang] = translate_simple(result, lang)
                except Exception as e:
                    st.error(f"Translation failed: {e}")
        tr = cache.get(lang)

    st.write(result.get("summary", ""))
    if tr and tr.get("summary"):
        st.info(f"**{lang}:** {tr['summary']}")

    c1, c2, c3 = st.columns(3)
    c1.metric("🔴 Attention", sum(c.get("risk_level") == "attention" for c in clauses))
    c2.metric("🟠 Review", sum(c.get("risk_level") == "review" for c in clauses))
    c3.metric("🟢 Info", sum(c.get("risk_level") == "info" for c in clauses))

    st.subheader("💰 Key financial terms")
    st.dataframe(result.get("key_terms", []), use_container_width=True, hide_index=True)

    st.subheader("🔍 Clause by clause")
    choice = st.radio("Show", ["All", "Attention", "Review", "Info"], horizontal=True)
    indexed = sorted(enumerate(clauses), key=lambda p: ORDER.get(p[1].get("risk_level"), 3))
    if choice != "All":
        indexed = [p for p in indexed if p[1].get("risk_level") == choice.lower()]

    for idx, c in indexed:
        icon, label = RISK.get(c.get("risk_level"), ("⚪", "Info"))
        with st.container(border=True):
            st.markdown(f"**{icon} {label}** · {c.get('category', 'other').title()}")
            left, right = st.columns(2)
            with left:
                st.caption("ORIGINAL TEXT")
                st.markdown(f"> {c.get('original_quote', '')}")
                if not c.get("verified"):
                    st.caption("⚠️ Could not be matched exactly to the contract text. Verify manually.")
            with right:
                st.caption("IN SIMPLE WORDS")
                st.write(c.get("simple_explanation", ""))
                if tr and idx < len(tr.get("explanations", [])):
                    st.write(f"**{lang}:** {tr['explanations'][idx]}")
                if c.get("risk_reason"):
                    st.info(f"Why this may matter: {c['risk_reason']}")

    show_extras(result)

    # ---------- Q&A ----------
    st.divider()
    st.subheader("💬 Ask a question about this contract")
    question = st.text_input("For example: What happens if I pay rent late?")
    if st.button("Get answer") and question.strip():
        with st.spinner("Checking the contract..."):
            try:
                ans = answer_question(st.session_state["text"], question)
                if ans.get("found"):
                    st.success(ans.get("answer", ""))
                    if ans.get("quote"):
                        st.caption("SUPPORTING TEXT FROM THE CONTRACT")
                        st.markdown(f"> {ans['quote']}")
                        if not ans.get("verified"):
                            st.caption("⚠️ Could not be matched exactly. Verify manually.")
                else:
                    st.info("The contract doesn't seem to mention this. " + ans.get("answer", ""))
            except Exception as e:
                st.error(f"Something went wrong: {e}")

    # ---------- Loan check ----------
    st.divider()
    st.subheader("🏦 True loan cost check")
    st.caption("For loan or EMI agreements. Estimates the real yearly rate after upfront fees. Not legal or financial advice.")
    if st.button("Check true loan cost"):
        with st.spinner("Calculating..."):
            try:
                st.session_state["loan"] = cached_loan(st.session_state["text"])
            except Exception as e:
                st.error(f"Something went wrong: {e}")
    loan = st.session_state.get("loan")
    if loan:
        if not loan.get("calculated_apr"):
            st.info("This doesn't look like a loan with an EMI, so no loan rate could be calculated.")
        else:
            m1, m2, m3 = st.columns(3)
            m1.metric("Advertised rate", f"{loan.get('stated_rate', 0)}% p.a.")
            m2.metric("Estimated real rate", f"{loan['calculated_apr']}% p.a.")
            m3.metric("Total extra cost", f"Rs {loan.get('total_extra_cost', 0):,.0f}")
            st.write(loan.get("plain_summary", ""))
            for f in loan.get("red_flags", []):
                st.warning(f"**{f.get('clause', '')}** ({f.get('severity', '')}): {f.get('issue', '')}  \n*Potential concern, not a legal conclusion.*")
