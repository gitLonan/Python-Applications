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

pollution_data = {
        "co": None,     #Carbon monoxide
        "no": None,     #Nitrogen monoxide
        "no2": None,    #Nitrogen dioxide
        "o3": None,     #Ozone
        "so2": None,    #Sulphur dioxide
        "pm2_5": None,  #particulate matter and the 2.5 refers to size 2.5 micrometres or smaller
        "pm10": None,   #particulate matter and the 10 refers to size 10 micrometres or smaller
        "nh3": None     #Ammonia

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
                       
                        weather_data[i] = value[0][i]
        #print(weather_data)

def loading_pollution():
    with open("Weather and Pollution/all the json files/Current Pollution.json", "r") as f:
        data = json.load(f)
        #get to the dict thats raping dicts with list called ->`list` in json
        for key, value in data.items():
            if type(value) == list:
                break
        #getting to the key called components
        for i in value:
            for key, val in i.items():
                if key == 'components':
                    break
        #extracting information from the components dict and adding to our pollution data
        for key,value in val.items():
            if key in pollution_data:
                pollution_data[key] = value
           

        print(pollution_data)


def main(user):
    latitude, longitude = Network_communication.get_latitude_longitude(user)
    #Network_communication.get_current_weather_data(latitude, longitude, user)
    #Network_communication.get_current_pollution(latitude, longitude, user)
    #Network_communication.get_forecast_weatherFor_5days_data(latitude, longitude, user)
    #Network_communication.get_forcast_air_polution(latitude, longitude, user)




if __name__ == "__main__":
    user = User()
    user.set_place_name()
    user.set_Alpha2_code_for_country()
    user.set_API_key()
    loading_current_weather(user)
    loading_pollution()
    main(user)




