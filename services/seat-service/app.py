from flask import Flask, jsonify, request

app = Flask(__name__)

# Initial seat layout for events (Rows A and B, seats 1-5)
seats_db = {
    1: {
        "A1": "available",
        "A2": "available",
        "A3": "available",
        "A4": "available",
        "A5": "available",
        "B1": "available",
        "B2": "available",
        "B3": "available",
        "B4": "available",
        "B5": "available"
    },
    2: {
        "A1": "available",
        "A2": "available",
        "A3": "available",
        "A4": "available",
        "A5": "available",
        "B1": "available",
        "B2": "available",
        "B3": "available",
        "B4": "available",
        "B5": "available"
    }
}


@app.route("/")
def home():
    return jsonify({
        "service": "Seat Service",
        "status": "running"
    })


@app.route("/seats/<int:event_id>", methods=["GET"])
def get_seats(event_id):
    if event_id not in seats_db:
        return jsonify({"error": "Event not found"}), 404
    return jsonify({
        "event_id": event_id,
        "seats": seats_db[event_id]
    })


@app.route("/seats/<int:event_id>/available", methods=["GET"])
def get_available_seats(event_id):
    if event_id not in seats_db:
        return jsonify({"error": "Event not found"}), 404
    available = [seat for seat, status in seats_db[event_id].items() if status == "available"]
    return jsonify({
        "event_id": event_id,
        "available_seats": available
    })


@app.route("/seats/<int:event_id>/reserve", methods=["POST"])
def reserve_seats(event_id):
    if event_id not in seats_db:
        return jsonify({"error": "Event not found"}), 404

    data = request.get_json()
    if not data or "seats" not in data:
        return jsonify({"error": "Seats list is required"}), 400

    requested_seats = data["seats"]
    if not isinstance(requested_seats, list) or len(requested_seats) == 0:
        return jsonify({"error": "Invalid seats list"}), 400

    event_seats = seats_db[event_id]
    unavailable = []

    for seat in requested_seats:
        if seat not in event_seats or event_seats[seat] != "available":
            unavailable.append(seat)

    if unavailable:
        return jsonify({
            "error": "Some seats are not available",
            "seats": unavailable
        }), 409

    for seat in requested_seats:
        event_seats[seat] = "reserved"

    return jsonify({
        "message": "Seats reserved successfully",
        "event_id": event_id,
        "seats": requested_seats
    }), 200


@app.route("/seats/<int:event_id>/release", methods=["POST"])
def release_seats(event_id):
    if event_id not in seats_db:
        return jsonify({"error": "Event not found"}), 404

    data = request.get_json()
    if not data or "seats" not in data:
        return jsonify({"error": "Seats list is required"}), 400

    seats_to_release = data["seats"]
    if not isinstance(seats_to_release, list):
        return jsonify({"error": "Invalid seats list"}), 400

    event_seats = seats_db[event_id]
    for seat in seats_to_release:
        if seat in event_seats:
            event_seats[seat] = "available"

    return jsonify({
        "message": "Seats released successfully",
        "event_id": event_id,
        "seats": seats_to_release
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
