from main import app
from layout.main import main_layout

from callbacks import navigation  # noqa
from callbacks import analysis  # noqa

app.layout = main_layout
server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
