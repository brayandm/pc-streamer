# pc-streamer

A small collection of Python/Flask scripts that stream your PC's screen and/or webcam as MJPEG video to any web browser on your local network.

## What it does

Each script starts a lightweight Flask server that captures frames (via [OpenCV](https://opencv.org/) for the webcam and [mss](https://github.com/BoboTiG/python-mss) for screen capture), encodes them as JPEG, and serves them as a `multipart/x-mixed-replace` MJPEG stream. A minimal HTML page is served at `/` to view the stream(s) directly in the browser.

## Scripts

- **`camera_stream.py`**, Streams only the webcam (device index `0`) at `/video_feed`.
- **`screen_stream.py`**, Streams only the primary monitor (resized to 1280x720) at `/video_feed`.
- **`pc_stream.py`**, Streams both the screen and the webcam side by side, exposed at `/screen_feed` and `/camera_feed` respectively.

All three servers listen on `0.0.0.0:5000` and serve a viewer page at `/`.

## Requirements

Each script imports:

- `opencv-python` (`cv2`)
- `numpy`
- `flask`
- `flask-cors`
- `mss` (required by `pc_stream.py` and `screen_stream.py`)

There is no `requirements.txt` in the repo; install the dependencies manually, e.g.:

```bash
pip install opencv-python numpy flask flask-cors mss
```

## Usage

Run whichever script matches what you want to stream:

```bash
python pc_stream.py       # screen + webcam
python screen_stream.py   # screen only
python camera_stream.py   # webcam only
```

Then open `http://<host-ip>:5000/` in a browser to view the stream.

## Notes

- Video quality is fixed at JPEG quality 50 to keep bandwidth low.
- Webcam capture uses device index `0` and is set to 320x240.
- Screen capture grabs `monitor[1]` (the primary monitor via `mss`) and resizes to 1280x720.
- This is a small, single-purpose utility project rather than a packaged application, there are no tests, config files, or a project manifest.
