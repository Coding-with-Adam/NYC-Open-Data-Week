import dash_bootstrap_components as dbc 
from dash import Dash, dcc, html, callback, Input, Output, no_update
import plotly.express as px
import pandas as pd
import json

# Load GeoJSON and dataset
with open("new-york-zip-codes-_1604.geojson") as f:
    zip_geojson = json.load(f)

df = pd.read_csv('NYC_Building_Energy_and_Water_Data_Disclosure_for_Local_Law_84__2022-Present__20250106.csv')
df["Postal Code"] = df["Postal Code"].astype(str)

def create_choropleth_map(dataframe, color, range_color, labels, map_style):
    fig = px.choropleth_map(
        data_frame=dataframe,
        color=color,
        range_color=range_color,
        labels=labels,
        geojson=zip_geojson,
        opacity=0.5,
        zoom=10,
        featureidkey="properties.ZCTA5CE10",
        map_style=map_style,
        locations='Postal Code',
        center={"lat": 40.7128, "lon": -74.0060},
        height=550
    )
    return fig

# Initialize Dash app with no default theme (empty list)
app = Dash()

# App Layout
app.layout = html.Div([
    # Title Section
    html.H1("New York City Building Data Visualization", style={"textAlign": "center", "margin": "30px"}),

    # Dropdown for selecting measurement type
    dcc.Dropdown(
        id='measurments', 
        value='ENERGY STAR Score',
        options=[
            {'label': 'ENERGY STAR Score', 'value': 'ENERGY STAR Score'},
            {'label': 'Indoor Water Use (All Water Sources) (kgal)', 'value': 'Indoor Water Use (All Water Sources) (kgal)'},
            {'label': 'Year Built', 'value': 'Year Built'}
        ],
        style={"width": "50%", "margin": "0 auto", "padding": "10px"}
    ),
    html.Br(),

    # Dropdown for selecting map style (dark/light mode)
   dcc.Dropdown(
        id='map-style', 
        value='open-street-map',  # Default to light mode
        options=[
            {'label': 'Light Mode', 'value': 'open-street-map'},
            {'label': 'Dark Mode', 'value': 'carto-darkmatter'}
        ],
        style={"width": "50%", "margin": "0 auto", "padding": "10px"}
    ),
    html.Br(),
    # KPI Card Section (below the title)
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Current value", "textAlign:" "center"),
            dbc.CardBody(html.H4(id="kpi-value", style={"textAlign": "center"}))
        ], color="danger", inverse=True), width=2)
    ], justify="center", style={"marginBottom": "10px"}),

    # Graph for Choropleth Map
    dcc.Graph(id='zip-map'),

    # Container for showing detailed map based on clicks
    html.Div(id='filler'),

    # Placeholder for the external stylesheet link
    html.Link(id="dynamic-stylesheet", rel="stylesheet", href=dbc.themes.COSMO)
])

# Callback to calculate the KPI value based on selected measurement and display in the KPI card
@callback(
    Output('kpi-value', 'children'),
    Input('measurments', 'value')
)
def update_kpi(measurment_chosen):
    df[measurment_chosen] = pd.to_numeric(df[measurment_chosen], errors='coerce')
    
    # Calculate the KPI value based on the selected measurement
    if measurment_chosen == 'ENERGY STAR Score':
        kpi_value = df[measurment_chosen].mean()
        return f"{kpi_value:.2f} (Avg Energy Score)"
    elif measurment_chosen == 'Indoor Water Use (All Water Sources) (kgal)':
        kpi_value = df[measurment_chosen].mean()
        return f"{kpi_value:.2f} kgal (Avg Water Use)"
    elif measurment_chosen == 'Year Built':
        kpi_value = df[measurment_chosen].mean()
        return f"{int(kpi_value)} (Avg Year Built)"
    return "N/A"

# Callback for updating the choropleth map based on selected measurement and map style
@callback(
    Output('zip-map', 'figure'),
    Input('measurments', 'value'),
    Input('map-style', 'value')  # Added map style to input
)
def make_graph(measurment_chosen, map_style):
    df[measurment_chosen] = pd.to_numeric(df[measurment_chosen], errors='coerce')
    df_filtered = df.groupby('Postal Code')[measurment_chosen].mean().reset_index()

    if measurment_chosen == 'ENERGY STAR Score':
        fig = create_choropleth_map(df_filtered, color=measurment_chosen, range_color=[35, 75],
                                    labels={'ENERGY STAR Score': 'Energy Score'}, map_style=map_style)
    elif measurment_chosen == 'Indoor Water Use (All Water Sources) (kgal)':
        fig = create_choropleth_map(df_filtered, color=measurment_chosen, range_color=[2000, 8000],
                                    labels={'Indoor Water Use (All Water Sources) (kgal)': 'Indoor Water Use'}, map_style=map_style)
    elif measurment_chosen == 'Year Built':
        df_filtered['Year Built'] = df_filtered['Year Built'].astype(int)
        fig = create_choropleth_map(df_filtered, color=measurment_chosen, range_color=[1925, 1965], labels=None, map_style=map_style)

    return fig

# Callback for displaying details when a zip code is clicked
@callback(
    Output('filler', 'children'),
    Input('zip-map', 'clickData'),
    Input('measurments', 'value'),  # Added 'measurments' to access chosen measurement
    Input('map-style', 'value')  # Added map style to input
)
def make_graph(clicked_data, measurment_chosen, map_style):
    if clicked_data:
        zipcode = clicked_data['points'][0]['location']
        df_filtered = df[df["Postal Code"] == zipcode]

        # Handle missing lat/lon values or ensure columns exist
        if 'Latitude' in df_filtered.columns and 'Longitude' in df_filtered.columns:
            fig = px.scatter_map(df_filtered, lat="Latitude", lon="Longitude",
                                 hover_name="Year Built",
                                 zoom=12,
                                 color=measurment_chosen,
                                 size_max=30,  # Maximum size of points
                                 color_continuous_scale=['green', 'orange', 'red'],  # Fixing color scale
                                 height=400,
                                 map_style=map_style  # Use selected map style
                                 )
            return dcc.Graph(figure=fig)
        else:
            return html.Div("No location data available.")
    else:
        return no_update

if __name__ == '__main__':
    app.run(debug=True)
