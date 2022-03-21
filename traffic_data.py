import geojson
import geopandas as gpd
import pandas as pd
import requests

traffic = requests.get('http://web.redant.net/~amsterdam/ndw/data/reistijdenAmsterdam.geojson').content

traffic_geojson = geojson.loads(traffic)
traffic_gdf = gpd.GeoDataFrame.from_features(traffic_geojson['features'])

traffic_gdf.dropna(subset=['Id', 'Velocity'], inplace=True)

traffic_gdf['Timestamp'] = pd.to_datetime(traffic_gdf['Timestamp'])
traffic_gdf['Velocity'] = traffic_gdf['Velocity'].astype(int)

idx = traffic_gdf.groupby('Id')['Timestamp'].transform(max) == traffic_gdf['Timestamp']
traffic_gdf = traffic_gdf[idx]


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
traffic_gdf.drop(columns=['Timestamp'], inplace=True)
traffic_gdf.crs = 'urn:ogc:def:crs:OGC:1.3:CRS84'
