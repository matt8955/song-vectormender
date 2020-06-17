import dash
import dash_core_components as dcc
import dash_html_components as html
import pickle
from dash.dependencies import Input, Output
import app_functions as af
import pandas as pd
import plotly.express as px


#load artist list (have to repickle with new data)
with open('artist_list.pkl', 'rb') as f:
    artist_options = pickle.load(f)

#load graph coords df (have to repickle with new data)
with open('graph_frame.pkl', 'rb') as f:
    df = pickle.load(f)

###HTML ELEMENTS

grid_pad = {'padding-bottom': '730px', 'text-align': 'center'}


header = html.Div(className="jumbotron-fluid text-center",
style = {'padding-bottom': '20px'},
children=[
    html.H1(children='Vectomendation Machine v0.01a'),
    html.P('A music recommendation engine powered by user playlists and the Word2Vec Model'),
    html.P(''),
    html.P('created by Matthew Wasserman, Flatiron School')
    ])

dropdown = html.Div(style = {'padding-bottom': '20px'},children=[
    dcc.Dropdown(id='artist-selector',
    options = list(artist_options),
    multi=True,
    placeholder="Select your favorite bands!!!"
    )
])
list_ = html.Span(children=[html.Ol(children=['hello',' its me.......'])])

grid = html.Div(className="row",
children=[
    html.Div(style=grid_pad,className="col", children = html.Div(id='my-div')),
    html.Div(style=grid_pad,className="col", children = dcc.Graph(style={'opacity': '0.75'},id='graph')),
    html.Div(className="w-100"),
])

test_div = html.Div([
    html.Div(id='my-div')
])


colors = {
    'background': '#1DB954',
    "text": "#00e5ff",
    # "background-image" : "url('/assets/wallpaper_opacity.png')",
    # "background-size": "cover",
}
####################### main site ###########################

app = dash.Dash(__name__)
server = app.server

app.title = 'ArtistVectomender'

app.layout = html.Div(id='body',style=colors, children = [
    header,dropdown,grid,
])

@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='artist-selector', component_property='value')]
)
def update_output_div(input_value):
    recs = af.recommend(input_value)
    h_list = []
    for rec in recs:
        h_list.append(html.H3(rec))
    return h_list

@app.callback(
    Output(component_id='graph', component_property='figure'),
    [Input(component_id='artist-selector', component_property='value')]
)
def make_figure(input_value):
    points = input_value + af.recommend(input_value)
    data = df[df.artist.isin(points)]
    return px.scatter_3d(
        data,
        x='x',
        y='y',
        z='z',
        color='cluster',
        hover_data=['artist','cluster'],
        height=700,
    )

if __name__ == '__main__':
    app.run_server(debug=True), #style={'columnCount': 1})

