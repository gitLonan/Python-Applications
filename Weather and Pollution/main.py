#!/usr/bin/env python
import json, urllib.request, time, sys, datetime, calendar
from style_class import Style
from user_class import User
from network_class import Network_communication
import PySimpleGUIQt as sg

weather_data = {
        "City name": "No information",
        "speed": None, #wind_speed
        "description": "None",
        "temp": None,
        "feels_like": None,
        "temp_min": None,
        "temp_max": None,
        "pressure": None,
        "humidity": None,
        "visibility": None,
        "country": "None",
        "timezone": None,
        "sunrise": None,
        "sunset": None 
}


def loading_current_weather(user):
    """ Loads data form Current Weather.json file """
    
    weather_data['City name'] = user.location
    with open("Weather and Pollution/all the json files/Current Weather.json", "r") as f:
        data = json.load(f)
        for key, value in data.items():
            #print(key, value, type(value))
            if type(value) == int:
                if key in weather_data:
                    weather_data[key] = data[key]
            elif type(value) == dict:
                for key_2 in value:
                    if key_2 in weather_data:
                        weather_data[key_2] = data[key][key_2]
            elif type(value) == list:
                for i in value[0]:
                    if i in weather_data:
                        print(i, weather_data[i])
                        weather_data[i] = value[0][i]

        print(weather_data)

def main(user):
    latitude, longitude = Network_communication.get_latitude_longitude(user)
    #Network_communication.get_current_weather_data(latitude, longitude, user)
    #Network_communication.get_weatherFor_5days_data(latitude, longitude, user)
    #Network_communication.get_pollution_4days_data(latitude, longitude, user)





if __name__ == "__main__":
    user = User()
    user.set_place_name()
    user.set_Alpha2_code_for_country()
    user.set_API_key()
    loading_current_weather(user)
    main(user)




