import base64
import datetime
import io
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

from functions import *

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash()
app.config['suppress_callback_exceptions']=True


app.layout = html.Div(children = [
                                html.H1('Simplified* TURF simulator'),
                                html.P('* only maximal incremental path calculated'),
                                html.H2('Upload CSV file'),
                                dcc.Upload(
                                            id='upload-file',
                                            children=[html.Button('Upload File')],multiple=False),
                                html.Hr(),
                                html.Div(id='el_list',children = [dcc.Checklist(id='symulator',options=[],values=[]),
                                                                  html.H2(id='total_reach'),
                                                                  dcc.Graph(id='usage')
                                                                  ],style={'width':'50%'}),
                                html.Hr(),
                                ])



@app.callback(Output('symulator', 'options'),
              [Input('upload-file', 'contents')])
def update_output(list_of_contents):
    if list_of_contents is not None:
        df = parse_contents(list_of_contents)
        return [{'label':i, 'value':i} for i in df.columns[2:df.shape[1]]]

@app.callback(Output('total_reach', 'children'),
              [Input('upload-file', 'contents'),Input('symulator', 'values')])
def update_reach(list_of_contents,vals):
    if list_of_contents is not None:
        df = parse_contents(list_of_contents)
        return calculate_reach(df,vals)

@app.callback(Output('usage', 'figure'),
              [Input('upload-file', 'contents'),Input('symulator', 'values')])
def update_usage(list_of_contents,vals):
    if list_of_contents is not None:
        df = parse_contents(list_of_contents)
    return {'data':[go.Bar(x=[vals],y=[100*calc_freq(df,i) for i in vals])]
            ,'layout':go.Layout(title='Reach of single elements')}




if __name__ == '__main__':
    app.run_server()
