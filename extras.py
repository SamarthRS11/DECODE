import streamlit as st
import pandas as pd

POINTS = {"attention": 3, "review": 1, "info": 0}

def risk_score(clauses):
    if not clauses:
        return 0
    total = sum(POINTS.get(c.get("risk_level"), 0) for c in clauses)
    return min(100, round(total / (3 * len(clauses)) * 100))

def build_report(result):
    lines = [f"# Contract Report: {result.get('contract_type', 'Contract')}", ""]
    lines += ["> Educational tool, not legal advice. Flags are potential concerns, not legal conclusions.", ""]
    lines += ["## Summary", result.get("summary", ""), "", "## Key financial terms"]
    for t in result.get("key_terms", []):
        lines.append(f"- {t.get('label')}: {t.get('value')}")
    lines += ["", "## Clauses"]
    for c in result.get("clauses", []):
        lines.append(f"### [{c.get('risk_level', '').upper()}] {c.get('category', '').title()}")
        lines.append(f"Original: {c.get('original_quote', '')}")
        lines.append(f"In simple words: {c.get('simple_explanation', '')}")
        if c.get("risk_reason"):
            lines.append(f"Why this may matter: {c['risk_reason']}")
        lines.append("")
    return "\n".join(lines)

def show_extras(result):
    clauses = result.get("clauses", [])
    st.divider()
    st.subheader("📊 Risk overview")

    score = risk_score(clauses)
    label = "Low" if score < 25 else "Moderate" if score < 55 else "High"
    col1, col2 = st.columns([1, 2])
    col1.metric("Risk score", f"{score} / 100", label)
    col2.progress(score / 100)
    col2.caption("A rough indicator based on how many clauses were flagged. It is not a legal verdict.")

    if clauses:
        df = pd.DataFrame(clauses)
        table = pd.crosstab(df["category"], df["risk_level"])
        table = table.reindex(columns=["attention", "review", "info"], fill_value=0)
        st.caption("Clauses by category and risk level")
        st.bar_chart(table, color=["#e74c3c", "#f39c12", "#2ecc71"])

    st.subheader("🧮 What-if simulator")
    st.caption("Change the numbers to match your contract. These are illustrative estimates only.")
    a, b, c = st.columns(3)
    rent = a.number_input("Monthly rent (Rs)", value=25000, step=1000)
    pct = b.number_input("Late penalty (% per day)", value=5.0, step=0.5)
    days = c.slider("Days late", 0, 30, 3)
    d, e, f = st.columns(3)
    deposit = d.number_input("Security deposit (Rs)", value=150000, step=5000)
    lock = e.number_input("Lock-in (months)", value=11, step=1)
    stayed = f.slider("Months you stay", 1, 24, 6)

    late_fee = rent * pct / 100 * days
    forfeited = deposit if stayed < lock else 0
    m1, m2 = st.columns(2)
    m1.metric("Late fee for this month", f"Rs {late_fee:,.0f}")
    m2.metric("Deposit at risk if you leave early", f"Rs {forfeited:,.0f}")
    if late_fee > rent * 0.5:
        st.warning("At these numbers the late fee is large compared to the rent. Worth checking.")

    st.subheader("⬇️ Download")
    st.download_button("Download contract report", build_report(result),
                       file_name="contract_report.md", mime="text/markdown")
