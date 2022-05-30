
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd, numpy as np
import matplotlib.pyplot as plt, seaborn as sns
import pathlib

from functions import *


''' PATH ----------------------------------------------------------------- '''

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("./data").resolve()


''' APP ------------------------------------------------------------------ '''

app = Dash(__name__, suppress_callback_exceptions=True,
                assets_ignore='.*chiddyp.*',
                external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
                )

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True


''' MAIN APP ------------------------------------------------------------- '''

def main():
    """
    - Radio button switch between county and school district
    """

    app.layout = html.Div(className='layout', children=[
    # ------------------------------------------------------------------------
    html.Div(className='header', children=[
        html.Div(className='title', children=[
            dcc.Markdown("# Colorado Crime and Education"),
        ],
        ),
        html.Div(className='main-controls-box', children=[
            html.Div(className='main-controls', children=[
                html.Div(className='choices', children=[
                    html.Div(className='var-choices', children=[
                        dcc.Dropdown(className='var-choices-dropdown',
                            options=VARS_ALL,
                            value=BY_1_ALL,
                            id='var-choices-dropdown',
                            clearable=False,
                            optionHeight=25,
                        ),
                    ],
                    ),
                    html.Div(className='year-choices', children=[
                        dcc.Dropdown(className='year-choices-dropdown',
                            options=YEARS_ALL,
                            value= YEAR_ALL,
                            id='year-choices-dropdown',
                            clearable=False,
                            optionHeight=25,
                        ),
                    ],
                    ),
                ],
                ),
                html.Div(className='agg-choices', children=[
                    dcc.RadioItems(className='agg-choices-radio',
                        options=AGG_CHOICES,
                        value=AGG,
                        id='agg-choices-radio',
                        labelStyle={'marginLeft':'15px', 'marginRight':'15px', 'marginBottom':'5px'},
                        inputStyle={'marginRight': '7px'},
                    ),
                ],
                ),
            ],
            ),
        ],
        ),
        html.Div(className='hide-header', children=[
            dbc.Button(className='me-1 hide-header-btn', children=[
                html.I(className='bi bi-chevron-up fa-2x', style={'marginRight':'7px'}),
                'Hide Options',
            ],
            color='light',
            id='hide-header-btn'
            ),
        ],
        ),
    ],
    ),
    html.Div(className='show-header', children=[
        dbc.Button(className='me-1 show-header-btn', children=[
            html.I(className='bi bi-chevron-down fa-2x', style={'marginRight':'7px'}),
            'Show Options',
        ],
        color='primary',
        id='show-header-btn'
        ),
    ],
    ),
    # html.Div(className='separator', children=[
    #     dbc.Button(className='me-1 separator-btn', children=[
    #         html.I(className="bi bi-chevron-up fa-2x", style={'marginRight':'7px'}),
    #         'Back to top',
    #     ],
    #     color='primary',
    #     id='separator-btn', 
    #     ),
    # ],
    # ),
    html.Div(className='map-box', children=[
        html.Iframe(className='map',
            id='map',
            srcDoc=None,
        ),
    ],
    )
    # ------------------------------------------------------------------------
    ])

    @app.callback(
        [
            Output('var-choices-dropdown', 'options'),
            Output('var-choices-dropdown', 'value'),
            Output('year-choices-dropdown', 'options'),
            Output('year-choices-dropdown', 'value'),
            Output('year-choices-dropdown', 'disabled'),
            Output('year-choices-dropdown', 'style'),
        ],
        Input('agg-choices-radio', 'value'),
    )
    def agg_change(agg):
        global CUR_AGG
        CUR_AGG = agg
        if agg == 'County':
            return (VARS_ALL, BY_1_ALL, YEARS_ALL, YEAR_ALL, False, {'background-color': 'white'})

        return (VARS_EDU, BY_1_EDU, YEARS_EDU, YEAR_EDU, True, {'background-color': '#e6e6e6'})
    

    @app.callback(
        Output('map', 'srcDoc'),
        [
            Input('agg-choices-radio', 'value'),
            Input('year-choices-dropdown', 'value'),
            Input('var-choices-dropdown', 'value'),
        ],
    )
    def var_change(agg, year, by_1):
        return update(agg, year, by_1)



''' DATA ----------------------------------------------------------------- '''

df_all = pd.read_csv(DATA_PATH.joinpath('everything_grouped_ready.csv'))
df_edu_dist = pd.read_csv(DATA_PATH.joinpath('education_dist_ready.csv'))
df_edu_dist = df_edu_dist[df_edu_dist.pupil_total > 150]

INDEX_ALL = ['year', 'county', 'geo_county_point', 'geo_county']
INDEX_EDU = ['county', 'dist', 'geo_county_point', 'geo_dist_point', 'geo_county', 'geo_dist']
VARS_ALL = [c for c in df_all.columns if c not in INDEX_ALL]
VARS_EDU = [c for c in df_edu_dist.columns if c not in INDEX_EDU]

YEARS_ALL = [str(y) for y in df_all.year.unique()]
YEARS_EDU = ['2012']

AGG_CHOICES = ['County', 'School District']
AGG = 'County'

BY_1_ALL = 'pop'
BY_1_EDU = 'mobile_rate'
BY_2_ALL = 'cr_rate'
BY_2_EDU = 'poor_graduated'
YEAR_ALL = '2019'
YEAR_EDU = '2012'

CUR_AGG = AGG

# agg_selection = 'County'
# var_selection = 'cr_rate'
# var_choices = VARS_ALL

# for c in df_edu_dist.columns:
    # print(c)

''' LOGIC ---------------------------------------------------------------- '''

def update(agg, year, by_1, by_2=None):
    year = int(year)

    if not by_2:
        if agg == 'County':
            by_2 = BY_2_ALL
        else:
            by_2 = BY_2_EDU

    m = plot(agg, df_all, df_edu_dist, year, by_1, by_2,
            point_scale=15,
            show_alt=False,
            show_alt_marks=False,
            reverse_cmap=True
            )
    m.save(DATA_PATH.joinpath('map.html'))

    return open(DATA_PATH.joinpath('map.html'), 'r').read()





''' 
------------------------------------------------------------------------------
RUN SERVER -------------------------------------------------------------------
------------------------------------------------------------------------------
'''

server = app.server

if __name__ == '__main__':
    main()
    app.run_server(debug=True)
else:
    main()

















            # dbc.DropdownMenu(
            #     children= [dbc.DropdownMenuItem(v) for v in VARS_ALL if v != var_selection],
            #     label=var_selection,
            #     id='var-choices-dropdown',
            # ),