import os
import uuid
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Service endpoints configurable via environment variables with container defaults
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user-service-container:5000")
EVENT_SERVICE_URL = os.getenv("EVENT_SERVICE_URL", "http://event-service-container:5000")
SEAT_SERVICE_URL = os.getenv("SEAT_SERVICE_URL", "http://seat-service-container:5000")
PAYMENT_SERVICE_URL = os.getenv("PAYMENT_SERVICE_URL", "http://payment-service-container:5000")

# In-memory store for confirmed bookings
bookings_db = []


@app.route("/")
def home():
    return jsonify({
        "service": "Booking Service",
        "status": "running"
    })


@app.route("/bookings", methods=["GET"])
def get_bookings():
    return jsonify(bookings_db), 200


@app.route("/bookings/<string:booking_id>", methods=["GET"])
def get_booking(booking_id):
    booking = next((b for b in bookings_db if b["booking_id"] == booking_id), None)
    if booking:
        return jsonify(booking), 200
    return jsonify({"error": "Booking not found"}), 404


@app.route("/bookings", methods=["POST"])
def create_booking():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Booking data is required"
        }), 400

    required_fields = ["user_id", "event_id", "seats"]
    for field in required_fields:
        if field not in data:
            return jsonify({
                "error": f"{field} is required"
            }), 400

    user_id = data["user_id"]
    event_id = data["event_id"]
    requested_seats = data["seats"]

    if not requested_seats or not isinstance(requested_seats, list):
        return jsonify({
            "error": "At least one seat is required as a list"
        }), 400

    # ------------------------------------------------
    # 1. Verify User
    # ------------------------------------------------
    try:
        user_response = requests.get(
            f"{USER_SERVICE_URL}/users/{user_id}",
            timeout=5
        )
    except requests.RequestException:
        return jsonify({
            "error": "User Service is unavailable"
        }), 503

    if user_response.status_code != 200:
        return jsonify({
            "error": "User not found"
        }), 404

    user = user_response.json()

    # ------------------------------------------------
    # 2. Verify Event
    # ------------------------------------------------
    try:
        event_response = requests.get(
            f"{EVENT_SERVICE_URL}/events/{event_id}",
            timeout=5
        )
    except requests.RequestException:
        return jsonify({
            "error": "Event Service is unavailable"
        }), 503

    if event_response.status_code != 200:
        return jsonify({
            "error": "Event not found"
        }), 404

    event = event_response.json()

    # ------------------------------------------------
    # 3. Reserve Seats
    # ------------------------------------------------
    try:
        seat_response = requests.post(
            f"{SEAT_SERVICE_URL}/seats/{event_id}/reserve",
            json={"seats": requested_seats},
            timeout=5
        )
    except requests.RequestException:
        return jsonify({
            "error": "Seat Service is unavailable"
        }), 503

    if seat_response.status_code != 200:
        return jsonify({
            "error": "Seat reservation failed",
            "details": seat_response.json()
        }), seat_response.status_code

    # ------------------------------------------------
    # 4. Calculate Amount (500 per seat)
    # ------------------------------------------------
    total_amount = len(requested_seats) * 500

    # ------------------------------------------------
    # 5. Process Payment
    # ------------------------------------------------
    try:
        payment_response = requests.post(
            f"{PAYMENT_SERVICE_URL}/payments",
            json={
                "user_id": user_id,
                "amount": total_amount
            },
            timeout=5
        )
    except requests.RequestException:
        # Compensating transaction: release reserved seats
        requests.post(
            f"{SEAT_SERVICE_URL}/seats/{event_id}/release",
            json={"seats": requested_seats},
            timeout=5
        )
        return jsonify({
            "error": "Payment Service is unavailable, seats released"
        }), 503

    if payment_response.status_code != 200:
        # Compensating transaction: release reserved seats
        requests.post(
            f"{SEAT_SERVICE_URL}/seats/{event_id}/release",
            json={"seats": requested_seats},
            timeout=5
        )
        return jsonify({
            "error": "Payment failed, seats released",
            "details": payment_response.json()
        }), payment_response.status_code

    payment = payment_response.json()

    # ------------------------------------------------
    # 6. Confirm Booking
    # ------------------------------------------------
    booking_id = str(uuid.uuid4())
    booking_record = {
        "message": "Booking created successfully",
        "booking_id": booking_id,
        "user": user,
        "event": event,
        "seats": requested_seats,
        "amount": total_amount,
        "payment": payment,
        "status": "confirmed"
    }

    bookings_db.append(booking_record)
    return jsonify(booking_record), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
