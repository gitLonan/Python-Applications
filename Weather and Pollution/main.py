#!/usr/bin/env python
import json, urllib.request, time, sys, datetime, calendar
from style_class import Style
from user_class import User
from network_class import Network_communication
import PySimpleGUIQt as sg


    


def main(user):
    latitude, longitude = Network_communication.get_latitude_longitude(user)
    Network_communication.get_current_weather_data(latitude, longitude, user)
    Network_communication.get_weatherFor_5days_data(latitude, longitude, user)
    Network_communication.get_pollution_4days_data(latitude, longitude, user)





if __name__ == "__main__":
    user = User()
    user.set_place_name()
    user.set_Alpha2_code_for_country()
    user.set_API_key()
    main(user)




