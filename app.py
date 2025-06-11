from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/split", methods=["POST"])
def split_expense():
    data = request.get_json()
    members = data.get("members", [])
    expenses = data.get("expenses", [])

    if not members or not expenses:
        return jsonify({"error": "Invalid input"}), 400

    total = sum(e["amount"] for e in expenses)
    share = total / len(members)

    paid_map = {member: 0 for member in members}
    for e in expenses:
        paid_map[e["paid_by"]] += e["amount"]

    balance = {m: round(paid_map[m] - share, 2) for m in members}
    return jsonify(balance)

@app.route("/", methods=["GET"])
def index():
    return "Smart Expense Splitter API is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
