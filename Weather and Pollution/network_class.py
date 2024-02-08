import json, urllib.request, time
from style_class import Style
from io import BytesIO
from PIL import Image, ImageTk
import PySimpleGUI as sg
class Network_communication:

    def url_access(url):
        with urllib.request.urlopen(url) as response:
            body = response.read().decode('utf-8')
            status_code = response.getcode()
            try:
                if status_code == 200:
                    return body
            except:
                pass
            
    def get_latitude_longitude(user)-> tuple[float, float]:
        print(user.location)
        
        """  Gets latitude and longitude based on user.place and user.alpha_2_code """

        url = f"http://api.openweathermap.org/geo/1.0/direct?q={user.location}&limit={5}&appid={user.api_key}"
        try:
            response = Network_communication.url_access(url)
        except urllib.error.HTTPError:
            sg.popup_error('ERROR Obtaining latitude and longitude Data, check if you spelled the name or that name isnt present in Country?')

        result = json.loads(response)
        #print(json.dumps(result, indent=2))                    
        for i in range(len(result)):
            if result[i].get('country') == user.alpha_2_code:
                latitude = result[i].get("lat")
                longitude = result[i].get('lon')
                return (latitude, longitude)
            
            
    def get_current_weather_data(latitude: float, longitude: float, user):
        """ Current weather for your location sends data to `all the json files` """

        url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={user.api_key}&units=metric"
        response = Network_communication.url_access(url)
        if response:
            result = json.loads(response)
            #print(json.dumps(result, indent=2))                    
            with open("Weather and Pollution/all the json files/Current Weather.json", "w") as f:
                json.dump(result, f, indent=2)
        return

    def get_forecast_weatherFor_5days_data(latitude: float, longitude: float, user):
        """ Weather for the next 5 days(including today) sends to `all the json files` """

        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={user.api_key}&units=metric"
        response = Network_communication.url_access(url)
        if response:
            result = json.loads(response)
            #print(json.dumps(result, indent=2))                    
            with open("Weather and Pollution/all the json files/Forecast_weather_3h_step_5days.json", "w") as f:
                json.dump(result, f, indent=2)
        return

    def get_current_pollution(latitude: float, longitude: float, user):
        """ Pollution for the next 4days, all the negative particals -> `all the json files` """
        
        url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={latitude}&lon={longitude}&appid={user.api_key}"
        response = Network_communication.url_access(url)
        if response:
            result = json.loads(response)
            #print(json.dumps(result, indent=2))                    
            with open("Weather and Pollution/all the json files/Current Pollution.json", "w") as f:
                json.dump(result, f, indent=2)
        return

    def get_forcast_air_polution(latitude: float, longitude: float, user):

        url = f"http://api.openweathermap.org/data/2.5/air_pollution/forecast?lat={latitude}&lon={longitude}&appid={user.api_key}"  
        response = Network_communication.url_access(url)
        if response:
            result = json.loads(response)
            #print(json.dumps(result, indent=2))                    
            with open("Weather and Pollution/all the json files/Forecast Pollution.json", "w") as f:
                json.dump(result, f, indent=2)

        return

    def request_weather_icon(icon_id=None):
        filename = 'Weather and Pollution/temp_image.png'
        url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
        with urllib.request.urlopen(url) as response:
            image_bytes = BytesIO(response.read()) #converting img to a byte like object
            image = Image.open(image_bytes)
            image.save(filename)

            return filename


