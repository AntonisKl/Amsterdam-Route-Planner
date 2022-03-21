#!/usr/bin/env python
# coding: utf-8

# In[1]:


# In[2]:


import requests
import geojson
import geopandas as gpd
import matplotlib.pyplot as plt
import folium
import pandas as pd


# In[3]:


traffic = requests.get('http://web.redant.net/~amsterdam/ndw/data/reistijdenAmsterdam.geojson').content

traffic_geojson = geojson.loads(traffic)
traffic_geojson


# In[4]:


traffic_gdf = gpd.GeoDataFrame.from_features(traffic_geojson['features'])
traffic_gdf


# In[5]:


traffic_gdf['Timestamp'] = pd.to_datetime(traffic_gdf['Timestamp'])
# print(traffic_gdf['Timestamp'])


# In[6]:


traffic_gdf.dropna(subset=['Id', 'Velocity'], inplace=True)

idx = traffic_gdf.groupby('Id')['Timestamp'].transform(max) == traffic_gdf['Timestamp']
traffic_gdf = traffic_gdf[idx]
# traffic_gdf.index = traffic_gdf.index.map(str)
traffic_gdf
# traffic_gdf.groupby('Id').count()


# In[7]:


traffic_gdf['Velocity'] = traffic_gdf['Velocity'].astype(int)
traffic_gdf['Id'] = traffic_gdf['Id'].astype(str)
traffic_gdf


# In[8]:


fig, ax = plt.subplots(figsize=(35, 15))

ax.set_title('Vehicles velocity in streets of Amsterdam', fontsize=20)
traffic_gdf.plot(ax=ax, column='Velocity', cmap='RdYlGn', legend=True)

plt.show()


# In[38]:


m = folium.Map(
    location=[52.3676, 4.9041],
    tiles="cartodbpositron",
    zoom_start=13
)
m


# In[39]:



# linear = folium.colormap.LinearColormap(['green','yellow','red'], vmin=3., vmax=10.)
# linear
import branca
colorscale = branca.colormap.linear.YlOrRd_09.scale(0, 500)
def style_function(feature):
    # employed = traffic_gdf.get(int(feature["id"][-5:]), None)
    return {
        # "fillOpacity": 0.5,
        # "weight": 1,
        # 'color': 'black',
        "fillColor":  "black" if 'Velocity' not in feature['properties'] else colorscale(feature['properties']['Velocity']),
    }

folium.GeoJson(traffic_geojson, name="geojson", style_function=style_function).add_to(m)
# traffic_gdf.drop(columns=['Timestamp'],inplace=True)
# traffic_gdf.crs = 'urn:ogc:def:crs:OGC:1.3:CRS84'
# folium.Choropleth(
#     geo_data=traffic_geojson,  #json
#     name='choropleth',
#     data=traffic_gdf,
#     columns=['Name', 'Velocity'],  #columns to work on
#     key_on='feature.properties.Name',
#     fill_color='RdYlGn',
#     fill_opacity=1,
#     line_opacity=0.5,
#     legend_name="Unemployment scale"
# ).add_to(m)

folium.LayerControl().add_to(m)
m.save('map.html')

# In[ ]:




