import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px

analysis_plot_config = {
    'modeBarButtonsToRemove': ['lasso2d', 'autoScale2d', 'toggleSpikelines', 'hoverClosestCartesian',
                               'hoverCompareCartesian'],
    'displaylogo': False,
    'displayModeBar': True}

colors = px.colors.qualitative.Plotly
power_color = colors[0]
speed_color = colors[1]
elevation_color = '#D3D3D3'
analysis_color = 'black'


def analysis_data_plot(analysis_data):
    n_rows = 3
    row_heights = [1 / n_rows] * n_rows

    figure = make_subplots(rows=n_rows, cols=1,
                           shared_xaxes=True,
                           vertical_spacing=0.02,
                           row_heights=row_heights)

    figure.add_trace(
        go.Scatter(x=analysis_data.time,
                   y=analysis_data.elevation,
                   fill='tozeroy',
                   name='elevation',
                   mode="lines+markers",
                   line=dict(color=elevation_color),
                   marker=dict(size=1)), row=1, col=1)

    figure.add_trace(
        go.Scatter(x=analysis_data.time,
                   y=analysis_data.speed,
                   name='speed',
                   mode="lines+markers",
                   line=dict(color=speed_color),
                   marker=dict(size=1)), row=2, col=1)

    figure.add_trace(
        go.Scatter(x=analysis_data.time,
                   y=analysis_data.power,
                   name='power',
                   mode="lines+markers",
                   line=dict(color=power_color),
                   marker=dict(size=1)), row=3, col=1)

    figure.update_yaxes(title_text="elevation (m)", row=1, col=1)
    figure.update_yaxes(title_text="speed (km/h)", row=2, col=1)
    figure.update_xaxes(title_text="time", row=n_rows, col=1)
    figure.update_yaxes(title_text="power (watts)", row=3, col=1)
    figure.update_layout(height=600, template="plotly_white", showlegend=False)

    return figure


def analysis_data_histogram_plot(speed, power):
    figure = make_subplots(rows=1, cols=2, subplot_titles=("Average speed = {:2.1f} km/h".format(np.mean(speed)),
                                                           "Average power = {:4.1f} watts".format(np.mean(power)))
                           )
    figure.add_trace(
        go.Histogram(x=speed, name='speed', marker_color=speed_color), row=1, col=1)
    figure.add_trace(
        go.Histogram(x=power, name='power', marker_color=power_color), row=1, col=2)

    figure.update_xaxes(title_text="speed (km/h)", row=1, col=1)
    figure.update_xaxes(title_text="power (watts)", row=1, col=2)
    figure.update_layout(height=350, bargap=0.1, margin=dict(t=20), template="plotly_white", showlegend=False)
    return figure


def analysis_regression_plot(selected_data, cp, wprime):
    selected_data_df = pd.DataFrame(selected_data)
    figure = make_subplots(rows=1, cols=2)

    max_duration = 3600

    work_done_duration = np.linspace(0, selected_data_df.duration_seconds.max()+100, 100)
    work_done = work_done_duration * cp + wprime

    power_duration = np.linspace(selected_data_df.duration_seconds.min(), max_duration, 1000)
    power = wprime/power_duration + cp

    figure.add_trace(
        go.Scatter(x=selected_data_df.duration_seconds,
                   y=selected_data_df.total_energy/selected_data_df.duration_seconds,
                   name='duration versus corrected power',
                   mode="markers",
                   line=dict(color=analysis_color)
                   ),
        row=1, col=1
    )
    figure.add_trace(
        go.Scatter(x=power_duration,
                   y=power,
                   mode="lines",
                   line=dict(color=analysis_color)
                   ),
        row=1, col=1
    )

    figure.add_trace(
        go.Scatter(x=selected_data_df.duration_seconds,
                   y=selected_data_df.total_energy,
                   name='duration versus energy',
                   mode="markers",
                   line=dict(color=analysis_color)
                   ),
        row=1, col=2
    )
    figure.add_trace(
        go.Scatter(x=work_done_duration,
                   y=work_done,
                   mode="lines",
                   line=dict(color=analysis_color)
                   ),
        row=1, col=2
    )

    figure.update_xaxes(title_text="duration (s)", row=1, col=1)
    figure.update_yaxes(title_text="power (watts)", row=1, col=1)

    figure.update_xaxes(title_text="duration (s)", row=1, col=2)
    figure.update_yaxes(title_text="work done (joules)", row=1, col=2)
    figure.update_layout(height=350, bargap=0.1, margin=dict(t=20), template="plotly_white", showlegend=False)
    return figure
