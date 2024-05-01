import pandas as pd
import dash
from dash import html,dcc
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input,Output



data=pd.read_csv('datasets/airline_data.csv')
# print(data[data['Year']==int(2012)].groupby('avg_car')['Year'].mean().reset_index())


app=dash.Dash(__name__)

app.layout=html.Div(
    children=[
        html.H1(
            'AirLines Dashboard',
            style={'textAlign':'center','color':'#503D36','font-size':30}
        ),
        html.Div(
            ['Input Year:',dcc.Input(id='input-year',value='2010',type='number',
                                     style={'height':'35px', 'font-size': 30})
            ],style={'font-size': 30}
        ),
        html.Br(),
        html.Br(),
        html.Div(
            [
                html.Div(dcc.Graph(id='carrier-line')),
                html.Div(dcc.Graph(id='weather-line'))
            ],style={'display':'flex'}
        ),
        html.Div(
            [
                html.Div(dcc.Graph(id='nas-line')),
                html.Div(dcc.Graph(id='security-line'))
            ],style={'display':'flex'}
        ),
        html.Div(
            [
                html.Div(dcc.Graph(id='late-line'),style={'width':'65%'}),

            ]
        ),
    ]
)

@app.callback(
                [Output(component_id='carrier-line',component_property='figure'),
                Output(component_id='weather-line',component_property='figure'),
                Output(component_id='nas-line',component_property='figure'),
                Output(component_id='security-line',component_property='figure'),
                Output(component_id='late-line',component_property='figure'),
                 ],
                Input(component_id='input-year',component_property='value'),
              )
def get_graph(entered_year):
    avg_car, avg_weather, avg_NAS, avg_sec, avg_late = compute_info(data, entered_year)
    carrier_fig = px.line(avg_car, x='Month', y='CarrierDelay', color='Reporting_Airline',
                          title='Average carrrier delay time (minutes) by airline')
    # Line plot for weather delay
    weather_fig = px.line(avg_weather, x='Month', y='WeatherDelay', color='Reporting_Airline',
                          title='Average weather delay time (minutes) by airline')
    # Line plot for nas delay
    nas_fig = px.line(avg_NAS, x='Month', y='NASDelay', color='Reporting_Airline',
                      title='Average NAS delay time (minutes) by airline')
    # Line plot for security delay
    sec_fig = px.line(avg_sec, x='Month', y='SecurityDelay', color='Reporting_Airline',
                      title='Average security delay time (minutes) by airline')
    # Line plot for late aircraft delay
    late_fig = px.line(avg_late, x='Month', y='LateAircraftDelay', color='Reporting_Airline',
                       title='Average late aircraft delay time (minutes) by airline')

    return [carrier_fig, weather_fig, nas_fig, sec_fig, late_fig]

def compute_info(airline_data, entered_year):
    df = airline_data[airline_data['Year'] == int(entered_year)]
    # Compute delay averages
    avg_car = df.groupby(['Month', 'Reporting_Airline'])['CarrierDelay'].mean().reset_index()
    avg_weather = df.groupby(['Month', 'Reporting_Airline'])['WeatherDelay'].mean().reset_index()
    avg_NAS = df.groupby(['Month', 'Reporting_Airline'])['NASDelay'].mean().reset_index()
    avg_sec = df.groupby(['Month', 'Reporting_Airline'])['SecurityDelay'].mean().reset_index()
    avg_late = df.groupby(['Month', 'Reporting_Airline'])['LateAircraftDelay'].mean().reset_index()
    # print(avg_late)
    return avg_car, avg_weather, avg_NAS, avg_sec, avg_late

# compute_info(data,2012)
# get_graph(data,2012)

app.run_server(debug='True',port=3005)

