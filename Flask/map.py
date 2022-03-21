from traffic_data import *
from crowd_data import *
from walk_data import *


m = folium.Map(
    location=[52.3676, 4.9041],
    tiles="cartodbpositron",
    zoom_start=13
)

base_map = folium.FeatureGroup(name='Basemap', overlay=True, control=False)
folium.TileLayer(tiles='cartodbpositron').add_to(base_map)
base_map.add_to(m)

colorscale = branca.colormap.step.RdYlGn_04.scale(0, 3)
colorscale2 = branca.colormap.step.YlOrBr_05.scale(0, 3)
# colormap = branca.colormap.linear.YlOrRd_09.scale(0, 8500)
# colorscale = colorscale.to_step(index=[0, 1000, 3000, 5000, 8500])
# colorscale.caption = 'Incidents of Crime in Victoria (year ending June 2018)'
# colorscale.add_to(world_map)

traffic_gdf.drop(columns=['Timestamp'], inplace=True)
traffic_gdf.crs = 'urn:ogc:def:crs:OGC:1.3:CRS84'
folium.GeoJson(traffic_gdf, name="Traffic",
               style_function=lambda feature: {'color': colorscale(feature['properties']['vehicle_flow'])}).add_to(m)

current_crowd_prediction_gdf.crs = 'urn:ogc:def:crs:EPSG::28992'
folium.GeoJson(current_crowd_prediction_gdf[['points_with_radius', 'crowd_level']], name="crowd",
               style_function=lambda feature: {'color': colorscale(feature['properties']['crowd_level'])}).add_to(m)

folium.GeoJson(walkability_gdf, name="Walking area",
               style_function=lambda feature: {'color': colorscale2(feature['properties']['walking_area'])},
               overlay=False).add_to(m)
folium.GeoJson(walkability_gdf, name="Walkability",
               style_function=lambda feature: {'color': colorscale2(feature['properties']['walkability'])},
               overlay=False).add_to(m)
folium.GeoJson(walkability_gdf, name="Business",
               style_function=lambda feature: {'color': colorscale2(feature['properties']['busyness'])},
               overlay=False).add_to(m)
folium.LayerControl(collapsed=False).add_to(m)
folium.LayerControl().add_to(m)

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

# colorscale = branca.colormap.step.RdYlGn_04.scale(0, 3)
#
# current_crowd_prediction_gdf.crs = 'urn:ogc:def:crs:EPSG::28992'
# folium.GeoJson(current_crowd_prediction_gdf[['points_with_radius', 'crowd_level']], name="crowd",
#                style_function=lambda feature: {'color': colorscale(feature['properties']['crowd_level'])}).add_to(m)
# folium.LayerControl().add_to(m)
m
# m
# print(m)
m.save("mymap.html")
