import dash
from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
import plotly.express as px

dash.register_page(__name__, path="/personal-collection")

# Placeholder for user collection data
user_collection = pd.DataFrame(columns=[
    'brand', 'collection', 'reference', 'year', 'purchase_price', 'current_value', 'change_pct'
])

# Define layout
layout = dbc.Container([
    html.H2("Personal Collection", className="text-center mb-4"),

    # Add Watch Form
    dbc.Card(
        dbc.CardBody([
            html.H4("Add a Watch", className="mb-3"),
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        # Brand Input
                        dbc.Label("Brand", html_for="input-brand", width=12),
                        dbc.Col(
                            dbc.Input(
                                type="text",
                                id="input-brand",
                                placeholder="Enter brand"
                            ),
                            width=12,
                            className="mb-3"
                        ),
                    ]),
                    dbc.Row([
                        # Collection Input
                        dbc.Label("Collection", html_for="input-collection", width=12),
                        dbc.Col(
                            dbc.Input(
                                type="text",
                                id="input-collection",
                                placeholder="Enter collection"
                            ),
                            width=12,
                            className="mb-3"
                        ),
                    ]),
                    dbc.Row([
                        # Reference Input
                        dbc.Label("Reference", html_for="input-reference", width=12),
                        dbc.Col(
                            dbc.Input(
                                type="text",
                                id="input-reference",
                                placeholder="Enter reference"
                            ),
                            width=12,
                            className="mb-3"
                        ),
                    ]),
                ], md=6),
                dbc.Col([
                    dbc.Row([
                        # Year Input
                        dbc.Label("Year", html_for="input-year", width=12),
                        dbc.Col(
                            dbc.Input(
                                type="number",
                                id="input-year",
                                placeholder="Enter year"
                            ),
                            width=12,
                            className="mb-3"
                        ),
                    ]),
                    dbc.Row([
                        # Purchase Price Input
                        dbc.Label("Purchase Price", html_for="input-purchase-price", width=12),
                        dbc.Col(
                            dbc.Input(
                                type="number",
                                id="input-purchase-price",
                                placeholder="Enter purchase price"
                            ),
                            width=12,
                            className="mb-3"
                        ),
                    ]),
                ], md=6),
            ]),
            dbc.Button(
                "Add to Collection",
                id="add-watch-button",
                color="primary",
                className="mt-3"
            ),
        ]),
        className="mb-4",
    ),

    # Collection Overview
    html.H4("Your Collection", className="mb-3"),
    dash_table.DataTable(
        columns=[
            {"name": "Brand", "id": "brand"},
            {"name": "Collection", "id": "collection"},
            {"name": "Reference", "id": "reference"},
            {"name": "Year", "id": "year"},
            {"name": "Purchase Price", "id": "purchase_price", "type": "numeric", "format": {"specifier": "$,.2f"}},
            {"name": "Current Value", "id": "current_value", "type": "numeric", "format": {"specifier": "$,.2f"}},
            {"name": "Change (%)", "id": "change_pct", "type": "numeric", "format": {"specifier": ".1f"}},
        ],
        data=user_collection.to_dict('records'),
        id="collection-table",
        page_size=10,
        style_table={'overflowX': 'auto'},
        style_cell={
            'textAlign': 'left',
            'padding': '8px'
        },
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },
    ),
    html.Br(),

    # Collection Value Chart
    html.H4("Collection Value Over Time", className="mb-3"),
    dcc.Graph(id="collection-value-graph"),
], fluid=True)

# Callbacks
@callback(
    [Output("collection-table", "data"),
     Output("collection-value-graph", "figure"),
     Output("input-brand", "value"),
     Output("input-collection", "value"),
     Output("input-reference", "value"),
     Output("input-year", "value"),
     Output("input-purchase-price", "value")],
    Input("add-watch-button", "n_clicks"),
    [State("input-brand", "value"),
     State("input-collection", "value"),
     State("input-reference", "value"),
     State("input-year", "value"),
     State("input-purchase-price", "value"),
     State("collection-table", "data")],
    prevent_initial_call=True,
)
def add_watch(n_clicks, brand, collection, reference, year, purchase_price, table_data):
    if not all([brand, collection, reference, year, purchase_price]):
        raise dash.exceptions.PreventUpdate
        
    # Append new watch to collection
    new_entry = {
        'brand': brand,
        'collection': collection,
        'reference': reference,
        'year': int(year),
        'purchase_price': float(purchase_price),
    }
    table_data.append(new_entry)
    df_collection = pd.DataFrame(table_data)

    # Estimate current value (this is a placeholder)
    df_collection['current_value'] = df_collection['purchase_price'] * 1.05  # Assume 5% increase
    df_collection['change_pct'] = ((df_collection['current_value'] - df_collection['purchase_price']) / 
                                 df_collection['purchase_price'] * 100)

    # Update collection value graph
    df_collection_sorted = df_collection.sort_values('year')
    fig = px.line(
        df_collection_sorted,
        x='year',
        y='current_value',
        title='Collection Value Over Time',
        markers=True,
        labels={'current_value': 'Current Value ($)', 'year': 'Year'}
    )
    fig.update_layout(
        template="simple_white",
        xaxis_title="Year",
        yaxis_title="Current Value ($)",
        showlegend=False
    )

    # Clear input fields
    return (df_collection.to_dict('records'), fig, 
            "", "", "", None, None)  # Reset all input fields