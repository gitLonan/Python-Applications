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
weather_data_forecast = {
        "City name": "No information",
        "speed": {}, #wind_speed
        "description": {}, 
        "temp": {},         
        "icon": {},
        #"dt": [],
        # "pressure": [],
        # "humidity": [],
        # "visibility": [],
        # "temp_min": [],      
        # "temp_max": [], 
}  


pollution_data = {
        "co": None,     #Carbon monoxide    #
        "no": None,     #Nitrogen monoxide  
        "no2": None,    #Nitrogen dioxide   #
        "o3": None,     #Ozone              #
        "so2": None,    #Sulphur dioxide    #
        "pm2_5": None,  #particulate matter and the 2.5 refers to size 2.5 micrometres or smaller   #
        "pm10": None,   #particulate matter and the 10 refers to size 10 micrometres or smaller     #
        "nh3": None,     #Ammonia
        "dt": None
}

pollution_data_forecast = {
        "co": {},     #Carbon monoxide    #
        "no": {},     #Nitrogen monoxide  
        "no2": {},    #Nitrogen dioxide   #
        "o3": {},     #Ozone              #
        "so2": {},    #Sulphur dioxide    #
        "pm2_5": {},  #particulate matter and the 2.5 refers to size 2.5 micrometres or smaller   #
        "pm10": {},   #particulate matter and the 10 refers to size 10 micrometres or smaller     #
        "nh3": {},     #Ammonia
        "dt": {}
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
                    components_key = val
                elif type(val) == int:
                    if key in pollution_data:
                        pollution_data[key] = val
        #extracting information from the components dict and adding to our pollution data
        for key,value in components_key.items():
            if key in pollution_data:
                pollution_data[key] = value
        #print(pollution_data)
                
def loading_forecast_pollution(days_pollution): 
    """
        Loading all the values from `Forecast Pollution.json` to thier respected nested dicts in `pollution_data_forecast`
        Now they are ready to be parsed, for further logical reasoning behind this algo, look for the comments between steps
        they will clarify further details

        day_pollution : list -> getting the list of days by which ill compare the current time of data['list']['dt']

    """
    day_index = 0
    checking_for_next_day = 0
    with open("Weather and Pollution/all the json files/Forecast Pollution.json", "r") as file:
        data = json.load(file)
        #get to the list that is bascially the whole file
        for key, value in data.items():
            if type(value) == list:
                break
        index_of_nested_dicts_of_components = 0
        while True:
            # by the index above going through the list in data for the key `components``
            list_component = value[index_of_nested_dicts_of_components]['components']

            #in every index in the list i need to check for key `dt`, because that will determine further down if the key `component`
            #is in the current day or next
            date_object = datetime.datetime.utcfromtimestamp(value[index_of_nested_dicts_of_components]['dt'])
            day = date_object.day

            for key, val in list_component.items():
                if day == days_pollution[day_index]:

                    day_str = str(days_pollution[day_index]) #just soo its compact, basically index of the day that i will be comparing

                    if day_str not in pollution_data_forecast[key]:
                        # If the key does not exist, initialize it with an empty list, if there isnt blank nested dict of that day its added
                        pollution_data_forecast[key][day_str] = []
                    else:
                        pollution_data_forecast[key][day_str].append(val)
            try:
                checking_for_next_day = datetime.datetime.utcfromtimestamp(value[index_of_nested_dicts_of_components+1]['dt'])
            except IndexError:
                break
            
            if checking_for_next_day.day != day:
                day_index +=1
            if index_of_nested_dicts_of_components+1 > len(data['list']):
                break
            index_of_nested_dicts_of_components += 1
        #print(pollution_data_forecast)

def loading_forecast_weather(days_weather,user):
    """
    Did diffirent approach to `forecast weather` then `forecast pollution`, wanted to design a diffrent algo and see which one is more
    readable and understandable, this second one i wrote much faster, maybe because i had a clear picture in my mind what i wanted to do

    """
    weather_data_forecast['City name'] = user.location
    day_index = 0
    checking_for_next_day = 0
    with open("Weather and Pollution/all the json files/Forecast_weather_3h_step_5days.json", "r") as file:
        data = json.load(file)
        #get to the list that is bascially the whole file
        for key, value in data.items():
            if type(value) == list:
                break

        current_day = 0
        index_of_nested_dicts_of_components = 0
        while True:

            date_object = datetime.datetime.utcfromtimestamp(value[index_of_nested_dicts_of_components]['dt'])
            current_intervalIn_a_day = date_object.day

            day_str = str(days_weather[day_index]) #just soo its compact, basically index of the day that i will be comparing

            #if current_day is diffirent than i will add another sub dict to the appropriate keys
            if current_day != current_intervalIn_a_day:
                weather_data_forecast['description'][day_str] = []
                weather_data_forecast['icon'][day_str] = []
                weather_data_forecast["temp"][day_str] = []
                weather_data_forecast["speed"][day_str] = []
            #This will will change current day if it is diffirent, soo the above code triggers only when the `current_intervalIn_a_day`
                #passes to the next day 
            if current_day != current_intervalIn_a_day:
                current_day = current_intervalIn_a_day

            #Just appends the values based on index of nested dicts of components
            weather_data_forecast['description'][day_str].append(value[index_of_nested_dicts_of_components]["weather"][0]['description'])
            weather_data_forecast['icon'][day_str].append(value[index_of_nested_dicts_of_components]['weather'][0]['icon'])
            weather_data_forecast["temp"][day_str].append(value[index_of_nested_dicts_of_components]['main']['temp'])
            weather_data_forecast["speed"][day_str].append(value[index_of_nested_dicts_of_components]['wind']['speed'])
            
            print(value[index_of_nested_dicts_of_components]["weather"][0]['description'])
            try:
                checking_for_next_day = datetime.datetime.utcfromtimestamp(value[index_of_nested_dicts_of_components+1]['dt'])
            except IndexError:
                pass

            if checking_for_next_day.day != current_intervalIn_a_day:
                day_index +=1
            if index_of_nested_dicts_of_components+1 >= len(data['list']):
                print("breakuje u dole kod len(od kurac)")
                break
            index_of_nested_dicts_of_components += 1 
        print(weather_data_forecast)

#prodjem kroz fajl da nadjem sve razlicite dane, onda idem opet kroz fajl i sve dok je vreme u tom danu ono ce dodavati u listu, a kad 
    #ne bude vise onda cemo dodati novu sub listu ?
def get_days_from_forecast(ID):
    """
        before parsing through the json files to get the data, first i get the days
        Logic: since pollution has commponents every 1hour, i neeed to check if its still the same day, if it is ill add a list to a 
        chemical element which will contain dict with lists, every key will be a day, and values will be values for that day 
    """

    number_of_days = []
    current_day = ''
    if ID == 1:
        folderFrom_which_to_scrape = 'Forecast Pollution'
    elif ID == 2:
        folderFrom_which_to_scrape = 'Forecast_weather_3h_step_5days'

    with open(f"Weather and Pollution/all the json files/{folderFrom_which_to_scrape}.json", "r") as file:
        data = json.load(file)
        for key, value in data.items():
            if type(value) == list:
                break
        for i in value:
            for key, val in i.items():
                if key == "dt":
                    date_object = datetime.datetime.utcfromtimestamp(val)
                    day = date_object.day
                    if day != current_day:
                        current_day = day
                        number_of_days.append(current_day)
    #print(number_of_days)
    #print(type(number_of_days))
    return number_of_days      

        
def window_Current_weather_creation(win_location):
    print(win_location)
    """ Creating window for `Current Weather` and its layout """

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



    ################ THESE ARE KEYS #################
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
    middle_col3 = sg.Column([   metric_row_current_weather('feels_like',DEGREE_SIGN,"Feels like:"),
                                metric_row_current_weather('temp_min',DEGREE_SIGN,"Area temp min:"), 
                                metric_row_current_weather('temp_max',DEGREE_SIGN,"Area temp max:"),
                                metric_row_current_weather('pressure',"Pa","Pressure:"),
                                metric_row_current_weather('humidity',"%", "Humidity:"), 
                                metric_row_current_weather('visibility',"m","Visibility:"),
                                metric_row_current_weather('speed',"km/h","Wind speed:")
                                ],
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
    """ Creating window layout for the current pollution """

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
    

    middle_col1 = [ metric_pollution_bar('co'),
                    metric_pollution_bar('no'),
                    metric_pollution_bar("no2"), 
                    metric_pollution_bar("o3"), 
                    metric_pollution_bar("so2"),
                    metric_pollution_bar("pm2_5"), 
                    metric_pollution_bar("pm10"), 
                    metric_pollution_bar("nh3")
                ]    

    middle_col2 =  [    metric_pollution_chemical_symbol('CO','Carbon monoxide'),
                        metric_pollution_chemical_symbol('NO','Nitrogen monoxide'),
                        metric_pollution_chemical_symbol("NO2",'Nitrogen dioxide'),
                        metric_pollution_chemical_symbol("O3",'Ozone'),
                        metric_pollution_chemical_symbol("SO2",'Sulphur dioxide'),
                        metric_pollution_chemical_symbol("PM2.5","Fine particulates 2.5 micrometers or smaller"),
                        metric_pollution_chemical_symbol("PM10","Inhalable particles, with diameters that are generally 10 micrometers and smaller"), 
                        metric_pollution_chemical_symbol("NH3","Ammonia")
                    ]
                       
    #middle_layer = sg.Frame([middle_col1],)

    bottom_layer = [sg.Text(f"Last updated: {current_time}",font=('Arial', 10),text_color=TXT_COLOR,
                                 background_color=BG_COLOR,pad=(0,0), key="-current pollution update time"),
                    sg.Text("Update", font=('Arial', 10),text_color=TXT_COLOR, background_color=BG_COLOR, 
                                pad=(0,0), justification='right', key="-current pollution update-")]
    layout = [[top_layer],
              [middle_col1], 
              [middle_col2],
              [bottom_layer]]

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

def metric_row_current_weather(data_in_weatherDic, symbol,text):
    """ Return a pair of labels for each metric """

    return [sg.Text(text, font=('Arial', 10), pad=(2, 0), size=(12, 1)),
            sg.Text(f"{weather_data[data_in_weatherDic]}{symbol}", font=('Arial', 10, 'bold'), pad=(0, 0), size=(7, 1), key=data_in_weatherDic)]
#0~25    25~50   50~75   75~100  100~125 125~150 150~175 175~200 200~300 300~400 >400
def color_decider(data):
    """ Returns air string and color for the bars in `metrics_pollution_bar` """

    if pollution_data[data] < 25:
        color = '#008573'
        air = "Good"
    elif 25 < pollution_data[data] < 50:
        color = "#6ca672"
        air = "Good"
    elif 50 < pollution_data[data] < 75:
        color = "#27bf36"
        air = "Moderate"
    elif 75 < pollution_data[data] < 100:
        color = "#ffe342"
        air = "Moderate"
    elif 100 < pollution_data[data] < 125:
        color = "#ff9f46"
        air = "Unhealthy for Sensitive Groups"
    elif 125 < pollution_data[data] < 150:
        color = "#f77c09"
        air = "Unhealthy for Sensitive Groups"
    elif 150 < pollution_data[data] < 175:
        color = "#ed7272"
        air = "Unhealthy"
    elif 175 < pollution_data[data] < 200:
        color = "#d92222"
        air = "Unhealthy"
    elif 200 < pollution_data[data] < 300:
        color = "#a10e7c"
        air = "Very Unhealthy"
    elif 300 < pollution_data[data] < 400:
        color = "#730858"
        air = "Hazardous"
    elif pollution_data[data] > 400:
        color = "#000000"
        air = "Hazardous"
    return color,air

def metric_pollution_bar(data):
    color, air = color_decider(data)
    return sg.Canvas(background_color=f"{color}", size=(50,70), key=f"-{data}-",tooltip=f"{air}: {pollution_data[data]}")

def metric_pollution_chemical_symbol(data,text):
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
    days_pollution = get_days_from_forecast(1)
    days_weather = get_days_from_forecast(2)

    loading_forecast_pollution(days_pollution)
    loading_forecast_weather(days_weather,user)

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




