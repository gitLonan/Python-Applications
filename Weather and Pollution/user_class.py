import time
from style_class import Style


class User:
    """ Alpha-2 code is a standard, look online ISO3166"""
    def __init__(self,):
        self.location = ''
        self.alpha_2_code = ''
        self.api_key = ''

    def set_place_name(self,place):
        """ Sets at what place on the planet you want to search for the weather and the other stuff """
        place = place.lower()
        place = place.capitalize()

        self.location = place

    def set_Alpha2_code_for_country(self,code) -> type(str):
        """ Sets alpha 2 code which you can find by typing ISO3166 in google and find your country """

        self.alpha_2_code = code.upper()

    def set_API_key(self):
        key = "b885a811ff1c82c0621f6a1b9cb9c10b"
        self.api_key = key