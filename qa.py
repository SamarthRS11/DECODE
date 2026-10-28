import json, time
from google.genai import types
from analyzer import client, MODEL, _norm

QA_PROMPT = """You answer questions about a contract for an ordinary person.
Use ONLY the contract text below. Do not use outside knowledge. Do not give legal advice.
If the contract does not clearly answer the question, set "found" to false and say the contract does not mention it.

Return ONLY valid JSON in this shape:
{"found": true or false, "answer": "simple 1-3 sentence answer", "quote": "EXACT text copied word-for-word from the contract that supports the answer, or empty string"}

CONTRACT:
{contract}

QUESTION: {question}
"""

def answer_question(contract_text: str, question: str) -> dict:
    prompt = QA_PROMPT.replace("{contract}", contract_text).replace("{question}", question)
    last_error = None
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(response_mime_type="application/json"),
            )
            data = json.loads(response.text)
            break
        except Exception as e:
            last_error = e
            time.sleep(3 * (attempt + 1))
    else:
        raise RuntimeError(f"The AI service is busy. Please try again. ({last_error})")

    quote = data.get("quote", "")
    data["verified"] = bool(quote) and _norm(quote) in _norm(contract_text)
    return data
