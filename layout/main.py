import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

logo_image = '/assets/img/cpzones.svg'

nav_links = dbc.Row(
    children=[],
    id='nav-items',
    no_gutters=True,
    className="ml-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

navbar = dbc.Navbar(
    children=[
        html.A(
            dbc.Row(
                [
                    dbc.Col(html.Img(src=logo_image, height="34px", className='ml-2')),
                ],
                align="center",
                no_gutters=True,
            ),
            href="/",
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
        dbc.Collapse(nav_links, id="navbar-collapse", navbar=True),
    ],
    color="dark",
    dark=True,
)

main_layout = html.Div(
    children=[
        dcc.Location(
            id='url',
            refresh=False
        ),
        navbar,
        dbc.Container(
            children=[],
            id='page_content',
            className="mt-4",
        )
    ]
)