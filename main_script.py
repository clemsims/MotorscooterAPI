import config   

import os 
import folium
from folium import plugins

import matplotlib.pyplot as plt
import numpy as np
import requests
import json
import pandas as pd
import cv2 as cv
import os

# import variable token from config.py
token = config.token

# I want to get the list of electric motoscooters in the city of Paris.
lat = str(48.85524)
lng = str(2.34585)
# show on map
url = 'https://api.roote.io/realtime/'+lat+','+lng+'/freefloat/motorscooter'+'?token='+ token
response = requests.get(url)
data = response.json()

df = pd.DataFrame(data)

df['provider_name'] = df.provider.apply(lambda x: x['name'])
df.drop(columns=['provider'], inplace=True)
df.drop(columns=['id'], inplace=True)

# Create a map using Stamen Terrain as the basemap
m = folium.Map(location=[48.85524, 2.34585],
               tiles = 'OpenStreetMap', zoom_start=17)

# Add marker for each point in df with proper title 
for i in range(len(df)):
    if df.iloc[i]['provider_name'] == 'Cooltra':
        popup_name = df.iloc[i]['provider_name'] + ' ' + str(df.iloc[i]['battery'])+ '%' + ' left'
        folium.Marker(location=[df.lat[i], df.lng[i]],
                    popup=popup_name,
                    icon=folium.Icon(color='lightblue')).add_to(m)
    elif df.iloc[i]['provider_name'] == 'Yego':
        popup_name = df.iloc[i]['provider_name'] + ' ' + str(df.iloc[i]['battery'])+ '%' + ' left'
        folium.Marker(location=[df.lat[i], df.lng[i]],
                    popup=popup_name,
                    icon=folium.Icon(color='green')).add_to(m)
    elif df.iloc[i]['provider_name'] == 'Cityscoot':
        popup_name = df.iloc[i]['provider_name'] + ' ' + str(df.iloc[i]['battery'])+ '%' + ' left'
        folium.Marker(location=[df.lat[i], df.lng[i]],
                    popup=popup_name,
                    icon=folium.Icon(color='blue')).add_to(m)
    else:
        popup_name = df.iloc[i]['provider_name'] + ' ' + str(df.iloc[i]['battery'])+ '%' + ' left'
        folium.Marker(location=[df.lat[i], df.lng[i]],
                    popup=popup_name,
                    icon=folium.Icon(color='red')).add_to(m)
                    

# Display map
m

m.save('map.html')