# % load_ext autoreload
# % autoreload 2
# import plotly.graph_objects as go
import branca
import folium
import geojson
import geopandas as gpd
import pandas as pd
import requests

traffic = requests.get('http://web.redant.net/~amsterdam/ndw/data/reistijdenAmsterdam.geojson').content

traffic_geojson = geojson.loads(traffic)
traffic_geojson

traffic_gdf = gpd.GeoDataFrame.from_features(traffic_geojson['features'])
traffic_gdf



traffic_gdf.dropna(subset=['Id', 'Velocity'], inplace=True)

traffic_gdf['Timestamp'] = pd.to_datetime(traffic_gdf['Timestamp'])
traffic_gdf['Velocity'] = traffic_gdf['Velocity'].astype(int)

idx = traffic_gdf.groupby('Id')['Timestamp'].transform(max) == traffic_gdf['Timestamp']
traffic_gdf = traffic_gdf[idx]
traffic_gdf


def calculate_vehicle_flow(velocity):
    if velocity < 20:
        return 0
    elif velocity < 30:
        return 1
    elif velocity < 40:
        return 2
    else:
        return 3


traffic_gdf['vehicle_flow'] = traffic_gdf['Velocity'].apply(calculate_vehicle_flow)
# print(traffic_gdf['Timestamp'])


# m = folium.Map(
#     location=[52.3676, 4.9041],
#     tiles="cartodbpositron",
#     zoom_start=13
# )
#
# colorscale = branca.colormap.step.RdYlGn_04.scale(0, 3)
#
# traffic_gdf.drop(columns=['Timestamp'], inplace=True)
# traffic_gdf.crs = 'urn:ogc:def:crs:OGC:1.3:CRS84'
# folium.GeoJson(traffic_gdf, name="Traffic",
#                style_function=lambda feature: {'color': colorscale(feature['properties']['vehicle_flow'])}).add_to(m)
# folium.LayerControl().add_to(m)
# # print(m)
# m.save("mymap.html")
