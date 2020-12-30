import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from dash_table.Format import Format

analysis_layout = [
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and drop or ',
            html.A('select .fit file')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=False
    ),
    dbc.Row(
        dbc.Col(
            children=[
                dcc.Loading(id="loading_power_data")
            ],
            md=12
        ),
    ),
    dbc.Row(
        dbc.Col(
            id='selected_data_histogram',
            md=12
        )
    ),
    dbc.Collapse(
        id='selected_data_table_container',
        children=[
            dbc.Row(
                dbc.Col(
                    dash_table.DataTable(
                        id='selected_data_table',
                        columns=[
                            {'id': 'duration_seconds', 'name': 'duration (s)', 'type': 'numeric',
                             'format': Format(precision=3)},
                            {'id': 'average_speed', 'name': 'average speed (m/s)', 'type': 'numeric',
                             'format': Format(precision=3)},
                            {'id': 'average_power', 'name': 'average power (watts)', 'type': 'numeric',
                             'format': Format(precision=4)},
                        ],
                        data=[],
                        style_header={'fontWeight': 'bold'},
                        sort_action='native',
                        editable=True,
                        row_deletable=True
                    ),
                    md=12
                ),
                className='mt-3 mb-3'
            ),
            dbc.Row(
                children=[
                    dbc.Col(id="analysis_message_number", md=6),
                    dbc.Col(id="analysis_message_monotonic", md=6)
                ]
            ),
            dbc.Row(
                children=[
                    dbc.Col(md=6),
                    dbc.Col(
                        dbc.Button("Calculate power zones", id="analysis_btn", color="light", size="lg",
                                   block=True, disabled=True),
                        md=12
                    )
                ],
                className='mb-3'
            ),
        ],
    ),
    dbc.Collapse(
        id='analysis_results_container',
        children=[
            dbc.Row(
                children=[
                    dbc.Col(
                        children=[
                            dbc.Toast(
                                [html.H1(id='cp_value')],
                                header="Critical Power (watts)",
                                style={'max-width': '100%'}
                            )
                        ],
                        md=6),
                    dbc.Col(
                        children=[
                            dbc.Toast(
                                [html.H1(id='wprime_value')],
                                header="W' (joules)",
                                style={'max-width': '100%'}
                            )
                        ],
                        md=6)
                ]
            ),
            dbc.Row(
                children=[
                    dbc.Col(
                        id='analysis_output',
                        md=12
                    ),
                ],
                className='mt-3 mb-3'
            )
        ]
    )
]
