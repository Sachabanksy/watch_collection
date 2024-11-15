# app.py
import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

# ok so this could be a good start

# Initialize the Dash app with a Bootstrap theme
app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP, 'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.5.0/font/bootstrap-icons.css'],
    suppress_callback_exceptions=True
)

server = app.server

# Define the app layout
app.layout = dbc.Container(
    fluid=True,
    children=[
        # Navigation Bar
        dbc.NavbarSimple(
            brand="Watch Auction Explorer",
            brand_href="/",
            color="dark",
            dark=True,
            children=[
                dbc.NavItem(dbc.NavLink("Watch Collection", href="/watch_collection")),
                dbc.NavItem(dbc.NavLink("Test", href="/watch_collection1")),
                #dbc.NavItem(dbc.NavLink("Trends & Analysis", href="/trends-analysis")),
                #dbc.NavItem(dbc.NavLink("Test Page", href="/test-page")),
            ],
        ),
        # Main Content
        dbc.Container(
            id="page-content",
            className="mt-4",
            children=dash.page_container,
        ),
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True)
