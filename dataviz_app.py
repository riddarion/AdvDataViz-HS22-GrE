import pandas as pd
import plotly.express as px
import numpy as np
import statistics

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
                html.H4("Hier folgt der Datepicker"),
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

            #Erste Zeile mit Stacked Bar Chart
            html.Div(children = [
                    dcc.Graph(id='stacked-bar', figure = {}, style = {'display': 'inline-block'}, responsive=True,
                              config={'displayModeBar': False}),
            ], className="parallel-coordinates-row"),

            #Zweite Zeile, Inhalt folgt später
            html.Div(children = [
            ], className="rest"),
        ], className="graph-container"),
    ], className="container")
])


###Befüllen des Dash Gerüsts mit den Visualisierungen###

#Callback
@app.callback(
    [Output(component_id='treemap', component_property='figure'),
     Output(component_id='stacked-bar', component_property='figure'),
     ],
    [Input(component_id='mood', component_property='value') ,
     Input(component_id='datepicker', component_property='start_date'),
     Input(component_id='datepicker', component_property='end_date') #,
     #Input(component_id='attributes', component_property='value')
    ],
)

def update_moods(mood_slctd, date_slctd1, date_slctd2):  #, date_slctd1, date_slctd2

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
        marker_colors = ["red", "yellow", "aqua", "fuchsia"],
        root_color="#111111"))

    fig1.update_layout(margin=dict(l=0, r=0, t=0, b=0), template='plotly_dark')


    #Ursprungsdatensatz kopieren
    dflpd = dff.copy()

    #Release Datum aufspalten in Jahr, Monat und Tag
    dflpd[["year", "month", "day"]] = dflpd["release_date"].str.split("-", expand=True)
    dflpd = dflpd.sort_values("year")

    # #df mit Länge und Jahr
    # dflpd = dflpd[['length', 'year']].copy()
    # dflpd['length'] = dflpd['length']/60000
    # dflpd = dflpd.rename(columns={"length": "av. length in min"})
    #
    # dfb2000 = dflpd[dflpd['year']<"2000"]
    # dfa2000 = dflpd[dflpd['year']>="2000"]
    #
    # b2000 = pd.DataFrame(columns=["av len", "med year"])
    # b2000["av len"] = dfb2000["av. length in min"].mean()
    # b2000["med year"] = statistics.median(dfb2000["year"].unique())
    #
    # a2000 = pd.DataFrame(columns=["av len", "med year"])
    # a2000["av len"] = dfa2000["av. length in min"].mean()
    # a2000["med year"] = statistics.median(dfa2000["year"].unique())
    #
    # df2000 = pd.concat([b2000, a2000], axis=0)
    #
    # dflpd = dflpd.groupby(['year']).mean()
    # dflpd = dflpd.reset_index(level=0)
    #
    # fig2 = go.Figure()
    #
    # fig2.add_trace(
    #     go.Scatter(x=df2000["med year"], y=df2000["av len"], marker=dict(color="red"), name="Trendline"
    #     ))
    #
    # fig2.add_trace(
    #     go.Bar(x=dflpd["year"], y=dflpd["av. length in min"], marker=dict(color="#1DB954"), marker_line_width = 0, name="Length"
    #     ))
    #
    # fig2.update_xaxes(title_font=dict(color='#1DB954'), tickfont=dict(color='#1DB954'), type='category', categoryorder='category ascending', showgrid=False)
    # fig2.update_yaxes(title_font=dict(color='#1DB954'), tickfont=dict(color='#1DB954'), gridcolor='#303030')
    # fig2.update_layout({'plot_bgcolor': 'rgba(0,0,0,250)', 'paper_bgcolor': 'rgba(0,0,0,250)'},
    #               legend=dict(
    #                 x=1,
    #                 y=1,
    #                 traceorder="reversed",
    #                 font=dict(
    #                 size=12,
    #                 color="white"
    #                     )))

    dfff = dff.copy()
    #dfff["release_date"] = dfff["release_date"].astype(str)
    dfff[["year", "month", "day"]] = dfff["release_date"].str.split("-", expand=True)

    dfMoodspYear = dfff.groupby(["year", "mood"]).count()

    MpY = dfMoodspYear.iloc[:,0]
    MpY = MpY.reset_index(level=(0,1))
    MpY["year"] = MpY["year"].astype("int")
    MpY = MpY.sort_values(by=["year"])

    fig2 = px.bar(MpY, x="year", y="name", color="mood", template='plotly_dark', color_discrete_map={
                "Happy": "red",
                "Sad": "yellow",
                "Energetic": "aqua",
                "Calm": "fuchsia"})

    fig2.update_xaxes(title_font=dict(color='#1DB954'), tickfont=dict(color='#1DB954'))
    fig2.update_yaxes(title_font=dict(color='#1DB954'), tickfont=dict(color='#1DB954'))



    return fig1, fig2



if __name__ == '__main__':
    app.run_server(debug=False, port=8051)
