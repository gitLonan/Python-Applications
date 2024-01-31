import json, urllib.request, time
from style_class import Style
from user_class import User
from network_class import Network_communication


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
                return (latitude, longitude, result)
    else:
        print(f"{Style.RED}Wrong City name or wrong country name, pls look ISO 3166 for guidence on country codes{Style.END_COLOR}")
    
def current_weather_data(latitude, longitude, user):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={user.api_key}&units=metric"
    response = Network_communication.url_access(url)
    if response:
        result = json.loads(response)
        #print(json.dumps(result, indent=2))
        with open("Weather & Pollution/all the json files/Current Weather.json", "w") as f:
            json.dump(result, f, indent=2)

def weather_dayBy_day(latitude, longitude, user, day=5):
    
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={user.api_key}&units=metric"
    response = Network_communication.url_access(url)
    if response:
        result = json.loads(response)
        #print(json.dumps(result, indent=2))
        with open("Weather & Pollution/all the json files/Weather_3h_step_5days.json", "w") as f:
            json.dump(result, f, indent=2)

def main(user):
    latitude, longitude, result_just_for_bug = get_latitude_longitude(user)
    result_just_for_bug = json.dumps(result_just_for_bug, indent=2)    
    print(result_just_for_bug)
    print(latitude, longitude)
    current_weather_data(latitude, longitude, user)
    weather_dayBy_day(latitude, longitude, user)



if __name__ == "__main__":
    user = User()
    user.set_place_name()
    user.set_Alpha2_code_for_country()
    user.set_API_key()
    main(user)




