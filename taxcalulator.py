# tax_calculator.py
from flask import Flask, request, jsonify

app = Flask(__name__)

# Malaysia Personal Income Tax Bracket 2024 (simplified for demo)
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
    previous_limit = 0.0

    for limit, rate in tax_brackets:
        if income > limit:
            taxable_income = limit - previous_limit
        else:
            taxable_income = income - previous_limit

        if taxable_income > 0:
            tax += taxable_income * rate

        if income <= limit:
            break

        previous_limit = limit

    return tax

@app.route('/calculate_tax', methods=['POST'])
def tax_endpoint():
    data = request.get_json()
    income = data.get('income', 0)

    try:
        income = float(income)
    except ValueError:
        return jsonify({"error": "Invalid income value"}), 400

    tax_amount = calculate_tax(income)
    net_income = income - tax_amount

    return jsonify({
        "income": income,
        "tax_amount": round(tax_amount, 2),
        "net_income": round(net_income, 2)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
