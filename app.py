# central_server.py
from flask import Flask, Response, render_template, request
import cv2
import numpy as np

app = Flask(__name__)

frame = None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    def generate():
        global frame
        while True:
            if frame is not None:
                # Encode the frame in JPEG format
                _, buffer = cv2.imencode('.jpg', frame)
                frame_bytes = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            else:
                yield b''

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/receive_feed', methods=['POST'])
def receive_feed():
    global frame
    # Read the received frame
    frame_data = request.data
    # Decode the JPEG frame back to OpenCV format
    nparr = np.frombuffer(frame_data, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return '', 204


