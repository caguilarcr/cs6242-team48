import pandas as pd
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


STYLESHEETS = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
X_COL = 'Date'


DEFAULT_DATA_FILENAME = './data/data.csv'
CLASS_COL = 'PartyName'
Y_COL = 'Score'
CLASS_LIST = ['Democrat', 'Republic']
ANNOTATIONS = {
    '2020-07-04': 'Independece Day',
    '2020-07-30': 'Twitter blocks Trump account',
    '2020-09-01': 'Black Live Matter conflicts',
    '2020-09-30': 'Committe investigate Trump fraud allegations',
    '2020-10-19': 'Fauci urged face mask mandate',
}

# region Line Chart


def load_data_frame(path=DEFAULT_DATA_FILENAME):
    df = pd.read_csv(path)
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
    annotation_keys = ANNOTATIONS.keys()
    trace_list = list(range(num_traces))
    frames = []
    annotations = []
    for k in range(1, num_data_points - 1):
        data = [
            go.Scatter(x=line[X_COL][:k+1], y=line[Y_COL][:k+1])
            for line in lines
        ]
        current_x = lines[0][X_COL][2*k]
        current_y = lines[0][Y_COL][2*k]
        current_y_rep = lines[1][Y_COL][2*k+1]
        if current_x in annotation_keys:
            annotations.append(
                go.layout.Annotation(
                    x=current_x,
                    y=current_y if current_y > 0 and current_x != '2020-09-30' else current_y_rep,
                    ax=10,
                    ay=-60 if current_x != '2020-09-30' else 60,
                    xref='x',
                    yref='y',
                    text=ANNOTATIONS[current_x],
                    showarrow=True,
                    arrowhead=7,
                )
            )
            layout = go.Layout(annotations=annotations)
            frames.append(go.Frame(name=f'Frame_{k}', data=data, traces=trace_list, layout=layout))
        else:
            frames.append(go.Frame(name=f'Frame_{k}', data=data, traces=trace_list))
    return frames


def create_layout():
    layout = go.Layout(
        # width=700,
        height=500,
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
                            frame=dict(duration=50, redraw=False),
                            transition=dict(duration=0),
                            fromcurrent=True,
                            mode='immediate'
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
        xaxis=dict(range=['2020-07-03', '2020-11-02'], autorange=False),
        yaxis=dict(range=[-4.5, 4.5], autorange=False)
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


styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    },
    'center': {
        'display': 'block',
        'marginLeft': 'auto',
        'marginRight': 'auto',
        'marginTop': '30px',
        'width': '80%'
    }
}


def create_app(line_chart_fig):
    app.layout = html.Div([
        html.H1(
            children='2020 US Presidencial Race Stance Analysis (DEMO)',
            style={'textAlign': 'center'}
        ),
        dcc.Graph(id='LineChart', figure=line_chart_fig, config={'displayModeBar': False}),
        html.Img(
            id='wordcloud',
            src='',
            style=styles['center']
        )
    ])
    return app


app = dash.Dash(__name__, external_stylesheets=STYLESHEETS, assets_folder='assets')
app.config.suppress_callback_exceptions = True
fig = create_figure()
create_app(fig)
server = app.server


@app.callback(
    Output('wordcloud', 'src'),
    Input('LineChart', 'clickData'))
def display_click_data(clickData):
    if clickData:
        date = clickData['points'][0]['x']
        # return f'https://storage.googleapis.com/cs6242_project/twitter/{date}.png'
        return app.get_asset_url(f'twitter/{date}.png')
    return ''

# endregion


if __name__ == '__main__':
    # fig = create_figure()
    # create_app(fig)
    app.run_server(host='0.0.0.0', port=8080, debug=True)
    # app.run_server(debug=True)
