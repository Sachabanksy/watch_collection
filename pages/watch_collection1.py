import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
from utils.fakedata import generate_watch_data

dash.register_page(__name__, path="/watch_collection1")

# Load the data
watch_data_df = generate_watch_data(100)

# Create 'name' column
watch_data_df['name'] = watch_data_df['brand'] + ' ' + watch_data_df['collection']

# Replace NaNs in 'sold_price' with zero
watch_data_df['sold_price'] = watch_data_df['sold_price'].fillna(0)

# Calculate 'profit_percentage' (assuming 'estimate_low' as the purchase price)
watch_data_df['profit_percentage'] = (
    (watch_data_df['sold_price'] - watch_data_df['estimate_low']) / watch_data_df['estimate_low'] * 100
).round(2)

# Determine 'is_popular' based on 'sold_price' in the top 25%
watch_data_df['is_popular'] = watch_data_df['sold_price'] >= watch_data_df['sold_price'].quantile(0.75)

# Limit the number of watches displayed for performance
display_df = watch_data_df.head(20)

# Layout components
header = html.Div(
    className="d-flex justify-content-between align-items-center",
    style={"alignItems": "center"},
    children=[
        html.H1("Watch Collection"),
        html.Div(
            dbc.Button(
                [html.I(className="bi bi-plus-lg me-2"), "Add a watch"],
                color="secondary",
                href="/add-item?watchCollectionItemOrigin=WatchCollection",
                className="text-decoration-none",
            ),
            style={"flex": "0 1 0%"},
        ),
    ],
)

tabs = html.Div(
    className="mt-3 mb-5 text-lg d-flex border-bottom",
    children=[
        html.Div(
            html.A("My Watches", href="/overview/owned-watches", className="active"),
            className="wt-overview-navigation-link-desktop router-link relative",
        ),
        html.Div(
            html.A("Followed Watches", href="/overview/followed-watches"),
            className="wt-overview-navigation-link-desktop router-link relative",
        ),
    ],
)

overview_section = html.Div(
    className="wt-overview-carousel mt-3 mb-2 mb-sm-5",
    children=[
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardBody(
                                [
                                    html.Div(
                                        className="d-flex justify-content-between",
                                        style={"alignItems": "center"},
                                        children=[
                                            html.Div(
                                                [
                                                    html.H2(
                                                        f"£ {watch_data_df['sold_price'].sum():,.2f}",
                                                        className="mt-0 mb-1",
                                                    ),
                                                    html.P("Current estimated value"),
                                                ]
                                            ),
                                            html.Div(
                                                [
                                                    html.H2(
                                                        f"+£ {(watch_data_df['sold_price'].sum() - watch_data_df['estimate_low'].sum()):,.2f}",
                                                        className="mt-0 mb-1 text-success",
                                                    ),
                                                    html.P("Profit"),
                                                ]
                                            ),
                                        ],
                                    ),
                                    dbc.Button(
                                        [
                                            "Performance in detail ",
                                            html.I(className="bi bi-arrow-down"),
                                        ],
                                        color="link",
                                        className="mt-5",
                                    ),
                                ]
                            ),
                        ],
                        className="h-100 p-3 p-md-5 bg-light",
                    ),
                    width=12,
                ),
            ],
            className="full-xs",
        )
    ],
)

watch_list_header = html.Div(
    className="d-flex justify-content-between align-items-center mt-4 mt-md-6 mb-4",
    children=[
        html.H2(f"{len(display_df)} watches owned", className="h4 m-0"),
        html.Div(
            className="d-flex align-items-center",
            children=[
                html.Label("Sort by", className="mr-3 my-0 flex-shrink-0", htmlFor="sortWatchCollectionItems"),
                dcc.Dropdown(
                    id="sortWatchCollectionItems",
                    options=[
                        {"label": "Date added (newest first)", "value": "CreationDateDesc"},
                        {"label": "Date purchased (newest first)", "value": "PurchaseDateDesc"},
                        {"label": "Estimated value (high to low)", "value": "ValueDesc"},
                        {"label": "Profit (high to low)", "value": "ValueDeltaDesc"},
                        {"label": "Alphabetical (A-Z)", "value": "AlphaNumericAsc"},
                    ],
                    value="CreationDateDesc",
                    clearable=False,
                    className="wt-overview-sort-select",
                ),
            ],
        ),
    ],
)

# Generate watch cards
watch_cards = []
for _, row in display_df.iterrows():
    card = html.A(
        href=f"/view-item/{row['reference']}",
        className="text-decoration-none",
        children=dbc.Card(
            className="rcard border-radius-large l-1 d-flex overflow-hidden wt-overview-list-item mb-3",
            children=[
                html.Div(
                    className="overview-list-item-image img-circle overflow-hidden relative",
                    children=html.Img(src=row["image"], alt="watch image", className="img-fluid"),
                ),
                html.Div(
                    className="mx-3 d-flex flex-column justify-content-center flex-grow-1",
                    children=[
                        html.Div(
                            className="pb-1",
                            children=dbc.Badge(
                                [html.I(className="bi bi-fire me-1"), "Very popular"],
                                color="warning",
                                className="watch-collection-hot-watch-badge border-radius-small",
                            )
                            if row["is_popular"]
                            else None,
                        ),
                        html.Div(
                            className="d-flex align-items-start mb-1",
                            children=html.P(row["name"], className="mb-0"),
                        ),
                        html.Div(
                            className="d-flex justify-content-between",
                            children=[
                                html.P(f"£ {row['sold_price']:,.2f}", className="h4 my-0"),
                                dbc.Badge(
                                    f"+{row['profit_percentage']}%",
                                    color="success",
                                    className="pill text-weight-normal border-radius-medium text-sm",
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    )
    watch_cards.append(card)

# Add the "Add a watch" card
add_watch_card = html.A(
    href="/add-item?watchCollectionItemOrigin=WatchCollection",
    className="text-decoration-none",
    children=dbc.Card(
        className="rcard border-radius-large l-1 d-flex overflow-hidden",
        children=[
            html.Div(
                className="overview-list-item-image img-circle overflow-hidden relative",
                children=html.Div(
                    className="bi bi-plus add-watch-icon",
                    style={"fontSize": "2rem", "textAlign": "center", "padding": "1rem"},
                ),
            ),
            html.Div(
                className="mx-3 d-flex flex-column justify-content-center flex-grow-1",
                children=html.P("Add a watch"),
            ),
        ],
    ),
)
watch_cards.append(add_watch_card)

layout = html.Div(
    [
        header,
        tabs,
        overview_section,
        watch_list_header,
        html.Div(watch_cards, className="scroll-reload-list overview-list mt-3"),
    ]
)
