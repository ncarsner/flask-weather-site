import random
# import sys

from datetime import datetime

from flask import Flask, render_template, request, send_from_directory
from waitress import serve

import cities
from weather import get_current_weather, get_five_day_forecast
from weather_descriptions import weather_descriptions
import provinces


app = Flask(__name__)


def _process_forecast(forecast_data: dict) -> list[dict]:
    """Collapse 3-hourly forecast entries into one summary per day."""
    days: dict[str, list] = {}
    for entry in forecast_data["list"]:
        date_str = entry["dt_txt"].split(" ")[0]
        days.setdefault(date_str, []).append(entry)

    result = []
    for date_str, entries in days.items():
        noon = min(entries, key=lambda e: abs(int(e["dt_txt"][11:13]) - 12))
        temps = [e["main"]["temp"] for e in entries]
        status = noon["weather"][0]["description"].capitalize()
        icon_file = weather_descriptions.get(status.lower())
        result.append({
            "day": datetime.strptime(date_str, "%Y-%m-%d").strftime("%A"),
            "high": int(max(temps)),
            "low": int(min(temps)),
            "status": status,
            "icon": f"images/{icon_file}" if icon_file else None,
            "precip_chance": int(max(e.get("pop", 0) for e in entries) * 100),
        })
    return result[:5]


@app.route("/favicon.ico")
def favicon():
    return send_from_directory("static/images", "sun_yellow.ico", mimetype="image/vnd.microsoft.icon")


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/weather")
def get_weather():
    city = request.args.get("city")

    # Check for empty strings or string with only spaces
    if not city or not city.strip():
        city = random.choice(cities.world_cities)

    weather_data = get_current_weather(city)

    # City is not found by API
    if not weather_data["cod"] == 200:
        return render_template("city-not-found.html")

    include_forecast = request.args.get("forecast") == "true"
    forecast_days = None
    if include_forecast:
        forecast_data = get_five_day_forecast(city)
        if str(forecast_data.get("cod")) == "200":
            forecast_days = _process_forecast(forecast_data)

    status = weather_data["weather"][0]["description"].capitalize()
    desc_path = weather_descriptions.get(status.lower(), None)
    desc_url = f"/images/{desc_path}" if desc_path else None
    hot = "/images/hot.png" if weather_data["main"]["feels_like"] >= 90 else None
    warm = "/images/warm.png" if 78 < weather_data["main"]["feels_like"] < 90 else None
    # ROOM TEMP 65-77
    cool = "/images/cool.png" if 40 < weather_data["main"]["feels_like"] < 58 else None
    cold = "/images/cold.png" if weather_data["main"]["feels_like"] < 40 else None

    actual_temp = weather_data["main"]["temp"]
    feels_like = weather_data["main"]["feels_like"]

    feels_like = int(feels_like) if abs(actual_temp - feels_like) > 5 else None

    territory = weather_data["sys"]["country"]

    city = city.title()
    territory_name = (
        provinces.us_cities.get(city) if territory == "US" else
            provinces.territories.get(territory, None) or
            provinces.countries.get(territory, None)
    )

    return render_template(
        "weather.html",
        title=weather_data["name"],
        country=territory_name,
        status=status,
        description_image=desc_url,
        temp=f"{int(weather_data['main']['temp'])}",
        hot=hot,
        warm=warm,
        cool=cool,
        cold=cold,
        feels_like=feels_like,
        include_forecast=include_forecast,
        forecast_days=forecast_days,
    )


if __name__ == "__main__":
    test = None
    if test is not None:
        # Development
        app.run(debug=True, host="0.0.0.0", port=8000)
    else:
        # Production WSGI
        serve(app, host="0.0.0.0", port=8000)
