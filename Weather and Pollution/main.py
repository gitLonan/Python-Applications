#!/usr/bin/env python
import json, urllib.request, time, sys, datetime
from style_class import Style
from user_class import User
from network_class import Network_communication
from parse_class import Parsed
import PySimpleGUI as sg
from io import BytesIO
from PIL import Image, ImageTk

sg.theme('LightBlue6')
BG_COLOR = sg.theme_text_color()
TXT_COLOR = sg.theme_background_color()

#For Canvas, air quality 
    #Green color -  #19a627
    #Yellow color - #ecc836
    #Orange color - #c96526
    #Purple color - #cf3baa
#                               0~25    25~50   50~75   75~100  100~125 125~150 150~175 175~200 200~300 300~400 >400





     

        
def window_Current_weather_creation(win_location):
    """ Creating window for `Current Weather` and its layout """

    def metric_row_current_weather(data_in_weatherDic, symbol,text):
        """ Return a pair of labels for each metric """

        return [sg.Text(text, font=('Arial', 10), pad=(2, 0), size=(12, 1)),
                sg.Text(f"{Parsed.weather_data[data_in_weatherDic]}{symbol}", font=('Arial', 10, 'bold'), pad=(0, 0), size=(7, 1), key=data_in_weatherDic)]

    global BG_COLOR
    global TXT_COLOR
    
    #BG_COLOR = sg.theme_text_color()
    #TXT_COLOR = sg.theme_background_color()
    DEGREE_SIGN = u"\N{DEGREE SIGN}"

    #### Date object
    date_object = datetime.datetime.utcfromtimestamp(Parsed.weather_data['dt'])
    year = date_object.year
    month = date_object.month
    day = date_object.day
    current_date = f'{day:02d}-{month:02d}-{year}'

    #Getting img from the weeb
    image = Network_communication.request_weather_icon(Parsed.weather_data["icon"])

    #Getting sec,min,hour from the datetime module
    current_time = datetime.datetime.now().strftime('%H:%M:%S')
   
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
    top_col2 = sg.Column([[sg.Text(Parsed.weather_data['City name'], background_color=BG_COLOR, text_color=TXT_COLOR, font=('Arial', 25), justification="left", key='-city name-')]],pad=(10, 5), expand_x=True,background_color=BG_COLOR)

    top_layer = sg.Column([[top_col1, top_col2]],
                                pad=(0,0),background_color=BG_COLOR,expand_y=True, expand_x=True, key="-top layer-")
    
    middle_col1 = sg.Column([[sg.Image(image, size=(150,100),background_color=BG_COLOR, key="-image-")],
                             [sg.Text(f"Weather: {Parsed.weather_data['description']}",background_color=BG_COLOR,text_color=TXT_COLOR,pad=(10,0), key="-weather description-")]],background_color=BG_COLOR)
    middle_col2 = sg.Column([[sg.Text(f'{Parsed.weather_data["temp"]}{DEGREE_SIGN}C', font=('Haettenschweiler', 60),background_color=BG_COLOR, text_color=TXT_COLOR,pad=((0, 0), (10, 10)))]],background_color=BG_COLOR)
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

    bottom_layer = [sg.Text(f"Last updated: {current_time}",font=('Arial', 10),text_color=TXT_COLOR,
                                 background_color=BG_COLOR,pad=(0,0), key="-current weather update time"),
                    sg.Button("Update", font=('Arial', 10), pad=(0,0),enable_events=True,  key="-current weather update-")]
    

    layout = [[top_layer],
          [middle_layer],
          [bottom_layer]
          ]
    window = sg.Window(layout=layout,title="Weather",
                        element_justification='left',
                        margins=(0, 0),
                        grab_anywhere=True,
                        alpha_channel=0.8,
                        right_click_menu=[[''], ['Current Weather', "Current Pollution", "Forecast Weather", "Forecast Pollution","Change Place", 'Exit',]],
                        no_titlebar=True,
                        finalize=True,
                        location=win_location,
                        background_color=BG_COLOR)
    
    return window

