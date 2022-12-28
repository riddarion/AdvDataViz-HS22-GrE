import pandas as pd
import plotly.express as px
import webbrowser
import numpy as np
import statistics
import json

import dash
from dash import ctx
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
#import dash_bootstrap_components as dbc

import plotly.graph_objects as go


df = pd.read_csv("data_moods.csv")
df['url'] = "https://open.spotify.com/track/" + df['id']


###Layout###

#Iniziieren der Dash App
app = dash.Dash(__name__)
server = app.server


app.layout = html.Div([
    #Titelzeile
    html.Div(children = [
        html.A(html.H1('Music Moods'), href='/'),


        dcc.Tabs(id='selection-tabs', value='tab-1',
             parent_className='custom-tabs',
             className='custom-tabs-container',
             children=[

            dcc.Tab(label='Dark Mode', value='tab-1',
                className='custom-tab',
                selected_className='custom-tab--selected'),

            dcc.Tab(label='Scientific', value='tab-2',
                className='custom-tab',
                selected_className='custom-tab--selected'),

        ])

    ], className="header"),
    html.Div(id='selection-tabs-content')
])


@app.callback(Output('selection-tabs-content', 'children'),
              Input('selection-tabs', 'value'))


def render_content(tab):

    #Content Tab1
    if tab == 'tab-1':
        return html.Div(children = [
            html.Div(children = [


                #Linke Spalte
                html.Div(children=[
                    html.H2("Selection"),
                ], className="selection-title"),

                html.Div(children=[
                    dcc.Dropdown(id='mood',
                                options = [{'label': i, 'value': i} for i in df["mood"].unique()],
                                multi = True,
                                value = ["Happy", "Sad", "Energetic", "Calm"],
                                className="dropdown"),

                ], className="selectionrow"),

                html.Br(),

                html.Div(children=[
                        dcc.DatePickerRange(
                            id='datepicker',
                            min_date_allowed= "1963-1-1",
                            start_date="1963-1-1",
                            max_date_allowed="2021-1-1",
                            end_date="2021-1-1"
                            ),
                ], className="selectionrow2"),

                #Zeile mit den Infos
                html.Div(children=[
                        html.H2("Data Info"),
                        html.P("686 Songs - 540 Artists"),
                         html.Pre(id='data')
                ], className="info-row"),


                #Zeile mit der Treemap
                #html.Div(children=[
                        dcc.Graph(id='treemap', figure = {}, responsive=True,
                                config={'displayModeBar': False}
                        )
                #], className="treemap-row"),


            ], className="wrapper-list"),

            #rechte Spalte

            #Erste Zeile mit Parallel Coordinates
            html.Div(children= [
                html.Div(children = [
                    dcc.Graph(id='parallel-coord', figure = {}, responsive=True,
                            config={'displayModeBar': False}),
                ]  , className="parallel-coord-row"),



                html.Div( children=[
                    html.Div( children=[
                        dcc.Dropdown(
                                options= ['popularity', 'danceability', 'speechiness', 'acousticness', 'energy', 'instrumentalness', 'liveness', 'valence', 'loudness', 'tempo']
                                , id='scatter-dropdown-1',
                                multi = False,
                                value = 'popularity'),
                        dcc.Dropdown(
                                options= ['popularity', 'danceability', 'speechiness', 'acousticness', 'energy', 'instrumentalness', 'liveness', 'valence', 'loudness', 'tempo']
                                , id='scatter-dropdown-2',
                                multi = False,
                                value = 'danceability'),
                    ]  , className="dropdowns"),
                    html.Div( children=[
                        html.Button('Song Distribution', id='view-stacked', n_clicks=0),
                        html.Button('Song Length', id='view-length', n_clicks=0),
                    ]  , className="buttons"),
                ]  , className="menu-row"),

                html.Div(children = [
                    html.Div( children = [
                        dcc.Graph(id='scatter', figure = {}, responsive=True,
                                    config={'displayModeBar': False}),


                    ], className='scatter-div'),
                    #], className='scatter-row')

                #Erste Zeile mit Stacked Bar Chart

                     html.Div(children = [
                        dcc.Graph(id='switch', figure = {}, responsive=True,
                                config={'displayModeBar': False}),
                    ], className="switch-visual"),
                ]  , className="lower-row"),
            ], className="right-side")
        ], className="container")

    #Content Tab2
    elif tab == 'tab-2':
        return html.Div(children = [
            html.Div(children = [


                #Linke Spalte
                html.Div(children=[
                    html.H2("Selection"),
                ], className="selection-title-w"),

                #Selektionstools auf der ersten Zeile (nebeneinander abbgebildet)
                html.Div(children=[
                    dcc.Dropdown (id='mood',
                                options = [{'label': i, 'value': i} for i in df["mood"].unique()],
                                multi = True,
                                value = ["Happy", "Sad", "Energetic", "Calm"],
                                className="dropdown"),

                ], className="selectionrow"),

                html.Br(),

                #Selektionstools auf der zweiten Zeile (nur Datepicker)
                html.Div(children=[
                        dcc.DatePickerRange(
                            id='datepicker',
                            min_date_allowed= "1963-1-1",
                            start_date="1963-1-1",
                            max_date_allowed="2021-1-1",
                            end_date="2021-1-1"
                            ),
                ], className="selectionrow2"),

                #Zeile mit den Infos
                html.Div(children=[
                        html.H2("Data Info"),
                        html.P("686 Songs - 540 Artists"),
                        html.Pre(id='data-w')
                ], className="info-row-w"),

                #Zeile mit der Treemap

                        dcc.Graph(id='treemap-w', figure = {}, responsive=True,
                                config={'displayModeBar': False}
                        )


            ], className="wrapper-list-w"),

            #rechte Spalte

            #Erste Zeile mit Parallel Coordinates
            html.Div(children= [
                html.Div(children = [
                    dcc.Graph(id='parallel-coord-w', figure = {}, responsive=True,
                            config={'displayModeBar': False}),
                ]  , className="parallel-coord-row"),

                html.Div(children = [
                    html.Div(children = [
                        dcc.Dropdown(
                            options= ['popularity', 'danceability', 'speechiness', 'acousticness', 'energy', 'instrumentalness', 'liveness', 'valence', 'loudness', 'tempo']
                            , id='scatter-dropdown-1w',
                            multi = False,
                            value = 'popularity'),
                        dcc.Dropdown(
                            options= ['popularity', 'danceability', 'speechiness', 'acousticness', 'energy', 'instrumentalness', 'liveness', 'valence', 'loudness', 'tempo']
                            , id='scatter-dropdown-2w',
                            multi = False,
                            value = 'danceability'),
                    ]  , className="dropdowns"),
                    html.Div( children = [
                        html.Button('Song Distribution', id='view-stacked-w', n_clicks=0),
                        html.Button('Song Length', id='view-length-w', n_clicks=0),
                    ]  , className="buttons"),
                ]  , className="menu-row"),

                html.Div(children = [
                    html.Div( children = [
                            dcc.Graph(id='scatter-w', figure = {}, responsive=True,
                                    config={'displayModeBar': False}),
                    ], className='scatter-div'),

                    html.Div(children = [
                            dcc.Graph(id='switch-w', figure = {}, style = {'display': 'inline-block'}, responsive=True,
                                    config={'displayModeBar': False}),
                    ], className="switch-visual"),
                ], className='lower-row')
            ], className="right-side")
        ], className="container_w")


