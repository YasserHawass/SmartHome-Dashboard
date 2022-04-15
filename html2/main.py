import plotly.express as px
import pandas as pd
import sys

# to run this code, using jupyter on VS Code
from plotly.offline import plot
import plotly.io as pio
# pio.renderers.default = "notebook_connected"
# pio.renderers.default = "browser"
# pio.renderers.default = "webgl"

from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
from dash_extensions import DeferScript

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
import threading
from quart import Quart, websocket
from dash_extensions import WebSocket


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
    print("stream0", file=sys.stderr)
    camera = VideoCamera(0)
    await stream(camera)


app = Dash(__name__ )
app.layout = html.Div([
    html.Div([
        html.H1("Hello Dash"),
        # <iframe style="border-radius:12px" src="https://open.spotify.com/embed/playlist/09vDAnj6ezlRoHDu6fH1BW?utm_source=generator" width="50%" height="80" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>
        html.Iframe(id='spotify', src="https://open.spotify.com/embed/playlist/09vDAnj6ezlRoHDu6fH1BW?utm_source=generator", allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"),
    ],id='menu', className="grid place-items-center bg-plant bg-center bg-cover box-border min-h-screen w-full p-8 lg:p-0"),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Img(src="https://i.ibb.co/09fmVRK/plan.png",className="w-full"),
                    html.Div(id="light-1" ,className="light-1 absolute rounded-full"),
                    html.Div(id="light-2" ,className="light-2 absolute rounded-full"),
                    html.Div(id="light-3" ,className="light-3 absolute rounded-full"),
                    html.Img(id="vacuum" ,className="vacuum-start absolute", src="https://img.icons8.com/external-vitaliy-gorbachev-flat-vitaly-gorbachev/58/000000/external-robot-vacuum-cleaner-internet-technology-vitaliy-gorbachev-flat-vitaly-gorbachev.png"),
                    html.Div(id="sensor" ,className="absolute rounded-full"),
                ],className="relative grid place-items-center w-full lg:w-4/6", id="view-container"),
                html.Div([
                    html.Div([
                        html.Div([
                            html.P("Lights", className="m-0 text-sm"),
                            html.Img(className="w-8 m-2", src="https://img.icons8.com/pastel-glyph/64/000000/light--v1.png"),
                            dcc.Input(id="lights-toggle-button", type="checkbox", className="absolute w-full h-full opacity-0"),
                            html.Label([
                                html.Div(className="toggle-dot bg-white m-1 h-5 w-5 rounded-full")
                            ],htmlFor="lights-toggle-button", className="flex items-center bg-gray-400 h-6 w-12 rounded-full")
                        ], className="glassmorphism relative grid place-items-center py-1 px-1 box-border w-full h-full cursor-pointer"),
                        html.Div([
                            html.P("Cleaning", className="m-0 text-sm"),
                            html.Img(className="w-8 m-2", src="https://img.icons8.com/external-vitaliy-gorbachev-lineal-vitaly-gorbachev/60/000000/external-robot-vacuum-cleaner-internet-of-things-vitaliy-gorbachev-lineal-vitaly-gorbachev.png"),
                            dcc.Input(id="cleaning-toggle-button", type="checkbox", className="absolute w-full h-full opacity-0"),
                            html.Label([
                                html.Div(className="toggle-dot bg-white m-1 h-5 w-5 rounded-full")
                            ],htmlFor="cleaning-toggle-button", className="flex items-center bg-gray-400 h-6 w-12 rounded-full")
                        ], className="glassmorphism relative grid place-items-center py-1 px-1 box-border w-full h-full cursor-pointer"),
                        html.Div([
                            html.P("Motion sensor", className="m-0 text-sm"),
                            html.Img(className="w-8 m-2", src="https://img.icons8.com/ios-glyphs/90/000000/infrared-beam-sending.png"),
                            dcc.Input(id="motion-sensor-toggle-button", type="checkbox", className="absolute w-full h-full opacity-0"),
                            html.Label([
                                html.Div(className="toggle-dot bg-white m-1 h-5 w-5 rounded-full")
                            ],htmlFor="motion-sensor-toggle-button", className="flex items-center bg-gray-400 h-6 w-12 rounded-full")
                        ], className="glassmorphism relative grid place-items-center py-1 px-1 box-border w-full h-full cursor-pointer"),

                    ],className="controls flex gap-5 grid-cols-2 md:grid-cols-4 lg:grid-cols-2 grid-rows-2 md:grid-rows-1 lg:grid-rows-2 max-w-full w-full"),
                ], className="controls flex place-items-center w-full mt-8 lg:mt-0", style={"width": "81%"})
            ],className="flex flex-col lg:gap-5 justify-center items-center w-full mt-8 lg:mt-16 mb-0 lg:my-16")
        ],className="glassmorphism flex flex-col box-border max-w-screen-lg w-full lg:w-8/12", style={"width":"81%"}),
        
    ], className="grid place-items-center bg-plant bg-center bg-cover box-border min-h-screen w-full p-8 lg:p-0"),
    html.Div([
        html.Div([
            html.Div([
                html.Div(
                    [html.Img(style={'width': '100%'}, id=f"v0")] +
                    [WebSocket(url=f"ws://127.0.0.1:5000/stream0", id=f"ws0")]
                ,className="relative grid place-items-center w-full lg:w-4/6", id="camera-container"),
                html.Div([
                    html.Div([
                        html.Div([
                            html.P("Lights", className="m-0 text-sm"),
                            html.Img(className="w-8 m-2", src="https://img.icons8.com/pastel-glyph/64/000000/light--v1.png"),
                            dcc.Input(id="ights-toggle-button", type="checkbox", className="absolute w-full h-full opacity-0"),
                            html.Label([
                                html.Div(className="toggle-dot bg-white m-1 h-5 w-5 rounded-full")
                            ],htmlFor="lights-toggle-button", className="flex items-center bg-gray-400 h-6 w-12 rounded-full")
                        ], className="glassmorphism relative grid place-items-center py-1 px-1 box-border w-full h-full cursor-pointer"),
                        html.Div([
                            html.P("Cleaning", className="m-0 text-sm"),
                            html.Img(className="w-8 m-2", src="https://img.icons8.com/external-vitaliy-gorbachev-lineal-vitaly-gorbachev/60/000000/external-robot-vacuum-cleaner-internet-of-things-vitaliy-gorbachev-lineal-vitaly-gorbachev.png"),
                            dcc.Input(id="leaning-toggle-button", type="checkbox", className="absolute w-full h-full opacity-0"),
                            html.Label([
                                html.Div(className="toggle-dot bg-white m-1 h-5 w-5 rounded-full")
                            ],htmlFor="cleaning-toggle-button", className="flex items-center bg-gray-400 h-6 w-12 rounded-full")
                        ], className="glassmorphism relative grid place-items-center py-1 px-1 box-border w-full h-full cursor-pointer"),
                        html.Div([
                            html.P("Motion sensor", className="m-0 text-sm"),
                            html.Img(className="w-8 m-2", src="https://img.icons8.com/ios-glyphs/90/000000/infrared-beam-sending.png"),
                            dcc.Input(id="otion-sensor-toggle-button", type="checkbox", className="absolute w-full h-full opacity-0"),
                            html.Label([
                                html.Div(className="toggle-dot bg-white m-1 h-5 w-5 rounded-full")
                            ],htmlFor="motion-sensor-toggle-button", className="flex items-center bg-gray-400 h-6 w-12 rounded-full")
                        ], className="glassmorphism relative grid place-items-center py-1 px-1 box-border w-full h-full cursor-pointer"),

                    ],className="controls flex gap-5 grid-cols-2 md:grid-cols-4 lg:grid-cols-2 grid-rows-2 md:grid-rows-1 lg:grid-rows-2 max-w-full w-full"),
                ], className="controls flex place-items-center w-full mt-8 lg:mt-0", style={"width": "81%"})
            ],className="flex flex-col lg:gap-5 justify-center items-center w-full mt-8 lg:mt-16 mb-0 lg:my-16")
        ],className="glassmorphism flex flex-col box-border max-w-screen-lg w-full lg:w-8/12", style={"width":"81%"}),
        
    ],id="camera", className="grid place-items-center bg-plant bg-center bg-cover box-border min-h-screen w-full p-8 lg:p-0")
], style={"display":"flex"}, id="main")

app

app.clientside_callback("function(m){return m? m.data : '';}", Output(f"v0", "src"), Input(f"ws0", "message"))

if __name__ == '__main__':
    print("Running app", file=sys.stderr)
    threading.Thread(target=app.run_server).start()
    print("Server started", file=sys.stderr)
    server.run()