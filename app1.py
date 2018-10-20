import base64
import datetime
import io
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

import base64
import datetime
import io
import time
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_auth


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,title='S_TURF', external_stylesheets=external_stylesheets)
#app = dash.Dash()
app.config['suppress_callback_exceptions']=True
#app.scripts.config.serve_locally = True
USERNAME_PASSWORD_PAIRS = [['Andrzej', 'Boguta']]
auth = dash_auth.BasicAuth(app,USERNAME_PASSWORD_PAIRS)
server = app.server

####################################################################
####################################################################
####################################################################
####################################################################
def parse_contents(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    return pd.read_csv(io.StringIO(decoded.decode('utf-8')))


def calc_freq(df,column,total=-1):
    if total<0:
        total = df.iloc[:,1].sum(axis=0)
    count = df[df[column]>0].iloc[:,1].sum(axis=0)
    return count/total

def calculate_reach(df,columns):
    df['suma'] = df[columns].sum(axis=1)
    return 'Reach: {} %'.format(100*calc_freq(df,'suma'))

def calculate_incr(df):
    labels=['no elements']
    reach=[0]
    total=df.shape[0]

    while (df.shape[1]>2):
        columns=df.columns[2:df.shape[1]]
        temp_max = 0
        for i in columns:
            a=calc_freq(df,i,total)
            if a>=temp_max:
                temp=i
                temp_max=a
        labels.append(temp)
        reach.append(reach[len(reach)-1]+100*temp_max)
        df=df[df[temp]==0]
        df.drop(temp,axis=1,inplace=True)

    return (labels,reach)
####################################################################
####################################################################
####################################################################
####################################################################

app.layout = html.Div(children = [
                                html.H1('Simplified* TURF simulator'),
                                html.P('* only maximal incremental path calculated'),
                                html.H2('Upload CSV file'),
                                dcc.Upload(id='upload-file',
                                            children=[html.Button('Upload File')],multiple=False),
                                html.Hr(),
                                html.Div(id='el_list',style={'display':'block'}),
                                html.Div([html.Div(id='ugraph',style={'width':'45%','float':'left','display':'inline','height':'200%'}),
                                html.Div(id='incr-graph',style={'width':'45%','float':'right','display':'inline','height':'200%'})])])


@app.callback(Output('el_list', 'children'),
              [Input('upload-file', 'contents')])
def update_output(list_of_contents):
    if list_of_contents is not None:
        df = parse_contents(list_of_contents)
        val = df.columns[2:df.shape[1]]
        children = [dcc.Checklist(id='symulator',options=[{'label':i, 'value':i} for i in val],values=val),
                    html.H2(id='total_reach',children=[calculate_reach(df,val)])]
        return children

@app.callback(Output('ugraph', 'children'),
              [Input('upload-file', 'contents')])
def update_output(list_of_contents):
    if list_of_contents is not None:
        df = parse_contents(list_of_contents)
        val = df.columns[2:df.shape[1]]
        children = [dcc.Graph(id='usage',figure={'data':[go.Bar(x=val,y=[100*calc_freq(df,i) for i in val])],
                                                 'layout':go.Layout(title='Reach of single elements')})]
        return children

@app.callback(Output('total_reach', 'children'),
              [Input('symulator', 'values')],
              [State('upload-file', 'contents')])
def update_reach(val,list_of_contents):
    if list_of_contents is not None:
        df = parse_contents(list_of_contents)
        return calculate_reach(df,val)

@app.callback(Output('usage', 'figure'),
              [Input('symulator', 'values')],
              [State('upload-file', 'contents')])
def update_usage(val,list_of_contents):
    if list_of_contents is not None:
        df = parse_contents(list_of_contents)
        return {'data':[go.Bar(x=val,y=[100*calc_freq(df,i) for i in val])]
                ,'layout':go.Layout(title='Reach of single elements')}


@app.callback(Output('incr-graph','children'),
              [Input('symulator', 'values')],
              [State('upload-file', 'contents')])
def gen_inc_graph(val,list_of_contents):
    if list_of_contents is not None:
        df = parse_contents(list_of_contents)
        kolumny=[df.columns[0],df.columns[1]]
        for x in val:
            kolumny.append(x)
        temp = calculate_incr(df[kolumny])
        children = [dcc.Graph(id='increm_graph',figure={'data':[go.Scatter(x=temp[0],y=temp[1],mode='lines+markers')],
                                                        'layout':go.Layout(title='Incremental graph',yaxis=dict(nticks = 20,
                                                                    range = [0, 100],
                                                                    autorange=False,
                                                                    showgrid=True,
                                                                    gridcolor='#bdbdbd',
                                                                    gridwidth=2,
                                                                    dtick=5,title='Reach'))})]
        return children

if __name__ == '__main__':
    app.run_server()
