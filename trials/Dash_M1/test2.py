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

# to run this code, using jupyter on VS Code
from plotly.offline import plot
import plotly.io as pio
# pio.renderers.default = "notebook_connected"
# pio.renderers.default = "browser"
# pio.renderers.default = "webgl"

from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State

# mp_drawing = mp.solutions.drawing_utils
# mp_pose = mp.solutions.pose


class VideoCamera(object):
    def __init__(self, video_path):
        self.video = cv2.VideoCapture(video_path)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, frame = self.video.read()
            
        # We will search face in every 15 frames to speed up process.
        # global frame_count
        # frame_count += 1
        # if frame_count % 15 == 0:    
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
            # mp_drawing.draw_landmarks(frame, face_locations.DrawingSpec(color=(0, 255, 0), alpha=0.7))
        _, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
            # plt.imshow(frame)        

            # Find all the faces and face encodings in the current frame of video
        #     rgb_frame = frame[:, :, ::-1]
        #     face_locations = face_recognition.face_locations(rgb_frame)
            
        #     # If faces were found, we will mark it on frame with blue dots
        #     for face_location in face_locations:        
        #         plt.plot(face_location[1], face_location[0], 'bo')
        #         plt.plot(face_location[1], face_location[2], 'bo')
        #         plt.plot(face_location[3], face_location[2], 'bo')
        #         plt.plot(face_location[3], face_location[0], 'bo')

        # # with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        #     # success, image = self.video.read()

        #     # # Recolor image to RGB
        #     # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        #     # image.flags.writeable = False

        #     # # Make detection
        #     # results = pose.process(image)

        #     # # Recolor back to BGR
        #     # image.flags.writeable = True
        #     # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        #     # # Render detections
        #     # mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
        #     #                           mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
        #     #                           mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
        #     #                           )

        #     # _, jpeg = cv2.imencode('.jpg', image)
            # return jpeg.tobytes()


# Setup small Quart server for streaming via websocket, one for each stream.
server = Quart(__name__)
n_streams = 2


async def stream(camera, delay=None):
    while True:
        if delay is not None:
            await asyncio.sleep(delay)  # add delay if CPU usage is too high
        frame = camera.get_frame()
        await websocket.send(f"data:image/jpeg;base64, {base64.b64encode(frame).decode()}")


@server.websocket("/stream0")
async def stream0():
    camera = VideoCamera(0)
    await stream(camera,2)


@server.websocket("/stream1")
async def stream1():
    camera = VideoCamera(0)
    await stream(camera,2)


# Create small Dash application for UI.
app = dash.Dash(__name__)
app.layout = html.Div(
    [html.Img(style={'width': '40%', 'padding': 10}, id=f"v{i}") for i in range(n_streams)] +
    [WebSocket(url=f"ws://127.0.0.1:5000/stream{i}", id=f"ws{i}") for i in range(n_streams)]
)
# Copy data from websockets to Img elements.
for i in range(n_streams):
    app.clientside_callback("function(m){return m? m.data : '';}", Output(f"v{i}", "src"), Input(f"ws{i}", "message"))

if __name__ == '__main__':
    threading.Thread(target=app.run_server).start()
    server.run()