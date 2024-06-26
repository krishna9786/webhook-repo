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
        # Example structure to be stored, you need to extract actual details from the payload
        event_type = request.headers.get('X-GitHub-Event')
        if event_type == "push":
            # Extract relevant push details
            info = {
                "author": data['pusher']['name'],
                "to_branch": data['ref'].split('/')[-1],
                "timestamp": datetime.datetime.utcnow(),
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
        # Add more cases if needed
        else:
            info = {"error": "Unhandled event"}

        # Store in MongoDB
        webhook_collection.insert_one(info)
        return jsonify(info), 201
    else:
        return jsonify({"error": "Unsupported Media Type"}), 415

if __name__ == '__main__':
    app.run(debug=True)
