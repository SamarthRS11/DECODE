import os, json, re, time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pypdf import PdfReader

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.7-flash")

PROMPT = """You are a contract explainer for ordinary people with no legal background.
Analyze the contract below. Return ONLY valid JSON in exactly this shape:

{
  "contract_type": "e.g. Rental agreement",
  "summary": "5-6 sentence plain-English summary",
  "key_terms": [
    {"label": "e.g. Monthly rent", "value": "e.g. Rs 25,000", "category": "fee|penalty|interest|deposit|payment|renewal|termination|other"}
  ],
  "clauses": [
    {
      "original_quote": "EXACT text copied word-for-word from the contract",
      "category": "fee|penalty|interest|deposit|payment|renewal|termination|other",
      "simple_explanation": "1-2 simple sentences, grade 8 reading level",
      "risk_level": "info|review|attention",
      "risk_reason": "why this deserves attention, or empty string if info"
    }
  ]
}

Rules:
- original_quote must be copied EXACTLY from the contract. Never paraphrase it.
- Cover the 8-15 most important clauses, especially money, penalties, renewal and termination.
- Use "attention" only for clauses that are one-sided, vague, or have costly consequences.
- Use cautious wording like "may", "could", "worth checking". These are potential concerns, not legal conclusions.
- Never cite laws or case names. Never give legal advice.

CONTRACT:
"""

def extract_pdf_text(file) -> str:
    reader = PdfReader(file)
    return "\n".join((page.extract_text() or "") for page in reader.pages)

def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().lower()

def analyze_contract(text: str) -> dict:
    last_error = None
    for attempt in range(4):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=PROMPT + text,
                config=types.GenerateContentConfig(response_mime_type="application/json"),
            )
            data = json.loads(response.text)
            break
        except Exception as e:
            last_error = e
            time.sleep(3 * (attempt + 1))
    else:
        raise RuntimeError(f"The AI service is busy. Please try again in a minute. ({last_error})")

    # Anti-hallucination check: does the quote really appear in the contract?
    contract_norm = _norm(text)
    for clause in data.get("clauses", []):
        clause["verified"] = _norm(clause.get("original_quote", "")) in contract_norm
    return data
