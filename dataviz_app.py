import pandas as pd
import plotly.express as px
import numpy as np

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import date

df = pd.read_csv("data_moods.csv")


###Layout###

#Iniziieren der Dash App
app = dash.Dash(__name__)
server = app.server

colors = {
    'background': '#000000',
    'text': '#7FDBFF'
}

app.layout = html.Div([
    #Titelzeile
    html.Div(children = [
        html.H1('Music Moods'),
    ], className="header"),

    html.Div(children = [
        html.Div(children = [

            #Linke Spalte
            html.H2("Selection"),

            #Selektionstools auf der ersten Zeile (nebeneinander abbgebildet)
            html.Div(children=[
                dcc.Dropdown(id='mood',
                                options = [{'label': i, 'value': i} for i in df["mood"].unique()],
                                multi = True,
                                value = ["Happy", "Sad", "Energetic", "Calm"],
                                className="dropdown"),

                # dcc.Dropdown(id='attributes',
                #                 options = [{'label': "Popularity", 'value': "popularity"},
                #                             {'label': "Danceability", 'value': "danceability"}],
                #                 multi = True,
                #                 value = ["Popularity, Danceability"],
                #                 className="dropdown")
            ], className="selectionrow"),

            html.Br(),

            #Selektionstools auf der zweiten Zeile (nur Datepicker)
            html.Div(children=[
                html.H4("Hier folgt der Datepicker")
                    # dcc.DatePickerRange(
                    #     id='datepicker',
                    #     min_date_allowed=date(1963, 1, 1),
                    #     start_date=date(1963, 1, 1),
                    #     max_date_allowed=(2021, 1, 1),
                    #     end_date=(2021, 1, 1)
                    #     ),
            ], className="selectionrow2"),

            #Zeile mit den Infos
            html.Div(children=[
                    html.H2("Data Info"),
                    html.P("686 Songs - 54X Artists")
            ], className="info-row"),

            #Zeile mit der Treemap
            #html.Div(children=[
                    dcc.Graph(id='treemap', figure = {}, responsive=True,
                              config={'displayModeBar': False}
                    )
            #], className="treemap-row"),


        ], className="wrapper-list"),

        #rechte Spalte
        html.Div(children = [

            #Erste Zeile mit Parallel Coordinates
            html.Div(children = [
                    dcc.Graph(id='parallel-coordinates', figure = {}, style = {'display': 'inline-block'}, responsive=True,
                              config={'displayModeBar': False}),
            ], className="parallel-coordinates-row"),

            #Zweite Zeile, Inhalt folgt später
            html.Div(children = [
                html.P("Weitere Visualisierungen folgen")
            ], className="rest"),
        ], className="graph-container"),
    ], className="container")
])


###Befüllen des Dash Gerüsts mit den Visualisierungen###

#Callback
@app.callback(
    [Output(component_id='treemap', component_property='figure'),
     Output(component_id='parallel-coordinates', component_property='figure'),
     ],
    [Input(component_id='mood', component_property='value') #,
     #Input(component_id='datepicker', component_property='start_date'),
     #Input(component_id='datepicker', component_property='end_date') #,
     #Input(component_id='attributes', component_property='value')
    ],
)

def update_moods(mood_slctd):  #, date_slctd1, date_slctd2

    #Arbeitskopie der des Dataframe erstellen
    dff = df.copy()


    dff = dff[dff["mood"].isin(mood_slctd)]


    #Eingrenzen der Zeitserie anhand der beiden Werte aus dem Datepicker
    #dff = dff[dff["release_date"] >= date_slctd1]
    #dff = dff[dff["release_date"] <= date_slctd2]



    fig1 = go.Figure(go.Treemap(
        labels = ["Happy", "Sad", "Energetic", "Calm"],
        values = [140, 197, 154, 195],
        parents = ["Mood", "Mood", "Mood", "Mood"],
        marker_colors = ["red", "yellow", "aqua", "fuchsia"],
        root_color="lightgrey"))

    fig1.update_layout(margin=dict(l=0, r=0, t=0, b=0))

    dfcolmap = dff.copy()
    dfcolmap= dfcolmap.astype({"mood": str})
    dfcolmap["mood"].replace({"Happy": 1, "Sad": 2, "Energetic": 3, "Calm": 4}, inplace=True)

    fig2 = px.parallel_coordinates(dfcolmap, color="mood", color_continuous_scale=[(0.00, "red"), (0.25, "red"),
                                                                               (0.25, "yellow"), (0.50, "yellow"),
                                                                               (0.50, "aqua"),  (0.75, "aqua"),
                                                                               (0.75, "fuchsia"), (1.00, "fuchsia")])



    return fig1, fig2



if __name__ == '__main__':
    app.run_server(debug=False, port=8051)
