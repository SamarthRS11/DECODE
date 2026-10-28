import numpy_financial as npf
from analyzer import ask_json

def calculate_real_apr(principal, monthly_emi, tenure_months, upfront_fees):
    net = principal - upfront_fees
    if net <= 0 or monthly_emi <= 0 or tenure_months <= 0:
        return 0.0
    try:
        irr = npf.irr([net] + [-monthly_emi] * tenure_months)
        return round(float(irr) * 12 * 100, 2)
    except Exception:
        return 0.0

def _num(v):
    try:
        return float(v or 0)
    except Exception:
        return 0.0

def audit_contract_with_llm(contract_text):
    prompt = """You are a consumer finance auditor. Read the loan or EMI agreement below.
Return ONLY valid JSON, no markdown:
{
  "principal": <number: total sanctioned amount, 0 if not a loan>,
  "tenure_months": <integer>,
  "stated_rate": <number: advertised interest percent per year>,
  "monthly_emi": <number>,
  "upfront_fees": <number: processing fees, admin charges and insurance deducted at disbursal>,
  "red_flags": [{"clause": "<short title>", "issue": "<short explanation of why it may be costly or unfair>", "severity": "HIGH or MEDIUM"}],
  "plain_summary": "<2 sentence plain-English summary for an everyday borrower>"
}
Use cautious wording like "may" and "could". Do not cite laws.

CONTRACT:
""" + contract_text[:8000]
    data = ask_json(prompt)
    principal = _num(data.get("principal"))
    emi = _num(data.get("monthly_emi"))
    months = int(_num(data.get("tenure_months")))
    fees = _num(data.get("upfront_fees"))
    data["calculated_apr"] = calculate_real_apr(principal, emi, months, fees)
    data["total_extra_cost"] = round(emi * months + fees - principal, 2)
    return data
