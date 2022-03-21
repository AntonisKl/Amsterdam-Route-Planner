import branca
import folium
import geopandas as gpd
import pandas as pd

walkability_df = pd.read_csv('WALKABILITY.csv', sep=';')
walkability_df

walkability_df.rename(columns={'Loopruimte': 'walking_area', 'Walkability_algemeen': 'walkability_general',
                               'Drukte_algemeen': 'busy_general', 'Walkability_recreatief': 'walkability_recreational',
                               'Drukte_recreatief': 'busy_recreational',
                               'Walkability_toeristisch': 'walkability_touristy', 'Drukte_toeristisch': 'busy_touristy',
                               'Walkability_werkgerelateerd': 'walkability_work-related',
                               'Drukte_werkgerelateerd': 'busy_work-related'}, inplace=True)

walkability_df = walkability_df.copy()[['walking_area', 'walkability_general', 'busy_general', 'WKT_LNG_LAT']]
walkability_df.rename(columns={'walkability_general': 'walkability', 'busy_general': 'busyness'}, inplace=True)

walkability_df['walking_area'].replace({'zeer krap': 0, 'krap': 1, 'ruim': 2, 'zeer ruim': 3}, inplace=True)
walkability_df['walkability'].replace({'slecht': 0, 'matig': 1, 'goed': 2, 'uitstekend': 3}, inplace=True)
walkability_df['busyness'].replace({'zeer druk': 0, 'druk': 1, 'rustig': 2, 'zeer rustig': 3}, inplace=True)

walkability_df

walkability_df['WKT_LNG_LAT'] = gpd.GeoSeries.from_wkt(walkability_df['WKT_LNG_LAT'])
walkability_gdf = gpd.GeoDataFrame(walkability_df, geometry='WKT_LNG_LAT')
walkability_gdf.crs = 'WGS84'
walkability_gdf

# m = folium.Map(
#     location=[52.3676, 4.9041],
#     tiles=None,
#     zoom_start=13
# )
#
# base_map = folium.FeatureGroup(name='Basemap', overlay=True, control=False)
# folium.TileLayer(tiles='cartodbpositron').add_to(base_map)
# base_map.add_to(m)
#
# colorscale = branca.colormap.step.RdYlGn_04.scale(0, 3)
#
# folium.GeoJson(walkability_gdf, name="Walking area",
#                style_function=lambda feature: {'color': colorscale(feature['properties']['walking_area'])},
#                overlay=False).add_to(m)
# folium.GeoJson(walkability_gdf, name="Walkability",
#                style_function=lambda feature: {'color': colorscale(feature['properties']['walkability'])},
#                overlay=False).add_to(m)
# folium.GeoJson(walkability_gdf, name="Busyness",
#                style_function=lambda feature: {'color': colorscale(feature['properties']['busyness'])},
#                overlay=False).add_to(m)
# folium.LayerControl(collapsed=False).add_to(m)
# m
