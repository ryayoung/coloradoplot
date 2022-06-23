import time
import math
import pathlib
import pandas as pd, numpy as np
import dash_bootstrap_components as dbc
from dash import html, dcc
from geo_df import GDF
import folium as fl

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("./data").resolve()

META = {
    'county': dict(
        df = pd.read_csv(DATA_PATH.joinpath('county.csv')),
        name = 'County',
        default_year = '2019',
        default_1 = 'Crime - Average age',
        default_2 = 'Crime Rate (per 100,000 people)',
        tooltip_1 = ['Crime Count'],
        tooltip_2 = ['% Housing units occupied'],
        idx = ['year', 'county', 'geo_county_point', 'geo_county'],
    ),
    'dist': dict(
        df = pd.read_csv(DATA_PATH.joinpath('dist.csv')),
        name = 'School District',
        default_year = '2012',
        default_1 = 'Rate: Edu: Mobile',
        default_2 = 'Rate: Edu: Poor - Graduated',
        tooltip_1 = ['Edu: Pupil total'],
        tooltip_2 = ['Rate: Edu: Disabled - Stable'],
        idx = ['year', 'county', 'dist', 'geo_county_point', 'geo_dist_point', 'geo_county', 'geo_dist'],
    ),
}


'''
PLOTTING ---------------------------------------------------------------------
------------------------------------------------------------------------------
'''


''' HELPERS -------------------------------------------------------------- '''

ZOOM = 7
LOCATION = [37.362701, -105.613936]

def normalize(data):
    result = (data - np.min(data)) / (np.max(data) - np.min(data))
    return result


def lower_peak(y, coef):
    '''
    Make maximums smaller while keeping smaller values similar
    Pass an int, 1-10
    '''
    if coef != 0:
        y = y + 1
        m = (coef ** 2) / 10
        y = np.ma.log(y) / np.log(math.e - 0.7 + m)
        y = y.filled(0)
        y -= 1
        y += 1 - np.max(y)
    return y


def straighten(y, coef):
    if coef != 0:
        y_straight = np.linspace(0, 1, len(y))
        dist = y_straight - y
        coef = 12 - coef
        dist2 = (dist + 1) ** 1.1 - 1
        y = y + dist2 / (coef * 0.6)
    return y


def adjust(y, coef_straighten, coef_lower_peak, scale):
    scale *= 3
    y = np.array(y)
    order = np.argsort(y, kind='mergesort')
    reverse = np.argsort(order, kind='mergesort')

    y = y[order]
    yn = normalize(y)

    y1 = straighten(yn, coef_straighten)
    y2 = lower_peak(y1, coef_lower_peak)

    y2 = y2[reverse]
    y2 *= scale
    y2 = np.where(y2 == 0, 0.0001, y2)
    return y2


def add_points(m, gdf, loc, val, tooltip_xtra,
        coef_straighten, coef_lower_peak, scale, color):
    for geo, v, v_norm, *xtra in zip(
                gdf[loc],
                gdf[val],
                adjust(gdf[val], coef_straighten, coef_lower_peak, scale),
                *[gdf[x] for x in tooltip_xtra]
        ):
        fl.CircleMarker(
            location=(geo.y, geo.x),
            radius=v_norm,
            color=color,
            fill=True,
            tooltip=''.join(
                [f'<b>{val}</b>: {v}<br>'] \
                + [f'<b>{tooltip_xtra[i]}</b>: {xtra[i]}<br>' for i in range(0, len(tooltip_xtra))]
            )
        ).add_to(m)
    return m


def add_marks(m, gdf, loc, var_name, tooltip_title=None):
    if not tooltip_title:
        tooltip_title = var_name
    for geo, name in zip(gdf[loc], gdf[var_name]):
        fl.Marker(
            location=(geo.y, geo.x),
            icon=fl.Icon(color="gray", icon="info-sign"),
            opacity=0.75,
            tooltip=f'''{tooltip_title}:<br><b>{name}</b>'''
        ).add_to(m)
    return m


''' GENERATE PLOTS ------------------------------------------------------- '''


def plot(
        agg_str         : str   = META[list(META.keys())[0]]['name'],
        year            : str   = 2019,
        by_1            : str   = None,
        by_2            : str   = None,
        by_1_tooltip_xtra: list = [],
        by_2_tooltip_xtra: list = ['Crime - Against property', 'Crime - Against society'],
        mark_straighten : float = 0,
        mark_lower_peak : float = 2,
        mark_scale      : float = 6,
        show_alt_borders: bool  = False,
        show_alt_pins   : bool  = False,
        reverse_cmap    : bool  = True,
    ):

    year = int(year)

    style_kwds = dict(
        fillOpacity=0.5,
        weight=2
    )
    style_kwds_border = dict(
        fill=False,
        color='#bababa',
        weight=4
    )
    highlight_kwds = dict(
        fillOpacity=0.8
    )


    cmap= 'flare' if not reverse_cmap else 'flare_r'

    # Convert string agg to tuple
    if agg_str == 'County':
        agg = ('county', 'dist')
    else:
        agg = ('dist', 'county')

    df_1 = META[agg[0]]['df']
    gdf_1 = GDF(df_1[df_1.year == year], geo=f'geo_{agg[0]}').df()

    if show_alt_borders or show_alt_pins:
        df_2 = META[agg[1]]['df']
        year_2 = int(META[agg[1]]['default_year'])
        gdf_2 = GDF(df_2[df_2.year == year_2], geo=f'geo_{agg[1]}').df()
    else:
        gdf_2 = None

    if by_1:
        tooltip = [agg[0]] + by_1_tooltip_xtra + [by_1]
        column = gdf_1[by_1]
        by_2_color = 'white'
    else:
        column = None
        tooltip = [agg[0]] + by_1_tooltip_xtra
        by_2_color = '#0d6efd'

    if show_alt_borders:
        alt_borders = gdf_2.explore(
            location=LOCATION,
            style_kwds=style_kwds_border,
            zoom_start=ZOOM
        )
    else:
        alt_borders = None
                

    if by_1 == None:
        kwargs = dict(color='white')
    else:
        kwargs = dict()

    result = gdf_1.explore(
        location=LOCATION,
        tooltip=tooltip,
        column=column,
        m=alt_borders,
        cmap=cmap,
        zoom_start=ZOOM,
        style_kwds=style_kwds,
        highlight_kwds=highlight_kwds,
        **kwargs
    )
    
    if show_alt_pins == True:
        result = add_marks(
            m=result,
            gdf=gdf_2,
            loc=f'geo_{agg[1]}_point',
            var_name=agg[1],
            tooltip_title=META[agg[1]]['name'],
        )
    
    if by_2:
        result = add_points(
            m=result,
            gdf=gdf_1,
            loc=f'geo_{agg[0]}_point',
            val=by_2,
            tooltip_xtra=by_2_tooltip_xtra,
            coef_straighten=mark_straighten,
            coef_lower_peak=mark_lower_peak,
            scale=mark_scale,
            color=by_2_color,
        )

    # result.save(DATA_PATH.joinpath('map.html'))
    # the_map = open(DATA_PATH.joinpath('map.html'), 'r').read()
    return result.get_root().render()
