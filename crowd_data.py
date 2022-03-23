from datetime import datetime

import geojson
import geopandas as gpd
import pandas as pd
import pytz
import requests
from dateutil.relativedelta import relativedelta
from shapely.geometry import shape

current_hour = datetime.utcnow().replace(tzinfo=pytz.UTC, minute=0, second=0, microsecond=0)

month_ago_same_hour = current_hour - relativedelta(months=1)
month_ago_same_hour_s = month_ago_same_hour.strftime('%Y-%m-%dT%H:%M:%SZ')

last_month_same_hour_same_weekday = []
week_ago = current_hour - relativedelta(days=7)
while week_ago >= month_ago_same_hour:
    last_month_same_hour_same_weekday.append(week_ago)
    week_ago = week_ago - relativedelta(days=7)

crowd = requests.get(
    f'https://api.data.amsterdam.nl/v1/wfs/crowdmonitor/?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature&TYPENAMES=passanten&OUTPUTFORMAT=geojson&Filter=%3CFilter%3E%3CPropertyIsGreaterThan%3E%3CPropertyName%3Edatum_uur%3C/PropertyName%3E%3CLiteral%3E{month_ago_same_hour_s}%3C/Literal%3E%3C/PropertyIsGreaterThan%3E%3C/Filter%3E').content

crowd_geojson = geojson.loads(crowd)

crowd_gdf = gpd.GeoDataFrame.from_features(crowd_geojson['features'])

crowd_gdf.rename(columns={'periode': 'period', 'naam_locatie': 'location_name', 'datum_uur': 'datetime',
                          'aantal_passanten': 'people_count', 'gebied': 'area'}, inplace=True)

crowd_gdf['datetime'] = pd.to_datetime(crowd_gdf['datetime'])
crowd_gdf = crowd_gdf[crowd_gdf['period'] == 'uur'].drop(columns=['period'])

crowd_last_month_same_hour_same_weekday_gdf = crowd_gdf[crowd_gdf['datetime'].isin(last_month_same_hour_same_weekday)]
mean_crowd_same_weekday_per_sensor_gdf = crowd_last_month_same_hour_same_weekday_gdf.groupby('sensor')[
    'people_count'].mean().apply(round)


def calculate_crowd_level(people_count_normalized):
    if people_count_normalized < .25:
        return 0
    elif people_count_normalized < .5:
        return 1
    elif people_count_normalized < .75:
        return 2
    else:
        return 3


current_crowd_prediction_gdf = crowd_last_month_same_hour_same_weekday_gdf.drop_duplicates(subset=['sensor']).drop(
    columns=['people_count', 'datetime'])
current_crowd_prediction_gdf = pd.merge(current_crowd_prediction_gdf, mean_crowd_same_weekday_per_sensor_gdf,
                                        on='sensor', how='left')

people_counts = current_crowd_prediction_gdf['people_count']
current_crowd_prediction_gdf['people_count_normalized'] = (people_counts - people_counts.min()) / (
        people_counts.max() - people_counts.min())
current_crowd_prediction_gdf['crowd_level'] = current_crowd_prediction_gdf['people_count_normalized'].apply(
    calculate_crowd_level)

current_crowd_prediction_gdf['geometry'] = current_crowd_prediction_gdf['geometry'].apply(
    lambda point: shape(point).buffer(20))
# current_crowd_prediction_gdf.set_geometry('points_with_radius', inplace=True)
current_crowd_prediction_gdf.crs = 'urn:ogc:def:crs:EPSG::28992'
