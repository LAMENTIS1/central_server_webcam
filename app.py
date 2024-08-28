from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('video_frame')
def handle_video_frame(frame):
    emit('video_frame', frame, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=False)
