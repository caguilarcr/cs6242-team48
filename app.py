import numpy as np
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html

DEFAULT_DATA_FILENAME = 'data.csv'
STYLESHEETS = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# region Line Chart


def load_data_frame(path=DEFAULT_DATA_FILENAME):
    df = pd.read_csv(path)
    df.columns = ['Country', 'Code', 'Date', 'Confirmed', 'Days since confirmed']
    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
    return df


def store_data_frame(df, path=DEFAULT_DATA_FILENAME):
    df.to_csv(path, index=False)


def create_classes(df, class_list):
    return [df[df['Country'].isin([c])] for c in class_list]


def create_traces(lines=[]):
    return [
        go.Scatter(
            x=l['Date'][:2],
            y=l['Confirmed'][:2],
            mode='lines',
            line=dict(width=1.5),
            name=str(l.iloc[0]['Country'])
        ) for l in lines
    ]


def create_frames(lines=[], num_traces=0, num_data_points=0):
    trace_list = list(range(num_traces))
    return [
        dict(
            data=[
                dict(
                    type='scatter',
                    x=line['Date'][:k+1],
                    y=line['Confirmed'][:k+1])
                for line in lines
            ],
            traces=trace_list,
        ) for k in range(1, num_data_points - 1)
    ]


def create_layout():
    layout = go.Layout(
        # width=700,
        # height=600,
        showlegend=True,
        hovermode='x unified',
        updatemenus=[dict(
            type='buttons',
            showactive=False,
            y=1.05,
            x=1.15,
            xanchor='right',
            yanchor='bottom',
            pad=dict(t=0, r=10),
            buttons=[dict(
                label='Play',
                method='animate',
                args=[
                    None,
                    dict(
                        frame=dict(duration=3, redraw=False),
                        transition=dict(duration=0),
                        fromcurrent=True,
                        mode='immediate'
                    )
                ]
            )]
        )]
    )

    layout.update(
        xaxis=dict(range=['2020-03-16', '2020-06-13'], autorange=False),
        yaxis=dict(range=[0, 35000], autorange=False)
    )
    return layout


def create_figure(path=DEFAULT_DATA_FILENAME):
    df = load_data_frame(path)
    class_list = ['United States', 'Russia', 'India', 'Brazil']
    classes = create_classes(df, class_list)
    traces = create_traces(classes)
    frames = create_frames(
        classes,
        num_traces=len(traces),
        num_data_points=classes[0].shape[0]
    )
    layout = create_layout()
    return go.Figure(data=traces, frames=frames, layout=layout)

#endregion

# region Dash App


app = dash.Dash(__name__, external_stylesheets=STYLESHEETS)

server = app.server


def create_app(line_chart_fig):
    app.layout = html.Div([
        html.H1(
            children='2020 US Presidencial Race Stance Analysis (DEMO)',
            style={'textAlign': 'center'}
        ),
        dcc.Graph(id='LineChart', figure=line_chart_fig)
    ])
    return app

# endregion


if __name__ == '__main__':
    # store_data_frame(load_data_frame('https://raw.githubusercontent.com/shinokada/covid-19-stats/master/data/daily-new-confirmed-cases-of-covid-19-tests-per-case.csv'))
    fig = create_figure()
    app = create_app(fig)
    app.run_server(debug=True)
