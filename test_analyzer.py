from analyzer import analyze_contract

try:
    text = open("sample_rental_agreement.txt", encoding="utf-8").read()
except FileNotFoundError:
    text = """RENTAL AGREEMENT. The Tenant shall pay monthly rent of Rs 25,000 on or before the 5th of each month.
A late payment penalty of 5% per day shall be charged on overdue rent.
The Tenant shall pay a refundable security deposit of Rs 1,50,000.
The lock-in period is 11 months; if the Tenant vacates earlier, the deposit shall be forfeited.
The Landlord may revise maintenance charges at his sole discretion.
This agreement renews automatically each year with a rent increase of 15%.
The Landlord may terminate this agreement at any time with 7 days notice."""

result = analyze_contract(text)
print("TYPE:", result["contract_type"])
print("SUMMARY:", result["summary"])
print("KEY TERMS:", len(result["key_terms"]))
for c in result["clauses"]:
    print(f"[{c['risk_level'].upper()}] verified={c['verified']} | {c['original_quote'][:70]}")
