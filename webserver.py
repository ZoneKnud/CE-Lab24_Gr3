from threading import Lock
from flask import Flask, render_template, jsonify, session, request, \
    copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
from flask_cors import CORS

import json

async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()
CORS(app)


@app.route('/receive_data', methods=['POST'])
def receive_data():
    if "data" in request.json:
        data = request.json['data']
        data = json.loads(data)

        socketio.emit('data_from_robot',{'data': data})
    elif "color" in request.json:
        color = request.json['color']
        color = json.loads(color)

        socketio.emit('data_from_robot_color',{'data': color})

    return "ok"

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected', request.sid)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')