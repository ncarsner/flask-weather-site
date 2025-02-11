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

"""
import time

provinces = {}
batch_size = 60
total_processed = 0
errored_cities = []

for i in range(0, len(cities.world_cities), batch_size):
    batch = cities.world_cities[i : i + batch_size]
    for city in batch:
        try:
            country_code = get_current_weather(city)["sys"]["country"]
            provinces[city] = country_code
        except Exception as e:
            errored_cities.append(city)
            print(f"Error processing city {city}: {e}")
        total_processed += 1

    print(f"Processed {total_processed} records so far.")
    time.sleep(60)  # Respect rate limits

with open(os.path.join(os.path.dirname(__file__), "provinces.py"), "w") as f:
    f.write(f"provinces = {provinces}")

if errored_cities:
    with open(os.path.join(os.path.dirname(__file__), "errored_cities.txt"), "w") as f:
        f.write("\n".join(errored_cities))
"""
