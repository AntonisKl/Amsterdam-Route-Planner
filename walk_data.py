import geopandas as gpd
import pandas as pd

walkability_df = pd.read_csv('WALKABILITY.csv', sep=';')

walkability_df.rename(columns={'Loopruimte': 'walking_area', 'Walkability_algemeen': 'walkability_general',
                               'Drukte_algemeen': 'busy_general', 'Walkability_recreatief': 'walkability_recreational',
                               'Drukte_recreatief': 'busy_recreational',
                               'Walkability_toeristisch': 'walkability_touristy', 'Drukte_toeristisch': 'busy_touristy',
                               'Walkability_werkgerelateerd': 'walkability_work-related',
                               'Drukte_werkgerelateerd': 'busy_work-related', 'WKT_LNG_LAT': 'geometry'}, inplace=True)

walkability_df = walkability_df.copy()[['walking_area', 'walkability_general', 'busy_general', 'geometry']]
walkability_df.rename(columns={'walkability_general': 'walkability', 'busy_general': 'busyness'}, inplace=True)

walkability_df['walking_area'].replace({'zeer krap': 0, 'krap': 1, 'ruim': 2, 'zeer ruim': 3}, inplace=True)
walkability_df['walkability'].replace({'slecht': 0, 'matig': 1, 'goed': 2, 'uitstekend': 3}, inplace=True)
walkability_df['busyness'].replace({'zeer druk': 0, 'druk': 1, 'rustig': 2, 'zeer rustig': 3}, inplace=True)

walkability_df['geometry'] = gpd.GeoSeries.from_wkt(walkability_df['geometry'])
walkability_gdf = gpd.GeoDataFrame(walkability_df)
walkability_gdf.crs = 'WGS84'
