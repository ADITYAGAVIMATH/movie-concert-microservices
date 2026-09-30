from flask import Flask, jsonify

app = Flask(__name__)

events = [
    {
        "id": 1,
        "name": "Avengers: Secret Wars",
        "type": "movie",
        "venue": "PVR Hubli",
        "date": "2026-10-05"
    },
    {
        "id": 2,
        "name": "Arijit Singh Live",
        "type": "concert",
        "venue": "Bengaluru",
        "date": "2026-10-10"
    }
]


@app.route("/")
def home():
    return jsonify({
        "service": "Event Service",
        "status": "running"
    })


@app.route("/events", methods=["GET"])
def get_events():
    return jsonify(events)


@app.route("/events/<int:event_id>", methods=["GET"])
def get_event(event_id):
    for event in events:
        if event["id"] == event_id:
            return jsonify(event)

    return jsonify({"error": "Event not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)