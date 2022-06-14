import requests
import pandas as pd
import folium
from map import display_map

import config 
token = config.token
api_key = config.api_key

def nearest_electric_bike(lat, lng):
    url = 'https://api.roote.io/realtime/'+str(lat)+','+str(lng)+'/freefloat/motorscooter'+'?token='+token
    response = requests.get(url)
    data = response.json()
    error_dic = {'message': 'No result'}
    if data == error_dic:
        # create empty dataframe
        df_error = pd.DataFrame()

        print('No result')
        return df_error, 0  # error
    else:
        df = pd.DataFrame(data)

        df['provider_name'] = df.provider.apply(lambda x: x['name'])
        df.drop(columns=['provider'], inplace=True)
        df.drop(columns=['id'], inplace=True)
        # df.head() 
        return df, 1  # no error

def address_search(address,api_key):
    """
    Displays a map of the nearest electric bike station to the user's address (using the HERE API)
    """
    # Get the latitude and longitude of the user's address
    url = 'https://geocode.search.hereapi.com/v1/geocode?q=' + address + '&apiKey=' + api_key
    response = requests.get(url)
    data = response.json()
    if data['items'] == []:
        status = 0
        lat,lng = 0,0
        print('No adress found')
    else:
        status = 1
        lat = data['items'][0]['position']['lat']
        lng = data['items'][0]['position']['lng']

    return status, lat, lng
