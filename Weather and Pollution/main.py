#!/usr/bin/env python
import json, urllib.request, time, sys, datetime
from style_class import Style
from user_class import User
from network_class import Network_communication
import PySimpleGUI as sg

sg.theme('LightBlue6')
BG_COLOR = sg.theme_text_color()
TXT_COLOR = sg.theme_background_color()

#For Canvas, air quality 
    #Green color -  #19a627
    #Yellow color - #ecc836
    #Orange color - #c96526
    #Purple color - #cf3baa
#                               0~25    25~50   50~75   75~100  100~125 125~150 150~175 175~200 200~300 300~400 >400

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
#               SO2         NO2         PM10        PM2,5       O3          CO
# #Good	1	    [0; 20)	    [0; 40)	    [0; 20)	    [0; 10)	    [0; 60)	    [0; 4400)
# Fair	2	    [20; 80)	[40; 70)	[20; 50)	[10; 25)	[60; 100)	[4400; 9400)
# Moderate	3	[80; 250)	[70; 150)	[50; 100)	[25; 50)	[100; 140)	[9400-12400)
# Poor	4	    [250; 350)	[150; 200)	[100; 200)	[50; 75)	[140; 180)	[12400; 15400)
# Very Poor	5	⩾350	    ⩾200	    ⩾200	   ⩾75	       ⩾180	       ⩾15400

pollution_data = {
        "co": None,     #Carbon monoxide    #
        "no": None,     #Nitrogen monoxide  
        "no2": None,    #Nitrogen dioxide   #
        "o3": None,     #Ozone              #
        "so2": None,    #Sulphur dioxide    #
        "pm2_5": None,  #particulate matter and the 2.5 refers to size 2.5 micrometres or smaller   #
        "pm10": None,   #particulate matter and the 10 refers to size 10 micrometres or smaller     #
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

    global BG_COLOR
    global TXT_COLOR
    
    #BG_COLOR = sg.theme_text_color()
    #TXT_COLOR = sg.theme_background_color()
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
    middle_col3 = sg.Column([metric_row('feels_like',DEGREE_SIGN,"Feels like:"), metric_row('temp_min',DEGREE_SIGN,"Area temp min:"), 
                             metric_row('temp_max',DEGREE_SIGN,"Area temp max:"), metric_row('pressure',"Pa","Pressure:"), metric_row('humidity',"%", "Humidity:"), 
                             metric_row('visibility',"m","Visibility:")],
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
    #BG_COLOR = sg.theme_text_color()
    #TXT_COLOR = sg.theme_background_color()
    global BG_COLOR
    global TXT_COLOR
    current_time = datetime.datetime.now().strftime('%H:%M:%S')
    current_date = datetime.datetime.now().strftime('%d-%m-%Y')

    top_col1 = sg.Column([[sg.Text(text=current_date, background_color=BG_COLOR, text_color=TXT_COLOR, font=('Arial', 14), key="-date time-")],
                          [sg.Text(text=current_time, background_color=BG_COLOR, text_color=TXT_COLOR, font=('Arial', 14), pad=(10,0), key="-TIME-")]],element_justification='left',pad=(10, 5), expand_x=True,background_color=BG_COLOR)
    top_col2 = sg.Column([[sg.Text(weather_data['City name'], background_color=BG_COLOR, text_color=TXT_COLOR, font=('Arial', 25), justification="left", key='-city name-')]],pad=(10, 5), expand_x=True,background_color=BG_COLOR)

    top_layer = sg.Column([[top_col1, top_col2]],
                                background_color=BG_COLOR,expand_y=True, expand_x=True, key="-top layer-")
    

    middle_col1 = [metric_pollution_bar('co'), metric_pollution_bar('no'), metric_pollution_bar("no2"), metric_pollution_bar("o3"), metric_pollution_bar("so2"),
                              metric_pollution_bar("pm2_5"), metric_pollution_bar("pm10"), metric_pollution_bar("nh3")]    
    
    middle_col2 = [metric_pollution('CO','Carbon monoxide'), metric_pollution('NO','Nitrogen monoxide'), metric_pollution("NO2",'Nitrogen dioxide'),
                            metric_pollution("O3",'Ozone'), metric_pollution("SO2",'Sulphur dioxide'),
                            metric_pollution("PM2.5","Fine particulates 2.5 micrometers or smaller"),
                            metric_pollution("PM10","Inhalable particles, with diameters that are generally 10 micrometers and smaller"), 
                            metric_pollution("NH3","Ammonia")]                       
    #middle_layer = sg.Frame([middle_col1],)

    layout = [[top_layer],
              [middle_col1], 
              [middle_col2]]

    window = sg.Window(layout=layout,title="Weather",
                        element_justification='center',
                        margins=(0, 0),
                        grab_anywhere=True,
                        alpha_channel=0.8,
                        right_click_menu=[[''], ['Current Weather', "Current Pollution", "Forecast Weather", "Forecast Pollution","Change Place", 'Exit',]],
                        no_titlebar=True,
                        finalize=True,
                        location=win_location,
                        background_color=BG_COLOR)
    return window

def metric_row(data_in_weatherDic, symbol,text):
    """ Return a pair of labels for each metric """

    return [sg.Text(text, font=('Arial', 10), pad=(2, 0), size=(12, 1)),
            sg.Text(f"{weather_data[data_in_weatherDic]}{symbol}", font=('Arial', 10, 'bold'), pad=(0, 0), size=(6, 1), key=data_in_weatherDic)]
#0~25    25~50   50~75   75~100  100~125 125~150 150~175 175~200 200~300 300~400 >400
def color_decider(data):
    if pollution_data[data] < 25:
        color = '#008573'
    elif 25 < pollution_data[data] < 50:
        color = "#6ca672"
    elif 50 < pollution_data[data] < 75:
        color = "#27bf36"
    elif 75 < pollution_data[data] < 100:
        color = "#ffe342"
    elif 100 < pollution_data[data] < 125:
        color = "#ff9f46"
    elif 125 < pollution_data[data] < 150:
        color = "#f77c09"
    elif 150 < pollution_data[data] < 175:
        color = "#ed7272"
    elif 175 < pollution_data[data] < 200:
        color = "#d92222"
    elif 200 < pollution_data[data] < 300:
        color = "#a10e7c"
    elif 300 < pollution_data[data] < 400:
        color = "#730858"
    elif pollution_data[data] > 400:
        color = "#000000"
    return color

def metric_pollution_bar(data):
    color = color_decider(data)
    return sg.Canvas(background_color=f"{color}", size=(50,70), key=f"-{data}-",tooltip=f"{pollution_data[data]}")

def metric_pollution(data,text):
    global BG_COLOR
    global TXT_COLOR
    return sg.Text(data, background_color=BG_COLOR, text_color=TXT_COLOR, font=("Ariel", 10, "bold"),pad=(15, 0), tooltip=f"{text}", justification='left')

                               


def main(user,win_location):
    
    latitude, longitude = Network_communication.get_latitude_longitude(user)
    Network_communication.get_current_weather_data(latitude, longitude, user)
    Network_communication.get_current_pollution(latitude, longitude, user)
    Network_communication.get_forecast_weatherFor_5days_data(latitude, longitude, user)
    Network_communication.get_forcast_air_polution(latitude, longitude, user)
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
            sg.user_settings_set_entry('-win location-', window.current_location())
            windo_copy = window
            window = window_Current_weather_creation(win_location)
            windo_copy.close()
        elif event == "Current Pollution":
            sg.user_settings_set_entry('-win location-', window.current_location())
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




