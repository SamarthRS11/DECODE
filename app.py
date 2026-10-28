import os
import streamlit as st
from analyzer import extract_pdf_text, analyze_contract

st.set_page_config(page_title="Contract Explainer", page_icon="📄", layout="wide")

st.title("📄 AI Contract Explainer")
st.caption("Understand a contract in plain language before you sign it.")
st.warning(
    "Educational tool, not legal advice. Flags are potential concerns, "
    "not legal conclusions. For important decisions, consult a qualified professional."
)

RISK = {
    "attention": ("🔴", "Attention"),
    "review": ("🟠", "Review"),
    "info": ("🟢", "Info"),
}
ORDER = {"attention": 0, "review": 1, "info": 2}

tab_paste, tab_upload = st.tabs(["Paste text", "Upload PDF"])
with tab_paste:
    pasted = st.text_area("Paste your contract text here", height=250)
with tab_upload:
    pdf = st.file_uploader("Upload a PDF", type=["pdf"])

use_sample = False
if os.path.exists("sample_rental_agreement.txt"):
    use_sample = st.checkbox("Use the sample rental agreement instead")

text = ""
if use_sample:
    text = open("sample_rental_agreement.txt", encoding="utf-8").read()
elif pdf is not None:
    text = extract_pdf_text(pdf)
    if len(text.strip()) < 200:
        st.error("Could not read text from this PDF. It may be a scanned image. Try pasting the text instead.")
        text = ""
else:
    text = pasted

if st.button("Analyze contract", type="primary", disabled=not text.strip()):
    with st.spinner("Reading your contract... this takes 10-30 seconds"):
        try:
            st.session_state["result"] = analyze_contract(text)
            st.session_state["text"] = text
        except Exception as e:
            st.error(f"Something went wrong: {e}")

result = st.session_state.get("result")
if result:
    st.divider()
    st.subheader(f"📋 {result.get('contract_type', 'Contract')}")
    st.write(result.get("summary", ""))

    clauses = result.get("clauses", [])

    c1, c2, c3 = st.columns(3)
    c1.metric("🔴 Attention", sum(c["risk_level"] == "attention" for c in clauses))
    c2.metric("🟠 Review", sum(c["risk_level"] == "review" for c in clauses))
    c3.metric("🟢 Info", sum(c["risk_level"] == "info" for c in clauses))

    st.subheader("💰 Key financial terms")
    st.dataframe(result.get("key_terms", []), use_container_width=True, hide_index=True)

    st.subheader("🔍 Clause by clause")
    choice = st.radio("Show", ["All", "Attention", "Review", "Info"], horizontal=True)
    shown = sorted(clauses, key=lambda c: ORDER.get(c["risk_level"], 3))
    if choice != "All":
        shown = [c for c in shown if c["risk_level"] == choice.lower()]

    for c in shown:
        icon, label = RISK.get(c["risk_level"], ("⚪", "Info"))
        with st.container(border=True):
            st.markdown(f"**{icon} {label}** · {c.get('category', 'other').title()}")
            left, right = st.columns(2)
            with left:
                st.caption("ORIGINAL TEXT")
                st.markdown(f"> {c['original_quote']}")
                if not c.get("verified"):
                    st.caption("⚠️ Could not be matched exactly to the contract text. Verify manually.")
            with right:
                st.caption("IN SIMPLE WORDS")
                st.write(c["simple_explanation"])
                if c.get("risk_reason"):
                    st.info(f"Why this may matter: {c['risk_reason']}")

if st.session_state.get("result"):
    from qa import answer_question
    st.divider()
    st.subheader("💬 Ask a question about this contract")
    question = st.text_input("For example: What happens if I pay rent late?")
    if st.button("Get answer") and question.strip():
        with st.spinner("Checking the contract..."):
            try:
                ans = answer_question(st.session_state["text"], question)
                if ans.get("found"):
                    st.success(ans["answer"])
                    if ans.get("quote"):
                        st.caption("SUPPORTING TEXT FROM THE CONTRACT")
                        st.markdown(f"> {ans['quote']}")
                        if not ans.get("verified"):
                            st.caption("⚠️ Could not be matched exactly. Verify manually.")
                else:
                    st.info("The contract doesn't seem to mention this. " + ans.get("answer", ""))
            except Exception as e:
                st.error(f"Something went wrong: {e}")

if st.session_state.get("text"):
    from finance_engine import audit_contract_with_llm
    st.divider()
    st.subheader("🏦 True loan cost check")
    st.caption("For loan or EMI agreements. Works out the real yearly rate after upfront fees. Estimates only, not legal or financial advice.")
    if st.button("Check true loan cost"):
        with st.spinner("Calculating..."):
            try:
                st.session_state["loan"] = audit_contract_with_llm(st.session_state["text"])
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
