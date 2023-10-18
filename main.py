import tkinter as tk
import webview 
from tkinterweb import HtmlFrame

import geopandas as gpd
import math
import matplotlib.pyplot as plt
import numpy as np
import os
import warnings

from scipy import stats
from shapely.geometry import shape, Polygon
from ipyleaflet import (
     Map,
     basemaps,
     DrawControl,
     GeoData,
)

#globs
start = [38,-120]
zoom = 7

def load_base_map(start, zoom):
    m = Map(basemap=basemaps.OpenStreetMap.Mapnik, center=start, zoom=zoom)
    return m 

def add_map(m, gdf):
    grid = GeoData(geo_dataframe = gdf, style={})
    m.add(grid)
    return m

# def add_draw(m):
#     #add draw polygon func
#     draw_control = DrawControl(edit=False, circlemarker={}, polyline={}, 
#                             polygon = {
#                                 "shapeOptions": {
#                                     "fillColor": "#FF0000",
#                                     "color": "#FF0000",
#                                     "fillOpacity": 0.5
#                                 }})
#     m.add(draw_control)
#     return m

def filter(dc):
    coords = []
    #ignore future version err
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        #map based filter
        if dc.last_draw['geometry'] is not None:
            b = dc.last_draw['geometry']['coordinates'][0]
            poly = Polygon(b[:-1])
            c = df.clip(poly)
            coords = c.get_coordinates().to_numpy().tolist()
    return coords

if __name__ == "__main__":
    # os.system("pip install -r requirements.txt")

    #load base_map
    map = load_base_map(start, zoom)

    #load df 
    df = gpd.read_file('sets/cali1.geojson').drop(columns=['Creator_Date', 'Last_Editor_Date'])
    map = add_map(map, df)

    #add draw polygon control
    draw_control = DrawControl(edit=False, circlemarker={}, polyline={}, 
                            polygon = {
                                "shapeOptions": {
                                    "fillColor": "#FF0000",
                                    "color": "#FF0000",
                                    "fillOpacity": 0.5
                                }})
    map.add(draw_control)

    clipped = filter(draw_control)
    print(clipped)


