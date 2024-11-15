# pages/data_explorer.py
import dash
from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
import plotly.express as px
from utils.fakedata import generate_watch_data

dash.register_page(__name__, path="/test_page")

# Load the data (Replace 'your_data.csv' with your actual data file)
df = generate_watch_data(1000)

# Define layout
layout = dbc.Container([
    html.H2("Data Explorer", className="text-center"),

    # Filters Section
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Brand"),
                    dcc.Dropdown(
                        options=[{'label': brand, 'value': brand} for brand in sorted(df['brand'].unique())],
                        multi=True,
                        placeholder="Select brands",
                        id="brand-filter",
                    ),
                ], md=4),
                dbc.Col([
                    dbc.Label("Year Range"),
                    dcc.RangeSlider(
                        min=df['year'].min(),
                        max=df['year'].max(),
                        value=[df['year'].min(), df['year'].max()],
                        marks={str(year): str(year) for year in range(df['year'].min(), df['year'].max()+1, 5)},
                        id="year-filter",
                    ),
                ], md=4),
                dbc.Col([
                    dbc.Label("Sold Price Range"),
                    dcc.RangeSlider(
                        min=df['sold_price'].min(),
                        max=df['sold_price'].max(),
                        value=[df['sold_price'].min(), df['sold_price'].max()],
                        marks={int(price): f"${int(price)}" for price in range(int(df['sold_price'].min()), int(df['sold_price'].max()), int((df['sold_price'].max()-df['sold_price'].min())/5))},
                        id="price-filter",
                    ),
                ], md=4),
            ], className="mb-3"),
            dbc.Button("Apply Filters", id="apply-filters", color="primary"),
        ]),
        className="mb-4",
    ),

    # Data Table
    dbc.Card(
        dbc.CardBody([
            dash_table.DataTable(
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
                id="data-table",
                page_size=10,
                style_table={'overflowX': 'auto'},
            ),
        ]),
        className="mb-4",
    ),

    # Graphs Section
    dbc.Card(
        dbc.CardBody([
            html.H3("Visualizations"),
            dbc.Tabs([
                dbc.Tab(dcc.Graph(id="price-dist-graph"), label="Price Distribution"),
                dbc.Tab(dcc.Graph(id="brand-count-graph"), label="Watches per Brand"),
            ]),
        ]),
    ),
], fluid=True)

# Callbacks
@callback(
    Output("data-table", "data"),
    Input("apply-filters", "n_clicks"),
    State("brand-filter", "value"),
    State("year-filter", "value"),
    State("price-filter", "value"),
    prevent_initial_call=True,
)
def update_table(n_clicks, selected_brands, year_range, price_range):
    dff = df.copy()
    if selected_brands:
        dff = dff[dff['brand'].isin(selected_brands)]
    dff = dff[(dff['year'] >= year_range[0]) & (dff['year'] <= year_range[1])]
    dff = dff[(dff['sold_price'] >= price_range[0]) & (dff['sold_price'] <= price_range[1])]
    return dff.to_dict('records')

@callback(
    Output("price-dist-graph", "figure"),
    Output("brand-count-graph", "figure"),
    Input("data-table", "data"),
)
def update_graphs(table_data):
    dff = pd.DataFrame(table_data)

    # Price Distribution Histogram
    fig_price_dist = px.histogram(
        dff, x="sold_price", nbins=50, title="Sold Price Distribution"
    )

    # Watches per Brand Bar Chart
    brand_counts = dff['brand'].value_counts().reset_index()
    brand_counts.columns = ['brand', 'count']
    fig_brand_count = px.bar(
        brand_counts, x='brand', y='count', title="Number of Watches per Brand"
    )

    return fig_price_dist, fig_brand_count
