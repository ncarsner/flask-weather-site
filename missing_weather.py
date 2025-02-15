import time
from pprint import pprint

from weather_descriptions import weather_descriptions
from weather import get_current_weather
import cities

missing_descriptions = []
start_time = time.time()
request_count = 0

for city in cities.world_cities:
    if request_count >= 60:
        elapsed_time = time.time() - start_time
        if elapsed_time < 60:
            time.sleep(60 - elapsed_time)
        start_time = time.time()
        request_count = 0

    try:
        weather_data = get_current_weather(city.strip())
        request_count += 1

        description = weather_data["weather"][0]["description"]
        if description not in weather_descriptions:
            missing_descriptions.append((city, description))
    except KeyError:
        print(f"Weather data for {city} not found.")
    except Exception as e:
        print(f"An error occurred for {city}: {e}")

print("\n*** Missing Weather Descriptions ***")
pprint(missing_descriptions)
