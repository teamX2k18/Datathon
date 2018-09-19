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
    dcc.Graph(style={'height': '900px'},id='my-graph3'),
    dcc.Interval(id='myInterval', interval=600000, n_intervals=0)
])

@app.callback(Output('my-graph3', 'figure'), [Input('myInterval', 'n_intervals')])
def update_graph3(interval):    
    sqlquery1 = 'SELECT day as d, CAST(t AS DATETIME) as t,travelers, (@countvar := @countvar + travelers) AS CumulativeT FROM (SELECT dton.dt,dton.day, dton.Time as t, COUNT(CardID) as travelers from dton where dton.Time < CURTIME() GROUP by dton.Time order by dton.Time) my'
    sqlquery2 = 'SELECT day as d, CAST(t AS DATETIME) as t,travelers, (@countvar := @countvar + travelers) AS CumulativeT FROM (SELECT dton.dt,dton.day, dton.Time as t, COUNT(CardID) as travelers from dton where dton.day =2 AND dton.Time < CURTIME() GROUP by dton.Time order by dton.Time) my'
    cur.execute('SET @countvar := 0;')
    df = pd.read_sql(sqlquery1,con)
    cur.execute('SET @countvar := 0;')
    df2 = pd.read_sql(sqlquery2,con)
    
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

#localhost:8050 
if __name__ == '__main__':
    app.run_server(host = '0.0.0.0', port = 8051)
