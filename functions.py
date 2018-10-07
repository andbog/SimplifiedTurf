import base64
import datetime
import io
import pandas as pd

def calc_freq(df,column):
    total = df.iloc[:,1].sum(axis=0)
    count = df[df[column]>0].iloc[:,1].sum(axis=0)
    return count/total

def calculate_reach(df,columns):
    df['suma'] = df[columns].sum(axis=1)
    return 'Reach: {}%'.format(100*calc_freq(df,'suma'))

def parse_contents(contents):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    return pd.read_csv(io.StringIO(decoded.decode('utf-8')))
