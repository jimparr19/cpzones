import dash
import dash_bootstrap_components as dbc

# Style
THEME = dbc.themes.BOOTSTRAP

app = dash.Dash(__name__, external_stylesheets=[THEME], external_scripts=[
    'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML',
])
app.title = 'Power Training Zones'
app.config.suppress_callback_exceptions = True
