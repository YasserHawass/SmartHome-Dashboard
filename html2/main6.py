import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# code and plot setup
# settings
pd.options.plotting.backend = "plotly"
countdown = 20
#global df

# sample dataframe of a wide format
np.random.seed(4); cols = ["Temperature", "Humidity", "LUME"]
TempVar = 0
HumdVar = 0
LumeVar = 0

X = np.random.randn(1,len(cols))  
df=pd.DataFrame(X, columns=cols)
df.iloc[0]=0;

# plotly figure
fig = df.plot(template = 'plotly_dark')

app = JupyterDash(__name__)
app.layout = html.Div([
    html.H1("Streaming of random data"),
            dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        ),
    dcc.Graph(id='graph'),
])

# Define callback to update graph
@app.callback(
    Output('graph', 'figure'),
    [Input('interval-component', "n_intervals")]
)
def streamFig(value):
    global TempVar
    global HumdVar
    global LumeVar
    global df
    
    TempVar = np.random.randn()
    HumdVar = np.random.randn()
    LumeVar = np.random.randn()
    # Y = np.random.randn(1,len(cols))
    Y = np.array([[TempVar, HumdVar, LumeVar]])  
    df2 = pd.DataFrame(Y, columns = cols)
    df = df.append(df2, ignore_index=True)#.reset_index()
    # df.tail()
    # df3=df.copy()
    # df3 = df3.cumsum()
    fig = df.plot(template = 'plotly_dark')
    #fig.show()
    return(fig)

app.run_server(
              dev_tools_hot_reload =True, threaded=True)