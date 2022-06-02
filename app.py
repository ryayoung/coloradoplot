from dash import Dash, html, dcc, Input, Output, State, dash_table
from dash.development.base_component import Component
import dash_bootstrap_components as dbc
import pandas as pd, numpy as np
import matplotlib.pyplot as plt, seaborn as sns
import pathlib

from plotting import *

app = Dash(__name__, suppress_callback_exceptions=True,
                assets_ignore='.*chiddyp.*',
                external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
                )

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True


''' APP ------------------------------------------------------------------ '''

def main():
    app.layout = html.Div(className='layout', children=[
    # ------------------------------------------------------------------------
    html.Div(className='top-bar'),
    html.Div(className='page-contents', children=[
    html.Div(className='sidebar resize horizontal', children=[
        # html.Label('View by', className='header-label'),
        html.H2('Colorado Data',
            className='title-text'),
        html.Div(className='agg-choices', children=[
            html.Div(className='radio-group r-group', children=[
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
        ],
        ),
        html.Label('Variables', className='header-label'),
        dbc.Tabs(className='var-tabs', children=[
            dbc.Tab(className='by-1-tab', children=[
                html.Span(className='selection-display', children=[
                    html.P(BY_1_ALL, className='selection-display-value', id='by-1-selection-display'),
                ],
                ),
                dash_table.DataTable(
                    id='var-1-table',
                    selected_cells=val_to_cells(VARS_ALL, BY_1_ALL),
                    **TABLE_KWARGS,
                ),
            ],
            label='Primary',
            # active_label_style={'-webkit-text-stroke':'0.9px', 'borderRadius':'6px 6px 0 0'},
            active_label_style={'color':'black', 'borderRadius':'6px 6px 0 0'},
            ),
            dbc.Tab(className='by-2-tab', children=[
                html.Span(className='selection-display', children=[
                    html.P(BY_1_EDU, className='selection-display-value', id='by-2-selection-display'),
                ],
                ),
                dash_table.DataTable(
                    id='var-2-table',
                    selected_cells=val_to_cells(VARS_ALL, BY_2_ALL),
                    **TABLE_KWARGS,
                ),
            ],
            label='Secondary',
            style={'position':'sticky', 'top':'0'},
            # active_label_style={'-webkit-text-stroke':'0.9px'},
            # active_label_style={'color':'black'},
            active_label_style={'color':'black', 'borderRadius':'6px 6px 0 0'},
            ),
        ],
        ),
    ],
    ),
    html.Div(className='sidebar-handle', children=html.Div(className='sidebar-handle-line-outer', children=html.Div(className='sidebar-handle-line-inner'))),
    html.Div(className='main-content', children=[
    html.Div(className='header', children=[
        html.Div(className='main-controls-box', children=[
            html.Div(className='main-controls', children=[
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
                # html.Div(className='v-divider'
                # ),
                # html.Div(className='variables', children=[
                    # html.Div(className='var-1', children=[
                        # html.Label('Variable 1: Area color', htmlFor='var-1-dropdown'),
                        # dcc.Dropdown(className='var-choices-dropdown',
                            # options=VARS_ALL,
                            # value=BY_1_ALL,
                            # id='var-1-dropdown',
                            # clearable=False,
                            # optionHeight=25,
                        # ),
                    # ],
                    # ),
                    # html.Div(className='var-2', children=[
                        # html.Label('Variable 2: Marker size', htmlFor='var-2-dropdown'),
                        # dcc.Dropdown(className='var-choices-dropdown',
                            # options=VARS_ALL,
                            # value=BY_2_ALL,
                            # id='var-2-dropdown',
                            # clearable=False,
                            # optionHeight=25,
                        # ),
                    # ],
                    # ),
                # ],
                # ),
                html.Div(className='details-1', children=[
                    html.Label('Tooltip', htmlFor='details-1-dropdown'),
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
                    # html.Div(className='details-2', children=[
                        # html.Label('Tooltip', htmlFor='details-2-dropdown'),
                        # dcc.Dropdown(className='var-choices-dropdown',
                            # options=VARS_ALL,
                            # value=[],
                            # id='details-2-dropdown',
                            # clearable=True,
                            # optionHeight=25,
                            # multi=True,
                            # disabled=True,
                        # ),
                    # ],
                    # ),
                # ],
                # ),
                html.Div(className='v-divider'
                ),
                # html.ButtonGroup(className='options', children=[
                    # dbc.Button('Hide Secondary', id='hide-secondary', outline=True),
                    # dbc.Button('View Districts', id='view-districts', outline=True),
                    # dbc.Button('District Borders', id='district-borders', outline=True),
                    # dbc.Button('Reverse Color', id='reverse-color', outline=True),
                # ],
                # ),
                html.Div(className='switches', children=[
                    dbc.Checklist(className='switches-input',
                        options=SWITCH_OPT_ALL,
                        value=SWITCHES,
                        id="switches-input",
                        switch=True,
                    ),
                ],
                ),
            ],
            ),
        ],
        ),
        html.Div(className='hide-header', children=[
            dbc.Button(className='me-1 hide-header-btn', children=[
                # html.I(className='icon bi bi-chevron-up', style={'marginRight':'7px', 'float': 'left'}),
            ],
            color='secondary',
            outline=True,
            id='hide-header-btn'
            ),
        ],
        ),
    ],
    ),
    html.Div(className='show-header', children=[
        dbc.Button(className='me-1 show-header-btn', children=[
            html.I(className='bi bi-chevron-down', style={'marginRight':'7px', 'float':'left', 'paddingLeft':'50px'}),
        ],
        color='primary',
        outline=True,
        id='show-header-btn'
        ),
    ],
    ),
    dcc.Loading(id="loading", children=[html.Div(id="loading-output")], type="default"),
    html.Div(className='map-box', children=[
        html.Iframe(className='map',
            id='map',
            srcDoc=None,
        ),
    ],
    ),
    ],
    ),
    ],
    ),
    # ------------------------------------------------------------------------
    ], style={'height': '100%'})

    @app.callback(
        [
            Output('var-1-table', 'data'),
            Output('var-1-table', 'selected_cells'),
            Output('var-2-table', 'data'),
            Output('var-2-table', 'selected_cells'),
            Output('year-dropdown', 'options'),
            Output('year-dropdown', 'value'),
            Output('year-dropdown', 'disabled'),
            Output('year-dropdown', 'style'),
            Output('switches-input', 'options'),
            Output('switches-input', 'value'),
            Output('mark-scale-input', 'value'),
            Output('details-1-dropdown', 'value'),
        ],
        Input('agg-choices-radio', 'value'),
    )
    def agg_change(agg):
        if agg == 'County':
            return (
                VAR_DATA_ALL, val_to_cells(VARS_ALL, BY_1_ALL),
                VAR_DATA_ALL, val_to_cells(VARS_ALL, BY_2_ALL),
                YEARS_ALL, YEAR_ALL,
                False,
                {'background-color': 'white'},
                SWITCH_OPT_ALL, SWITCHES, MARK_SCALE, DETAILS_1_ALL,
            )

        return (
            VAR_DATA_EDU, val_to_cells(VARS_EDU, BY_1_EDU),
            VAR_DATA_EDU, val_to_cells(VARS_EDU, BY_2_EDU),
            YEARS_EDU, YEAR_EDU,
            True,
            {'background-color': '#e6e6e6'},
            SWITCH_OPT_EDU, SWITCHES, MARK_SCALE, DETAILS_1_EDU
        )
    

    @app.callback(
        [
            Output('map', 'srcDoc'),
            Output('loading-output', 'children'),
        ],
        [
            Input('agg-choices-radio', 'value'),
            Input('year-dropdown', 'value'),
            Input('var-1-table', 'selected_cells'),
            Input('var-2-table', 'selected_cells'),
            Input('switches-input', 'value'),
            Input('mark-scale-input', 'value'),
            Input('details-1-dropdown', 'value'),
        ],
    )
    def var_change(agg, year, by_1, by_2, switches, mark_scale, details_1):
        by_1 = cells_to_val(agg, by_1)
        by_2 = cells_to_val(agg, by_2)
        hide_by_2 = True if 'hide_by_2' in switches else False
        show_alt = True if 'show_alt' in switches else False
        show_alt_marks = True if 'show_alt_marks' in switches else False
        reverse_cmap = True if 'reverse_cmap' in switches else False
        
        if hide_by_2 == True:
            by_2 = None

        return update(agg, year, by_1, by_2, details_1, show_alt, show_alt_marks, reverse_cmap, mark_scale), []

    @app.callback(
        Output('by-1-selection-display', 'children'),
        [
            Input('agg-choices-radio', 'value'),
            Input('var-1-table', 'selected_cells'),
        ]
    )
    def selection_display(agg, by_1):
        by_1 = cells_to_val(agg, by_1)
        return by_1

    @app.callback(
        Output('by-2-selection-display', 'children'),
        [
            Input('agg-choices-radio', 'value'),
            Input('var-2-table', 'selected_cells'),
        ]
    )
    def selection_display(agg, by_2):
        by_2 = cells_to_val(agg, by_2)
        return by_2



''' DATA ----------------------------------------------------------------- '''

df_all = pd.read_csv(DATA_PATH.joinpath('everything_grouped_renamed.csv'))
df_edu_dist = pd.read_csv(DATA_PATH.joinpath('education_dist_renamed.csv'))
df_edu_dist = df_edu_dist[df_edu_dist['Edu: Pupil total'] > 150]

def cells_to_val(agg, cells:list) -> str:
    if agg == 'County':
        return VARS_ALL[cells[0]['row']]
    return VARS_EDU[cells[0]['row']]


def val_to_cells(cols, val:str) -> list:
    return [{'column': 0, 'row': cols.index(val)}]


INDEX_ALL = ['year', 'county', 'geo_county_point', 'geo_county']
INDEX_EDU = ['county', 'dist', 'geo_county_point', 'geo_dist_point', 'geo_county', 'geo_dist']
VARS_ALL = [c for c in df_all.columns if c not in INDEX_ALL]
VARS_EDU = [c for c in df_edu_dist.columns if c not in INDEX_EDU]
VAR_DATA_ALL = [{'value': v, 'id': v} for v in VARS_ALL]
VAR_DATA_EDU = [{'value': v, 'id': v} for v in VARS_EDU]



YEARS_ALL = [str(y) for y in df_all.year.unique()]
YEARS_EDU = ['2012']
YEAR_ALL = '2019'
YEAR_EDU = '2012'

AGG_CHOICES = ['County', 'School District'] 
AGG = 'County'

TYPE_CHOICES = ['Count/Sum', 'Proportion/Agg.']
TYPE = 'Proportion/Agg.'

# BY_1_ALL = 'age_avg'
# BY_1_EDU = 'mobile_rate'
# BY_2_ALL = 'cr_rate'
# BY_2_EDU = 'poor_graduated'
# DETAILS_1_ALL = ['cr_count']
# DETAILS_1_EDU = ['pupil_total']
BY_1_ALL = 'Crime  - Average age'
BY_1_EDU = 'Rate: Edu: Mobile'
BY_2_ALL = 'Crime Rate (per 100,000 people)'
BY_2_EDU = 'Edu: Poor - Graduated'
DETAILS_1_ALL = ['Crime Count']
DETAILS_1_EDU = ['Edu: Pupil total']

SWITCHES = ['show_by_2']
SWITCH_OPT_ALL = [
    {"label": "Hide Variable 2", "value": 'hide_by_2'},
    {"label": "District Locations", "value": 'show_alt_marks'},
    {"label": "District Borders", "value": 'show_alt'},
    {"label": "Reverse Color", "value": 'reverse_cmap'},
]
SWITCH_OPT_EDU = [
    {"label": "Hide Variable 2", "value": 'hide_by_2'},
    {"label": "County Locations", "value": 'show_alt_marks'},
    {"label": "County Borders", "value": 'show_alt'},
    {"label": "Reverse Color", "value": 'reverse_cmap'},
]

MARK_SCALE = 5


TABLE_KWARGS = dict(
    data=VAR_DATA_ALL,
    columns=[{'name':'', 'id':'value'}],
    # tooltip_data=VAR_DATA_ALL,
    page_action='none',
    style_table={
        # 'height': '90% !important',
        'max-height':'80vh',
        'overflow': 'scroll',
        # 'position': 'absolute',
        # 'top':'1000',
        # 'left':'0',
        # 'margin-top': '2px',
    },
    style_cell={
        'whiteSpace': 'no-wrap',
        'overflow':'hidden',
        'textOverflow': 'ellipsis',
        'maxWidth': 0,
        'textAlign':'left',
        'fontFamily':'var(--bs-body-font-family',
        'font-size':'0.9em',
        'height': '40px',
        'padding-left': '20px',
        'border':'none',
    },
    css=[{ 'selector': 'tr:first-child', 'rule': 'display: none'},
        {'selector': '.current-page-container', 'rule': 'display: none'},
    ],
    style_data_conditional=[
        {
            'if': {
                'state': 'selected',
            },
            'padding-left': '25px',
            'backgroundColor': '#f8f8f8',
            'border': 'none',
            # 'border-top': '1px solid #0d6efd',
            # 'border-bottom': '1px solid #0d6efd',
            'border-left': '6px solid #0d6efd',
        },
    ],
)



''' LOGIC ---------------------------------------------------------------- '''

def update(agg, year, by_1, by_2, details_1, show_alt, show_alt_marks, reverse_cmap, mark_scale):
    mark_scale = mark_scale * 3
    year = int(year)

    m = plot(agg, df_all, df_edu_dist, year, by_1, by_2, details_1,
            show_alt=show_alt,
            show_alt_marks=show_alt_marks,
            reverse_cmap=reverse_cmap,
            mark_scale=mark_scale,
            )
    m.save(DATA_PATH.joinpath('map.html'))

    return open(DATA_PATH.joinpath('map.html'), 'r').read()


def add_custom_props(component: Component, **kwargs) -> Component:
    prop_names: List[str] = component._prop_names
    new_props = set(kwargs.keys()) - set(prop_names)
    if new_props:
        prop_names.extend(new_props)
    for k, v in kwargs.items():
        setattr(component, k, v)
    return component



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

