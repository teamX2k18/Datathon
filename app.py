import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, Event
import plotly.graph_objs as go
from scipy.stats import rayleigh
from flask import Flask
import numpy as np
import pandas as pd
import os
import datetime as dt


app = dash.Dash('PTV-Datathon-Streaming-app')

server = app.server
mapbox_access_token = 'pk.eyJ1IjoiYWxpc2hvYmVpcmkiLCJhIjoiY2ozYnM3YTUxMDAxeDMzcGNjbmZyMmplZiJ9.ZjmQ0C2MNs1AzEBC_Syadg'

app.layout = html.Div([
    html.H1('PTV Passanger Live Tracker'),
    html.H3('Student Team Team X'),
    dcc.Graph(style={'height': '900px'},id='my-graph3'),
    dcc.Graph(style={'height': '900px'},id='my-graph1'),
    dcc.Graph(style={'height': '900px'},id='my-graph2'),
    dcc.Interval(id='myInterval', interval=60000000, n_intervals=0)
])




@app.callback(Output('my-graph3', 'figure'), [Input('myInterval', 'n_intervals')])
def update_graph3(interval):    
    df = pd.read_csv('mydt13.csv')
    df2 = pd.read_csv('mydt23.csv')
    
    data = [
        go.Scatter(
            x=df['t'],
            y=df['CumulativeT'],
            mode = 'lines+markers',
            name = "Real travelers",
            line = dict(color = '#17BECF'),
            opacity = 0.5
            ),
        go.Scatter(
            x=df2['t'],
            y=df2['CumulativeT'],
            mode = 'lines+markers',
            name = "Observed travelers",
            line = dict(color = 'rgb(255, 111, 0)'),
            opacity = 0.8
            )
        ]

    layout = dict(
        title = "Cumulative line graph for real-time comparison",
        xaxis=dict( title='Time duration'),
        yaxis=dict( title='Traveler count'),
        showlegend=True,
    )
    fig = { 'data':data, 'layout':layout }
    return fig
    
#graph 1

@app.callback(Output('my-graph1', 'figure'), [Input('myInterval', 'n_intervals')])
def update_graph1(interval):
    zoom = 9.0
    latInitial = -37.7
    lonInitial = 144.92
    bearing = 0
    df = pd.read_csv('mydt11.csv')
    grpdf = df;    
    grpdf['grpcount'] = grpdf.groupby(['SrcLon','SrcLat','CardGroup'])['CardID'].transform('count')
    grpdf = grpdf.drop_duplicates(['SrcLon','SrcLat','CardGroup'])[['SrcLon','SrcLat','CardGroup','grpcount']]
    data = [ 
         
        go.Scattermapbox(
        lat=grpdf['SrcLat'].loc[df['CardGroup'] == 'Other'],
        lon=grpdf['SrcLon'].loc[df['CardGroup'] == 'Other'],
        showlegend=True,
        mode='markers',
        text = grpdf['grpcount'].loc[df['CardGroup'] == 'Other'],
        marker=dict(
                    color="#1A5276",#blue
                    opacity=1,
                    size=14,
                ),
        name='Other',
        ), 
         
        go.Scattermapbox(
        lat=grpdf['SrcLat'].loc[df['CardGroup'] == 'Full Fare'],
        lon=grpdf['SrcLon'].loc[df['CardGroup'] == 'Full Fare'],
        showlegend=True,
        mode='markers',
        text = grpdf['grpcount'].loc[df['CardGroup'] == 'Full Fare'],
        marker=dict(
                    color="#7B241C",#blue
                    opacity=1,
                    size=13,
                ),
        name='Full Fare',
        ), 
        go.Scattermapbox(
        lat=grpdf['SrcLat'].loc[df['CardGroup'] == 'Student'],
        lon=grpdf['SrcLon'].loc[df['CardGroup'] == 'Student'],
        showlegend=True,
        mode='markers',
        text = grpdf['grpcount'].loc[df['CardGroup'] == 'Student'],
        marker=dict(
                    color="#C39BDE",#blue
                    opacity=1,
                    size=12,
                ),
        name='Student',
        ),  
        go.Scattermapbox(
        lat=grpdf['SrcLat'].loc[df['CardGroup'] == 'Tertiary'],
        lon=grpdf['SrcLon'].loc[df['CardGroup'] == 'Tertiary'],
        showlegend=True,
        mode='markers',
        text = grpdf['grpcount'].loc[df['CardGroup'] == 'Tertiary'],
        marker=dict(
                    color="F7DC6F",#blue
                    opacity=1,
                    size=10,
                ),
        name='Tertiary',
        ),         
        go.Scattermapbox(
        lat=grpdf['SrcLat'].loc[df['CardGroup'] == 'Other Concession'],
        lon=grpdf['SrcLon'].loc[df['CardGroup'] == 'Other Concession'],
        showlegend=True,
        mode='markers',
        text = grpdf['grpcount'].loc[df['CardGroup'] == 'Other Concession'],
        marker=dict(
                    color="#117864",#blue
                    opacity=1,
                    size=8,
                ),
        name='Other Concession',
        ), 
        go.Scattermapbox(
        lat=grpdf['SrcLat'].loc[df['CardGroup'] == 'Senior_Aged Pension'],
        lon=grpdf['SrcLon'].loc[df['CardGroup'] == 'Senior_Aged Pension'],
        showlegend=True,
        mode='markers',
        text = grpdf['grpcount'].loc[df['CardGroup'] == 'Senior_Aged Pension'],
        marker=dict(
                    color="#85C1E9",#blue
                    opacity=1,
                    size=6,
                ),
        name='Senior_Aged Pension',
        ), 
         
        
    ]

    layout = go.Layout(
        title='Real-Time passenger groups',
        autosize=True,
        hovermode='closest',
        showlegend=True,
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=bearing,
            center=dict(
                lat=latInitial,
                lon=lonInitial
            ),
            pitch=0,
            zoom=zoom,
            style='light'
        ),
    )
    fig = { 'data':data, 'layout':layout }
    return fig
   

#plot 3 Comparison

@app.callback(Output('my-graph2', 'figure'), [Input('myInterval', 'n_intervals')])
def update_graph2(interval):
    df = pd.read_csv('mydt12.csv')
    df2 = pd.read_csv('mydt22.csv')
    df['grpcount'] = df.groupby(['SrcName','Route'])['CardID'].transform('count')
    df2['grpcount'] = df2.groupby(['SrcName','Route'])['CardID'].transform('count')
    
    g1 = go.Bar(
        y=df['grpcount'],
        x=df['SrcName'],
        name='Real'
    )
    g2 = go.Bar(
        name='Observed',
        y=df2['grpcount'],
        x=df2['SrcName'],
    )
    data = [g1,g2]

    layout = go.Layout(
        title='PTV passengers groups from source station',
        #barmode='stack'
    )
    fig = { 'data':data, 'layout':layout }
    return fig
    
   
#localhost:8050 
if __name__ == '__main__':
    app.run_server(host = '0.0.0.0', port = 8050)
