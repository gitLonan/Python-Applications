import json, datetime
from user_class import User
import PySimpleGUI as sg
class Parsed:

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

    def get_days_for_forecast(ID):
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

    def loading_current_weather(user):
        """ Loads data form Current Weather.json file """

        Parsed.weather_data['City name'] = user.location
        with open("Weather and Pollution/all the json files/Current Weather.json", "r") as f:
            data = json.load(f)
            for key, value in data.items():
                #print(key, value, type(value))
                if type(value) == int:
                    if key in Parsed.weather_data:
                        Parsed.weather_data[key] = data[key]
                elif type(value) == dict:
                    for key_2 in value:
                        if key_2 in Parsed.weather_data:
                            Parsed.weather_data[key_2] = data[key][key_2]
                elif type(value) == list:
                    for i in value[0]:
                        if i in Parsed.weather_data:
                        
                            Parsed.weather_data[i] = value[0][i]
            #print(Parsed.weather_data)

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
                        if key in Parsed.pollution_data:
                            Parsed.pollution_data[key] = val
            #extracting information from the components dict and adding to our pollution data
            for key,value in components_key.items():
                if key in Parsed.pollution_data:
                    Parsed.pollution_data[key] = value
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

                        if day_str not in Parsed.pollution_data_forecast[key]:
                            # If the key does not exist, initialize it with an empty list, if there isnt blank nested dict of that day its added
                            Parsed.pollution_data_forecast[key][day_str] = []
                        else:
                            Parsed.pollution_data_forecast[key][day_str].append(val)
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
        for i in Parsed.weather_data_forecast:
            if Parsed.weather_data_forecast != Parsed.weather_data_forecast['City name']:
                Parsed.weather_data_forecast[i] = {}
        Parsed.weather_data_forecast['City name'] = user.location
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
                    Parsed.weather_data_forecast['description'][day_str] = []
                    Parsed.weather_data_forecast['icon'][day_str] = []
                    Parsed.weather_data_forecast["temp"][day_str] = []
                    Parsed.weather_data_forecast["speed"][day_str] = []
                #This will will change current day if it is diffirent, soo the above code triggers only when the `current_intervalIn_a_day`
                    #passes to the next day 
                if current_day != current_intervalIn_a_day:
                    current_day = current_intervalIn_a_day
                
                #Just appends the values based on index of nested dicts of components
                #if len(days_weather) == 6:
                Parsed.weather_data_forecast['description'][day_str].append(value[index_of_nested_dicts_of_components]["weather"][0]['description'])
                Parsed.weather_data_forecast['icon'][day_str].append(value[index_of_nested_dicts_of_components]['weather'][0]['icon'])
                Parsed.weather_data_forecast["temp"][day_str].append(value[index_of_nested_dicts_of_components]['main']['temp'])
                Parsed.weather_data_forecast["speed"][day_str].append(value[index_of_nested_dicts_of_components]['wind']['speed'])
                #else: pass
                
                #print(value[index_of_nested_dicts_of_components]["weather"][0]['description'])
                try:
                    checking_for_next_day = datetime.datetime.utcfromtimestamp(value[index_of_nested_dicts_of_components+1]['dt'])
                except IndexError:
                    pass

                if checking_for_next_day.day != current_intervalIn_a_day:
                    day_index +=1
                if index_of_nested_dicts_of_components+1 >= len(data['list']):
                    
                    break
                index_of_nested_dicts_of_components += 1 
            #print(Parsed.weather_data_forecast)