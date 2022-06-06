from pathlib import Path
import os 
import folium
from folium import plugins

import matplotlib.pyplot as plt
import numpy as np
import requests
import json
import pandas as pd

import config   


# import variable token from config.py
token = config.token

# I want to get the list of electric motoscooters in the city of Paris.

# def find_electric_motos():
def find_electric_motos(lat,lng):

    # show on map
    url = 'https://api.roote.io/realtime/'+str(lat)+','+str(lng)+'/freefloat/motorscooter'+'?token='+ token
    response = requests.get(url)
    data = response.json()
    error_dic = {'message': 'No result'}
    if data == error_dic:
        return 0 # error
    else:
        df = pd.DataFrame(data)
        df['provider_name'] = df.provider.apply(lambda x: x['name'])
        df.drop(columns=['provider'], inplace=True)
        df.drop(columns=['id'], inplace=True)

        # Create a map using Stamen Terrain as the basemap
        m = folium.Map(location=[lat, lng],
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
        # m
        path_map = 'templates/map'+str(lat)+','+str(lng)+'.html'
        m.save(path_map)
        # return to end the "main" function 
        return 1

########################### FLASK MODULES ##############################: 


from flask import Flask, render_template, flash, Response, redirect, request, url_for, send_from_directory
from werkzeug.utils import secure_filename
from flask_ngrok import run_with_ngrok
from pathlib import Path



def create_app():
    app = Flask(__name__)  # Creation of the app
    app.secret_key = "motorscooter"  # Key
    run_with_ngrok(app)
    # Home page
    @app.route('/') # when you go to the home page 
    def request_electric():
        # when the app restarts we want to delete all the files in the templates folder, except the map.html
        for file in Path('templates').glob('*'):
            if file.name != 'map.html':
                os.remove(file)
        return render_template('map.html')

    # I want to run find_electric_motos(lat,lng) when I run the app with domain_name.io/lat,lng where lat and lng are the coordinates user wants to see

    @app.route('/<lat>,<lng>')
    def request_electric_lat_lng(lat,lng):
        find_electric_motos(lat,lng) 
        path = 'map'+str(lat)+','+str(lng)+'.html'
        return render_template(path)

    
    # return
    return app


    