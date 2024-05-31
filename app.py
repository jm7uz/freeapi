from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/video-watched', methods=['POST'])
def video_watched():
    watch_data = request.get_json()
    print(watch_data)
    return jsonify({"message": "Data scanning..."})

@app.route('/', methods=['GET'])
def video_watcheds():
    return jsonify({"message": "hello"})

if __name__ == "__main__":
    app.run()
