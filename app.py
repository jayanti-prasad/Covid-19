from datetime import date
import os
import pandas as pd
import numpy as np
import dash
import plotly.express as px
from plotly.subplots import make_subplots 
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from scipy import fftpack
from common_utils import get_country_data,date_normalize,get_top_countries

external_stylesheets = ['bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

DATA_PATH="/Users/jayanti/Projects/Covid-19/Covid-19/data/"

dF = pd.read_csv(DATA_PATH + os.sep + "covid-19-global.csv")
countries=get_top_countries(dF)

app.layout = html.Div([
    html.H1(children='Covid-19 Dash Global',style={'text-align': 'center'}),

    html.Div([

        html.Div([
            dcc.Dropdown(
                id='country',
                options=[{'label': i, 'value': i} for i in countries],
                value="India"
            ),
        ],
        style={'width': '20%','display': 'inline-block','float': 'left', 'background-color': '#3CBC8D'}),

        html.Div([
            dcc.Dropdown(
                id='mode',
                options=[{'label': i, 'value': i} for i in ['Cumulative','Daily']],
                value="Cumulative",
                style={'width': '30%', 'display': 'inline-block','float': 'center'},
            ),
    ]),

    html.Div([
      dcc.RadioItems(
                id='plot-style',
                options=[{'label': i, 'value': i} for i in ['Dot','DotLine']],
                value='Dot',
                labelStyle={'display': 'inline-block'}
            )
            ],style={'width': '48%', 'float': 'left', 'display': 'inline-block'}),




    html.Div([
       dcc.DatePickerRange(
                id='date-picker-range',
                start_date_placeholder_text="Start Date",
                end_date_placeholder_text="End Date",
                start_date=dF['date'].min(),
                end_date=dF['date'].max(),
       style={'width': '45%', 'display': 'inline-block','float': 'right'}),

    html.Div(id='output-container-date-picker'),

    ]), 

    html.Br(),
    html.Br(),
    html.Br(),
    html.Hr(),

    dcc.Graph(id='indicator-graphic'),



    ])
    
])



@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('country', 'value'),
    Input(component_id='date-picker-range', component_property='start_date'),
    Input(component_id='date-picker-range', component_property='end_date'),
    Input('mode', 'value'),Input('plot-style', 'value')])


def update_graph(country,start_date,end_date,mode,plot_style):


    df = get_country_data (dF, country)
    df.index = df['date'].to_list()


    mask = (df['date'] > start_date) & (df['date'] <= end_date)
    df = df.loc[mask] 

    X = df['confirmed']
    Y = df['recovered']
    Z = df['deaths'] 

    if mode == 'Cumulative':
       x = X
       y = Y 
       z = Z
       title = country + " Covid-19 (Total Cases)"
   
    if mode == 'Daily':
       x = X.diff(periods=1).iloc[1:]
       y = Y.diff(periods=1).iloc[1:]
       z = Z.diff(periods=1).iloc[1:]
       title = country + " Covid-19 (Daily Cases)"

    fig1 = px.scatter(x)
    fig2 = px.scatter(y)
    fig3 = px.scatter(z)

    trace1 = fig1['data'][0]
    trace2 = fig2['data'][0]
    trace3 = fig3['data'][0]

    fig = make_subplots(rows=2, cols=1,shared_xaxes=False,\
      horizontal_spacing=0.1, vertical_spacing=0.05,\
     y_title=country,subplot_titles=([title]))

    fig.add_trace(trace1, row=1, col=1)
    fig.add_trace(trace2, row=1, col=1)
    fig.add_trace(trace3, row=2, col=1)

    if plot_style == 'DotLine':
       fig.data[0].update(mode='markers+lines')
       fig.data[1].update(mode='markers+lines')
       fig.data[2].update(mode='markers+lines')

    fig['data'][0]['marker']['color']="blue"
    fig['data'][1]['marker']['color']="green"
    fig['data'][2]['marker']['color']="red"


    fig.update_layout(width=1200,height=600,margin=dict(l=10, r=10, t=20, b=40))


    return fig

if __name__ == '__main__':
    app.run_server(debug=True,dev_tools_silence_routes_logging=False)
