import dash
from dash import html, dcc, Input, Output, State, ALL, callback
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import sys
import os
import time 
import random 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.fakedata import generate_watch_data, read_fake_data
import plotly.graph_objs as go

dash.register_page(__name__, path="/watch_collection")

# Load the data
#watch_data_df = generate_watch_data(1000)

watch_data_df = read_fake_data()

# Create 'name' column
#watch_data_df['name'] = watch_data_df['brand'].fillna('Unknown') + ' ' + watch_data_df['collection'].fillna('Unknown')

# Replace NaNs in 'sold_price' and 'estimate_low' with zero
watch_data_df['sold_price'] = watch_data_df['sold_price'].fillna(0)
watch_data_df['estimate_low'] = watch_data_df['estimate_low'].fillna(0)
watch_data_df['previous_price'] = watch_data_df['previous_price'].fillna(0)

# Calculate profit percentage using vectorized operations
# Avoid division by zero by creating a mask
watch_data_df['profit_percentage'] = np.where(
    watch_data_df['estimate_low'] != 0,
    ((watch_data_df['sold_price'] - watch_data_df['estimate_low']) / watch_data_df['estimate_low'] * 100).round(2),
    0
)

# Determine 'is_popular' based on 'sold_price' in the top 25%
threshold = watch_data_df['sold_price'].quantile(0.75)
watch_data_df['is_popular'] = watch_data_df['sold_price'] >= threshold

# Limit the number of watches displayed for performance
display_df = watch_data_df.head(20)

display_df['id'] = display_df.index 

print(display_df[['brand', 'name', 'sold_price', 'previous_price']])

# Portfolio summary calculations with safe handling of edge cases
total_estimated_value = display_df['sold_price'].sum()
previous_value = display_df['previous_price'].sum()
change_value = total_estimated_value - previous_value

# Calculate change percentage with safe division
change_percentage = (change_value / previous_value * 100)

number_of_watches = len(display_df)
number_of_brands = display_df['brand'].nunique()

# Add debug prints to verify calculations
print(f"Debug Information:")
print(f"Total Estimated Value: {total_estimated_value}")
print(f"Previous Value: {previous_value}")
print(f"Change Value: {change_value}")
print(f"Change Percentage: {change_percentage}")

portfolio_dates = ['2021-01', '2021-02', '2021-03', '2021-04', '2021-05']
portfolio_values = [5000, 5500, 5300, 6000, 6200]

# Create the sparkline figure
portfolio_sparkline_figure = go.Figure(
    data=[
        go.Scatter(
            x=portfolio_dates,
            y=portfolio_values,
            mode='lines',
            line=dict(color='#007bff', shape='spline', width=3),
            fill='tozeroy',
            fillcolor='rgba(0, 123, 255, 0.2)',
        )
    ]
)

# Update layout to remove gridlines, axis labels, etc.
portfolio_sparkline_figure.update_layout(
    xaxis=dict(showgrid=False, zeroline=False, visible=False),
    yaxis=dict(showgrid=False, zeroline=False, visible=False),
    margin=dict(l=0, r=0, t=0, b=0),
    plot_bgcolor='rgba(0,0,0,0)',
)