def window_current_polution_creation(win_location):
    """ Creating window layout for the current pollution """

    def metric_pollution_bar(data):
        color, air = color_decider(data)
        return sg.Canvas(background_color=f"{color}", size=(50,70), key=f"-{data}-",tooltip=f"{air}: {Parsed.pollution_data[data]}")

    def metric_pollution_chemical_symbol(data,text):
        global BG_COLOR
        global TXT_COLOR
        return sg.Text(data, background_color=BG_COLOR, text_color=TXT_COLOR, font=("Ariel", 10, "bold"),pad=(16, 0), tooltip=f"{text}", justification='left')

    #BG_COLOR = sg.theme_text_color()
    #TXT_COLOR = sg.theme_background_color()
    global BG_COLOR
    global TXT_COLOR
    current_time = datetime.datetime.now().strftime('%H:%M:%S')
    current_date = datetime.datetime.now().strftime('%d-%m-%Y')

    top_col1 = sg.Column([[sg.Text(text=current_date, background_color=BG_COLOR, text_color=TXT_COLOR, font=('Arial', 14), key="-date time-")],
                          [sg.Text(text=current_time, background_color=BG_COLOR, text_color=TXT_COLOR, font=('Arial', 14), pad=(10,0), key="-TIME-")]],element_justification='left',pad=(10, 5), expand_x=True,background_color=BG_COLOR)
    top_col2 = sg.Column([[sg.Text(Parsed.weather_data['City name'], background_color=BG_COLOR, text_color=TXT_COLOR, font=('Arial', 25), justification="left", key='-city name-')]],pad=(10, 5), expand_x=True,background_color=BG_COLOR)

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
                    sg.Button("Update", font=('Arial', 10), pad=(0,0),enable_events=True,  key="-current pollution update-")]
    layout = [[top_layer],
              [middle_col1], 
              [middle_col2],
              [bottom_layer]]

    window = sg.Window(layout=layout,title="Weather",
                        element_justification='left',
                        margins=(0, 0),
                        grab_anywhere=True,
                        alpha_channel=0.8,
                        right_click_menu=[[''], ['Current Weather', "Current Pollution", "Forecast Weather", "Forecast Pollution","Change Place", 'Exit',]],
                        no_titlebar=True,
                        finalize=True,
                        location=win_location,
                        background_color=BG_COLOR)
    return window

