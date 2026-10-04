from flask import Flask, jsonify, request
import uuid

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "service": "Payment Service",
        "status": "running"
    })


@app.route("/payments", methods=["POST"])
def process_payment():
    data = request.get_json()

    if not data or "user_id" not in data or "amount" not in data:
        return jsonify({
            "error": "user_id and amount are required"
        }), 400

    try:
        amount = float(data["amount"])
    except (ValueError, TypeError):
        return jsonify({
            "error": "Amount must be a valid number"
        }), 400

    if amount <= 0:
        return jsonify({
            "error": "Amount must be greater than zero"
        }), 400

    user_id = data["user_id"]
    transaction_id = str(uuid.uuid4())

    return jsonify({
        "message": "Payment successful",
        "transaction_id": transaction_id,
        "user_id": user_id,
        "amount": amount,
        "status": "completed"
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