###Befüllen des Dash Gerüsts mit den Visualisierungen###

#Callback Tab1
@app.callback(
    [Output(component_id='treemap', component_property='figure'),
     Output(component_id='parallel-coord', component_property='figure'),
     Output(component_id='scatter', component_property='figure'),
     Output(component_id='switch', component_property='figure')
     ],
    [Input(component_id='mood', component_property='value') ,
     Input(component_id='datepicker', component_property='start_date'),
     Input(component_id='datepicker', component_property='end_date'),
     Input('view-stacked', 'n_clicks'),
     Input('view-length', 'n_clicks'),
     Input(component_id='scatter-dropdown-1', component_property='value'),
     Input(component_id='scatter-dropdown-2', component_property='value')
    ],
)


def update_moods(mood_slctd, date_slctd1, date_slctd2, btn1, btn2, scatterdrop1, scatterdrop2):


    #Arbeitskopie der des Dataframe erstellen
    dff = df.copy()

    dff = dff[dff["mood"].isin(mood_slctd)]

    #Eingrenzen der Zeitserie anhand der beiden Werte aus dem Datepicker
    dff = dff[dff["release_date"] >= date_slctd1]
    dff = dff[dff["release_date"] <= date_slctd2]



    fig1 = go.Figure(go.Treemap(
        labels = ["Happy", "Sad", "Energetic", "Calm"],
        values = [140, 197, 154, 195],
        parents = ["Mood", "Mood", "Mood", "Mood"],
        marker_colors = ["goldenrod", "rebeccapurple", "maroon", "teal"],
        root_color="#111111"))

    fig1.update_layout(margin=dict(l=0, r=0, t=0, b=0), template='plotly_dark')

    dfcolmap = dff.copy()
    dfcolmap["mood"].replace({"Happy": 1, "Sad": 2, "Energetic": 3, "Calm": 4}, inplace=True)

    sel_moods = []
    for mood in dfcolmap["mood"]:
        if mood not in sel_moods:
            sel_moods.append(mood)
            sel_moods.sort()

    mood_comb1 = [1, 2, 3, 4]
    mood_comb2 = [1]
    mood_comb3 = [2]
    mood_comb4 = [3]
    mood_comb5 = [4]
    mood_comb6 = [1, 2]
    mood_comb7 = [1, 3]
    mood_comb8 = [1, 4]
    mood_comb9 = [2, 3]
    mood_comb10 = [2, 4]
    mood_comb11 = [3, 4]
    mood_comb12 = [1, 2, 3]
    mood_comb13 = [1, 2, 4]
    mood_comb14 = [1, 3, 4]
    mood_comb15 = [2, 3, 4]

    if sel_moods == mood_comb1:
        colors = [(0.00, "goldenrod"), (0.25, "goldenrod"),
                (0.25, "rebeccapurple"), (0.50, "rebeccapurple"),
                (0.50, "maroon"),  (0.75, "maroon"),
                (0.75, "teal"), (1.00, "teal")]
    elif sel_moods == mood_comb2:
        colors = [(0.0, "goldenrod"), (1.00, "goldenrod")]
    elif sel_moods == mood_comb3:
        colors = [(0.0, "rebeccapurple"), (1.00, "rebeccapurple")]
    elif sel_moods == mood_comb4:
        colors = [(0.0, "maroon"), (1.00, "maroon")]
    elif sel_moods == mood_comb5:
        colors = [(0.0, "teal"), (1.00, "teal")]
    elif sel_moods == mood_comb6:
        colors = [(0.0, "goldenrod"), (0.50, "goldenrod"),
                (0.50, "rebeccapurple"), (1.00, "rebeccapurple")]
    elif sel_moods == mood_comb7:
        colors = [(0.0, "goldenrod"), (0.50, "goldenrod"),
                (0.50, "maroon"), (1.00, "maroon")]
    elif sel_moods == mood_comb8:
        colors = [(0.0, "goldenrod"), (0.50, "goldenrod"),
                 (0.50, "teal"), (1.00, "teal")]
    elif sel_moods == mood_comb9:
        colors = [(0.0, "rebeccapurple"), (0.50, "rebeccapurple"),
                (0.50, "maroon"), (1.00, "maroon")]
    elif sel_moods == mood_comb10:
        colors = [(0.0, "rebeccapurple"), (0.50, "rebeccapurple"),
                 (0.50, "teal"), (1.00, "teal")]
    elif sel_moods == mood_comb11:
        colors = [(0.0, "maroon"), (0.50, "maroon"),
                (0.50, "teal"), (1.00, "teal")]
    elif sel_moods == mood_comb12:
        colors = [(0.0, "goldenrod"), (0.33, "goldenrod"),
                (0.33, "rebeccapurple"), (0.66, "rebeccapurple"),
                (0.66, "maroon"), (1.00, "maroon")]
    elif sel_moods == mood_comb13:
        colors = [(0.0, "goldenrod"), (0.33, "goldenrod"),
                (0.33, "rebeccapurple"), (0.66, "rebeccapurple"),
                (0.66, "teal"), (1.00, "teal")]
    elif sel_moods == mood_comb14:
        colors = [(0.0, "goldenrod"), (0.33, "goldenrod"),
                (0.33, "maroon"), (0.66, "maroon"),
                (0.66, "teal"), (1.00, "teal")]
    elif sel_moods == mood_comb15:
        colors = [(0.0, "rebeccapurple"), (0.33, "rebeccapurple"),
                (0.33, "maroon"), (0.66, "maroon"),
                (0.66, "teal"), (1.00, "teal")]

    fig2 = px.parallel_coordinates(dfcolmap, color="mood", template='plotly_dark', title = "Attribute Overview Songs",
                                   dimensions=['popularity', 'length', 'danceability', 'acousticness', 'energy', 'instrumentalness',
                                          'liveness', 'valence','loudness', 'speechiness', 'tempo'],
                                   color_continuous_scale=colors)

    fig2.update_xaxes(title_font=dict(color='#1DB954'), tickfont=dict(color='#1DB954'))
    fig2.update_yaxes(title_font=dict(color='#1DB954'), tickfont=dict(color='#1DB954'))
    fig2.update_layout(title_font_color="#1DB954", showlegend=False)
    fig2.update_coloraxes(showscale=False)


    #Ursprungsdatensatz kopieren
    dflpd = dff.copy()

    #Release Datum aufspalten in Jahr, Monat und Tag
    dflpd[["year", "month", "day"]] = dflpd["release_date"].str.split("-", expand=True)
    dflpd = dflpd.sort_values("year")

    #df mit Länge und Jahr
    dflpd = dflpd[['length', 'year']].copy()
    dflpd['length'] = dflpd['length']/60000
    dflpd = dflpd.rename(columns={"length": "av. length in min"})

    dflpd = dflpd.groupby(['year']).mean()
    dflpd = dflpd.reset_index(level=0)


    dfff = dff.copy()
    dfff[["year", "month", "day"]] = dfff["release_date"].str.split("-", expand=True)

    dfMoodspYear = dfff.groupby(["year", "mood"]).count()

    MpY = dfMoodspYear.iloc[:,0]
    MpY = MpY.reset_index(level=(0,1))
    MpY["year"] = MpY["year"].astype("int")
    MpY = MpY.sort_values(by=["year"])

    if "view-length" == ctx.triggered_id:

        fig3 = px.bar(dflpd, x="year", y="av. length in min",  template='plotly_dark', title = "Average Song Length per Year", color_discrete_sequence=["#1DB954"])

        fig3.update_xaxes(title_font=dict(color='#1DB954'), tickfont=dict(color='#1DB954'))
        fig3.update_yaxes(title_font=dict(color='#1DB954'), tickfont=dict(color='#1DB954'))
        fig3.update_layout(title_font_color="#1DB954")

    elif "view-stacked" == ctx.triggered_id:

        fig3 = px.bar(MpY, x="year", y="name", color="mood", template='plotly_dark', title = "Number of Songs per Mood and Year",
                  color_discrete_map={
                    "Happy": "goldenrod",
                    "Sad": "rebeccapurple",
                    "Energetic": "maroon",
                    "Calm": "teal"},
                  labels={
                     "year": "year",
                     "name": "count of songs",
                     "mood": "mood"
                 })

        fig3.update_xaxes(title_font=dict(color='#1DB954'), tickfont=dict(color='#1DB954'))
        fig3.update_yaxes(title_font=dict(color='#1DB954'), tickfont=dict(color='#1DB954'))
        fig3.update_layout(title_font_color="#1DB954", showlegend=False)

    else:
        fig3 = px.bar(MpY, x="year", y="name", color="mood", template='plotly_dark', title = "Number of Songs per Mood and Year",
                  color_discrete_map={
                    "Happy": "goldenrod",
                    "Sad": "rebeccapurple",
                    "Energetic": "maroon",
                    "Calm": "teal"},
                  labels={
                     "year": "year",
                     "name": "count of songs",
                     "mood": "mood"
                 })

        fig3.update_xaxes(title_font=dict(color='#1DB954'), tickfont=dict(color='#1DB954'))
        fig3.update_yaxes(title_font=dict(color='#1DB954'), tickfont=dict(color='#1DB954'))
        fig3.update_layout(title_font_color="#1DB954", showlegend=False)


    mcolors = {"Happy": "goldenrod", "Sad": "rebeccapurple", "Energetic": "maroon", "Calm": "teal"}


    fig5 = px.scatter(dff, x=scatterdrop1 , y=scatterdrop2, color="mood", color_discrete_map=mcolors, title = "Correlation of Attributes (Click on data point to open Song in Spotify)", template='plotly_dark',
                      hover_name="name", hover_data=[dff["artist"], scatterdrop1, scatterdrop2], custom_data=["url"])

    fig5.update_xaxes(title_font=dict(color='#1DB954'), tickfont=dict(color='#1DB954'))
    fig5.update_yaxes(title_font=dict(color='#1DB954'), tickfont=dict(color='#1DB954'))
    fig5.update_layout(title_font_color="#1DB954", showlegend=False, clickmode='event+select')

    return fig1, fig2, fig5, fig3