def window_forcast_weather_creation(win_location,days_weather):

    def metrics_days_layer(num):
                _ = datetime.date.today() + datetime.timedelta(num)
                day = _.strftime('%a')
                return sg.Text(day, background_color=BG_COLOR, text_color=TXT_COLOR, font=('Arial', 14),pad=(35, 0))

    def metrics_date_layer(num):
                _ = datetime.date.today() + datetime.timedelta(num)
                date = _.strftime('%d/%m')
                return sg.Text(date, background_color=BG_COLOR, text_color=TXT_COLOR, font=('Arial', 14),pad=(25, 0))
    
    def icon_provider(num):
                #print("GLEDAJ", days_weather[num])
                icon = Parsed.weather_data_forecast['icon'][f'{days_weather[num]}'][0]
                print(icon)
                filename = f"Weather and Pollution/icons/{icon}.png"
                return sg.Image(filename, size=(70,70),background_color=BG_COLOR, pad=(16,0))
        
    def description_provider(num):
                descr = Parsed.weather_data_forecast["description"][f'{days_weather[num]}'][0]
                return sg.Text(descr, background_color=BG_COLOR, text_color=TXT_COLOR, font=('Arial', 8),pad=(15, 0))

    def metric_max_temp(num):
                DEGREE_SIGN = u"\N{DEGREE SIGN}"
                return sg.Text(f"{num}{DEGREE_SIGN}C",background_color=BG_COLOR, text_color=TXT_COLOR, font=('Arial', 12),pad=(22,0))
    
    def metric_min_temp(num):
                DEGREE_SIGN = u"\N{DEGREE SIGN}"
                return sg.Text(f"{num}{DEGREE_SIGN}C",background_color=BG_COLOR, text_color=TXT_COLOR, font=('Arial', 12),pad=(26,0))
    

    global BG_COLOR
    global TXT_COLOR
    
    current_time = datetime.datetime.now().strftime('%H:%M:%S')
    current_date = datetime.datetime.now().strftime('%d-%m-%Y')

    top_col1 = sg.Column([[sg.Text(text=current_date, background_color=BG_COLOR, text_color=TXT_COLOR, font=('Arial', 14),key="-date time-")],
                          [sg.Text(text=current_time, background_color=BG_COLOR, text_color=TXT_COLOR, font=('Arial', 14),
                                    pad=(10,0), key="-TIME-")]],element_justification='left',pad=(10, 5),
                                      expand_x=True,background_color=BG_COLOR)
    top_col2 = sg.Column([[sg.Text(Parsed.weather_data['City name'], background_color=BG_COLOR, text_color=TXT_COLOR,
                                    font=('Arial', 25), justification="left", key='-city name-')]],pad=(10, 5),
                                      expand_x=True,background_color=BG_COLOR)

    top_layer = sg.Column([[top_col1, top_col2]],
                                background_color=BG_COLOR,expand_y=True, expand_x=True, key="-top layer-")
    days_layer = []
    for i in range(len(days_weather)):
         #print(i)
         days_layer.append(metrics_days_layer(i))
    dates_layers = []
    for i in range(len(days_weather)):
         #print(i)
         dates_layers.append(metrics_date_layer(i))
  
    icon_layer = []
    for i in range(len(days_weather)):
         #print(i)
         icon_layer.append(icon_provider(i))
  
    weather_type_layer = []
    for i in range(len(days_weather)):
         weather_type_layer.append(description_provider(i))

    
   
    bottom_layer = [sg.Text(f"Last updated: {current_time}",font=('Arial', 10),text_color=TXT_COLOR,
                                 background_color=BG_COLOR,pad=(0,0), key="-forecast weather update time"),
                    sg.Button("Update", font=('Arial', 10),
                                pad=(0,0),enable_events=True,  key="-forecast weather update-")]
    def max_temp(num):
         data = Parsed.weather_data_forecast["temp"][f'{days_weather[num]}']
         print(max(data))
         return max(data)
    def min_temp(num):
         data = Parsed.weather_data_forecast["temp"][f'{days_weather[num]}']
         print(min(data))
         return min(data)
    
    max_temp_layer = sg.Column([[metric_max_temp(max_temp(0)),metric_max_temp(max_temp(1)),metric_max_temp(max_temp(2)),metric_max_temp(max_temp(3)),metric_max_temp(max_temp(4)),metric_max_temp(max_temp(5))],
                                [metric_min_temp(min_temp(0)),metric_min_temp(min_temp(1)),metric_min_temp(min_temp(2)),metric_min_temp(min_temp(3)),metric_min_temp(min_temp(4)),metric_min_temp(min_temp(5))]],
                                  background_color=BG_COLOR)

    layout = [  [top_layer],
                [days_layer],
                [dates_layers],
                [icon_layer],
                [weather_type_layer],
                [max_temp_layer],
                [bottom_layer]
            ]
    window = sg.Window(layout=layout,title="Weather",
                        element_justification='left',
                        margins=(0, 0),
                        grab_anywhere=True,
                        alpha_channel=0.8,
                        right_click_menu=[[''], ['Current Weather', "Current Pollution", "Forecast Weather", "Forecast Pollution","Change Place", 'Exit',]],
                        no_titlebar=True,
                        finalize=True,
                        location=win_location,
                        background_color=BG_COLOR
                        )   #ovDE TREBA background_color=BG_COLOR
    
    return window

