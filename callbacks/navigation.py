import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output, State

from layout.about import about_layout
from layout.analysis import analysis_layout

from app import app

# update page based on url
@app.callback(
    Output('page_content', 'children'),
    [Input('url', 'pathname')])
def display_page(pathname):  # noqa
    if pathname == '/':
        return analysis_layout
    elif pathname == '/about':
        return about_layout
    else:
        return []


# update navbar items based on page
@app.callback(
    Output('nav-items', 'children'),
    [Input('url', 'pathname')])
def change_navbar(pathname):  # noqa
    if pathname == '/':
        navbar_items = [
            dbc.Col(dbc.NavLink("Home", id='home-link', href="/", className='nav_link active')),
            dbc.Col(dbc.NavLink("About", id='about-link', href="about", className='nav_link'))
        ]
    elif pathname == '/about':
        navbar_items = [
            dbc.Col(dbc.NavLink("Home", id='home-link', href="/", className='nav_link')),
            dbc.Col(dbc.NavLink("About", id='about-link', href="about", className='nav_link active'))
        ]
    else:
        navbar_items = []
    return navbar_items


# add callback for toggling the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open
