from dash import Dash, html, dcc, Input, Output, State, dash_table
import dash_daq as daq
from dash.development.base_component import Component
import dash_bootstrap_components as dbc
import pandas as pd, numpy as np
import matplotlib.pyplot as plt, seaborn as sns
import pathlib
import re

from boolean_switch import BooleanSwitch
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
        html.H2('Colorado Data', className='title-text'),
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
            dbc.Tab(className='by-1-tab', id='by-1-tab', children=[
                dbc.Accordion(flush=True, active_item=['options', 'variables'], always_open=True, children=[
                    dbc.AccordionItem(title='Options', item_id='options', children=[
                        html.Div(className='tab-options', children=[
                            html.Div(className='tab-option', children=[
                                html.P('Visible'),
                                BooleanSwitch(id='by-1-visible', on=True, size=38, className='tab-option-switch', color='#0d6efd'),
                            ],
                            ),
                            html.Div(className='tab-option', children=[
                                html.P('Reverse Color'),
                                BooleanSwitch(id='reverse-cmap', size=38, className='tab-option-switch', color='#0d6efd'),
                            ],
                            ),
                        ],
                        ),
                    ],
                    ),
                    dbc.AccordionItem(title='Value', item_id='variables', children=[
                        html.Span(id='selection-display-1', className='selection-display', children=[
                            html.I(className='bi bi-arrow-90deg-right'),
                            html.P(BY_1_COUNTY, className='selection-display-value', id='by-1-selection-display'),
                        ],
                        ),
                        dash_table.DataTable(
                            id='var-1-table',
                            selected_cells=val_to_cells(VARS_COUNTY, BY_1_COUNTY),
                            **TABLE_KWARGS,
                        ),
                    ],
                    ),
                ],
                ),
            ],
            label='Primary',
            active_label_style={'color':'black', 'borderRadius':'6px 6px 0 0'},
            tab_style={'marginLeft': '20px'},
            ),
            dbc.Tab(className='by-2-tab', id='by-2-tab', children=[
                dbc.Accordion(flush=True, active_item=['options', 'variables'], always_open=True, children=[
                    dbc.AccordionItem(title='Options', item_id='options', children=[
                        html.Div(className='tab-options', children=[
                            html.Div(className='tab-option', children=[
                                html.P('Visible'),
                                BooleanSwitch(id='by-2-visible', on=True, size=38, className='tab-option-switch', color='#0d6efd'),
                            ],
                            ),
                            html.Div(id='tab-option-scale', className='tab-option', children=[
                                html.P('Scale'),
                                html.Div(className='slider', children=[
                                    daq.Slider(id='mark-scale-slider', updatemode='drag', value=6, min=2, max=20, step=2, size=65, color='#0d6efd'),
                                    html.P(id='mark-scale-slider-output', children='6'),
                                ],
                                ),
                            ],
                            ),
                            html.Div(id='tab-option-suppress-peak', className='tab-option', children=[
                                html.P('Suppress Peak'),
                                html.Div(className='slider', children=[
                                    daq.Slider(id='mark-lower-peak-slider', updatemode='drag', value=0, min=0, max=10, step=1, size=65, color='#0d6efd'),
                                    html.P(id='mark-lower-peak-slider-output', children='0'),
                                ],
                                ),
                            ],
                            ),
                            html.Div(id='tab-option-linearize', className='tab-option', children=[
                                html.P('Linearize'),
                                html.Div(className='slider', children=[
                                    daq.Slider(id='mark-straighten-slider', updatemode='drag', value=0, min=0, max=10, step=1, size=65, color='#0d6efd'),
                                    html.P(id='mark-straighten-slider-output', children='0'),
                                ],
                                ),
                            ],
                            ),
                        ],
                        ),
                    ],
                    ),
                    dbc.AccordionItem(title='Value', item_id='variables', children=[
                        html.Span(id='selection-display-2', className='selection-display', children=[
                            html.I(className='bi bi-arrow-90deg-right'),
                            html.P(BY_1_DIST, className='selection-display-value', id='by-2-selection-display'),
                        ],
                        ),
                        dash_table.DataTable(
                            id='var-2-table',
                            selected_cells=val_to_cells(VARS_COUNTY, BY_2_COUNTY),
                            **TABLE_KWARGS,
                        ),
                    ],
                    ),
                ],
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
        html.Div(className='main-controls-parent', children=[
            html.Div(className='main-controls-box', children=[
                html.Div(className='switches', children=[
                    html.Label(id='alt-label', className='main-label', children='Districts'),
                    html.Div(className='switches-boxes', children=[
                        html.Div(className='vertical-divider-left'),
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
                html.Div(className='tooltip-section', children=[
                    html.Label(className='main-label', children='Tooltips'),
                    html.Div(className='tooltip-boxes', children=[
                        html.Div(className='vertical-divider-left'),
                        html.Div(id='tooltip-box-1', className='tooltip-box', children=[
                            html.Label(className='sub-label', children='Primary'),
                            dcc.Dropdown(className='tooltip-dropdown',
                                options=VARS_COUNTY,
                                value=TOOLTIP_BY_1_COUNTY,
                                id='tooltip-1-dropdown',
                                clearable=True,
                                optionHeight=25,
                                multi=True,
                                style={'text-overflow':'ellipsis'},
                            ),
                        ],
                        ),
                        html.Div(id='tooltip-box-2', className='tooltip-box', children=[
                            html.Label(className='sub-label', children='Secondary'),
                            dcc.Dropdown(className='tooltip-dropdown',
                                options=VARS_COUNTY,
                                value=TOOLTIP_BY_2_COUNTY,
                                id='tooltip-2-dropdown',
                                clearable=True,
                                optionHeight=25,
                                multi=True,
                            ),
                        ],
                        ),
                    ],
                    ),
                ],
                ),
            ],
            ),
            html.Div(id='download-container', className='download-container', children=[
                dbc.Button(id='download-button', className='download-button', children=[
                    html.I(className='bi bi-download'),
                ],
                ),
                dcc.Download(id='download-map'),
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
    make_tt('agg-choices-radio', 'right',
            'Select the type of geographic area to aggregate by. '
            "Note: 'School District' offers only education related data, "
            'and can be viewed for 2012 only'
    ),
    make_tt('selection-display-1', 'right', 'Currently selected value for map colors'),
    make_tt('selection-display-2', 'right', 'Currently selected value for circle markers'),
    make_tt('tab-option-scale', 'right', 'Multiplier to increase the size of markers'),
    make_tt('tab-option-suppress-peak', 'right',
        'Uses logarithms to reduce extremes in heavily skewed data. '
        "Use this instead of 'Scale' when most values appear tiny, except for a few large outliers. "
        'It will increase the size of smaller values while leaving outliers alone.'
    ),
    make_tt('tab-option-linearize', 'right',
        'Use this to help identify differences across areas when most values are similar in size, except for a handful of outliers. '
        "Unlike 'Suppress Peak', this has no effect on the highest or lowest values. "
        'It works by decreasing the rate of growth/decay in data that changes exponentially, '
        'bringing it closer to a straight line (having the strongest effect on middle values).'
    ),
    make_tt('switches-input', 'left', 'Drop pins or draw borders on alternative aggregation areas'),
    make_tt('tooltip-box-1', 'right', 'Extra values displayed when hovering over map areas'),
    make_tt('tooltip-box-2', 'right', 'Extra values displayed when hovering over circle markers'),
    make_tt('by-1-tab', 'top', 'Map colors'),
    make_tt('by-2-tab', 'top', 'Circle markers'),
    make_tt('download-container', 'left', 'Download the map as an html file you can open in your browser (without internet)'),
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
            Output('tooltip-1-dropdown', 'value'),
            Output('tooltip-2-dropdown', 'value'),
            Output('alt-label', 'children'),
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
                TOOLTIP_BY_1_COUNTY,
                TOOLTIP_BY_2_COUNTY,
                'Districts',
            )

        return (
            VAR_DATA_DIST, val_to_cells(VARS_DIST, BY_1_DIST),
            VAR_DATA_DIST, val_to_cells(VARS_DIST, BY_2_DIST),
            YEARS_DIST, YEAR_DIST,
            True,
            {'background-color': '#e6e6e6'},
            TOOLTIP_BY_1_DIST,
            TOOLTIP_BY_2_DIST,
            'Counties',
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
            Input('by-1-visible', 'on'),
            Input('by-2-visible', 'on'),
            Input('tooltip-1-dropdown', 'value'),
            Input('tooltip-2-dropdown', 'value'),
            Input('mark-straighten-slider', 'value'),
            Input('mark-lower-peak-slider', 'value'),
            Input('mark-scale-slider', 'value'),
            Input('reverse-cmap', 'on'),
            Input('switches-input', 'value'),
        ],
    )
    def var_change(agg_str, year, by_1, by_2, show_by_1, show_by_2, by_1_tooltip_xtra, by_2_tooltip_xtra, mark_straighten, mark_lower_peak, mark_scale, reverse_cmap, switches):
        show_alt_pins = True if 'show_alt_pins' in switches else False
        show_alt_borders = True if 'show_alt_borders' in switches else False
        
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
                agg_str=agg_str,
                year=year,
                by_1=by_1,
                by_2=by_2,
                by_1_tooltip_xtra=by_1_tooltip_xtra,
                by_2_tooltip_xtra=by_2_tooltip_xtra,
                mark_straighten=mark_straighten,
                mark_lower_peak=mark_lower_peak,
                mark_scale=mark_scale,
                show_alt_borders=show_alt_borders,
                show_alt_pins=show_alt_pins,
                reverse_cmap=reverse_cmap,
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
    
    @app.callback(
        Output('mark-scale-slider-output', 'children'),
        Input('mark-scale-slider', 'value')
    )
    def update_slider_label(val):
        return str(val)

    @app.callback(
        Output('mark-lower-peak-slider-output', 'children'),
        Input('mark-lower-peak-slider', 'value')
    )
    def update_slider_label(val):
        return str(val)

    @app.callback(
        Output('mark-straighten-slider-output', 'children'),
        Input('mark-straighten-slider', 'value')
    )
    def update_slider_label(val):
        return str(val)
    
    @app.callback(
        Output('download-map', 'data'),
        Input('download-button', 'n_clicks'),
        [
            State('map', 'srcDoc'),
            State('agg-choices-radio', 'value'),
            State('year-dropdown', 'value'),
            State('var-1-table', 'selected_cells'),
            State('var-2-table', 'selected_cells'),
            State('by-1-visible', 'on'),
            State('by-2-visible', 'on'),
        ],
        prevent_initial_call=True,
    )
    def download_map(n_clicks, map_src, agg_str, year, by_1, by_2, show_by_1, show_by_2):
        if map_src != None:
            if show_by_1 == False:
                by_1 = None
            else:
                by_1 = cells_to_val(agg_str, by_1)

            if show_by_2 == False:
                by_2 = None
            else:
                by_2 = cells_to_val(agg_str, by_2)

            name_parts = [s for s in [agg_str, year, by_1, by_2] if s != None]
            name_parts = filename_friendly(name_parts)
            if by_1 and by_2:
                name_parts.insert(3, 'by')

            filename = '_'.join(name_parts)
            return dict(content=map_src, filename=f'{filename}.html')

        return dict(content='You downloaded before the map loaded. Oops!', filename='not_a_map.html')

        


''' COMPONENTS ----------------------------------------------------------- '''

checkmark = html.I(className='bi bi-check-lg view-check')


''' DATA ----------------------------------------------------------------- '''

def cells_to_val(agg, cells:list) -> str:
    if agg == 'County':
        return VARS_COUNTY[cells[0]['row']]
    return VARS_DIST[cells[0]['row']]


def val_to_cells(cols, val:str) -> list:
    return [{'column': 0, 'row': cols.index(val)}]


def filename_friendly(parts:list) -> list:
    for i, s in enumerate(parts):
        s = str(s)
        s = s.lower() \
            .replace('%', 'percent') \
            .replace('<=', 'lteq') \
            .replace('>=', 'gteq') \
            .replace('<', 'lt') \
            .replace('>', 'gt') \
            .replace('&', 'and') \
            .replace(' - ', '-') \
            .replace('/', '-')

        s = re.sub('[:(,\.$)]', '', s)

        s = s.replace(' ', '-') \
            .strip()

        parts[i] = s

    return parts
    

def make_tt(target_id, pos, text, hide=50, show=50):
    return dbc.Tooltip(
        text,
        className='button-tooltip',
        target=target_id,
        placement=pos,
        delay=dict(hide=hide, show=show)
    )
    

df_county = META['county']['df']
df_dist = META['dist']['df']


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
TOOLTIP_BY_1_COUNTY = META['county']['tooltip_1']
TOOLTIP_BY_1_DIST = META['dist']['tooltip_1']
TOOLTIP_BY_2_COUNTY = META['county']['tooltip_2']
TOOLTIP_BY_2_DIST = META['dist']['tooltip_2']

SWITCHES = []
SWITCH_OPTIONS = [
    {"label": "Pins", "value": 'show_alt_pins'},
    {"label": "Borders", "value": 'show_alt_borders'},
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

