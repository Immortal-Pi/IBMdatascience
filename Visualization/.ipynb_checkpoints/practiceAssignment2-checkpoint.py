import pandas as pd
import dash
from dash import html, dcc
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input,Output
import datetime as dt


app=dash.Dash(__name__)
data_wf=pd.read_csv('datasets/Historical_Wildfires.csv')
data_wf['Year']=pd.to_datetime(data_wf['Date']).dt.year
data_wf['Month'] = pd.to_datetime(data_wf['Date']).dt.month

app.layout = html.Div(
    children=[
        html.H1(
            'Australia Wildfire Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 30}
        ),
        html.Div([
            html.Div([
                html.H2(
                    'Select Region',
                    style={'margin-right': '2em'}
                ),
                dcc.RadioItems([
                    {"label": "New South Wales", "value": "NSW"},
                    {"label": "Northern Territory", "value": "NT"},
                    {"label": "Queensland", "value": "QL"},
                    {"label": "South Australia", "value": "SA"},
                    {"label": "Tasmania", "value": "TA"},
                    {"label": "Victoria", "value": "VI"},
                    {"label": "Western Australia", "value": "WA"}
                ], value='NSW', id='region')

            ]),
            html.Div([
                html.H2('Select Year', style={'margin-right': '2em'}),
                dcc.Dropdown(
                    data_wf['Year'].unique(), value=2005, id='year'
                )
            ]),
            html.Div([
                html.Div(dcc.Graph(id='plot1')),
                html.Div(dcc.Graph(id='plot2'))
            ], style={'display': 'flex'}),

        ])
    ]
)


@app.callback([
    Output(component_id='plot1', component_property='figure'),
    Output(component_id='plot2', component_property='figure'),
],
    [
        Input(component_id='region', component_property='value'),
        Input(component_id='year', component_property='value')
    ]
)
def get_graph(input_region, input_year):
    print(input_region,input_year)
    region_df = data_wf[data_wf['Region'] == input_region]
    y_region_df = region_df[region_df['Year'] == input_year]
    y_region_df_pie = y_region_df.groupby('Month')['Estimated_fire_area'].mean().reset_index()
    veg_data = y_region_df.groupby('Month')['Count'].mean().reset_index()
    fig1 = px.pie(y_region_df_pie, values='Estimated_fire_area', names='Month',
                  title="{} : Monthly Average Estimated Fire Area in year {}".format(input_region, input_year))
    fig2 = px.bar(veg_data, x='Month', y='Count',
                  title='{} : Average Count of Pixels for Presumed Vegetation Fires in year {}'.format(input_region,
                                                                                                       input_year))
    return [fig1, fig2]


app.run_server(debug=True, port=3007)
