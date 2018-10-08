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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#app = dash.Dash()
app.config['suppress_callback_exceptions']=True
#app.scripts.config.serve_locally = True

app.layout = html.Div(children = [
                                html.H1('Simplified* TURF simulator'),
                                html.P('* only maximal incremental path calculated'),
                                html.H2('Upload CSV file'),
                                dcc.Upload(id='upload-file',
                                            children=[html.Button('Upload File')],multiple=False),
                                html.Hr(),
                                html.Div(id='el_list',style={'width':'50%','float':'left'}),
                                html.Div(id='incr'),
                                html.Div(id='incr-graph')
                                ])



@app.callback(Output('el_list', 'children'),
              [Input('upload-file', 'contents')])
def update_output(list_of_contents):
    if list_of_contents is not None:
        df = parse_contents(list_of_contents)
        val = df.columns[2:df.shape[1]]
        children = [dcc.Checklist(id='symulator',options=[{'label':i, 'value':i} for i in val],values=val,style={'display':'block'}),
                    dcc.Graph(id='usage',figure={'data':[go.Bar(x=val,y=[100*calc_freq(df,i) for i in val])],
                                                 'layout':go.Layout(title='Reach of single elements')}),
                    html.H2(id='total_reach',children=[calculate_reach(df,val)])]
        return children

@app.callback(Output('total_reach', 'children'),
              [Input('upload-file', 'contents'),Input('symulator', 'values')])
def update_reach(list_of_contents,val):
    if list_of_contents is not None:
        df = parse_contents(list_of_contents)
        return calculate_reach(df,val)

@app.callback(Output('usage', 'figure'),
              [Input('upload-file', 'contents'),Input('symulator', 'values')])
def update_usage(list_of_contents,val):
    if list_of_contents is not None:
        df = parse_contents(list_of_contents)
        return {'data':[go.Bar(x=val,y=[100*calc_freq(df,i) for i in val])]
                ,'layout':go.Layout(title='Reach of single elements')}

@app.callback(Output('incr', 'children'),
              [Input('upload-file', 'contents')])
def show_bt(list_of_contents):
    if list_of_contents is not None:
        return [html.Button(id='generate_incr',children=['Generate incremental graph'])]

@app.callback(Output('incr-graph','children'),
             [Input('generate_incr','n_clicks')],
             [State('upload-file', 'contents'),State('symulator', 'values')])
def gen_inc_graph(clicks,list_of_contents,val):
    if list_of_contents is not None:
        df = parse_contents(list_of_contents)
        temp = calculate_incr(df[val])
        children = [dcc.Graph(id='increm_graph',figure={'data':[go.Scatter(x=temp[0],y=temp[1],mode='line+markers')],
                                                        'layout':go.Layout(title='Incremental graph')})]
        return children

if __name__ == '__main__':
    app.run_server()
