import dash
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from utils.fakedata import generate_watch_data

dash.register_page(__name__, path="/")

# Load the data (Replace 'your_data.csv' with your actual data file)
df = generate_watch_data(1000)

def filter_data(df, selected_brands, selected_years, selected_auction_houses, box_papers):
    dff = df.copy()
    if selected_brands:
        dff = dff[dff['brand'].isin(selected_brands)]
    if selected_years:
        dff = dff[(dff['year'] >= selected_years[0]) & (dff['year'] <= selected_years[1])]
    if selected_auction_houses:
        dff = dff[dff['auction_house'].isin(selected_auction_houses)]
    if 'has_box' in box_papers:
        dff = dff[dff['has_box'] == True]
    if 'has_papers' in box_papers:
        dff = dff[dff['has_papers'] == True]
    return dff

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            # Sidebar with filters
            html.H5("Filters"),
            html.Div([
                dbc.Label("Brand"),
                dcc.Dropdown(
                    id='brand-filter',
                    options=[{'label': brand, 'value': brand} for brand in sorted(df['brand'].unique())],
                    multi=True
                ),
            ], className='mb-3'),
            html.Div([
                dbc.Label("Year"),
                dcc.RangeSlider(
                    id='year-filter',
                    min=df['year'].min(),
                    max=df['year'].max(),
                    step=1,
                    value=[df['year'].min(), df['year'].max()],
                    marks={str(year): str(year) for year in range(df['year'].min(), df['year'].max()+1, 5)}
                ),
            ], className='mb-3'),
            html.Div([
                dbc.Label("Auction House"),
                dcc.Dropdown(
                    id='auction-house-filter',
                    options=[{'label': house, 'value': house} for house in sorted(df['auction_house'].unique())],
                    multi=True
                ),
            ], className='mb-3'),
            html.Div([
                dbc.Label("Box and Papers"),
                dbc.Checklist(
                    options=[
                        {'label': 'Has Box', 'value': 'has_box'},
                        {'label': 'Has Papers', 'value': 'has_papers'}
                    ],
                    value=[],
                    id='box-papers-filter',
                    inline=True
                ),
            ], className='mb-3'),
        ], width=3),
        dbc.Col([
            # First row: KPIs
            dbc.Row([
                dbc.Col(dbc.Card(
                    dbc.CardBody([
                        html.H5("Total Watches Sold", className="card-title"),
                        html.H2(id='total-watches', className="card-text")
                    ])
                ), width=3),
                dbc.Col(dbc.Card(
                    dbc.CardBody([
                        html.H5("Total Sales", className="card-title"),
                        html.H2(id='total-sales', className="card-text")
                    ])
                ), width=3),
                dbc.Col(dbc.Card(
                    dbc.CardBody([
                        html.H5("Average Price", className="card-title"),
                        html.H2(id='average-price', className="card-text")
                    ])
                ), width=3),
                dbc.Col(dbc.Card(
                    dbc.CardBody([
                        html.H5("Top Brand", className="card-title"),
                        html.H2(id='top-brand', className="card-text")
                    ])
                ), width=3),
            ]),
            html.Br(),
            # Second row: Charts
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='brand-distribution-chart')
                ], width=6),
                dbc.Col([
                    dcc.Graph(id='average-price-over-time-chart')
                ], width=6),
            ]),
            html.Br(),
            # Top Sales Carousel
            html.H3("Top Sales"),
            dbc.Carousel(
                items=[],
                id='top-sales-carousel',
                controls=True,
                indicators=True,
                interval=5000,
                ride="carousel"
            ),
        ], width=9)
    ])
])

@callback(
    Output('total-watches', 'children'),
    Output('total-sales', 'children'),
    Output('average-price', 'children'),
    Output('top-brand', 'children'),
    Input('brand-filter', 'value'),
    Input('year-filter', 'value'),
    Input('auction-house-filter', 'value'),
    Input('box-papers-filter', 'value')
)
def update_kpis(selected_brands, selected_years, selected_auction_houses, box_papers):
    dff = filter_data(df, selected_brands, selected_years, selected_auction_houses, box_papers)
    total_watches = len(dff)
    total_sales = dff['sold_price'].sum()
    average_price = dff['sold_price'].mean()
    top_brand = dff['brand'].value_counts().idxmax() if not dff.empty else 'N/A'

    return (
        f"{total_watches:,}",
        f"${total_sales:,.2f}",
        f"${average_price:,.2f}",
        top_brand
    )

@callback(
    Output('brand-distribution-chart', 'figure'),
    Input('brand-filter', 'value'),
    Input('year-filter', 'value'),
    Input('auction-house-filter', 'value'),
    Input('box-papers-filter', 'value')
)
def update_brand_distribution_chart(selected_brands, selected_years, selected_auction_houses, box_papers):
    dff = filter_data(df, selected_brands, selected_years, selected_auction_houses, box_papers)
    fig = px.pie(
        dff,
        names='brand',
        title='Distribution of Watch Brands Sold'
    )
    return fig

@callback(
    Output('average-price-over-time-chart', 'figure'),
    Input('brand-filter', 'value'),
    Input('year-filter', 'value'),
    Input('auction-house-filter', 'value'),
    Input('box-papers-filter', 'value')
)
def update_average_price_over_time_chart(selected_brands, selected_years, selected_auction_houses, box_papers):
    dff = filter_data(df, selected_brands, selected_years, selected_auction_houses, box_papers)
    dff['auction_date'] = pd.to_datetime(dff['auction_date'])
    dff = dff.sort_values('auction_date')
    avg_price_over_time = dff.groupby(dff['auction_date'].dt.to_period('M'))['sold_price'].mean().reset_index()
    avg_price_over_time['auction_date'] = avg_price_over_time['auction_date'].dt.to_timestamp()

    fig = px.line(
        avg_price_over_time,
        x='auction_date',
        y='sold_price',
        title='Average Price Over Time'
    )
    fig.update_layout(xaxis_title='Date', yaxis_title='Average Sold Price')
    return fig

@callback(
    Output('top-sales-carousel', 'items'),
    Input('brand-filter', 'value'),
    Input('year-filter', 'value'),
    Input('auction-house-filter', 'value'),
    Input('box-papers-filter', 'value')
)
def update_top_sales_carousel(selected_brands, selected_years, selected_auction_houses, box_papers):
    dff = filter_data(df, selected_brands, selected_years, selected_auction_houses, box_papers)
    top_sales = dff.sort_values(by='sold_price', ascending=False).head(5)
    items = []
    for index, row in top_sales.iterrows():
        item = {
            'key': str(index),
            'src': row['image'],
            'header': f"{row['brand']} {row['collection']}",
            'caption': f"Sold Price: ${row['sold_price']:,.2f}"
        }
        items.append(item)
    return items
