from traffic_data import traffic_gdf
from crowd_data import current_crowd_prediction_gdf
from walk_data import walkability_gdf
from accessibility_data import accessibility_gdf
import folium
import branca


def create_map_with_features(show_traffic=True, show_crowd=True, show_walkability=True, show_accessibility=True):
    amsterdam_coords = [52.3676, 4.9041]

    m = folium.Map(
        location=amsterdam_coords,
        tiles="cartodbpositron",
        zoom_start=13
    )

    base_map = folium.FeatureGroup(name='Basemap', overlay=True, control=False)
    folium.TileLayer(tiles='cartodbpositron').add_to(base_map)
    base_map.add_to(m)

    colorscale = branca.colormap.step.RdYlGn_04.scale(0, 3)
    colorscale2 = branca.colormap.step.YlOrBr_05.scale(0, 3)

    folium.GeoJson(traffic_gdf, name="Traffic",
                   style_function=lambda feature: {'color': colorscale(feature['properties']['vehicle_flow'])},
                   show=show_traffic).add_to(
        m)
    folium.GeoJson(current_crowd_prediction_gdf, name="Crowd",
                   style_function=lambda feature: {'color': colorscale(feature['properties']['crowd_level'])},
                   show=show_crowd).add_to(m)
    folium.GeoJson(walkability_gdf, name="Walkability",
                   style_function=lambda feature: {'color': colorscale2(feature['properties']['walkability'])},
                   show=show_walkability).add_to(
        m)
    folium.GeoJson(accessibility_gdf, name="Accessibility",
                   style_function=lambda feature: {'color': colorscale(feature['properties']['score_0to3'])},
                   show=show_accessibility).add_to(m)

    return m
