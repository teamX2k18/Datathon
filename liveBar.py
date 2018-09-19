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

app.layout = html.Div([
    html.H1('PTV Passanger Live Tracker'),
    dcc.Markdown("[Datathon 2018: Student Team: Team X](https://github.com/belhe001/myptv)"),
    dcc.Graph(style={'height': '900px'},id='my-graph2'),
    dcc.Interval(id='myInterval', interval=6000000, n_intervals=0)
])

@app.callback(Output('my-graph2', 'figure'), [Input('myInterval', 'n_intervals')])
def update_graph2(interval):
    df = pd.read_sql('SELECT myon.CardID, myon.MI_Card_Group as CardGroup, trip_dim.routeID as Route, trip_dim.stop_name as SrcName, trip_dim.stop_lat as SrcLat, trip_dim.stop_lon as SrcLon FROM trip_dim, (select dton.CardID, dton.RouteID, dton.Time as ontime, dtoff.Time as offtime, dton.StopID as onstop,dtoff.StopID as offstop, card_dim.MI_Card_Group from dton, dtoff, card_dim where TIME(dton.Time) < CURTIME() AND dtoff.Time > CURTIME() AND dton.CardID = dtoff.CardID AND card_dim.Card_SubType_ID = dton.CardType GROUP by dton.CardID) myon WHERE myon.onstop = trip_dim.stop_id', con)
    df2 = pd.read_sql('SELECT myon.CardID, myon.MI_Card_Group as CardGroup, trip_dim.routeID as Route, trip_dim.stop_name as SrcName, trip_dim.stop_lat as SrcLat, trip_dim.stop_lon as SrcLon FROM trip_dim, (select dton.CardID, dton.RouteID, dton.Time as ontime, dtoff.Time as offtime, dton.StopID as onstop,dtoff.StopID as offstop, card_dim.MI_Card_Group from dton, dtoff, card_dim where dton.day=2 AND TIME(dton.Time) < CURTIME() AND dtoff.Time > CURTIME() AND dton.CardID = dtoff.CardID AND card_dim.Card_SubType_ID = dton.CardType GROUP by dton.CardID) myon WHERE myon.onstop = trip_dim.stop_id', con)
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
    app.run_server(host = '0.0.0.0', port = 8052)
