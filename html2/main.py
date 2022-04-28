from turtle import onclick
import plotly.express as px
import pandas as pd
import numpy as np
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
import datetime



flex_display = {'display':'flex'}
none_display = {'display':'none'}

frame_count = 0
import asyncio
import base64
import threading
from quart import Quart, websocket
from dash_extensions import WebSocket



# generate internet accumlated usage data, that follows the formula: y = 5X + 3, for 31 points
x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
y = [4*i + np.random.randint(-5,5) for i in x]
df = pd.DataFrame({"x": x, "y": y})
days = np.arange(1,31,1)
# use SVR to predict the future value of y
from sklearn.svm import SVR
svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
svr_rbf.fit(df[['x']], df['y'])
y_rbf = svr_rbf.predict(np.array(days).reshape(-1, 1))

fig = px.line(df[:25], x="x", y="y", title="Internet Usage")
# add the predicted value to the plot
fig.add_scatter(x=days[25:], y=y_rbf[25:], name="Predicted", mode="markers")
# draw horizontal line at y=140
fig.add_shape(type="line", x0=0, y0=140, x1=31, y1=140, line=dict(color="red", width=2), layer="below")
# change fig background color to transparent
fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
)

inverter_pwr_y = [221, 180, 181, 212, 211, 168, 185, 214, 172, 171, 202, 213, 205, 206, 241, 246, 163, 162, 206, 201, 159, 160, 202, 204, 161, 384, 386, 378, 375, 215, 201, 211, 212, 209, 210, 211, 210, 210, 167, 182, 210, 204, 130, 146, 187, 189, 148, 148, 222, 223, 179, 183, 221, 221, 180, 187, 221, 180, 179, 209, 224, 181, 205, 237, 258, 262, 223, 225, 275, 258, 217, 250, 249, 132, 176, 209, 232, 184, 209, 248, 258, 209, 212, 227, 258, 211, 189, 218, 295, 301, 278, 260, 299, 339, 275, 307, 309, 263, 269, 311, 307, 269, 276, 308, 257, 281, 305, 311, 272, 276, 319, 313, 268, 296, 308, 279, 283, 314, 313, 270, 2709, 354, 309, 327, 318, 277, 315, 325, 302, 818, 340, 474, 336, 318, 569, 306, 304, 335, 350, 309, 312, 314, 339, 277, 2577, 280, 227, 239, 276, 283, 249, 270, 335, 2669, 323, 320, 321, 318, 651, 731, 264, 243, 320, 315, 246, 259, 310, 321, 280, 257, 312, 311, 272, 277, 279, 300, 326, 2602, 2651, 353, 254, 327, 2607, 2559, 2438, 2424, 307, 282, 284, 324, 325, 294, 268, 313, 305, 263, 270, 319, 303, 262, 2628, 346, 346, 282, 285, 278, 328, 260, 281, 304, 327, 265, 314, 315, 270, 257, 304, 298, 258, 258, 300, 298, 321, 537, 550, 539, 2878, 290, 286, 284, 283, 296, 305, 298, 294, 293, 299, 268, 285, 319, 348, 288, 308, 289, 248, 259, 325, 328, 315, 309, 337, 356, 321, 279, 313, 2751, 339, 321, 340, 304, 302, 345, 350, 309, 277, 362, 339, 321, 316, 365, 363, 323, 283, 322, 309, 198, 161, 204, 198, 147, 157, 183, 218, 178, 197, 214, 174, 172]
inverter_pwr_x = [x for x in range(1, len(inverter_pwr_y)+1)]
feedin_pwr_y = [-221, -180, -181, -212, -211, -168, -185, -214, -172, -171, -202, -213, -205, -206, -241, -246, -163, -162, -206, -201, -159, -160, -202, -204, -161, -384, -386, -378, -375, -215, -201, -211, -212, -209, -210, -211, -210, -210, -167, -182, -210, -204, -130, -146, -187, -189, -148, -148, -222, -223, -179, -183, -221, -221, -180, -187, -221, -180, -179, -209, -224, -181, -205, -237, -258, -262, -223, -225, -275, -258, -217, -250, -249, -195, -176, -209, -232, -184, -209, -248, -258, -209, -212, -227, -258, -211, -180, 92, 72, -64, -265, -172, -5, -35, -45, -7, -2, -49, -30, 3, 21, -27, 3, -83, 17, -2, 5, -61, -3, 28, 4, 60, -25, -42, -69, 45, 101, -65, 73, 3, -87, -38, -29, -6, 282, 194, 51, 36, -4, -512, 644, 1468, 903, 1467, 2700, 915, 600, 419, 9, -66, -58, 61, 104, 637, 30, 341, 600, 222, -3, -27, 45, 521, 589, -493, 104, 333, 969, 1036, 385, 528, 289, 639, 806, 658, 692, 678, 568, 692, 177, 251, 352, 644, 506, 229, 195, 134, 84, -901, -816, -28, 28, 25, -599, -791, -655, -639, 44, 91, -71, -58, -15, -22, 23, -12, 28, 35, 11, 75, 31, 43, -1496, -32, -67, 64, -18, -17, -42, 3, -21, -44, -44, -3, -40, -52, -7, 3, -43, -36, 4, 2, -38, -35, -57, -13, -23, -14, -1937, 76, 7, 9, 8, -4, -14, -2, -2, 2, -4, 27, 8, -28, -51, 5, -15, 3, 45, 36, -34, -34, 52, 59, 30, 10, 41, 3, -32, -1892, 19, 44, 16, 57, 60, 16, 12, 48, 79, 2, 17, 37, 41, -3, -3, 39, 2, -39, -23, 4, 38, -2, 2, 54, 42, 17, -18, 25, 2, -13, 26, 28,]
feedin_pwr_x = [x for x in range(1, len(feedin_pwr_y)+1)]
load_pwr_y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -63, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 310, 367, 237, 13, 88, 294, 304, 230, 300, 307, 214, 239, 314, 328, 242, 279, 225, 274, 279, 310, 250, 269, 304, 323, 373, 243, 254, 239, 324, 384, 249, 386, 273, 2622, 316, 280, 321, 600, 471, 366, 361, 298, 306, 984, 1942, 1239, 1785, 3269, 1221, 904, 754, 359, 243, 254, 375, 443, 914, 2607, 621, 827, 461, 273, 256, 294, 791, 924, 2176, 427, 653, 1290, 1354, 1036, 1259, 553, 882, 1126, 973, 938, 937, 878, 1013, 457, 508, 664, 955, 778, 506, 474, 434, 410, 1701, 1835, 325, 282, 352, 2008, 1768, 1783, 1785, 351, 373, 213, 266, 310, 272, 291, 301, 333, 298, 281, 394, 334, 305, 1132, 314, 279, 346, 267, 261, 286, 263, 260, 260, 283, 262, 274, 263, 263, 260, 261, 262, 262, 260, 262, 263, 264, 524, 527, 525, 941, 366, 293, 293, 291, 292, 291, 296, 292, 295, 295, 295, 293, 291, 297, 293, 293, 292, 293, 295, 291, 294, 367, 368, 367, 366, 362, 282, 281, 859, 358, 365, 356, 361, 362, 361, 362, 357, 356, 364, 356, 358, 357, 362, 360, 362, 285, 283, 286, 202, 199, 202, 200, 201, 199, 200, 200, 203, 199, 201, 200, 200]
load_pwr_x = [x for x in range(1, len(load_pwr_y)+1)]
inverter_pwr = pd.DataFrame({"x": inverter_pwr_x, "y": inverter_pwr_y})
x_line = pd.DataFrame({"x": inverter_pwr_x, "y": inverter_pwr_x})
feedin_pwr = pd.DataFrame({"x": feedin_pwr_x, "y": feedin_pwr_y})
electricity_fig = px.line(x_line, x="x", y="y", title="Power Usage")
electricity_fig.add_scatter(x=inverter_pwr["x"], y=inverter_pwr["y"], name="Inverter")
electricity_fig.add_scatter(x=feedin_pwr["x"], y=feedin_pwr["y"], name="Feedin Power")
electricity_fig.add_scatter(x=load_pwr_x, y=load_pwr_y, name="Load Power")
# change electricity_fig backgroud color to transparent
electricity_fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
)


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
        html.H1("Hello Back, Irena", id="placeholder"),
        html.Button("Home/Dashboard", id="m_button", n_clicks=0),
        # <iframe style="border-radius:12px" src="https://open.spotify.com/embed/playlist/09vDAnj6ezlRoHDu6fH1BW?utm_source=generator" width="50%" height="80" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>
        html.Iframe(id='spotify', src="https://open.spotify.com/embed/playlist/37i9dQZEVXcKQGtztD3HbB?utm_source=generator", allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"),
    ],id='menu', className="place-items-center bg-plant bg-center bg-cover box-border min-h-screen w-full p-8 lg:p-0"),
    
    html.Div([



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

    ], id = "mainboard",className="mainboard", style=flex_display),

    html.Div([
        
        html.Div([
            html.Div([
                html.H1(datetime.datetime.now().strftime("%A, "), style={"color": "#52697C"}),
                html.H2(datetime.datetime.now().strftime(" %d %B %Y"), style={"padding-left": "10px", "color": "#778997"}),
            ], id='date-container', style={'display': 'flex', 'position': 'absolute', 'right': '10px', 'top': '8px'}),
            # BAN banner
            html.Div([
            # consists of 3 parts: left, center, right
                html.Div([
                    html.Div([
                        html.H6("Internet Usage", className="text-sm", style={"color": "#778997"}),
                        html.H5("104 GB", className="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white", style={"color": "#40e122", "text-align": "center", "font-size": "50px"}),
                        html.H6("expires in ", className="font-normal text-gray-700 dark:text-gray-400", style={"color": "#778997"}),
                        html.H5("5 Days", className="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white", style={"color": "#278de1", "padding-left": "40px", "font-size": "25px"}),
                    ], className="p-6 bg-gray-100 rounded-lg block p-6 max-w-sm rounded-lg border-gray-200 shadow-md hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700", style={"width": "22em"})
                ], className="BAN1 grid grid-cols-1 gap-4 grid-BANs"),
                html.Div([
                    html.Div([
                        html.H5("BAN", className="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white", style={"color": "#52697C"}),
                        html.H6("BAN", className="font-normal text-gray-700 dark:text-gray-400", style={"color": "#778997"}),
                    ], className="p-6 bg-gray-100 rounded-lg block p-6 max-w-sm  rounded-lg  border-gray-200 shadow-md hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700")
                ], className="BAN2 grid grid-cols-1 gap-4 grid-BANs"),
                html.Div([
                    html.Div([
                        html.H5("BAN", className="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white", style={"color": "#52697C"}),
                        html.H6("BAN", className="font-normal text-gray-700 dark:text-gray-400", style={"color": "#778997"}),
                    ], className="p-6 bg-gray-100 rounded-lg block p-6 max-w-sm  rounded-lg  border-gray-200 shadow-md hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700")
                ], className="BAN3 grid grid-cols-1 gap-4 grid-BANs"),
                
            ], className="ban-container BAN-Area", ),
            html.Div([
                dcc.Graph(id="internet_graph", figure=fig),
            ], className="dashbaord-container Graph1 glassmorphism "),
            html.Div([
                dcc.Graph(id="electricity_graph", figure=electricity_fig),
            ], className="electricity-container Graph2 glassmorphism "),
        ], className="test-container"),
    ], id = "dashboard" , style=none_display)

], style={"display":"flex"}, id="main")

app

@app.callback(
    Output("mainboard", 'style'),
    Output("dashboard", 'style'),
    Input("m_button", 'n_clicks')
)
def update_m_button(n_clicks):
    if n_clicks % 2 == 0:
        return flex_display, none_display
    else:
        return none_display, flex_display

app.clientside_callback("function(m){return m? m.data : '';}", Output(f"v0", "src"), Input(f"ws0", "message"))

if __name__ == '__main__':
    print("Running app", file=sys.stderr)
    threading.Thread(target=app.run_server).start()
    print("Server started", file=sys.stderr)
    server.run()