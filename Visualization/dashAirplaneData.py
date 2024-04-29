import pandas as pd
import dash
from dash import html,dcc
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input,Output


app=dash.Dash(__name__)

data1=pd.read_csv('datasets/airline_data.csv')
# print(data1[['Year','DestState']].dtypes)
# data_dest=data1[data1['Year']==int(2012)].groupby(['DestState'])['Flights'].count().reset_index()

app.layout=html.Div(
    children=[
        html.H1('Flight Frequency Dashboard',
                style={'textAlign':'center','color':'#503D36','font-size':40}),
        html.Div([
            'Input Year :',
            dcc.Input(id='input-year',value='2010',type='number',
                      style={'height':'25px','font-size':20})
        ],style={'font-size':20}),
        html.Br(),
        html.Br(),
        dcc.Graph(id='bar-plot')
    ]
)

@app.callback(Output(component_id='bar-plot',component_property='figure'),
              Input(component_id='input-year',component_property='value'))
def graph_plot(entered_year):
    data_dest = data1[data1['Year'] == int(entered_year)].groupby(['DestState'])['Flights'].count().reset_index()
    fig=px.bar(data_dest,x='DestState',y='Flights')
    fig.update_layout(title='Flight Frequency for state per year',xaxis_title='States',yaxis_title='frequency')
    return fig
# print(data_dest)
app.run_server(debug=True,port=3004)

