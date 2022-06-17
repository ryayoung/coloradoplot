import time
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
        tooltip = ['Crime Count'],
        idx = ['year', 'county', 'geo_county_point', 'geo_county'],
    ),
    'dist': dict(
        df = pd.read_csv(DATA_PATH.joinpath('dist.csv')),
        name = 'School District',
        default_year = '2012',
        default_1 = 'Rate: Edu: Mobile',
        default_2 = 'Edu: Poor - Graduated',
        tooltip = ['Edu: Pupil total'],
        idx = ['county', 'dist', 'geo_county_point', 'geo_dist_point', 'geo_county', 'geo_dist'],
    ),
}


'''
PLOTTING ---------------------------------------------------------------------
------------------------------------------------------------------------------
'''


''' HELPERS -------------------------------------------------------------- '''

ZOOM = 7
LOCATION = [37.362701, -105.613936]

def normalize(data, multiplier=None):
    result = (data - np.min(data)) / (np.max(data) - np.min(data))
    if multiplier:
        result = [v*multiplier for v in result]
    return result


def add_points(m, gdf, loc, val, scale=10):
    for geo, v, v_norm in zip(gdf[loc], gdf[val], normalize(list(gdf[val]), scale)):
        fl.CircleMarker(
            location=(geo.y, geo.x),
            radius=v_norm,
            color='white',
            fill=True,
            tooltip=f'{val}: {v}'
        ).add_to(m)
    return m


def add_marks(m, gdf, loc, var_name, tooltip_title=None):
    if not tooltip_title:
        tooltip_title = var_name
    for geo, name in zip(gdf[loc], gdf[var_name]):
        print(geo)
        fl.Marker(
            location=(geo.y, geo.x),
            icon=fl.Icon(color="gray", icon="info-sign"),
            opacity=0.75,
            tooltip=f'''{tooltip_title}:<br><b>{name}</b>'''
        ).add_to(m)
    return m


''' GENERATE PLOTS ------------------------------------------------------- '''


def plot(
        year : str,
        by_1 : str or None,
        by_2 : str or None,
        agg_str         : str   = META[list(META.keys())[0]]['name'],
        tooltip_xtra    : list  = [],
        mark_scale      : float = 15,
        show_alt_borders: bool  = False,
        show_alt_pins   : bool  = False,
        reverse_cmap    : bool  = True,
    ):

    mark_scale *= 3
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
        tooltip = [agg[0]] + tooltip_xtra + [by_1]
        column = gdf_1[by_1]
    else:
        column = None
        tooltip = [agg[0]] + tooltip_xtra

    if show_alt_borders:
        alt_borders = gdf_2.explore(
            location=LOCATION,
            style_kwds=style_kwds_border,
            zoom_start=ZOOM
        )
    else:
        alt_borders = None
                

    result = gdf_1.explore(
        location=LOCATION,
        tooltip=tooltip,
        column=column,
        m=alt_borders,
        cmap=cmap,
        zoom_start=ZOOM,
        style_kwds=style_kwds,
        highlight_kwds=highlight_kwds
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
            scale=mark_scale,
        )

    # result.save(DATA_PATH.joinpath('map.html'))
    # the_map = open(DATA_PATH.joinpath('map.html'), 'r').read()
    return result.get_root().render()
