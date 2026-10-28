import numpy_financial as npf
import json
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

def calculate_real_apr(principal: float, monthly_emi: float, tenure_months: int, upfront_fees: float) -> float:
    net_disbursed = principal - upfront_fees
    if net_disbursed <= 0 or monthly_emi <= 0 or tenure_months <= 0:
        return 0.0

    cash_flows = [net_disbursed] + [-monthly_emi] * tenure_months
    
    try:
        monthly_irr = npf.irr(cash_flows)
        annual_apr = monthly_irr * 12 * 100
        return round(float(annual_apr), 2)
    except Exception:
        return 0.0

def audit_contract_with_llm(contract_text: str) -> dict:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Missing GEMINI_API_KEY in .env file")

    client = genai.Client(api_key=api_key)

    prompt = f"""
    You are an expert consumer finance auditor. Read the loan or EMI agreement text below.
    Extract the following variables into valid JSON format with NO surrounding markdown or backticks:
    {{
      "principal": <float: total sanction amount>,
      "tenure_months": <int: loan duration in months>,
      "stated_rate": <float: advertised flat interest percentage p.a.>,
      "monthly_emi": <float: monthly installment amount>,
      "upfront_fees": <float: sum of processing fees, admin charges, mandatory insurance deducted at source>,
      "red_flags": [
        {{
          "clause": "<clause title or number>",
          "issue": "<short explanation of the predatory term or trap>",
          "severity": "<HIGH or MEDIUM>"
        }}
      ],
      "plain_summary": "<2-sentence plain-English verdict for an everyday consumer>"
    }}

    Contract Text:
    {contract_text[:8000]}
    """

    response = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL", "gemini-3.7-flash"),
        contents=prompt,
        config={"response_mime_type": "application/json"}
    )
    
    raw_text = response.text.strip()
    if raw_text.startswith("```json"):
        raw_text = raw_text[7:]
    if raw_text.startswith("```"):
        raw_text = raw_text[3:]
    if raw_text.endswith("```"):
        raw_text = raw_text[:-3]

    data = json.loads(raw_text.strip())
    
    real_apr = calculate_real_apr(
        principal=float(data.get("principal", 0)),
        monthly_emi=float(data.get("monthly_emi", 0)),
        tenure_months=int(data.get("tenure_months", 1)),
        upfront_fees=float(data.get("upfront_fees", 0))
    )
    
    data["calculated_apr"] = real_apr
    total_paid = float(data.get("monthly_emi", 0)) * int(data.get("tenure_months", 1))
    data["total_extra_cost"] = round(total_paid + float(data.get("upfront_fees", 0)) - float(data.get("principal", 0)), 2)
    
    return data

if __name__ == "__main__":
    sample = "Loan: INR 100,000 for 12 months at 10% flat rate. EMI: 9166. Upfront processing fee: 3500 deducted. Insurance: 2500 deducted."
    print("Testing local calculation...")
    res = audit_contract_with_llm(sample)
    print("Result Calculated APR:", res.get("calculated_apr"), "%")
