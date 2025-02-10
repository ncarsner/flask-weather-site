import time

import cities
from weather import get_current_weather

BATCH_SIZE = 60
BATCH_DELAY = 60


def get_weather_descriptions(weather_data):
    descriptions = {}
    if "weather" in weather_data:
        for weather in weather_data["weather"]:
            description = weather.get("description")
            if description:
                descriptions[description] = descriptions.get(description, 0) + 1
    return descriptions


def get_all_weather_descriptions():
    all_descriptions = {}
    for i, city in enumerate(cities.world_cities):
        if i > 0 and i % BATCH_SIZE == 0:
            time.sleep(BATCH_DELAY)
        weather_data = get_current_weather(city)
        descriptions = get_weather_descriptions(weather_data)
        for description in descriptions:
            all_descriptions[description] = None
    return all_descriptions


if __name__ == "__main__":

    all_weather_descriptions = get_all_weather_descriptions()

    # with open("weather_descriptions.py", "w") as file:
    #     file.write("weather_descriptions = ")
    #     file.write(repr(all_weather_descriptions))

    try:
        with open("weather_descriptions.py", "r") as file:
            existing_data = eval(file.read().split(" = ")[1])
    except FileNotFoundError:
        existing_data = {}

    for description in all_weather_descriptions:
        if description not in existing_data:
            existing_data[description] = None

    with open("weather_descriptions.py", "w") as file:
        file.write("weather_descriptions = ")
        file.write(repr(existing_data))
