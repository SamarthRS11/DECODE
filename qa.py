from analyzer import ask_json, _norm

QA_PROMPT = """You answer questions about a contract for an ordinary person.
Use ONLY the contract text below. Do not use outside knowledge. Do not give legal advice.
If the contract does not clearly answer the question, set "found" to false and say the contract does not mention it.

Return ONLY valid JSON in this shape:
{"found": true or false, "answer": "simple 1-3 sentence answer", "quote": "EXACT text copied word-for-word from the contract that supports the answer, or empty string"}

CONTRACT:
{contract}

QUESTION: {question}
"""

def answer_question(contract_text, question):
    prompt = QA_PROMPT.replace("{contract}", contract_text).replace("{question}", question)
    data = ask_json(prompt)
    quote = data.get("quote", "") or ""
    data["verified"] = bool(quote) and _norm(quote) in _norm(contract_text)
    return data
