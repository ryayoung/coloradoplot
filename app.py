
# import plotly.express as px
# import plotly.graph_objects as go
# import plotly.figure_factory as ff
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd, numpy as np
import matplotlib.pyplot as plt, seaborn as sns
import pathlib

from functions import *


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
                html.Div(className='agg-year', children=[
                    html.Div(className='radio-group agg-choices', children=[
                        html.Label('Group by', htmlFor='agg-choices-radio'),
                        dbc.RadioItems(className='btn-group agg-choices-radio',
                            inputClassName='btn-check',
                            labelClassName='btn btn-outline-primary',
                            labelCheckedClassName='active',
                            options=[{'label': v, 'value': v} for v in AGG_CHOICES],
                            value=AGG,
                            id='agg-choices-radio',
                        ),
                    ],
                    ),
                    html.Div(className='year', children=[
                        html.Label('Year', htmlFor='year-dropdown'),
                        dcc.Dropdown(className='year-dropdown',
                            options=YEARS_ALL,
                            value= YEAR_ALL,
                            id='year-dropdown',
                            clearable=False,
                            optionHeight=32,
                        ),
                    ],
                    ),
                ],
                ),
                html.Div(className='v-divider'
                ),
                html.Div(className='variables', children=[
                    html.Div(className='var-1', children=[
                        html.Label('Variable 1: Area color', htmlFor='var-1-dropdown'),
                        dcc.Dropdown(className='var-choices-dropdown',
                            options=VARS_ALL,
                            value=BY_1_ALL,
                            id='var-1-dropdown',
                            clearable=False,
                            optionHeight=25,
                        ),
                    ],
                    ),
                    html.Div(className='var-2', children=[
                        html.Label('Variable 2: Marker size', htmlFor='var-2-dropdown'),
                        dcc.Dropdown(className='var-choices-dropdown',
                            options=VARS_ALL,
                            value=BY_2_ALL,
                            id='var-2-dropdown',
                            clearable=False,
                            optionHeight=25,
                        ),
                    ],
                    ),
                ],
                ),
                html.Div(className='details', children=[
                    html.Div(className='details-1', children=[
                        html.Label('Tooltip #1: Extra Variables', htmlFor='details-1-dropdown'),
                        dcc.Dropdown(className='var-choices-dropdown',
                            options=VARS_ALL,
                            value=DETAILS_1_ALL,
                            id='details-1-dropdown',
                            clearable=True,
                            optionHeight=25,
                            multi=True,
                        ),
                    ],
                    ),
                    html.Div(className='details-2', children=[
                        html.Label('Tooltip #2: Extra Variables', htmlFor='details-2-dropdown'),
                        dcc.Dropdown(className='var-choices-dropdown',
                            options=VARS_ALL,
                            value=[],
                            id='details-2-dropdown',
                            clearable=True,
                            optionHeight=25,
                            multi=True,
                            disabled=True,
                        ),
                    ],
                    ),
                ],
                ),
                html.Div(className='v-divider'
                ),
                html.Div(className='switches', children=[
                    dbc.Checklist(className='switches-input',
                        options=SWITCH_OPT_ALL,
                        value=SWITCHES,
                        id="switches-input",
                        switch=True,
                    ),
                ],
                ),
                html.Div(className='mark-scale', children=[
                    html.Label('Marker Scale'),
                    dcc.Input(className='mark-scale-input',
                        type='number',
                        min=1,
                        max=40,
                        step=1,
                        value=MARK_SCALE,
                        id='mark-scale-input',
                    ),
                ],
                ),
            ],
            ),
        ],
        ),
        html.Div(className='hide-header', children=[
            dbc.Button(className='me-1 hide-header-btn', children=[
                # html.I(className='bi bi-chevron-up fa-2x', style={'marginRight':'7px', 'font-size':'1.3em'}),
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
            Output('var-1-dropdown', 'options'),
            Output('var-1-dropdown', 'value'),
            Output('var-2-dropdown', 'options'),
            Output('var-2-dropdown', 'value'),
            Output('year-dropdown', 'options'),
            Output('year-dropdown', 'value'),
            Output('year-dropdown', 'disabled'),
            Output('year-dropdown', 'style'),
            Output('switches-input', 'options'),
            Output('mark-scale-input', 'value'),
            Output('details-1-dropdown', 'value'),
        ],
        Input('agg-choices-radio', 'value'),
    )
    def agg_change(agg):
        global CUR_AGG
        CUR_AGG = agg
        if agg == 'County':
            return (VARS_ALL, BY_1_ALL, VARS_ALL, BY_2_ALL, YEARS_ALL, YEAR_ALL, False,
                    {'background-color': 'white'}, SWITCH_OPT_ALL, MARK_SCALE, DETAILS_1_ALL)

        return (VARS_EDU, BY_1_EDU, VARS_EDU, BY_2_EDU, YEARS_EDU, YEAR_EDU, True,
                    {'background-color': '#e6e6e6'}, SWITCH_OPT_EDU, MARK_SCALE, DETAILS_1_EDU)
    

    @app.callback(
        Output('map', 'srcDoc'),
        [
            Input('agg-choices-radio', 'value'),
            Input('year-dropdown', 'value'),
            Input('var-1-dropdown', 'value'),
            Input('var-2-dropdown', 'value'),
            Input('switches-input', 'value'),
            Input('mark-scale-input', 'value'),
            Input('details-1-dropdown', 'value'),
        ],
    )
    def var_change(agg, year, by_1, by_2, switches, mark_scale, details_1):
        show_by_2 = True if 'show_by_2' in switches else False
        show_alt = True if 'show_alt' in switches else False
        show_alt_marks = True if 'show_alt_marks' in switches else False
        reverse_cmap = True if 'reverse_cmap' in switches else False
        
        if show_by_2 == False: by_2 = None

        return update(agg, year, by_1, by_2, details_1, show_alt, show_alt_marks, reverse_cmap, mark_scale)



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

DETAILS_1_ALL = ['cr_count']
DETAILS_1_EDU = ['pupil_total']

CUR_AGG = AGG

SWITCHES = ['show_by_2']
SWITCH_OPT_ALL = [
    {"label": "Show Variable #2", "value": 'show_by_2'},
    {"label": "District Locations", "value": 'show_alt_marks'},
    {"label": "District Borders", "value": 'show_alt'},
    {"label": "Reverse Color", "value": 'reverse_cmap'},
]
SWITCH_OPT_EDU = [
    {"label": "Show Variable #2", "value": 'show_by_2'},
    {"label": "County Locations", "value": 'show_alt_marks'},
    {"label": "County Borders", "value": 'show_alt'},
    {"label": "Reverse Color", "value": 'reverse_cmap'},
]

MARK_SCALE = 5

# agg_selection = 'County'
# var_selection = 'cr_rate'
# var_choices = VARS_ALL

# for c in df_edu_dist.columns:
    # print(c)

''' LOGIC ---------------------------------------------------------------- '''

def update(agg, year, by_1, by_2, details_1, show_alt, show_alt_marks, reverse_cmap, mark_scale):
    mark_scale = mark_scale * 3
    year = int(year)

    # if not by_2:
    #     if agg == 'County':
    #         by_2 = BY_2_ALL
    #     else:
    #         by_2 = BY_2_EDU

    m = plot(agg, df_all, df_edu_dist, year, by_1, by_2, details_1,
            show_alt=show_alt,
            show_alt_marks=show_alt_marks,
            reverse_cmap=reverse_cmap,
            mark_scale=mark_scale,
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
                # html.Div(className='agg-choices', children=[
                #     dcc.RadioItems(className='agg-choices-radio',
                #         options=AGG_CHOICES,
                #         value=AGG,
                #         id='agg-choices-radio',
                #         labelStyle={'marginLeft':'15px', 'marginRight':'15px', 'marginBottom':'5px'},
                #         inputStyle={'marginRight': '7px'},
                #     ),
                # ],
                # ),