from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import datetime

app = Flask(__name__)

# Configure MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/webhookDB"
mongo = PyMongo(app)

# Define the collection
webhook_collection = mongo.db.webhooks

@app.route('/')
def api_root():
    return 'Welcome to the Webhook Receiver'

@app.route('/github', methods=['POST'])
def api_gh_message():
    if request.headers.get('Content-Type') == 'application/json':
        data = request.get_json()
        event_type = request.headers.get('X-GitHub-Event')
        
        if event_type == "push":
            # Extract relevant push details
            info = {
                "author": data['pusher']['name'],
                "to_branch": data['ref'].split('/')[-1],
                "timestamp": datetime.datetime.utcnow(),  # Use current UTC time for consistency
                "event": "push"
            }
        elif event_type == "pull_request":
            # Extract relevant pull request details
            info = {
                "author": data['pull_request']['user']['login'],
                "from_branch": data['pull_request']['head']['ref'],
                "to_branch": data['pull_request']['base']['ref'],
                "timestamp": data['pull_request']['created_at'],
                "event": "pull_request"
            }
        else:
            # Log unhandled events (if any)
            return jsonify({"error": f"Unhandled event type: {event_type}"}), 400

        # Store the event details in MongoDB
        webhook_collection.insert_one(info)
        return jsonify(info), 201

    return jsonify({"error": "Unsupported Media Type"}), 415

@app.route('/events', methods=['GET'])
def get_events():
    events = webhook_collection.find().sort("timestamp", -1)  # Sort by timestamp in descending order
    events_list = []
    
    for event in events:
        # Format the timestamp for display
        formatted_timestamp = event.get("timestamp").strftime('%d %B %Y - %I:%M %p UTC')
        
        # Append formatted event details
        events_list.append({
            "author": event.get("author"),
            "to_branch": event.get("to_branch"),
            "from_branch": event.get("from_branch", ""),  # Default to an empty string if not available
            "timestamp": formatted_timestamp,
            "event": event.get("event")
        })

    return jsonify(events_list)

if __name__ == '__main__':
    app.run(debug=True)
