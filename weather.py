import os
import random
from pprint import pprint

import requests
from dotenv import load_dotenv

import cities

load_dotenv()


def get_current_weather(city=random.choice(cities.world_cities)):
    request_url = f'http://api.openweathermap.org/data/2.5/weather?appid={os.getenv("API_KEY")}&q={city}&units=imperial'
    weather_data = requests.get(request_url).json()
    return weather_data


if __name__ == "__main__":
    print("\n*** Get Current Weather Conditions ***")

    city = input("\nPlease enter a city name: ")

    # Check for empty strings or string with only spaces
    if not city.strip():
        city = random.choice(cities.world_cities)


    weather_data = get_current_weather(city)

    print("\n")
    pprint(weather_data)
