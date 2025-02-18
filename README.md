# Welcome to my Weather & Pollution app

This Weather App utilizes the **OpenWeather API** to provide users with current weather information, pollution levels, weather and pollution forcasts for the next few days.

## Table of Contents
- [Features](#features)
- [Screenshots](#screenshots)
- [Getting Started](#getting-started)
- [Technologies used](#technologies-used)

## Features

- **Current Weather**: View the current weather conditions at your location or any specified location.
- **Current Pollution Levels**: Check the current pollution levels for various pollutants.
- **Forecast Weather**: Get a forecast of weather conditions for the next few days.
- **Forecast Pollution Levels**: View the forecasted pollution levels for the next few days.
- **Change location**: Change your location by typing in the name of the place and alpha 2 code(string of lenght two that represent your country)  

### Screenshots:  
  
1. **Current Weather**
Shows current temperature, date, time and metrics on the right side  
![Alt Text](/Weather_and_Pollution/Screenshots/current_weather.PNG)  
  
2. **Current Pollution Levels**  
Shows current pollution level for the pollutants:  
    - **CO-Carbon monoxide**  
    - **NO-Nitrogen monoxide**  
    - **NO2-Nitrogen dioxide**  
    - **O3-Ozone**  
    - **SO2-Sulphur dioxide**  
    - **PM2.5-Fine particulates 2.5 micrometers or smaller**  
    - **PM10-Inhalable particles, with diameters that are generally 10 micrometers and smaller**  
    - **NH3-Ammonia**  
By hovering with your mouse over the choosen bar it will show you it's number, the color will represent how polluted it is
-For the meanings of color go to [Getting Started](#getting-started)  
![Alt Text](/Weather_and_Pollution/Screenshots/current_pollution.PNG)  
  
3. **Forecast Weather**  
Shows temperature for the next few days and it's highest and lowest projection  
![Alt Text](/Weather_and_Pollution/Screenshots/forecast_weather.PNG)  

4. **Forecast Pollution Levels**  
Shows average levels of pollution for the said pollutants for the given day, same as before, by hovering with your mouse you get to see number and what element it is  
![Alt Text](/Weather_and_Pollution/Screenshots/forecast_pollution.PNG)  
  
5. **Change Location**  
On the picture you can see you have two input fields to fill, first one is *location*, it can be city, region, small city, any place you want and if the OpenWeather database doesn't have anything with said name it will create a **pop up** and tell you.(check if you typed the name correctly, just google it). Second one is *alpha 2 code*, every country is represented by a code, and it is a string of lenght two, just scroll and find your country, they are orderd alphabeticaly.  
![Alt Text](/Weather_and_Pollution/Screenshots/change_location.PNG)  
  
6. **How to change between said features**  
Just right click, since PySimpleGui has it's own limits, for some parts of the screen it won't work, thats because padding for the text creates unclickable 'zones', soo just try somewhere else.  
![Alt Text](/Weather_and_Pollution/Screenshots/right_click.PNG)  


## Getting Started
-Before you get all hyped up about this app first you gotta **register** at [OpenWeather](https://openweathermap.org/). By doing soo you will get your own **API key** which you'll be able to make all the needed API calls from the server.  
-Then you will need to copy the said key from their site and paste it in `user_class.py` in variable: **`key`**
![Alt Text](/Weather_and_Pollution/Screenshots/for_API_key.PNG)  

1. Clone repository: https://github.com/MujoHarac/Python-Applications.git

2. Make sure you have all the dependencies installed on your computer.

3. Colors by an increase of pollution from left to right  
![Alt Text](/Weather_and_Pollution/Screenshots/colors_representing_pollution_levels.PNG)



## Technologies and Libraries Used

- Python 3.9.5
- PySimpleGUI
- urllib.request
- Pillow
- json


