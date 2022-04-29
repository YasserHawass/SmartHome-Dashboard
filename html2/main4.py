# -*- coding: utf-8 -*-
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Input(id='input-1-submit', type='text', value='Montréal'),
    dcc.Input(id='input-2-submit', type='text', value='Canada'),
    html.Div(id='output-submit')
])


@app.callback(Output('output-submit', 'children'),
              [Input('input-1-submit', 'n_submit'), Input('input-1-submit', 'n_blur'),
               Input('input-2-submit', 'n_submit'), Input('input-2-submit', 'n_blur')],
              [State('input-1-submit', 'value'),
               State('input-2-submit', 'value')])
def update_output(ns1, nb1, ns2, nb2, input1, input2):
    return u'''
        Input 1 is "{}",
        and Input 2 is "{}"
    '''.format( input1, input2)


if __name__ == '__main__':
    app.run_server(debug=True)