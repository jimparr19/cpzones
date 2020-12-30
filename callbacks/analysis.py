import io
import base64

import numpy as np
import pandas as pd
import dash_table

import dash_core_components as dcc
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output, State

from app import app
from plots.analysis import analysis_data_plot, analysis_plot_config, analysis_data_histogram_plot

from fitparse import FitFile
from collections import namedtuple

from dash_table.Format import Format

FitData = namedtuple('FitData', ['time', 'distance', 'speed', 'power', 'elevation', 'latitude', 'longitude'])


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'fit' in filename.split('.')[1]:
            fit_file = FitFile(io.BytesIO(decoded))
            time = []
            distance = []
            speed = []
            power = []
            elevation = []
            latitude = []
            longitude = []
            for record in fit_file.get_messages('record'):
                values = record.get_values()
                time.append(values.get('timestamp', None))
                distance.append(values.get('distance', None))
                speed.append(values.get('enhanced_speed', None))
                elevation.append(values.get('enhanced_altitude', None))
                latitude.append(values.get('position_lat', None))
                longitude.append(values.get('position_long', None))
                power.append(values.get('power', None))

            latitude_degrees = [i * (180 / 2 ** 31) if i is not None else None for i in latitude]
            longitude_degrees = [i * (180 / 2 ** 31) if i is not None else None for i in longitude]
            data = FitData(time=time, distance=distance, speed=speed, power=power, elevation=elevation,
                           latitude=latitude_degrees, longitude=longitude_degrees)
        else:
            return None
    except Exception as e:
        print(e)
        return None
    return data


@app.callback(
    Output('loading_power_data', 'children'),
    [
        Input('upload-data', 'contents')
    ],
    [
        State('upload-data', 'filename')
    ])
def update_output_regression(file_contents, file_name):
    error_message = dbc.Alert("There was an error processing this file.", color="danger")
    if file_contents is not None:
        data = parse_contents(file_contents, file_name)
        if data:
            figure = analysis_data_plot(analysis_data=data)
            plot_object = dcc.Graph(figure=figure, config=analysis_plot_config, id='plot_analysis_data')
            return plot_object
        else:
            return error_message
    else:
        return None


@app.callback(
    [
        Output('selected_data_table', 'data'),
        Output('analysis_btn', 'disabled'),
        Output('selected_data_histogram', 'children'),
        Output('selected_data_table_container', 'is_open'),
        Output('analysis_message_number', 'children'),
        Output('analysis_message_monotonic', 'children')
    ],
    [
        Input('plot_analysis_data', 'selectedData')
    ],
    [
        State('plot_analysis_data', 'figure'),
        State('selected_data_table', 'data'),
    ])
def display_selected_data(selected_data, figure, rows):
    histogram = None
    data_is_monotonic = False

    if selected_data and figure:
        index = [point['pointIndex'] for point in selected_data['points']]

        if index:
            time = [value for i, value in enumerate(figure['data'][0]['x']) if i in index]
            speed = [value for i, value in enumerate(figure['data'][1]['y']) if i in index]
            power = [value for i, value in enumerate(figure['data'][2]['y']) if i in index]

            interval = (pd.to_datetime(time).max() - pd.to_datetime(time).min()).total_seconds()
            mean_speed = np.mean(speed)
            mean_power = np.mean(power)

            row = {'duration_seconds': interval,
                   'average_speed': mean_speed,
                   'average_power': mean_power}
            rows.append(row)

            figure = analysis_data_histogram_plot(speed, power)
            histogram = dcc.Graph(figure=figure, id='histogram_plot', config={'displayModeBar': False})

            data_is_monotonic = pd.DataFrame(rows).sort_values(by='duration_seconds')[
                'average_power'].is_monotonic_decreasing

    number_message = None if len(rows) > 2 else dbc.Alert("Select a minimum of 3 intervals.", color="warning")
    monotonic_message = None if data_is_monotonic else dbc.Alert("Power must decrease with increasing duration.",
                                                                 color="warning")
    disabled_btn = False if len(rows) > 2 and data_is_monotonic else True
    open_container = True if rows else False

    return rows, disabled_btn, histogram, open_container, number_message, monotonic_message


def create_power_zones(data):
    data_df = pd.DataFrame(data)
    coef = np.polyfit(data_df.duration_seconds, data_df.duration_seconds * data_df.average_power, 1)
    cp = coef[0]
    wprime = coef[1]
    power_zones_df = pd.DataFrame({
        'zone': ['Z1', 'Z2', 'Z3', 'Z4', 'Z5'],
        'lower power': [cp * x for x in [0.65, 0.80, 0.9, 1, 1.15]],
        'upper power': [cp * x for x in [0.80, 0.9, 1, 1.15, 3]],
        'description': ['Easy', 'Moderate', 'Threshold', 'Interval', 'Repetition']
    })
    return power_zones_df, cp, wprime


@app.callback(
    [
        Output('analysis_output', 'children'),
        Output("analysis_results_container", "is_open"),
        Output("cp_value", "children"),
        Output("wprime_value", "children")
    ],
    [
        Input('analysis_btn', 'n_clicks')
    ],
    [
        State("selected_data_table", "data")
    ])
def display_analysis_output(n_clicks, data):
    if n_clicks:
        power_zones_df, cp, wprime = create_power_zones(data)
        analysis_output = dash_table.DataTable(
            id='power_zones_table',
            columns=[
                {'id': 'zone', 'name': 'zone'},
                {'id': 'lower power', 'name': 'lower power (watts)', 'type': 'numeric',
                 'format': Format(precision=3)},
                {'id': 'upper power', 'name': 'upper power (watts)', 'type': 'numeric',
                 'format': Format(precision=3)},
                {'id': 'description', 'name': 'description'},
            ],
            data=power_zones_df.to_dict('records'),
            style_header={'fontWeight': 'bold'},
        )
        return analysis_output, True, np.round(cp), np.round(wprime)
    else:
        return None, False, None, None
