#!/usr/bin/env python
import json, urllib.request, time, sys, datetime
from style_class import Style
from user_class import User
from network_class import Network_communication
import PySimpleGUI as sg

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
        "sunset": None, 
        "icon": None,
        "dt": None,
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
        print(weather_data)

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

def window_Current_weather_creation(win_location):
    print(win_location)
    """ Creating window for Current Weather and its layout """

    sg.theme('LightBlue6')
    BG_COLOR = sg.theme_text_color()
    TXT_COLOR = sg.theme_background_color()
    DEGREE_SIGN = u"\N{DEGREE SIGN}"

    #### Date object
    date_object = datetime.datetime.utcfromtimestamp(weather_data['dt'])
    year = date_object.year
    month = date_object.month
    day = date_object.day
    current_date = f'{day:02d}-{month:02d}-{year}'

    #Getting img from the weeb
    image = Network_communication.request_weather_icon(weather_data["icon"])

    #Getting sec,min,hour from the datetime module
    current_time = datetime.datetime.now().strftime('%H:%M:%S')
    #print(f'Current Time: {hour:02d}:{minute:02d}:{second:02d}')



    ################ THESE ARE KEYS FOR ALL THE THINGS #################
    # top_col1 -> -data time-   -time-
    # top_col2 -> -city name-
    # top_layer -> -top layer-

    # middle_col1 -> -image-  -weather description-
    # middle_col2 ->    
    # middle_col3 -> in func 'metric_row' -> -data_in_weatherDic- (name of the given metric form weather_data)
    # middle_layer -> -middle layer-

    

    top_col1 = sg.Column([[sg.Text(text=current_date, background_color=BG_COLOR, text_color=TXT_COLOR, font=('Arial', 14), key="-date time-")],
                          [sg.Text(text=current_time, background_color=BG_COLOR, text_color=TXT_COLOR, font=('Arial', 14), pad=(10,0), key="-TIME-")]],element_justification='left',pad=(10, 5), expand_x=True,background_color=BG_COLOR)
    top_col2 = sg.Column([[sg.Text(weather_data['City name'], background_color=BG_COLOR, text_color=TXT_COLOR, font=('Arial', 25), justification="left", key='-city name-')]],pad=(10, 5), expand_x=True,background_color=BG_COLOR)

    top_layer = sg.Column([[top_col1, top_col2]],
                                pad=(0,0),background_color=BG_COLOR,expand_y=True, expand_x=True, key="-top layer-")
    
    middle_col1 = sg.Column([[sg.Image(image, size=(150,100),background_color=BG_COLOR, key="-image-")],
                             [sg.Text(f"Weather: {weather_data['description']}",background_color=BG_COLOR,text_color=TXT_COLOR,pad=(10,0), key="-weather description-")]],background_color=BG_COLOR)
    middle_col2 = sg.Column([[sg.Text(f'{weather_data["temp"]}{DEGREE_SIGN}C', font=('Haettenschweiler', 60),background_color=BG_COLOR, text_color=TXT_COLOR,pad=((0, 0), (10, 10)))]],background_color=BG_COLOR)
    middle_col3 = sg.Column([metric_row('feels_like',DEGREE_SIGN,"Feels like:"), metric_row('temp_min',DEGREE_SIGN,"Area temp min:"), metric_row('temp_max',DEGREE_SIGN,"Area temp max:"), metric_row('pressure',"Pa","Pressure:"), metric_row('humidity',"%", "Humidity:"), metric_row('visibility',"m","Visibility:")],
                        pad=((10, 0), (5, 10)), key='RtCOL')
    
    middle_layer = sg.Column([[middle_col1, middle_col2, middle_col3]],
                                pad=(0,0),background_color=BG_COLOR, key="-middle layer-")

    

    layout = [[top_layer],
          [middle_layer],
          
          ]
    window = sg.Window(layout=layout,title="Weather",
                        element_justification='center',
                        margins=(0, 0),
                        grab_anywhere=True,
                        alpha_channel=0.8,
                        right_click_menu=[[''], ['Current Weather', "Current Pollution", "Forecast Weather", "Forecast Pollution","Change Place", 'Exit',]],
                        no_titlebar=True,
                        finalize=True,
                        location=win_location)
    
    return window

