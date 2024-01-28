import sys
import subprocess
from geopy.geocoders import Nominatim

import control_files as cf

class GeoInfo:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="MyApp")

    def get_coordinates_from_city(self, city_name: str, county_name=""):
        location = self.geolocator.geocode(city_name + " " + county_name)
        if location is None:
            return "Error. There's no city with that name."
        else:
            return "Success", location.latitude, location.longitude

    def check_coordinates(self, latitude: float, longitude: float):
        if -90 < latitude < 90 and -90 < longitude < 90:
            coordinates = latitude, longitude
            location = self.geolocator.reverse(coordinates)
            if location is None:
                return "None", "", "", ""
            address = location.raw['address']
            city = address.get('city', '')
            state = address.get('state', '')
            country = address.get('country', '')
            return "Success", city, state, country
        else:
            return "Error. The latitude and longitude should be in range from -90 to 90"
    def save_coordinates(self, latitude: float, longitude: float):
        cf.DataHandler.write_localization(latitude,longitude)
        """check_data = cf.DataHandler.read_localization()
        print(check_data)"""
    def launch_coordinates(self, latitude: float, longitude: float):
        result = subprocess.check_output([sys.executable, "get_info.py", "--supervise", f"{latitude}",
                                          f"{longitude}"])


def main(arg1: str, arg2: str, arg3=""):
    global result
    geo_info = GeoInfo()

    if arg1 == "--check-city":
        result = geo_info.get_coordinates_from_city(arg2, arg3)
        if result[0] == "Success":
            result = geo_info.check_coordinates(result[1], result[2])
        else:
            return result[0]

    elif arg1 == "--check-coords":
        arg2 = float(arg2)
        arg3 = float(arg3)
        result = geo_info.check_coordinates(arg2, arg3)

    elif arg1 == "--set-city":
        coords = geo_info.get_coordinates_from_city(arg2, arg3)
        if coords[0] == "Success":
            result = geo_info.check_coordinates(coords[1], coords[2])
            if result[0] == "Success":
                geo_info.save_coordinates(coords[1], coords[2])
        else:
            return result[0]

    elif arg1 == "--set-coords":
        arg2 = float(arg2)
        arg3 = float(arg3)
        coords = geo_info.check_coordinates(arg2, arg3)
        if coords[0] == "Success":
            geo_info.save_coordinates(arg2, arg3)

    return result


if __name__ == '__main__':
    if len(sys.argv) == 3:
        result = main(sys.argv[1], sys.argv[2])
        print(result)
    elif len(sys.argv) == 4:
        result = main(sys.argv[1], sys.argv[2], sys.argv[3])
        print(result)
