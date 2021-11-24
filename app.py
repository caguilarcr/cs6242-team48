"""
@TODO:
1. Create word cloud
2. Add annotations
3. Show word cloud when annotation is clicked
4. Deploy
5. Import Correct Data
6. Styling
    6.1 Change color of republican line to red
    6.2 If I have time, adding a slider
"""
import pandas as pd
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html


STYLESHEETS = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
X_COL = 'Date'

# DEFAULT_DATA_FILENAME = 'data.csv'
# CLASS_COL = 'Country'
# Y_COL = 'Confirmed'
# CLASS_LIST = ['United States', 'Brazil', 'India', 'Russia']

DEFAULT_DATA_FILENAME = 'data_project.csv'
CLASS_COL = 'PartyName'
Y_COL = 'Score'
CLASS_LIST = ['Democrats', 'Republicans']

# region Line Chart


def load_data_frame(path=DEFAULT_DATA_FILENAME):
    df = pd.read_csv(path)

    # df.columns = ['Country', 'Code', 'Date', 'Confirmed', 'Days since confirmed']
    # df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
    # return df

    df[X_COL] = pd.to_datetime(df['Created-At']).dt.strftime('%Y-%m-%d')
    return df.loc[:, df.columns != 'Created-At']


def store_data_frame(df, path=DEFAULT_DATA_FILENAME):
    df.to_csv(path, index=False)


def create_classes(df, class_list):
    return [df[df[CLASS_COL].isin([c])] for c in class_list]


def create_traces(lines=[]):
    return [
        go.Scatter(
            x=line[X_COL][:2],
            y=line[Y_COL][:2],
            mode='lines+markers',
            line=dict(width=1.5),
            name=str(line.iloc[0][CLASS_COL])
        ) for line in lines
    ]


def create_frames(lines=[], num_traces=0, num_data_points=0):
    trace_list = list(range(num_traces))
    return [
        go.Frame(
            data=[
                go.Scatter(
                    # type='scatter',
                    x=line[X_COL][:k+1],
                    y=line[Y_COL][:k+1])
                for line in lines
            ],
            # traces=trace_list,
        ) for k in range(1, num_data_points - 1)
    ]


def create_layout():
    layout = go.Layout(
        # width=700,
        height=600,
        showlegend=True,
        hovermode='x unified',
        updatemenus=[dict(
            type='buttons',
            showactive=True,
            y=-0.1,
            x=0.1,
            xanchor='right',
            yanchor='top',
            direction='left',
            pad=dict(t=0, r=10),
            buttons=[
                dict(
                    label='Play',
                    method='animate',
                    args=[
                        None,
                        dict(
                            frame=dict(duration=100, redraw=False),
                            transition=dict(duration=0),
                            fromcurrent=True,
                            # mode='immediate'
                        )
                    ]
                ),
                dict(
                    label='Pause',
                    method='animate',
                    args=[
                        [None],
                        dict(
                            frame=dict(duration=0, redraw=False),
                            mode='immediate',
                            transition=dict(duration=0)
                        )
                    ]
                )
            ]
        )]
    )

    layout.update(
        xaxis=dict(range=['2020-07-03', '2020-11-13'], autorange=False),
        yaxis=dict(range=[-0.5, 0.5], autorange=False)
    )
    return layout


def create_figure(path=DEFAULT_DATA_FILENAME):
    df = load_data_frame(path)
    classes = create_classes(df, CLASS_LIST)
    traces = create_traces(classes)
    frames = create_frames(
        classes,
        num_traces=len(traces),
        num_data_points=classes[0].shape[0]
    )
    layout = create_layout()
    fig = go.Figure(data=traces, frames=frames, layout=layout)
    fig.add_layout_image(dict(
        source="https://images.plot.ly/language-icons/api-home/python-logo.png",
        xref="x",
        yref="y",
        x=0,
        y=3,
        sizex=2,
        sizey=2,
        sizing="stretch",
        opacity=0.5
    ))
    fig.update_layout(template="xgridoff")
    return fig

# endregion

# region Dash App


app = dash.Dash(__name__)

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
    # df = load_data_frame()
    # print(df.head())