layout = html.Div(
    [
        # Page Header
        html.Div(
            [
                html.H2("Watch Collection", className="display-4 text-center mb-4"),
                html.Hr(className="my-2"),
            ],
            className="mb-4",
        ),
        # Tabs and Add Watch Button
        dbc.Row(
            [
                dbc.Col(
                    dbc.Tabs(
                        [
                            dbc.Tab(label="My Watches", tab_id="my-watches", tabClassName="custom-tab"),
                            dbc.Tab(label="Followed Watches", tab_id="followed-watches", tabClassName="custom-tab"),
                        ],
                        id="tabs",
                        active_tab="my-watches",
                        className="custom-tabs",
                    ),
                    width=9,
                ),
                dbc.Col(
                    dbc.Button(
                        "+ Add Watch",
                        color="primary",
                        className="float-end",
                        id="add-watch-button",
                    ),
                    width=3,
                    className="d-flex align-items-center justify-content-end",
                ),
            ],
            className="mb-4",
        ),
        # Content
        html.Div(
            id="content",
            children=[
                # Summary Section
                dbc.Card(
                    dbc.CardBody(
                        dbc.Row(
                            [
                                # Left Column: Portfolio Information
                                dbc.Col(
                                    [
                                        html.H5("Portfolio Summary", className="card-title"),
                                        html.H2(f"£{total_estimated_value:,.2f}", className="card-text"),
                                        html.P(
                                            [
                                                html.Span("Change: ", className="me-1"),
                                                html.Span(
                                                    f"{'+' if change_value >= 0 else '-'}£{abs(change_value):,.2f} ({change_percentage:.2f}%)",
                                                    className="text-success" if change_value >= 0 else "text-danger",
                                                ),
                                                html.I(
                                                    className=f"bi bi-arrow-{ 'up' if change_value >= 0 else 'down' }",
                                                    style={"marginLeft": "5px"},
                                                ),
                                            ],
                                            className="card-text",
                                        ),
                                        html.P(f"Number of Watches: {number_of_watches}", className="card-text"),
                                        html.P(f"Different Brands: {number_of_brands}", className="card-text"),
                                    ],
                                    width=8,
                                ),
                                # Right Column: Sparkline Chart
                                dbc.Col(
                                    dcc.Graph(
                                        figure=portfolio_sparkline_figure,
                                        config={'displayModeBar': False},
                                        style={"height": "150px"},
                                    ),
                                    width=4,
                                ),
                            ],
                            align="center",
                        )
                    ),
                    className="mb-5 shadow-sm",
                ),
                # Watch List
                html.Div(
                    [
                        html.H3("Your Watches", className="mb-4"),
                        dbc.Container(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Card(
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            dbc.CardImg(
                                                                src=row["image"],
                                                                className="img-fluid rounded-start",
                                                                style={
                                                                    "height": "100px",
                                                                    "object-fit": "cover",
                                                                },
                                                            ),
                                                            width=4,
                                                        ),
                                                        dbc.Col(
                                                            dbc.CardBody(
                                                                [
                                                                    html.Div(
                                                                        [
                                                                            html.H5(
                                                                                row["name"],
                                                                                className="card-title mb-0 me-2",
                                                                            ),
                                                                            dbc.Badge(
                                                                                "Popular",
                                                                                color="warning",
                                                                                className="",
                                                                                pill=True,
                                                                            )
                                                                            if row["is_popular"]
                                                                            else None,
                                                                        ],
                                                                        className="d-flex align-items-center mb-2",
                                                                    ),
                                                                    html.P(
                                                                        f"Estimated Value: £{row['sold_price']:,.2f}",
                                                                        className="card-text mb-1",
                                                                    ),
                                                                    html.P(
                                                                        f"Profit: +{row['profit_percentage']}%",
                                                                        className="card-text text-success mb-1",
                                                                    ),
                                                                    dbc.Button(
                                                                        "Details",
                                                                        color="primary",
                                                                        className="mt-1",
                                                                        size="sm",
                                                                        outline=True,
                                                                        id={'type': 'details-button', 'index': str(row['id'])},
                                                                    ),
                                                                ],
                                                                className="p-2",
                                                            ),
                                                            width=8,
                                                        ),
                                                    ],
                                                    className="g-0 d-flex align-items-center",
                                                ),
                                                className="mb-3 shadow-sm",
                                            ),
                                            width=12,
                                            md=6,
                                        )
                                        for _, row in display_df.iterrows()
                                    ]
                                )
                            ],
                            fluid=True,
                        ),
                    ]
                ),
                # Modal
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("Watch Details"), close_button=True),
                        dbc.ModalBody(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            html.Img(
                                                id='modal-image',
                                                src='',
                                                className='img-fluid',
                                                style={"width": "100%"}
                                            ),
                                            width=12,
                                        ),
                                    ],
                                    className="mb-3",
                                ),
                                html.H4(id='modal-name', className="mb-3"),
                                html.P(id='modal-description', className="mb-3"),
                                html.P(id='modal-prices', className="mb-3"),
                                dcc.Graph(
                                    id='modal-chart',
                                    config={'displayModeBar': False},
                                    style={"height": "250px"},
                                ),
                            ]
                        ),
                    ],
                    id='details-modal',
                    size='lg',
                    centered=True,
                    is_open=False,
                ),

                dbc.Modal([
                            dbc.ModalHeader([
                                dbc.ModalTitle("Add Watch to Collection"),
                                    dbc.Input(
                                            type="search",
                                            id="watch-search-input",
                                            placeholder="Search for watches...",
                                            className="mt-2",
                                            debounce=True,
                                        ),
                                    ],
                                    close_button=True,
                                ),
                                dbc.ModalBody(
                                    [
                                    # Placeholder text for initial state before search results
                                    html.Div(
                                        [
                                            html.I(
                                                className="bi bi-search", 
                                                style={
                                                    "fontSize": "4rem",  # Increased from 2rem to 4rem
                                                    "color": "gray",
                                                    "marginBottom": "1rem",  # Added spacing between icon and text
                                                    "opacity": "0.6"  # Added slight transparency for a softer look
                                                }
                                            ),
                                            html.P(
                                                "Search by name, model, make, etc.",
                                                className="text-muted",
                                                style={
                                                    "fontSize": "1.25rem",
                                                    "margin": "0",  # Reset margin to ensure proper centering
                                                    "padding": "0 1rem"  # Added horizontal padding for better text wrapping
                                                }
                                            ),
                                        ],
                                        id="search-placeholder",
                                        style={
                                            "textAlign": "center",
                                            "marginTop": "4rem",  # Increased from 2rem to 4rem
                                            "marginBottom": "4rem",  # Added bottom margin
                                            "display": "flex",
                                            "flexDirection": "column",
                                            "alignItems": "center",
                                            "justifyContent": "center",
                                            "minHeight": "200px"  # Added minimum height for better vertical spacing
                                        }
                                    ),
                                        # Search results container
                                        html.Div(
                                            dbc.Container(
                                                dbc.Row(id="search-results-container", className="g-3"),
                                                fluid=True,
                                            ),
                                            style={"maxHeight": "60vh", "overflowY": "auto"},
                                            className="pe-2",
                                        ),
                                    ]
                                ),
                            ],
                            id="add-watch-modal",
                            size="xl",
                            scrollable=True,
                            is_open=False,
                        ), 
                ],
        ),
    ],
    className="container-fluid",
)

