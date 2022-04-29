# %pylab inline 
import face_recognition
import cv2
import matplotlib.patches as patches
from IPython.display import clear_output
from matplotlib.pyplot import imshow
import matplotlib.pylab as plt


frame_count = 0
import asyncio
import base64
import mediapipe as mp
import threading
from quart import Quart, websocket
from dash_extensions import WebSocket
import dash

import plotly.express as px
import pandas as pd

from plotly.offline import plot
import plotly.io as pio


from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State


class VideoCamera(object):
    def __init__(self, video_path):
        self.video = cv2.VideoCapture(video_path)
        

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, frame = self.video.read()   
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # uncomment only use if using matplotlib to display
        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
        print(face_locations)
        for face_location in face_locations:
            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        _, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()


# Setup small Quart server for streaming via websocket, one for each stream.
server = Quart(__name__)


async def stream(camera, delay=None):
    while True:
        if delay is not None:
            await asyncio.sleep(delay)  # add delay if CPU usage is too high
        frame = camera.get_frame()
        await websocket.send(f"data:image/jpeg;base64, {base64.b64encode(frame).decode()}")


@server.websocket("/stream0")
async def stream0():
    # camera = VideoCamera("http://192.168.249.238/mjpeg/1")
    camera = VideoCamera(0)
    await stream(camera)


# Create small Dash application for UI.
app = dash.Dash(__name__)
app.layout = html.Div(
    [html.Img(style={'width': '40%', 'padding': 10}, id=f"v0")] +
    [WebSocket(url=f"ws://127.0.0.1:5000/stream0", id=f"ws0")]
)
# Copy data from websockets to Img elements.
app.clientside_callback("function(m){return m? m.data : '';}", Output(f"v0", "src"), Input(f"ws0", "message"))

if __name__ == '__main__':
    threading.Thread(target=app.run_server).start()
    server.run()