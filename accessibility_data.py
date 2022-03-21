import geojson
import geopandas as gpd
import requests

accessibility = requests.get(
    'https://sidewalk-amsterdam.cs.washington.edu/v2/access/score/streets?lng1=4.769276&lat1=52.300761&lng2=5.004452&lat2=52.426341').content

accessibility_geojson = geojson.loads(accessibility)

accessibility_gdf = gpd.GeoDataFrame.from_features(accessibility_geojson['features'])


def calculate_accessibility_level(score):
    if score < 0.25:
        return 0
    elif score < 0.5:
        return 1
    elif score < 0.75:
        return 2
    else:
        return 3


accessibility_gdf['score_0to3'] = accessibility_gdf['score'].apply(calculate_accessibility_level)
accessibility_gdf.crs = 'urn:ogc:def:crs:OGC:1.3:CRS84'
