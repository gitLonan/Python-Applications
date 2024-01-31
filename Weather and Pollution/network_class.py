import json, urllib.request, time
from style_class import Style
class Network_communication:

    def url_access(url):
        with urllib.request.urlopen(url) as response:
            body = response.read().decode('utf-8')
            status_code = response.getcode()
            if status_code == 200:
                return body
            
    def get_latitude_longitude(user)-> tuple[float, float]:
        """  Gets latitude and longitude based on user.place and user.alpha_2_code """

        url = f"http://api.openweathermap.org/geo/1.0/direct?q={user.place_name}&limit={5}&appid={user.api_key}"
        response = Network_communication.url_access(url)
        if response:
            result = json.loads(response)
            #print(json.dumps(result, indent=2))                    #for finding bugs in json.load   
            for i in range(len(result)):
                if result[i].get('country') == user.alpha_2_code:
                    latitude = result[i].get("lat")
                    longitude = result[i].get('lon')
                    return (latitude, longitude)
        else:
            print(f"{Style.RED}Wrong City name or wrong country name, pls look ISO 3166 for guidence on country codes{Style.END_COLOR}")
            
    def get_current_weather_data(latitude: float, longitude: float, user):
        """ Current weather for your location sends data to `all the json files` """

        url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={user.api_key}&units=metric"
        response = Network_communication.url_access(url)
        if response:
            result = json.loads(response)
            #print(json.dumps(result, indent=2))                    #for finding bugs in json.load  
            with open("Weather and Pollution/all the json files/Current Weather.json", "w") as f:
                json.dump(result, f, indent=2)

    def get_weatherFor_5days_data(latitude: float, longitude: float, user):
        """ Weather for the next 5 days(including today) sends to `all the json files` """

        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={user.api_key}&units=metric"
        response = Network_communication.url_access(url)
        if response:
            result = json.loads(response)
            #print(json.dumps(result, indent=2))                    #for finding bugs in json.load  
            with open("Weather and Pollution/all the json files/Weather_3h_step_5days.json", "w") as f:
                json.dump(result, f, indent=2)

    def get_pollution_4days_data(latitude: float, longitude: float, user):
        """ Pollution for the next 4days, all the negative particals -> `all the json files` """
        
        url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={latitude}&lon={longitude}&appid={user.api_key}"
        response = Network_communication.url_access(url)
        if response:
            result = json.loads(response)
            #print(json.dumps(result, indent=2))                    #for finding bugs in json.load  
            with open("Weather and Pollution/all the json files/Pollution_4days.json", "w") as f:
                json.dump(result, f, indent=2)
