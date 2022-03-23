import folium
import geojson
from shapely import geometry
from shapely.geometry import LineString, MultiPolygon

from config import ors_api_key
from openrouteservice import client

ors = client.Client(key=ors_api_key)


def find_coordinates_of_place(text):
    request_params = {'text': text}
    response = ors.pelias_search(**request_params)
    response_geojson = geojson.loads(geojson.dumps(response))

    try:
        return response_geojson['features'][0]['geometry']['coordinates']
    except KeyError as e:
        print(f"Unexpected {e}, {type(e)}")
        raise


def add_overlapping_streets(overlapping_streets, streets_series, route_buffer, style_function, folium_map):
    for street in streets_series:
        if route_buffer.intersects(street):
            overlapping_streets.append(street)


def get_text_instructions(route):
    instructions = []
    for feature in route['features']:
        for segment in feature['properties']['segments']:
            for step in segment['steps']:
                instructions.append(step['instruction'])

    return instructions


def find_route(folium_map, destination, avoid_low_accessibility, avoid_traffic, avoid_low_walkability,
               avoid_high_crowds, accessibility_gdf, traffic_gdf, walkability_gdf, crowd_gdf):
    destination_coords = find_coordinates_of_place(destination)
    source_coords = [4.899431, 52.379189]

    avoid_something = avoid_low_accessibility or avoid_traffic or avoid_low_walkability or avoid_high_crowds

    folium.Marker(
        destination_coords[::-1], popup=f"<i>{destination}</i>",
        icon=folium.Icon(color='green', prefix='fa', icon='location-dot')
    ).add_to(folium_map)

    folium.Marker(
        source_coords[::-1], popup=f"<i>Starting point</i>",
        icon=folium.Icon(color='blue', prefix='fa', icon='location-dot')
    ).add_to(folium_map)

    request_params = {'coordinates': [source_coords,
                                      destination_coords],
                      'format_out': 'geojson',
                      'profile': 'foot-walking',
                      'preference': 'shortest',
                      'instructions': 'true', }

    route_normal = ors.directions(**request_params)

    def style_function(color):
        return lambda feature: dict(color=color,
                                    weight=3,
                                    opacity=0.5)

    folium.GeoJson(data=route_normal,
                   name='Initial route',
                   style_function=lambda feature: {'color': 'red' if avoid_something else 'green'},
                   overlay=True).add_to(folium_map)

    if not avoid_something:
        return get_text_instructions(route_normal)

    route_buffer = LineString(route_normal['features'][0]['geometry']['coordinates']).buffer(0.00015)
    folium.GeoJson(data=geometry.mapping(route_buffer),
                   name='Route buffer',
                   style_function=style_function('orange'),
                   overlay=True).add_to(folium_map)

    streets_to_avoid = []
    if avoid_low_accessibility:
        low_accessibility_streets_gdf = accessibility_gdf[accessibility_gdf['score_0to3'] <= 0]['geometry']
        low_accessibility_streets_gdf.crs = 'urn:ogc:def:crs:OGC:1.3:CRS84'
        low_accessibility_streets_gdf = low_accessibility_streets_gdf.copy().apply(
            lambda linestring: linestring.buffer(0.0002))
        add_overlapping_streets(streets_to_avoid, low_accessibility_streets_gdf, route_buffer, style_function,
                                folium_map)

    if avoid_traffic:
        high_traffic_streets_gdf = traffic_gdf[traffic_gdf['vehicle_flow'] <= 0]['geometry']
        high_traffic_streets_gdf.crs = 'urn:ogc:def:crs:OGC:1.3:CRS84'
        high_traffic_streets_gdf = high_traffic_streets_gdf.copy().apply(
            lambda linestring: linestring.buffer(0.0002))
        add_overlapping_streets(streets_to_avoid, high_traffic_streets_gdf, route_buffer, style_function, folium_map)

    if avoid_low_walkability:
        low_walkability_streets_gdf = walkability_gdf[walkability_gdf['walkability'] <= 0]['geometry']
        low_walkability_streets_gdf.crs = 'WGS84'
        low_walkability_streets_gdf = low_walkability_streets_gdf.copy().apply(
            lambda linestring: linestring.buffer(0.0002))
        add_overlapping_streets(streets_to_avoid, low_walkability_streets_gdf, route_buffer, style_function, folium_map)

    if avoid_high_crowds:
        high_crowd_streets_gdf = crowd_gdf[crowd_gdf['crowd_level'] <= 0]['geometry']
        high_crowd_streets_gdf.crs = 'urn:ogc:def:crs:EPSG:28992'
        add_overlapping_streets(streets_to_avoid, high_crowd_streets_gdf, route_buffer, style_function, folium_map)

    folium.GeoJson(geometry.mapping(MultiPolygon(streets_to_avoid)), name="Areas overlapping with initial route",
                   style_function=style_function('red')).add_to(folium_map)

    request_params['options'] = {'avoid_polygons': geometry.mapping(MultiPolygon(streets_to_avoid))}
    route_detour = ors.directions(**request_params)

    folium.GeoJson(data=route_detour,
                   name='Recommended route',
                   style_function=style_function('green'),
                   overlay=True).add_to(folium_map)

    return get_text_instructions(route_detour)
    # instructions = [feature['properties']['segments'] for feature in route_detour['features']]

    # print(route_detour)
