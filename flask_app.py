# A very simple Flask Hello World app for you to get started with...

from flask import Flask

server = Flask(__name__)

import sys
print(sys.version)


####DASH APP 'app.py'
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# visit http://127.0.0.1:8050/ in your web browser.
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Load data from csv included in dash file format.
df = pd.read_csv(
    "/home/Kevaman/mysite/data/contacts_dataframe.csv"
)
df_simulation = pd.read_csv(
    "/home/Kevaman/mysite/data/agents_dataframe.csv"
)

#animations, app, external css and color.
animations = {
    'Scatter': px.scatter(
        df_simulation, x="x", y="y", animation_frame="Ticks", animation_group="id",
        hover_name="id", color = 'status', width = 800, height = 800,
        range_x=[-17,17], range_y=[-17,17]),
    'Close Contacts': px.line(
        df, x="Ticks", y = "Close Contacts", hover_name="Close Contacts", width = 800, height = 800,
    )
}

app = dash.Dash(__name__, server=server, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

#app layout
app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.RadioItems(
                id='selection',
                options=[{'label': x, 'value': x} for x in animations],
                value='Scatter'
            ),
            dcc.Graph(id="graph")
        ],
        style={'width': '49%', 'display': 'inline-block', 'float': 'center', 'padding-left' : '33%'})


    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),
    html.Div([
        html.Div([
                dcc.Graph(
                    id='Model2-Graph-CloseContacts',
                    figure={
                        'data': [

                            {'x': df['Ticks'], 'y': df['Avg Close Contacts'], 'mode' : 'line+markers', 'type': 'scatter', 'name': 'Avg Close Contacts'},

                        ],
                        'layout': {
                            'title': 'Average Close Contacts',
                            'xaxis': {'title': 'Time in Ticks'},
                            'yaxis': {'title': 'Number of Contacts'},
                            'width' : '50%',
                            'height' : '50%',
                        }
                    },
                ),
        ], style={'width': '25%', 'float': 'left', 'display': 'inline-block'}),
        html.Div([
                dcc.Graph(
                    id='Model2-Graph-IRH',
                    figure={
                        'data': [
                            {'x': df['Ticks'], 'y': df['Infected'], 'type': 'line', 'name': 'Infected', 'line':dict(color='red')},
                            {'x': df['Ticks'], 'y': df['Recovered'], 'type': 'line', 'name': 'Recovered', 'line':dict(color='green')},
                            {'x': df['Ticks'], 'y': df['Healthy'], 'type': 'line', 'name': 'Healthy', 'line':dict(color='blue')},
                        ],
                        'layout': {
                            'title': 'Healthy, Infected and Recovered',
                            'xaxis': {'title': 'Time in Ticks'},
                            'yaxis': {'title': 'Number of Agents'},
                            'width' : '50%',
                            'height' : '50%',
                        }
                    }
                )
        ], style={'width': '25%', 'float': 'right', 'display': 'inline-block'}),
    ], style={'width': '49%', 'float': 'left', 'display': 'inline-block', 'margin-left' : '15%'})
])

@app.callback(
    Output("graph", "figure"),
    [Input("selection", "value")]
)
def display_animated_graph(s):
    return animations[s]

if __name__ == '__main__':
    app.run_server(debug=True)