def window_forcast_pollution_creation(win_location, days_pollution):

    def metrics_days_layer(num):
                _ = datetime.date.today() + datetime.timedelta(num)
                day = _.strftime('%a')
                return sg.Text(day, background_color=BG_COLOR, text_color=TXT_COLOR, font=('Arial', 14),pad=(35, 0))

    def metrics_date_layer(num):
                _ = datetime.date.today() + datetime.timedelta(num)
                date = _.strftime('%d/%m')
                return sg.Text(date, background_color=BG_COLOR, text_color=TXT_COLOR, font=('Arial', 14),pad=(25, 0))
    
    def metric_pollution_bar(data, symbol):
        color, air = color_decider_forecast(data)
        if symbol == "co":
             symbol_text = 'CO-Carbon monoxide'
        elif symbol == "no":
             symbol_text = 'NO-Nitrogen monoxide'
        elif symbol == "no2":
             symbol_text = "NO2-Nitrogen dioxide"
        elif symbol == "o3":
             symbol_text = "O3-Ozone"
        elif symbol == "so2":
             symbol_text = "SO2-Sulphur dioxide"
        elif symbol == "pm2_5":
             symbol_text = "PM2.5-Fine particulates 2.5 micrometers or smaller"
        elif symbol == "pm10":
             symbol_text = "PM10-Inhalable particles, with diameters that are generally 10 micrometers and smaller"
        elif symbol == "nh3":
             symbol_text = "NH3-Ammonia"
        return sg.Canvas(background_color=f"{color}", size=(45,40), key=f"-{data}-",tooltip=f"{air}: {data} {symbol_text}")
                                                        #30,30 je prolazno
    def metric_symbol(num):
         return [sg.Text(num, background_color=BG_COLOR, text_color=TXT_COLOR, font=('Arial', 14),pad=((0, 10), (0,0)) )]
    global BG_COLOR
    global TXT_COLOR
    
    current_time = datetime.datetime.now().strftime('%H:%M:%S')
    current_date = datetime.datetime.now().strftime('%d-%m-%Y')

    top_col1 = sg.Column([[sg.Text(text=current_date, background_color=BG_COLOR, text_color=TXT_COLOR, font=('Arial', 14),key="-date time-")],
                          [sg.Text(text=current_time, background_color=BG_COLOR, text_color=TXT_COLOR, font=('Arial', 14),
                                    pad=(10,0), key="-TIME-")]],element_justification='left',pad=(10, 5),
                                      expand_x=True,background_color=BG_COLOR)
    top_col2 = sg.Column([[sg.Text(Parsed.weather_data['City name'], background_color=BG_COLOR, text_color=TXT_COLOR,
                                    font=('Arial', 25), justification="left", key='-city name-')]],pad=(10, 5),
                                      expand_x=True,background_color=BG_COLOR)

    top_layer = sg.Column([[top_col1, top_col2]],
                                background_color=BG_COLOR,expand_y=True, expand_x=True, key="-top layer-")

    bottom_layer = [sg.Text(f"Last updated: {current_time}",font=('Arial', 10),text_color=TXT_COLOR, background_color=BG_COLOR,pad=(0,0), key="-forecast weather update time"),
                    sg.Button("Update", font=('Arial', 10), pad=(0,0),enable_events=True,  key="-forecast pollution update-"),
                    sg.Text("Numbers represent averages for that day", font=('Arial', 10),text_color=TXT_COLOR, background_color=BG_COLOR,pad=(10,0))
                                ]

    days_layer = []
    dates_layers = []

    for i in range(len(days_pollution)):
         #print(i)
         days_layer.append(metrics_days_layer(i))
    
    for i in range(len(days_pollution)):
         #print(i)
         dates_layers.append(metrics_date_layer(i))

    
    

    ######here im using symbol index and day index to parse the nested dics in pollutioon_data_forecast
    """
        Logic: in for loop ill just get the chemical symbols for `Parsed.pollution_data_forecast` because they are keys for the nested dict in 
                `pollution_data_forest`
                In while loop first ill get rid of zeros because they'll skew the calculations in `average`, first `values` here im just getting
                to the list in nested dict that has that chemical symbol with its corresponding day and callculating average from the `list_values`. 
                By first adding to the `average_pollution` and then to the `days_average_pollution` ill get nested lists that represent cehmicals
                with each list lenght of 5 and each element in the list represents average for that day for that particular chemical element

    """
    day_index = 0
    symbol_index = 0
    average_pollution = []
    days_average_pollution = []
    
    chemical_symbols = []
    for key,value in enumerate(Parsed.pollution_data_forecast.items()):
          print(value[0])
          chemical_symbols.append(value[0])
    chemical_symbols.remove(chemical_symbols[-1])
    
    while True:
        values = Parsed.pollution_data_forecast[chemical_symbols[symbol_index]][f"{days_pollution[day_index]}"]
        list_values = [i for i in values if i != 0]
        #print(list_values) #ZeroDivisionError
        if sum(list_values) == 0:
            list_values = [0.01]
        average = round(sum(list_values) / len(list_values), 2)
        #print(average)
        average_pollution.append(average)
        day_index += 1
        #print(day_index, len(days_pollution))
        print("SYMBOL",chemical_symbols[symbol_index])
        if day_index == len(days_pollution):
            day_index = 0
            symbol_index += 1
            days_average_pollution.append(average_pollution)
            average_pollution = []
        if symbol_index == len(chemical_symbols):
             break
    
    pollution_layer = []
    pause_layer = []
    print(days_average_pollution)
    symbol_layer = []
    for i in chemical_symbols:
         symbol_layer.append(metric_symbol(i))
    
    
    """
        Logic: First in one passing of the list `days_average pollution` ill get first element from each of the 8 nested lists and create 'squares' in 
        metric_pollution_bar,  then ill just index the second element of every nested list and soo on till i get it to the end.

    """

    index_list = 0
    index_in_list = 0
    stop = 0
    while True:
        if index_in_list > 6:
             index_in_list = 6
        metric = days_average_pollution[index_list][index_in_list]
        print(metric)
        chemical_layer = [metric_pollution_bar(metric,chemical_symbols[index_list])]
        pause_layer.append(chemical_layer)
        index_list += 1
        if index_list == 8:
            index_list = 0
            index_in_list += 1
            pollution_layer.append(sg.Column(pause_layer, pad=(25,0),background_color=BG_COLOR))
            pause_layer = []
        if metric == days_average_pollution[-1][-1]:
            break


    layout = [  [top_layer],
                [days_layer],
                [dates_layers],
                [pollution_layer],
                [bottom_layer]
            ]
    window = sg.Window(layout=layout,title="Weather",
                        element_justification='left',
                        margins=(0, 0),
                        grab_anywhere=True,
                        alpha_channel=0.8,
                        right_click_menu=[[''], ['Current Weather', "Current Pollution", "Forecast Weather", "Forecast Pollution","Change Place", 'Exit',]],
                        no_titlebar=True,
                        finalize=True,
                        location=win_location,
                        background_color=BG_COLOR
                        )   #ovDE TREBA background_color=BG_COLOR
    
    return window