# Callbacks for the modal functionality
@callback(
    Output('details-modal', 'is_open'),
    Output('modal-image', 'src'),
    Output('modal-name', 'children'),
    Output('modal-description', 'children'),
    Output('modal-prices', 'children'),
    Output('modal-chart', 'figure'),
    [Input({'type': 'details-button', 'index': ALL}, 'n_clicks'),
     Input('details-modal', 'n_close'),
     Input('details-modal', 'n_dismiss')],
    [State('details-modal', 'is_open')],
)
def toggle_modal(n_clicks_list, n_close, n_dismiss, is_open):
    ctx = dash.callback_context
    if not ctx.triggered:
        return is_open, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
    else:
        prop_id = ctx.triggered[0]['prop_id']
        if 'details-button' in prop_id:
            # A 'Details' button was clicked
            button_id = prop_id.split('.')[0]
            index = eval(button_id)['index']
            # Retrieve the watch data based on the index
            watch_row = display_df[display_df['id'] == int(index)].iloc[0]

            # Update modal content
            image_src = watch_row['image']
            name = watch_row['name']
            description = 'Detailed description of the watch goes here.'  # Replace with actual data
            prices = f"Bought Price: £{watch_row['previous_price']:,.2f} | Estimated Price: £{watch_row['sold_price']:,.2f}"

            # Create the price over time chart
            price_dates = ['2021-01', '2021-06', '2022-01', '2022-06', '2023-01']  # Replace with actual data
            price_values = [
                watch_row['previous_price'],
                watch_row['previous_price'] * 1.05,
                watch_row['previous_price'] * 1.10,
                watch_row['previous_price'] * 1.15,
                watch_row['sold_price']
            ]  # Example data

            price_chart = go.Figure(
                data=[
                    go.Scatter(
                        x=price_dates,
                        y=price_values,
                        mode='lines',
                        line=dict(color='#007bff', shape='spline', width=3),
                        fill='tozeroy',
                        fillcolor='rgba(0, 123, 255, 0.2)',
                    )
                ]
            )
            price_chart.update_layout(
                xaxis=dict(showgrid=False, zeroline=False, visible=False),
                yaxis=dict(showgrid=False, zeroline=False, visible=False),
                margin=dict(l=0, r=0, t=0, b=0),
                plot_bgcolor='rgba(0,0,0,0)',
            )

            return True, image_src, name, description, prices, price_chart
        elif 'details-modal' in prop_id:
            # Modal close or dismiss was triggered
            return False, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    return is_open, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

