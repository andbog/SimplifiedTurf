import base64
import datetime
import io
import time
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html

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