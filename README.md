# Flask Weather Site

This is a simple Flask web application that provides weather information for a given location. Forked from Dave Gray's Python tutorial.

## Features

- Get current weather information for any city.
- Simple, user-friendly interface.
- Display details such as temperature, weather description, with helpful visual icons.
- Conditional expressions for US states or country of city.
- "Feels like" expressed when > 5&deg; difference from actual temperature.
- Optional 5-day forecast, toggled via checkbox; state persists across page reloads.
- Optimized for mobile-friendly devices.

## Requirements

- Python >=3.9
- Flask
- Requests
- python-dotenv
- waitress

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/ncarsner/flask-weather-site.git
    ```
2. Navigate to the project directory:
    ```bash
    cd flask-weather-site
    ```
3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Set your OpenWeatherMap API key as `API_KEY` in the `.env` file.
2. Run the application:
    ```bash
    python server.py
    ```
3. Open your web browser to `http://127.0.0.1:8000`

## Contributing

Contributions welcome. Please open an issue or submit a pull request for any changes.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [OpenWeatherMap](https://openweathermap.org/)
- [Dave Gray](https://github.com/gitdagray/python-flask-rest-api)