def window_change_user_creation(win_location, user):
    current_time = datetime.datetime.now().strftime('%H:%M:%S')
    current_date = datetime.datetime.now().strftime('%d-%m-%Y')

    top_layer = sg.Column([[sg.Text(text=current_date, background_color=BG_COLOR, text_color=TXT_COLOR, font=('Arial', 14),key="-date time-")],
                          [sg.Text(text=current_time, background_color=BG_COLOR, text_color=TXT_COLOR, font=('Arial', 14),
                                    pad=(10,0), key="-TIME-")]],element_justification='left',pad=(10, 5),
                                      expand_x=True,background_color=BG_COLOR)
    
    middle_layer = [sg.Text("Type the name of the place: ",background_color=BG_COLOR, font=('Arial', 10), text_color=TXT_COLOR, tooltip="Can be region, city, small city, small village"),
                sg.Input("...",background_color=BG_COLOR,font=('Arial', 10),text_color=TXT_COLOR, key="-place input-")
                ]

    layout = [  [top_layer],
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
                        location=win_location,
                        background_color=BG_COLOR)
    return window


def color_decider_forecast(data):
    """ Returns air string and color for the bars in `metrics_pollution_bar` """

    if data < 25:
        color = '#008573'
        air = "Good"
    elif 25 < data < 50:
        color = "#6ca672"
        air = "Good"
    elif 50 < data < 75:
        color = "#27bf36"
        air = "Moderate"
    elif 75 < data < 100:
        color = "#ffe342"
        air = "Moderate"
    elif 100 < data < 125:
        color = "#ff9f46"
        air = "Unhealthy for Sensitive Groups"
    elif 125 < data < 150:
        color = "#f77c09"
        air = "Unhealthy for Sensitive Groups"
    elif 150 < data < 175:
        color = "#ed7272"
        air = "Unhealthy"
    elif 175 < data < 200:
        color = "#d92222"
        air = "Unhealthy"
    elif 200 < data < 300:
        color = "#a10e7c"
        air = "Very Unhealthy"
    elif 300 < data < 400:
        color = "#730858"
        air = "Hazardous"
    elif data > 400:
        color = "#000000"
        air = "Hazardous"
    return color,air

