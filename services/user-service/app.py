from flask import Flask, jsonify, request

app = Flask(__name__)

users = [
    {
        "id": 1,
        "name": "Manasa",
        "email": "manasa@example.com"
    },
    {
        "id": 2,
        "name": "Renuka",
        "email": "renuka@test.conm"
    },
    {
        "id": 3,
        "name": "Aditya",
        "email": "aditya@test.conm"
    }
]


@app.route("/")
def home():
    return jsonify({
        "service": "User Service",
        "status": "running"
    })


@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users)


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404


@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    if not data or "name" not in data or "email" not in data:
        return jsonify({
            "error": "Name and email are required"
        }), 400

    new_user = {
        "id": len(users) + 1,
        "name": data["name"],
        "email": data["email"]
    }

    users.append(new_user)
    return jsonify(new_user), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
