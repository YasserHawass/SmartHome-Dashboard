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
from dash_extensions import DeferScript


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
                html.Div([
                    html.Img(src="https://i.ibb.co/09fmVRK/plan.png",className="w-full"),
                    html.Div(id="light1" ,className="light-1 absolute rounded-full"),
                    html.Div(id="light2" ,className="light-2 absolute rounded-full"),
                    html.Div(id="light3" ,className="light-3 absolute rounded-full"),
                    html.Img(id="vacuu" ,className="vacuum-start absolute", src="https://img.icons8.com/external-vitaliy-gorbachev-flat-vitaly-gorbachev/58/000000/external-robot-vacuum-cleaner-internet-technology-vitaliy-gorbachev-flat-vitaly-gorbachev.png"),
                    html.Div(id="senso" ,className="absolute rounded-full"),
                ],className="relative grid place-items-center w-full lg:w-4/6", id="iew-container"),
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

app.run_server()