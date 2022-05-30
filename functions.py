import pathlib
import pandas as pd, numpy as np
import dash_bootstrap_components as dbc
from dash import html, dcc
from geo_df import GDF
import folium as fl

from app import DATA_PATH


'''
USER INTERFACE ---------------------------------------------------------------
------------------------------------------------------------------------------
'''


def gray(x):
    return f"#f{x}f{x}f{x}"


def code_btn(ID):
    return dbc.Button(
        [
            html.I(className="bi bi-code-slash fa-2x"),
            "CODE",
        ],
        id=ID,
        className="me-1",
        outline=True,
        color="secondary",
        n_clicks=0,
        )

def code_dropdown(code, btn_id, collapse_id):
    return html.Div(
            [
                html.Div(html.Div(code_btn(btn_id)), className="code-btn"),
                dbc.Collapse(
                    dcc.Markdown(code, className='markdowns'),
                    id=collapse_id,
                    is_open=False,
                ),
            ], style={"width": "1000px"}
        )


'''
DATA -------------------------------------------------------------------------
------------------------------------------------------------------------------
'''


'''
PLOTTING ---------------------------------------------------------------------
------------------------------------------------------------------------------
'''


''' HELPERS -------------------------------------------------------------- '''

ZOOM=7

def normalize(data, multiplier=None):
    result = (data - np.min(data)) / (np.max(data) - np.min(data))
    if multiplier:
        result = [v*multiplier for v in result]
    return result


def add_points(m, df, loc, val, scale=10):
    for geo, v, v_norm in zip(df[loc], df[val], normalize(list(df[val]), scale)):
        fl.CircleMarker(
            location=(geo.y, geo.x),
            radius=v_norm,
            color='white',
            fill=True,
            tooltip=f'{val}: {v}'
        ).add_to(m)
    return m


def add_marks(m, df, loc, var_name, tooltip_title=None):
    if not tooltip_title:
        tooltip_title = var_name
    for geo, name in zip(df[loc], df[var_name]):
        fl.Marker(
            location=(geo.y, geo.x),
            icon=fl.Icon(color="gray", icon="info-sign"),
            opacity=0.75,
            tooltip=f'''{tooltip_title}:<br><b>{name}</b>'''
        ).add_to(m)
    return m


''' GENERATE PLOTS ------------------------------------------------------- '''


def plot_county(df, by_1, dist, year,
        by_2,
        details_1,
        point_scale,
        show_alt,
        show_alt_marks,
        reverse_cmap,
    ):

    cmap='flare'
    style_kwds=dict( fillOpacity=0.5, weight=2 )
    highlight_kwds=dict( fillOpacity=0.8 )

    df = df[df.year == year]

    if details_1 == None or details_1 == []:
        details_1 = [by_1]

    if reverse_cmap == True:
        cmap = f'{cmap}_r'

    main = GDF(df, geo='geo_county').df()

    color_range = dict()
    if (50 < main[by_1].max() < 101) and (0 < main[by_1].min() < 50):
        color_range = dict(vmin=0, vmax=100)

    if show_alt == True or show_alt_marks == True:
        dist = GDF(dist, geo='geo_dist').df()
    
    if show_alt == True:

        dist_map = dist.explore(style_kwds=dict(fill=False, color='#bababa', weight=4), zoom_start=ZOOM)

        result = main.explore(tooltip=['county']+details_1, column=main[by_1],
                    m=dist_map, cmap=cmap, **color_range,
                    style_kwds=style_kwds, highlight_kwds=highlight_kwds)
    else:
        result = main.explore(tooltip=['county']+details_1, column=main[by_1],
                    cmap=cmap, **color_range,
                    style_kwds=style_kwds, highlight_kwds=highlight_kwds, zoom_start=ZOOM)
    
    if show_alt_marks == True:
        result = add_marks(result, dist, 'geo_dist_point', 'dist', 'School District')
    
    if by_2:
        result = add_points(result, main, 'geo_county_point', by_2, point_scale)

    return result



def plot_edu_dist(df, by_1,
        by_2,
        details_1,
        point_scale,
        show_county,
        show_county_marks,
        reverse_cmap,
    ):

    cmap='flare'
    style_kwds=dict( fillOpacity=0.5, weight=2 )
    highlight_kwds=dict( fillOpacity=0.8 )


    if details_1 == None or details_1 == []:
        details_1 = [by_1]
    
    if reverse_cmap == True:
        cmap = f'{cmap}_r'

    main = GDF(df, geo='geo_dist').df()

    if show_county == True:
        county = GDF(df, geo='geo_county').df()

        county_map = county.explore(style_kwds=dict(fill=False, color='gray', weight=4), zoom_start=ZOOM)

        result = main.explore(tooltip=['dist']+details_1, column=main[by_1],
                    m=county_map, cmap=cmap, vmin=0, vmax=100,
                    style_kwds=style_kwds, highlight_kwds=highlight_kwds)
    else:
        result = main.explore(tooltip=['dist']+details_1, column=main[by_1],
                    cmap=cmap, vmin=0, vmax=100,
                    style_kwds=style_kwds, highlight_kwds=highlight_kwds, zoom_start=ZOOM)
    
    if by_2:
        result = add_points(result, main, 'geo_dist_point', by_2, point_scale)
    return result



def plot(agg, df_all, df_edu, year, by_1, by_2,
        details_1:list      =None,
        point_scale:float   =10,
        show_alt:bool      =False,
        show_alt_marks:bool=False,
        reverse_cmap:bool   =True,
    ):
    if agg == 'County':
        return plot_county(df_all, by_1, df_edu, year, by_2, details_1, point_scale, show_alt, show_alt_marks, reverse_cmap)
    
    return plot_edu_dist(df_edu, by_1, by_2, details_1, point_scale, show_alt, show_alt_marks, reverse_cmap)