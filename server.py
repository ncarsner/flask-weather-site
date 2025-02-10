import random

from flask import Flask, render_template, request, send_from_directory
# from waitress import serve

import cities
from weather import get_current_weather
from weather_descriptions import weather_descriptions

app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static/images', 'sun_yellow.ico', mimetype='image/vnd.microsoft.icon')


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

    status = weather_data["weather"][0]["description"].capitalize()
    desc_path = weather_descriptions.get(status.lower(), None)
    desc_url = f"/images/{desc_path}" if desc_path else None
    hot = "/images/hot.png" if weather_data["main"]["temp"] >= 90 else None
    warm = "/images/warm.png" if 78 < weather_data["main"]["temp"] < 90 else None
    # ROOM TEMP 65-77
    cool = "/images/cool.png" if 40 < weather_data["main"]["temp"] < 58 else None
    cold = "/images/cold.png" if weather_data["main"]["temp"] < 40 else None

    return render_template(
        "weather.html",
        # favicon=favicon(),
        title=weather_data["name"],
        status=status,
        description_image=desc_url,
        temp=f"{int(weather_data['main']['temp'])}",
        hot=hot,
        warm=warm,
        cool=cool,
        cold=cold,
        feels_like=f"{int(weather_data['main']['feels_like'])}"
    )

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
