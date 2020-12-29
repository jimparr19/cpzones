import dash
import dash_bootstrap_components as dbc

# Style
THEME = dbc.themes.BOOTSTRAP

app = dash.Dash(__name__, external_stylesheets=[THEME])
app.title = 'Power Training Zones'
app.config.suppress_callback_exceptions = True