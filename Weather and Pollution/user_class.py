import time
from style_class import Style

class User:
    """ Alpha-2 code is a standard, look online ISO3166"""
    def __init__(self,):
        self.location = ''
        self.alpha_2_code = ''
        self.api_key = ''

    def set_place_name(self,):
        """ Sets at what place on the planet you want to search for the weather and the other stuff """

        #place = input("Type where you are form: ")
        place = "Zvezdara"  #Ž i slicna slova ne moze da cita... AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        self.location = place

    def set_Alpha2_code_for_country(self,) -> type(str):
        """ Sets alpha 2 code which you can find by typing ISO3166 in google and find your country """

        print(f"Look online:  Type 'ISO3166' and look for {Style.RED}Alpha-2 code{Style.END_COLOR} of your country")
        while True:
            #code = input("Type your Alpha-2 code: ")
            code = 'RS'
            if len(code) != 2:
                continue
            elif code.isnumeric():
                continue
            break
        self.alpha_2_code = code.upper()

    def set_API_key(self):
        #Ovo moram da snipujem i pokazem u readme.md NEMOJ DA ZABORAVIS, jer kao jako je bitno...
        print(f"{Style.RED}If you want to use it you'll have to copy API key, from OpenWeather site:{Style.END_COLOR} {Style.YELLOW}https://openweathermap.org/{Style.END_COLOR}")
        key = "b885a811ff1c82c0621f6a1b9cb9c10b"
        self.api_key = key