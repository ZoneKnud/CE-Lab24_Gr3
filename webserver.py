from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

import json

app = Flask(__name__)
CORS(app)


currentData = []

@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.json['data']
    data = json.loads(data)
    global currentData
    currentData = data
    return "ok"


@app.route('/get_data')
def get_data():
    return jsonify(currentData)

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')