@app.callback(
    Output('data', 'clickData'),
    Input('scatter', 'clickData'))

def open_url(clickData):
    if clickData:
        webbrowser.open_new_tab(clickData['points'][0]['customdata'][0])
    else:
        raise PreventUpdate
    # return json.dumps(clickData, indent=2)

#Callback Tab2
@app.callback(
    [Output(component_id='treemap-w', component_property='figure'),
     Output(component_id='parallel-coord-w', component_property='figure'),
     Output(component_id='scatter-w', component_property='figure'),
     Output(component_id='switch-w', component_property='figure'),
     ],
    [Input(component_id='mood', component_property='value') ,
     Input(component_id='datepicker', component_property='start_date'),
     Input(component_id='datepicker', component_property='end_date'),
     Input('view-stacked-w', 'n_clicks'),
     Input('view-length-w', 'n_clicks'),
     Input(component_id='scatter-dropdown-1w', component_property='value'),
     Input(component_id='scatter-dropdown-2w', component_property='value')
    ],

)

def update_moods(mood_slctd, date_slctd1, date_slctd2, btn1, btn2, scatterdrop1, scatterdrop2):

    #Arbeitskopie der des Dataframe erstellen
    dff = df.copy()


    dff = dff[dff["mood"].isin(mood_slctd)]


    #Eingrenzen der Zeitserie anhand der beiden Werte aus dem Datepicker
    dff = dff[dff["release_date"] >= date_slctd1]
    dff = dff[dff["release_date"] <= date_slctd2]



    fig1 = go.Figure(go.Treemap(
        labels = ["Happy", "Sad", "Energetic", "Calm"],
        values = [140, 197, 154, 195],
        parents = ["Mood", "Mood", "Mood", "Mood"],
        marker_colors = ["goldenrod", "rebeccapurple", "maroon", "teal"],
        root_color="#FFFFFF"))

    fig1.update_layout(margin=dict(l=0, r=0, t=0, b=0), template='plotly_white')

    dfcolmap = dff.copy()
    dfcolmap["mood"].replace({"Happy": 1, "Sad": 2, "Energetic": 3, "Calm": 4}, inplace=True)

    sel_moods = []
    for mood in dfcolmap["mood"]:
        if mood not in sel_moods:
            sel_moods.append(mood)
            sel_moods.sort()

    mood_comb1 = [1, 2, 3, 4]
    mood_comb2 = [1]
    mood_comb3 = [2]
    mood_comb4 = [3]
    mood_comb5 = [4]
    mood_comb6 = [1, 2]
    mood_comb7 = [1, 3]
    mood_comb8 = [1, 4]
    mood_comb9 = [2, 3]
    mood_comb10 = [2, 4]
    mood_comb11 = [3, 4]
    mood_comb12 = [1, 2, 3]
    mood_comb13 = [1, 2, 4]
    mood_comb14 = [1, 3, 4]
    mood_comb15 = [2, 3, 4]

    if sel_moods == mood_comb1:
        colors = [(0.00, "goldenrod"), (0.25, "goldenrod"),
                (0.25, "rebeccapurple"), (0.50, "rebeccapurple"),
                (0.50, "maroon"),  (0.75, "maroon"),
                (0.75, "teal"), (1.00, "teal")]
    elif sel_moods == mood_comb2:
        colors = [(0.0, "goldenrod"), (1.00, "goldenrod")]
    elif sel_moods == mood_comb3:
        colors = [(0.0, "rebeccapurple"), (1.00, "rebeccapurple")]
    elif sel_moods == mood_comb4:
        colors = [(0.0, "maroon"), (1.00, "maroon")]
    elif sel_moods == mood_comb5:
        colors = [(0.0, "teal"), (1.00, "teal")]
    elif sel_moods == mood_comb6:
        colors = [(0.0, "goldenrod"), (0.50, "goldenrod"),
                (0.50, "rebeccapurple"), (1.00, "rebeccapurple")]
    elif sel_moods == mood_comb7:
        colors = [(0.0, "goldenrod"), (0.50, "goldenrod"),
                (0.50, "maroon"), (1.00, "maroon")]
    elif sel_moods == mood_comb8:
        colors = [(0.0, "goldenrod"), (0.50, "goldenrod"),
                 (0.50, "teal"), (1.00, "teal")]
    elif sel_moods == mood_comb9:
        colors = [(0.0, "rebeccapurple"), (0.50, "rebeccapurple"),
                (0.50, "maroon"), (1.00, "maroon")]
    elif sel_moods == mood_comb10:
        colors = [(0.0, "rebeccapurple"), (0.50, "rebeccapurple"),
                 (0.50, "teal"), (1.00, "teal")]
    elif sel_moods == mood_comb11:
        colors = [(0.0, "maroon"), (0.50, 'maroon'),
                   (0.50, "teal"), (1.00, "teal")]
    elif sel_moods == mood_comb12:
        colors = [(0.0, "goldenrod"), (0.33, "goldenrod"),
                (0.33, "rebeccapurple"), (0.66, "rebeccapurple"),
                (0.66, "maroon"), (1.00, "maroon")]
    elif sel_moods == mood_comb13:
        colors = [(0.0, "goldenrod"), (0.33, "goldenrod"),
                (0.33, "rebeccapurple"), (0.66, "rebeccapurple"),
                (0.66, "teal"), (1.00, "teal")]
    elif sel_moods == mood_comb14:
        colors = [(0.0, "goldenrod"), (0.33, "goldenrod"),
                (0.33, "maroon"), (0.66, "maroon"),
                (0.66, "teal"), (1.00, "teal")]
    elif sel_moods == mood_comb15:
        colors = [(0.0, "rebeccapurple"), (0.33, "rebeccapurple"),
                (0.33, "maroon"), (0.66, "maroon"),
                (0.66, "teal"), (1.00, "teal")]

    fig2 = px.parallel_coordinates(dfcolmap, color="mood", template='plotly_white', title = "Attribute Overview Songs",
                                   dimensions=['popularity', 'length', 'danceability', 'acousticness', 'energy', 'instrumentalness',
                                          'liveness', 'valence','loudness', 'speechiness', 'tempo'],
                                   color_continuous_scale=colors)

    fig2.update_xaxes(title_font=dict(color='#111111'), tickfont=dict(color='#111111'))
    fig2.update_yaxes(title_font=dict(color='#111111'), tickfont=dict(color='#111111'))
    fig2.update_layout(title_font_color="#1DB954", showlegend=False)
    fig2.update_coloraxes(showscale=False)


    #Ursprungsdatensatz kopieren
    dflpd = dff.copy()

    #Release Datum aufspalten in Jahr, Monat und Tag
    dflpd[["year", "month", "day"]] = dflpd["release_date"].str.split("-", expand=True)
    dflpd = dflpd.sort_values("year")

    #df mit Länge und Jahr
    dflpd = dflpd[['length', 'year']].copy()
    dflpd['length'] = dflpd['length']/60000
    dflpd = dflpd.rename(columns={"length": "av. length in min"})

    dflpd = dflpd.groupby(['year']).mean()
    dflpd = dflpd.reset_index(level=0)

    dfff = dff.copy()
    dfff[["year", "month", "day"]] = dfff["release_date"].str.split("-", expand=True)

    dfMoodspYear = dfff.groupby(["year", "mood"]).count()

    MpY = dfMoodspYear.iloc[:,0]
    MpY = MpY.reset_index(level=(0,1))
    MpY["year"] = MpY["year"].astype("int")
    MpY = MpY.sort_values(by=["year"])


    if "view-length-w" == ctx.triggered_id:

        fig3 = px.bar(dflpd, x="year", y="av. length in min",  template='plotly_white', title = "Average Song Length per Year", color_discrete_sequence=["#111111"])

        fig3.update_xaxes(title_font=dict(color="#111111"), tickfont=dict(color="#111111"))
        fig3.update_yaxes(title_font=dict(color="#111111"), tickfont=dict(color="#111111"))
        fig3.update_layout(title_font_color="#1DB954")
        fig3.update_traces(marker_color='#1DB954')


    elif "view-stacked-w" == ctx.triggered_id:

        fig3 = px.bar(MpY, x="year", y="name", color="mood", template='plotly_white', title = "Number of Songs per Mood and Year",
                  color_discrete_map={
                    "Happy": "goldenrod",
                    "Sad": "rebeccapurple",
                    "Energetic": "maroon",
                    "Calm": "teal"},
                  labels={
                     "year": "year",
                     "name": "count of songs",
                     "mood": "mood"
                 })

        fig3.update_xaxes(title_font=dict(color="#111111"), tickfont=dict(color="#111111"))
        fig3.update_yaxes(title_font=dict(color="#111111"), tickfont=dict(color="#111111"))
        fig3.update_layout(title_font_color="#1DB954", showlegend=False)

    else:
        fig3 = px.bar(MpY, x="year", y="name", color="mood", template='plotly_white', title = "Number of Songs per Mood and Year",
                  color_discrete_map={
                    "Happy": "goldenrod",
                    "Sad": "rebeccapurple",
                    "Energetic": "maroon",
                    "Calm": "teal"},
                  labels={
                     "year": "year",
                     "name": "count of songs",
                     "mood": "mood"
                 })

        fig3.update_xaxes(title_font=dict(color="#111111"), tickfont=dict(color="#111111"))
        fig3.update_yaxes(title_font=dict(color="#111111"), tickfont=dict(color="#111111"))
        fig3.update_layout(title_font_color="#1DB954", showlegend=False)


    mcolors = {"Happy": "goldenrod", "Sad": "rebeccapurple", "Energetic": "maroon", "Calm": "teal"}

    fig5 = px.scatter(dff, x=scatterdrop1, y=scatterdrop2, color="mood", color_discrete_map=mcolors, title = "Correlation of Attributes (Click on data point to open Song in Spotify)", template='plotly_white',
                      hover_name="name", hover_data=[dff["artist"], scatterdrop1, scatterdrop2], custom_data=["url"])

    fig5.update_xaxes(title_font=dict(color="#111111"), tickfont=dict(color="#111111"))
    fig5.update_yaxes(title_font=dict(color="#111111"), tickfont=dict(color="#111111"))
    fig5.update_layout(title_font_color="#1DB954", showlegend=False, clickmode='event+select')

    return fig1, fig2, fig5, fig3


@app.callback(
    Output('data-w', 'clickData'),
    Input('scatter-w', 'clickData'))

def open_urlw(clickData):
    if clickData:
        webbrowser.open_new_tab(clickData['points'][0]['customdata'][0])
    else:
        raise PreventUpdate
    # return json.dumps(clickData, indent=2)

if __name__ == '__main__':
    app.run_server(debug=False, port=8051)
