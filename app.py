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
        html.Div(className='year', children=[
            dcc.Dropdown(className='year-dropdown',
                options=YEARS_COUNTY,
                value= YEAR_COUNTY,
                id='year-dropdown',
                clearable=False,
                optionHeight=32,
            ),
        ],
        ),
        dbc.Tabs(className='var-tabs', children=[
            dbc.Tab(className='by-1-tab', children=[
                html.Span(className='selection-display', children=[
                    html.P(BY_1_COUNTY, className='selection-display-value', id='by-1-selection-display'),
                ],
                ),
                dash_table.DataTable(
                    id='var-1-table',
                    selected_cells=val_to_cells(VARS_COUNTY, BY_1_COUNTY),
                    **TABLE_KWARGS,
                ),
            ],
            label='Primary',
            active_label_style={'color':'black', 'borderRadius':'6px 6px 0 0'},
            tab_style={'marginLeft': '20px'},
            ),
            dbc.Tab(className='by-2-tab', children=[
                html.Span(className='selection-display', children=[
                    html.P(BY_1_DIST, className='selection-display-value', id='by-2-selection-display'),
                ],
                ),
                dash_table.DataTable(
                    id='var-2-table',
                    selected_cells=val_to_cells(VARS_COUNTY, BY_2_COUNTY),
                    **TABLE_KWARGS,
                ),
            ],
            label='Secondary',
            style={'position':'sticky', 'top':'0'},
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
                html.Div(className='details-1', children=[
                    html.Label('Tooltip', htmlFor='details-1-dropdown'),
                    dcc.Dropdown(className='var-choices-dropdown',
                        options=VARS_COUNTY,
                        value=TOOLTIP_COUNTY,
                        id='details-1-dropdown',
                        clearable=True,
                        optionHeight=25,
                        multi=True,
                    ),
                ],
                ),
            ],
            ),
            html.Div(className='switches', children=[
                dbc.Checklist(className='switches-input',
                    options=SWITCH_OPTIONS,
                    value=SWITCHES,
                    id="switches-input",
                    switch=True,
                ),
            ],
            ),
        ],
        ),
        html.Div(className='hide-header', children=[
            dbc.Button(className='me-1 hide-header-btn', children=[],
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
            Output('mark-scale-input', 'value'),
            Output('details-1-dropdown', 'value'),
        ],
        Input('agg-choices-radio', 'value'),
    )
    def agg_change(agg):
        if agg == 'County':
            return (
                VAR_DATA_COUNTY, val_to_cells(VARS_COUNTY, BY_1_COUNTY),
                VAR_DATA_COUNTY, val_to_cells(VARS_COUNTY, BY_2_COUNTY),
                YEARS_COUNTY, YEAR_COUNTY,
                False,
                {'background-color': 'white'},
                MARK_SCALE, TOOLTIP_COUNTY,
            )

        return (
            VAR_DATA_DIST, val_to_cells(VARS_DIST, BY_1_DIST),
            VAR_DATA_DIST, val_to_cells(VARS_DIST, BY_2_DIST),
            YEARS_DIST, YEAR_DIST,
            True,
            {'background-color': '#e6e6e6'},
            MARK_SCALE, TOOLTIP_DIST
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
    def var_change(agg_str, year, by_1, by_2, switches, mark_scale, tooltip_xtra):
        show_by_1 = True if 'show_by_1' in switches else False
        show_by_2 = True if 'show_by_2' in switches else False
        show_alt_pins = True if 'show_alt_pins' in switches else False
        show_alt_borders = True if 'show_alt_borders' in switches else False
        reverse_cmap = True if 'reverse_cmap' in switches else False
        
        if show_by_1 == False:
            by_1 = None
        else:
            by_1 = cells_to_val(agg_str, by_1)

        if show_by_2 == False:
            by_2 = None
        else:
            by_2 = cells_to_val(agg_str, by_2)

        return (
            plot(
                year,
                by_1,
                by_2,
                agg_str,
                tooltip_xtra,
                mark_scale,
                show_alt_borders,
                show_alt_pins,
                reverse_cmap,
            ),
            [],
        )

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

df_county = META['county']['df']
df_dist = META['dist']['df']

def cells_to_val(agg, cells:list) -> str:
    if agg == 'County':
        return VARS_COUNTY[cells[0]['row']]
    return VARS_DIST[cells[0]['row']]


def val_to_cells(cols, val:str) -> list:
    return [{'column': 0, 'row': cols.index(val)}]


INDEX_COUNTY = META['county']['idx']
INDEX_DIST = META['dist']['idx']
VARS_COUNTY = [c for c in df_county.columns if c not in INDEX_COUNTY]
VARS_DIST = [c for c in df_dist.columns if c not in INDEX_DIST]
VAR_DATA_COUNTY = [{'value': v, 'id': v} for v in VARS_COUNTY]
VAR_DATA_DIST = [{'value': v, 'id': v} for v in VARS_DIST]

YEARS_COUNTY = [str(y) for y in df_county.year.unique()]
YEARS_DIST = [str(y) for y in df_dist.year.unique()]
YEAR_COUNTY = max(df_county.year.unique())
YEAR_DIST = max(df_dist.year.unique())

AGG_CHOICES = [META[k]['name'] for k in META.keys()] 
AGG = META['county']['name']

BY_1_COUNTY = META['county']['default_1']
BY_1_DIST = META['dist']['default_1']
BY_2_COUNTY = META['county']['default_2']
BY_2_DIST = META['dist']['default_2']
TOOLTIP_COUNTY = META['county']['tooltip']
TOOLTIP_DIST = META['dist']['tooltip']

SWITCHES = ['show_by_1', 'show_by_2']
SWITCH_OPTIONS = [
    {"label": "Primary", "value": 'show_by_1'},
    {"label": "Secondary", "value": 'show_by_2'},
    {"label": "Pins", "value": 'show_alt_pins'},
    {"label": "Borders", "value": 'show_alt_borders'},
    {"label": "Reverse Color", "value": 'reverse_cmap'},
]

MARK_SCALE = 5


TABLE_KWARGS = dict(
    data=VAR_DATA_COUNTY,
    columns=[{'name':'', 'id':'value'}],
    page_action='none',
    style_table={
        'max-height':'80vh',
        'overflow': 'scroll',
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
            'border-left': '6px solid #0d6efd',
        },
    ],
)


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

