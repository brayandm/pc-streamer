import cv2
import numpy as np
from flask import Flask, Response
from flask_cors import CORS
import mss
import mss.tools

app = Flask(__name__)
CORS(app)


def generate_frames():
    with mss.mss() as sct:
        monitor = sct.monitors[1]

        while True:
            sct_img = sct.grab(monitor)

            img = np.array(sct_img)

            img = cv2.resize(img, (1280, 720))

            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            ret, buffer = cv2.imencode(".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
            frame = buffer.tobytes()

            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@app.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/")
def index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Screen Stream</title>
        <style>
            body, html {
                margin: 0;
                padding: 0;
                width: 100vw;
                height: 100vh;
                background-color: black;
                display: flex;
                justify-content: center;
                align-items: center;
                overflow: hidden; /* Para eliminar el scroll */
            }
            .video-container {
                width: 100vw; /* Ajusta este valor según el tamaño deseado */
                height: 100vh; /* Mantener la proporción 4:3 */
                position: relative;
            }
            .video-container img {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                object-fit: contain; /* Cambiado a 'contain' para ajustar la imagen sin recortarla */
            }
        </style>
    </head>
    <body>
        <div class="video-container">
            <img src="/video_feed" alt="Video Stream" />
        </div>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
