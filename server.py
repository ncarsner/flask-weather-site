from flask import Flask, render_template, request, send_from_directory
from weather import get_current_weather
# from waitress import serve

import random
import cities
# import os

app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('./images', 'sun_yellow.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/weather')
def get_weather():
    city = request.args.get('city')

    # Check for empty strings or string with only spaces
    if not city.strip():
        city = random.choice(cities.world_cities)

    weather_data = get_current_weather(city)

    # City is not found by API
    if not weather_data['cod'] == 200:
        return render_template('city-not-found.html')

    return render_template(
        "weather.html",
        favicon=favicon(),
        title=weather_data["name"],
        status=weather_data["weather"][0]["description"].capitalize(),
        temp=f"{int(weather_data['main']['temp'])}",
        feels_like=f"{int(weather_data['main']['feels_like'])}"
    )

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
