from flask import Flask, jsonify, request

app = Flask(__name__)

users = [
    {
        "id": 1,
        "name": "Manasa",
        "email": "manasa@example.com"
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
    for user in users:
        if user["id"] == user_id:
            return jsonify(user)

    return jsonify({"error": "User not found"}), 404


@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    new_user = {
        "id": len(users) + 1,
        "name": data["name"],
        "email": data["email"]
    }

    users.append(new_user)

    return jsonify(new_user), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)