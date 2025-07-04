from flask import Flask, request, jsonify

app = Flask(__name__)

# Malaysia personal income tax brackets (as of 2023)
tax_brackets = [
    (5000, 0.00),
    (20000, 0.01),
    (35000, 0.03),
    (50000, 0.08),
    (70000, 0.14),
    (100000, 0.21),
    (250000, 0.24),
    (400000, 0.245),
    (600000, 0.25),
    (2000000, 0.26),
    (float('inf'), 0.28)
]

def calculate_tax(income):
    tax = 0.0
    breakdown = []
    previous_limit = 0

    for limit, rate in tax_brackets:
        if income > limit:
            taxable = limit - previous_limit
        else:
            taxable = income - previous_limit

        if taxable > 0:
            taxed = taxable * rate
            breakdown.append({
                "bracket": f"{int(previous_limit)} - {int(limit)}",
                "rate": rate,
                "taxable_income": taxable,
                "taxed": taxed
            })
            tax += taxed

        if income <= limit:
            break
        previous_limit = limit

    return tax, breakdown

@app.route('/calculate_tax', methods=['POST'])
def tax_api():
    data = request.get_json()

    income = float(data.get('income', 0))
    deductions = float(data.get('deductions', 0))
    tax_credits = float(data.get('tax_credits', 0))
    is_self_employed = bool(data.get('self_employed', False))

    # Adjusted income = income - deductions - credits
    adjusted_income = max(0, income - deductions - tax_credits)

    # Calculate tax
    tax, breakdown = calculate_tax(adjusted_income)

    # Add 5% surcharge if self-employed
    surcharge = 0
    if is_self_employed:
        surcharge = round(tax * 0.05, 2)
        tax += surcharge

    return jsonify({
        "original_income": income,
        "deductions": deductions,
        "tax_credits": tax_credits,
        "adjusted_income": adjusted_income,
        "tax_amount": round(tax, 2),
        "surcharge_if_self_employed": surcharge,
        "net_income": round(income - tax, 2),
        "details": breakdown
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