def window_current_polution_creation(win_location):
    BG_COLOR = sg.theme_text_color()
    TXT_COLOR = sg.theme_background_color()
    current_time = datetime.datetime.now().strftime('%H:%M:%S')
    current_date = datetime.datetime.now().strftime('%d-%m-%Y')
    top_col1 = sg.Column([[sg.Text(text=current_date, background_color=BG_COLOR, text_color=TXT_COLOR, font=('Arial', 14), key="-date time-")],
                          [sg.Text(text=current_time, background_color=BG_COLOR, text_color=TXT_COLOR, font=('Arial', 14), pad=(10,0), key="-TIME-")]],element_justification='left',pad=(10, 5), expand_x=True,background_color=BG_COLOR)
    top_col2 = sg.Column([[sg.Text(weather_data['City name'], background_color=BG_COLOR, text_color=TXT_COLOR, font=('Arial', 25), justification="left", key='-city name-')]],pad=(10, 5), expand_x=True,background_color=BG_COLOR)

    top_layer = sg.Column([[top_col1, top_col2]],
                                pad=(0,0),background_color=BG_COLOR,expand_y=True, expand_x=True, key="-top layer-")
    middle_col1 = sg.Column([[sg.Text("image", size=(10,5),background_color=BG_COLOR, key="-image2-")]])

    layout = [[top_layer],
              [middle_col1]]

    window = sg.Window(layout=layout,title="Weather",
                        element_justification='center',
                        margins=(0, 0),
                        grab_anywhere=True,
                        alpha_channel=0.8,
                        right_click_menu=[[''], ['Current Weather', "Current Pollution", "Forecast Weather", "Forecast Pollution","Change Place", 'Exit',]],
                        no_titlebar=True,
                        finalize=True,
                        location=win_location)
    return window

def metric_row(data_in_weatherDic, symbol,text):
    """ Return a pair of labels for each metric """

    return [sg.Text(text, font=('Arial', 10), pad=(2, 0), size=(12, 1)),
            sg.Text(f"{weather_data[data_in_weatherDic]}{symbol}", font=('Arial', 10, 'bold'), pad=(0, 0), size=(6, 1), key=data_in_weatherDic)]

def main(user,win_location):
    
    #latitude, longitude = Network_communication.get_latitude_longitude(user)
    #Network_communication.get_current_weather_data(latitude, longitude, user)
    #Network_communication.get_current_pollution(latitude, longitude, user)
    #Network_communication.get_forecast_weatherFor_5days_data(latitude, longitude, user)
    #Network_communication.get_forcast_air_polution(latitude, longitude, user)
    loading_current_weather(user)
    loading_pollution()

    
    window = window_Current_weather_creation(win_location)
    window_pollution = None
#'Current Weather', "Current Pollution", "Forecast Weather", "Forecast Pollution","Change Place"
    while True:
        event, values = window.read(timeout=200)
        if event == "Exit":
            sg.user_settings_set_entry('-win location-', window.current_location())
            break
        elif event == "Change Place":
            print("Ulazim ?")
            pass
        elif event == "Current Weather":
            windo_copy = window
            window = window_Current_weather_creation(win_location)
            windo_copy.close()
        elif event == "Current Pollution":
            windo_copy = window
            window = window_current_polution_creation(win_location)
            windo_copy.close()
        if event == sg.TIMEOUT_KEY:
            current_time = datetime.datetime.now().strftime('%H:%M:%S')
            window["-TIME-"].update(current_time)

if __name__ == "__main__":
    user = User()
    user.set_place_name()
    user.set_Alpha2_code_for_country()
    user.set_API_key()
    win_location = sg.user_settings_get_entry('-win location-', (None, None))
    #if not isinstance(win_location, tuple) or len(win_location) != 2 or not all(isinstance(val, (int, float)) for val in win_location):
        # Set a default location if the retrieved value is not valid
        #win_location = (None, None)
    
    print(win_location)
    main(user,win_location)