@callback(
    Output("add-watch-modal", "is_open"),
    [
        Input("add-watch-button", "n_clicks"),
        Input("add-watch-modal", "n_close"),
        Input("add-watch-modal", "n_dismiss"),
    ],
    [State("add-watch-modal", "is_open")],
)
def toggle_add_watch_modal(n_clicks, n_close, n_dismiss, is_open):
    if n_clicks or n_close or n_dismiss:
        return not is_open
    return is_open

@callback(
    [
        Output("search-results-container", "children"),
        Output("search-placeholder", "style"),
    ],
    Input("watch-search-input", "value"),
)
def update_search_results(search_query):
    # Generate example watches as a DataFrame and convert to list of dictionaries
    example_watches_df = read_fake_data()
    #example_watches_df['name'] = example_watches_df['brand'].fillna('Unknown') + ' ' + example_watches_df['collection'].fillna('Unknown')
    example_watches_df['id'] = example_watches_df.index 
    example_watches = example_watches_df.to_dict(orient="records")  # Convert to list of dictionaries

    # If no search query, show placeholder text
    if not search_query:
        return [], {"display": "block"}  # Show placeholder text

    # Filter example watches based on search query
    filtered_watches = [
        watch for watch in example_watches
        if search_query.lower() in watch.get("name", "").lower() or search_query.lower() in watch.get("brand", "").lower()
    ]

    # Create cards for search results
    search_cards = [
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardImg(
                        src=watch["image"],
                        top=True,
                        style={"height": "200px", "objectFit": "cover"},
                    ),
                    dbc.CardBody(
                        [
                            html.H5(watch["name"], className="card-title mb-1"),
                            html.P(
                                [
                                    html.Span(watch["brand"], className="text-muted"),
                                    html.Br(),
                                    html.Small(f"Ref: {watch['reference']}", className="text-muted"),
                                ],
                                className="mb-2",
                            ),
                            html.P(
                                f"£{watch['sold_price']:,.2f}",
                                className="font-weight-bold mb-2",
                            ),
                            dbc.Button(
                                "Add to Collection",
                                id={"type": "add-watch-to-collection-button", "index": watch["id"]},
                                color="primary",
                                size="sm",
                                className="w-100",
                            ),
                        ],
                        className="p-3",
                    ),
                ],
                className="h-100 shadow-sm hover-shadow",
            ),
            width=12,
            md=6,
            lg=3,
            className="mb-3",
        )
        for watch in filtered_watches
    ]

    # Hide placeholder text if search results are found
    placeholder_style = {"display": "none"} if filtered_watches else {"display": "block"}

    return search_cards, placeholder_style