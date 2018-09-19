import MySQLdb
import dash
from dash.dependencies import Input, Output

import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go


app = dash.Dash('PTV-Datathon-Streaming-app')
#con = MySQLdb.connect(host="localhost", user="root", passwd="12345678", db="ptv2")
con = MySQLdb.connect(host="localhost", user="root", passwd="", db="ptv2")
cur = con.cursor()

server = app.server
mapbox_access_token = 'pk.eyJ1IjoiYWxpc2hvYmVpcmkiLCJhIjoiY2ozYnM3YTUxMDAxeDMzcGNjbmZyMmplZiJ9.ZjmQ0C2MNs1AzEBC_Syadg'


app.layout = html.Div([
    html.H1('PTV Passanger Live Tracker'),
    dcc.Markdown("[Datathon 2018: Student Team: Team X](https://github.com/belhe001/myptv)"),
    dcc.Graph(style={'height': '900px'},id='my-graph1'),
    dcc.Interval(id='myInterval', interval=60000, n_intervals=0)
])




@app.callback(Output('my-graph1', 'figure'), [Input('myInterval', 'n_intervals')])
def update_graph1(interval):
    zoom = 9.0
    latInitial = -37.7
    lonInitial = 144.92
    bearing = 0
    #SELECT fact.route_short_name as Bus, fact.stop_name as Name, fact.stop_lat as Lat, fact.stop_lon as Lon, COUNT(dton.CardID) as MykiCount FROM dtoff INNER JOIN dton ON dton.CardID = dtoff.CardID AND DATE(dton.BusinessDate) <= DATE(NOW()) AND TIME(dton.DateTime) <= TIME(NOW()) AND TIME(NOW()) <= TIME(dtoff.DateTime) INNER JOIN fact ON dton.RouteID=fact.route_short_name GROUP by dton.CardID
    df = pd.read_sql('SELECT myon.CardID, myon.MI_Card_Group as CardGroup, trip_dim.routeID as Route, trip_dim.stop_name as SrcName, trip_dim.stop_lat as SrcLat, trip_dim.stop_lon as SrcLon FROM trip_dim, (select dton.CardID, dton.RouteID, dton.Time as ontime, dtoff.Time as offtime, dton.StopID as onstop,dtoff.StopID as offstop, card_dim.MI_Card_Group from dton, dtoff, card_dim where dton.Time < CURTIME() AND dtoff.Time > CURTIME() AND dton.CardID = dtoff.CardID AND dton.day=2 AND dtoff.day = 2 AND card_dim.Card_SubType_ID = dton.CardType GROUP by dton.CardID) myon WHERE myon.onstop = trip_dim.stop_id', con)
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
                    color="#F7DC6F",#blue
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

#localhost:8050 
if __name__ == '__main__':
    app.run_server(host = '0.0.0.0', port = 8053)
