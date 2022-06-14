import folium 
import pandas as pd
def display_map(lat, lng, df):

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
    # add a marker for the user's location
    folium.Marker(location=[lat, lng],
                    popup='You are here',
                    icon=folium.Icon(color='red')).add_to(m)
    return m

