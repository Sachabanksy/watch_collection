# pages/trends_analysis.py
import dash
from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from utils.fakedata import generate_watch_data

dash.register_page(__name__, path="/trends-analysis")

# Load the data
df = generate_watch_data(1000)

# Define layout
layout = dbc.Container([
    html.H2("Trends & Analysis", className="text-center"),

    # Parameters Selection
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Select Analysis Type"),
                    dbc.Select(
                        options=[
                            {"label": "Average Price Over Time", "value": "price_over_time"},
                            {"label": "Brand Comparison", "value": "brand_comparison"},
                            {"label": "Attribute Impact", "value": "attribute_impact"},
                        ],
                        value="price_over_time",
                        id="analysis-type",
                    ),
                ], md=4),
                dbc.Col([
                    dbc.Label("Brands"),
                    dcc.Dropdown(
                        options=[{'label': brand, 'value': brand} for brand in sorted(df['brand'].unique())],
                        multi=True,
                        id="analysis-brands",
                    ),
                ], md=4),
                dbc.Col([
                    dbc.Button("Update Analysis", id="update-analysis", color="primary", className="mt-4"),
                ], md=4),
            ]),
        ]),
        className="mb-4",
    ),

    # Analysis Graph
    dbc.Card(
        dbc.CardBody([
            dcc.Loading(
                dcc.Graph(id="analysis-graph"),
                type="default",
            ),
        ]),
    ),
], fluid=True)

# Callback
@callback(
    Output("analysis-graph", "figure"),
    Input("update-analysis", "n_clicks"),
    State("analysis-type", "value"),
    State("analysis-brands", "value"),
    prevent_initial_call=True,
)
def update_analysis(n_clicks, analysis_type, selected_brands):
    dff = df.copy()
    if selected_brands:
        dff = dff[dff['brand'].isin(selected_brands)]

    if analysis_type == "price_over_time":
        dff_grouped = dff.groupby(['year']).agg({'sold_price': 'mean'}).reset_index()
        fig = px.line(
            dff_grouped,
            x='year',
            y='sold_price',
            title='Average Sold Price Over Time',
            markers=True,
        )
    elif analysis_type == "brand_comparison":
        dff_grouped = dff.groupby(['brand']).agg({'sold_price': 'mean'}).reset_index()
        fig = px.bar(
            dff_grouped,
            x='brand',
            y='sold_price',
            title='Average Sold Price by Brand',
        )
    elif analysis_type == "attribute_impact":
        fig = px.scatter(
            dff,
            x='year',
            y='sold_price',
            color='case_material',
            title='Sold Price vs Year Colored by Case Material',
        )
    else:
        fig = px.line(title="Select an analysis type.")

    return fig