def color_decider(data):
    """ Returns air string and color for the bars in `metrics_pollution_bar` """

    if Parsed.pollution_data[data] < 25:
        color = '#008573'
        air = "Good"
    elif 25 < Parsed.pollution_data[data] < 50:
        color = "#6ca672"
        air = "Good"
    elif 50 < Parsed.pollution_data[data] < 75:
        color = "#27bf36"
        air = "Moderate"
    elif 75 < Parsed.pollution_data[data] < 100:
        color = "#ffe342"
        air = "Moderate"
    elif 100 < Parsed.pollution_data[data] < 125:
        color = "#ff9f46"
        air = "Unhealthy for Sensitive Groups"
    elif 125 < Parsed.pollution_data[data] < 150:
        color = "#f77c09"
        air = "Unhealthy for Sensitive Groups"
    elif 150 < Parsed.pollution_data[data] < 175:
        color = "#ed7272"
        air = "Unhealthy"
    elif 175 < Parsed.pollution_data[data] < 200:
        color = "#d92222"
        air = "Unhealthy"
    elif 200 < Parsed.pollution_data[data] < 300:
        color = "#a10e7c"
        air = "Very Unhealthy"
    elif 300 < Parsed.pollution_data[data] < 400:
        color = "#730858"
        air = "Hazardous"
    elif Parsed.pollution_data[data] > 400:
        color = "#000000"
        air = "Hazardous"
    return color,air


# def proba():
#         lista = ["01d","02d","03d","04d","09d","10d","11d","13d","50d"]
#         for i in lista:
#             url = f"https://openweathermap.org/img/wn/{i}@2x.png"
#             with urllib.request.urlopen(url) as response:
#                 image_bytes = BytesIO(response.read()) #converting img to a byte like object
#                 image = Image.open(image_bytes)
#                 image.save(fp=f"Weather and Pollution/icons/{i}.png")                            

def main(user,win_location):

    latitude, longitude = Network_communication.get_latitude_longitude(user)
    Network_communication.get_current_weather_data(latitude, longitude, user)
    Network_communication.get_forecast_weatherFor_5days_data(latitude, longitude, user)
    Network_communication.get_current_pollution(latitude, longitude, user)
    Network_communication.get_forcast_air_polution(latitude, longitude, user)

    Parsed.loading_current_weather(user)
    Parsed.loading_pollution()

    days_pollution = Parsed.get_days_for_forecast(1)
    days_weather = Parsed.get_days_for_forecast(2)
    Parsed.loading_forecast_pollution(days_pollution)
    Parsed.loading_forecast_weather(days_weather,user)

    #print(days_weather)
    window = window_Current_weather_creation(win_location)
    
    window_pollution = None
#'Current Weather', "Current Pollution", "Forecast Weather", "Forecast Pollution","Change Place"
    while True:
        event, values = window.read(timeout=200)
        if event == "Exit":
            sg.user_settings_set_entry('-win location-', window.current_location())
            break

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

        elif event == "Forecast Weather":
            sg.user_settings_set_entry('-win location-', window.current_location())
            windo_copy = window
            window = window_forcast_weather_creation(win_location, days_weather)
            windo_copy.close()

        elif event == "Forecast Pollution":
            sg.user_settings_set_entry('-win location-', window.current_location())
            windo_copy = window
            window = window_forcast_pollution_creation(win_location, days_pollution)
            windo_copy.close()
        elif event == "Change Place":
            sg.user_settings_set_entry('-win location-', window.current_location())
            windo_copy = window
            window = window_change_user_creation(win_location, user)
            windo_copy.close()



        if event == "-forecast weather update-":
            latitude, longitude = Network_communication.get_latitude_longitude(user)
            Network_communication.get_forecast_weatherFor_5days_data(latitude, longitude, user)
            Parsed.loading_forecast_weather(days_weather, user)
            windo_copy = window
            window = window_forcast_weather_creation(win_location, days_weather)
            windo_copy.close()

        elif event == "-forecast pollution update-":
            latitude, longitude = Network_communication.get_latitude_longitude(user)
            Network_communication.get_forcast_air_polution(latitude, longitude, user)
            Parsed.loading_forecast_pollution(days_pollution)
            windo_copy = window
            window = window_forcast_pollution_creation(win_location, days_pollution)
            windo_copy.close()

        elif event == "-current pollution update-":
            latitude, longitude = Network_communication.get_latitude_longitude(user)
            Network_communication.get_current_pollution(latitude, longitude, user)
            Parsed.loading_pollution()
            windo_copy = window
            window = window_current_polution_creation(win_location, days_pollution)
            windo_copy.close()

        elif event == "-current weather update-":
            latitude, longitude = Network_communication.get_latitude_longitude(user)
            Network_communication.get_current_weather_data(latitude, longitude, user)     
            Parsed.loading_current_weather(user)
            windo_copy = window
            window = window_Current_weather_creation(win_location)
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



