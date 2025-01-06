from flask import Flask, request, jsonify, render_template
from config import Config
from models.local_database import LocalDatabase
from models.cloud_database import CloudDatabase
from services.cloud_sync import CloudSync
import threading

# Initialize Flask App
app = Flask(__name__)

# Initialize Databases
local_db = LocalDatabase(Config.LOCAL_DATABASE_FILE)
cloud_db = CloudDatabase(Config.MONGO_URI, Config.DATABASE_NAME, Config.COLLECTION_NAME) if Config.MONGO_URI else None

# Background Sync Initialization
def start_background_sync():
    if cloud_db:
        sync = CloudSync(local_db, cloud_db)
        thread = threading.Thread(target=sync.sync_to_cloud, daemon=True)
        thread.start()

start_background_sync()


# Route Handlers
@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')


@app.route('/submit_data', methods=['POST'])
def submit_data():
    """Submit data to the local database."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request must be JSON"}), 400

    voltage = data.get('voltage')
    timestamp = data.get('timestamp')

    if voltage is None or timestamp is None:
        return jsonify({"error": "Missing 'voltage' or 'timestamp'"}), 400

    try:
        local_db.enqueue_data({"voltage": voltage, "timestamp": timestamp})
        return jsonify({"message": "Data enqueued successfully."}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to enqueue data: {str(e)}"}), 500


@app.route('/get_local_data', methods=['GET'])
def get_local_data():
    """Retrieve all data from the local database."""
    try:
        data = local_db.get_all_data()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch local data: {str(e)}"}), 500


@app.route('/get_cloud_data', methods=['GET'])
def get_cloud_data():
    """Retrieve all data from the cloud database."""
    if not cloud_db:
        return jsonify({"error": "Cloud database is not configured."}), 400

    try:
        data = cloud_db.get_all_data()
        # Convert ObjectId to string for JSON serialization
        for item in data:
            if '_id' in item:
                item['_id'] = str(item['_id'])
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": f"Failed to fetch cloud data: {str(e)}"}), 500


# Main Execution
if __name__ == '__main__':
    app.run(debug=True)
