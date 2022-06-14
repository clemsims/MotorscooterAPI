import os 
import folium
from folium import plugins
import numpy as np
import requests
import json
import pandas as pd

import config   

from nearest import nearest_electric_bike, address_search
from map import display_map

# import variable token from config.py
token = config.token
api_key = config.api_key

# I want to get the list of electric motoscooters in the city of Paris.

def find_electric_motos(lat,lng):
                        
    df, status = nearest_electric_bike(lat,lng)
    if status == 0: # error
        return 0
    else:
        m = display_map(lat,lng,df)
        path_map = 'templates/map'+str(lat)+','+str(lng)+'.html'
        m.save(path_map)
        # return to end the "main" function 
        return 1

########################### FLASK MODULES ##############################: 


from flask import Flask, render_template, flash, Response, redirect, request, url_for, send_from_directory
from pathlib import Path

def create_app():
    app = Flask(__name__)  # Creation of the app
    app.secret_key = "motorscooter"  # Key
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
        status = find_electric_motos(lat,lng) 
        if status == 0:
            flash('No electric moto was found in this area')
            return render_template('map.html')
        else:
            path = 'map'+str(lat)+','+str(lng)+'.html'
            return render_template(path)
    
    # when i type the address in the search bar, i want to get the coordinates of the address using "nearest_electric_bike_search(address,api_key)": 
    @app.route('/search/<address>')
    def request_electric_address(address):
        # when the app restarts we want to delete all the files in the templates folder, except the map.html
        for file in Path('templates').glob('*'):
            if file.name != 'map.html':
                os.remove(file)
        stat,lat,lng = address_search(address,api_key)
        if stat == 0:
            flash('Error: No address found')
            return render_template('map.html')

        else: # stat == 1 # no error: we found the address! 
            flash('The address you searched for is: '+address)
            flash('The coordinates of the address are: '+str(lat)+','+str(lng))
                
            status = find_electric_motos(lat,lng)
            if status == 0:
                flash('No electric moto was found in this area')
                # check if lat,lng corresponds to an address in Paris:
                if lat > 48.8 and lat < 51.0 and lng > 2.35 and lng < 3.5:
                    flash('Hint: The address you searched for is in Paris but no electric moto was found in this area')
                else:
                    flash('Warning: The address you searched for is probably not in Paris, let s try entering Paris,France, at the end of the address')
                    # let's try adding 'Paris, France' at the end of the address
                    stat,lat,lng = address_search(address+', Paris, France',api_key)
                    if stat == 0:
                        flash('Whoops: no address was found, even after adding Paris, France at the end of the address')
                        return render_template('map.html')
                    else: # stat == 1 # no error: we now have found an address!
                        flash('The address you searched for is: '+address+', Paris, France')
                        flash('The coordinates of the address are: '+str(lat)+','+str(lng))
                        status = find_electric_motos(lat,lng)
                        if status == 0:
                            flash('No electric moto was found in this new area, now in Paris')
                        else: # status == 1 # no error: we now have found bikes for this address in Paris
                            path = 'map'+str(lat)+','+str(lng)+'.html'
                            return render_template(path)

            else: # no issue: we found bikes for this address and proceed
                path = 'map'+str(lat)+','+str(lng)+'.html'
                return render_template(path)
    return app