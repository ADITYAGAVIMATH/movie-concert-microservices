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
    event = next((e for e in events if e["id"] == event_id), None)
    if event:
        return jsonify(event)
    return jsonify({"error": "Event not found"}), 404


@app.route("/movies", methods=["GET"])
def get_movies():
    movies = [e for e in events if e.get("type") == "movie"]
    return jsonify(movies), 200


@app.route("/concerts", methods=["GET"])
def get_concerts():
    concerts = [e for e in events if e.get("type") == "concert"]
    return jsonify(concerts), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
