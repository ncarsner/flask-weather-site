"""Tests for server.py: Flask routes, rate limiting, and forecast processing."""

from datetime import datetime

import pytest
from flask.testing import FlaskClient
from pytest_mock import MockerFixture

import server

WEATHER_OK = {
    "cod": 200,
    "name": "Nashville",
    "weather": [{"description": "clear sky"}],
    "main": {"temp": 75.0, "feels_like": 75.0},
    "sys": {"country": "US"},
}


def _forecast_entry(
    date_str: str, hour: int, temp: float, description: str, pop: float = 0.0
) -> dict:
    """Build a single 3-hourly OpenWeatherMap forecast list entry."""
    return {
        "dt_txt": f"{date_str} {hour:02d}:00:00",
        "main": {"temp": temp},
        "weather": [{"description": description}],
        "pop": pop,
    }


FORECAST_OK = {
    "cod": "200",
    "list": [_forecast_entry("2026-07-21", 12, 75.0, "clear sky", pop=0.1)],
}


# --- Static routes -----------------------------------------------------


@pytest.mark.parametrize("path", ["/", "/index"])
def test_index_routes_return_ok(client: FlaskClient, path: str) -> None:
    """Both index aliases should render successfully."""
    response = client.get(path)
    assert response.status_code == 200


def test_favicon_route_serves_icon(client: FlaskClient) -> None:
    """The favicon route should serve the icon file with the right mimetype."""
    response = client.get("/favicon.ico")
    assert response.status_code == 200
    assert response.mimetype == "image/vnd.microsoft.icon"


# --- _is_rate_limited ----------------------------------------------------


def test_is_rate_limited_allows_up_to_the_threshold() -> None:
    """Requests at or under the limit should not be rate limited."""
    ip = "10.0.0.1"
    for _ in range(server.RATE_LIMIT_REQUESTS):
        assert server._is_rate_limited(ip) is False
    assert server._is_rate_limited(ip) is True


def test_is_rate_limited_tracks_per_ip_independently() -> None:
    """One IP being rate limited should not affect another IP."""
    for _ in range(server.RATE_LIMIT_REQUESTS + 1):
        server._is_rate_limited("10.0.0.2")
    assert server._is_rate_limited("10.0.0.3") is False


# --- _process_forecast ---------------------------------------------------


def test_process_forecast_summarizes_each_day() -> None:
    """Each day should collapse to one summary using the noon-closest entry."""
    forecast_data = {
        "list": [
            _forecast_entry("2026-07-21", 6, 60.0, "few clouds"),
            _forecast_entry("2026-07-21", 12, 75.0, "clear sky", pop=0.3),
            _forecast_entry("2026-07-22", 12, 80.0, "light rain", pop=0.5),
        ]
    }

    days = server._process_forecast(forecast_data)

    assert len(days) == 2
    first = days[0]
    assert first["day"] == datetime.strptime("2026-07-21", "%Y-%m-%d").strftime("%a")
    assert first["high"] == 75
    assert first["low"] == 60
    assert first["status"] == "Clear sky"
    assert first["icon"] == "images/clear_sky.png"
    assert first["precip_chance"] == 30


def test_process_forecast_limits_to_five_days() -> None:
    """Only the first five days should be returned."""
    entries = [
        _forecast_entry(f"2026-07-{21 + i}", 12, 70.0, "clear sky") for i in range(7)
    ]

    days = server._process_forecast({"list": entries})

    assert len(days) == 5


def test_process_forecast_unknown_description_has_no_icon() -> None:
    """A description with no icon mapping should leave icon as None."""
    forecast_data = {"list": [_forecast_entry("2026-07-21", 12, 70.0, "tornado")]}

    days = server._process_forecast(forecast_data)

    assert days[0]["icon"] is None


# --- /weather --------------------------------------------------------------


def test_weather_route_renders_city_weather(
    mocker: MockerFixture, client: FlaskClient
) -> None:
    """A known city should render its name, region, and conditions."""
    mocker.patch("server.get_current_weather", return_value=WEATHER_OK)
    mocker.patch("server.get_five_day_forecast", return_value=FORECAST_OK)

    response = client.get("/weather", query_string={"city": "Nashville"})

    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "Nashville" in body
    assert "Tennessee" in body
    assert "Clear sky" in body


def test_weather_route_uses_random_city_when_city_missing(
    mocker: MockerFixture, client: FlaskClient
) -> None:
    """No city query param should fall back to a random world city."""
    mocker.patch("server.random.choice", return_value="Tokyo")
    mock_current = mocker.patch(
        "server.get_current_weather",
        return_value={**WEATHER_OK, "name": "Tokyo", "sys": {"country": "JP"}},
    )
    mocker.patch("server.get_five_day_forecast", return_value=FORECAST_OK)

    response = client.get("/weather")

    assert response.status_code == 200
    mock_current.assert_called_once_with("Tokyo")


def test_weather_route_blank_city_uses_random_city(
    mocker: MockerFixture, client: FlaskClient
) -> None:
    """A whitespace-only city should be treated the same as a missing one."""
    mocker.patch("server.random.choice", return_value="Tokyo")
    mock_current = mocker.patch(
        "server.get_current_weather",
        return_value={**WEATHER_OK, "name": "Tokyo", "sys": {"country": "JP"}},
    )
    mocker.patch("server.get_five_day_forecast", return_value=FORECAST_OK)

    response = client.get("/weather", query_string={"city": "   "})

    assert response.status_code == 200
    mock_current.assert_called_once_with("Tokyo")


def test_weather_route_rejects_overlong_city(client: FlaskClient) -> None:
    """A city name over MAX_CITY_LENGTH should be rejected without an API call."""
    response = client.get("/weather", query_string={"city": "x" * 101})

    assert response.status_code == 400
    assert "City Not Found" in response.get_data(as_text=True)


def test_weather_route_city_not_found(
    mocker: MockerFixture, client: FlaskClient
) -> None:
    """A cod other than 200 from the API should render the not-found page."""
    mocker.patch(
        "server.get_current_weather",
        return_value={"cod": "404", "message": "city not found"},
    )

    response = client.get("/weather", query_string={"city": "Nowhereville"})

    assert response.status_code == 200
    assert "City Not Found" in response.get_data(as_text=True)


def test_weather_route_forecast_api_failure_omits_forecast(
    mocker: MockerFixture, client: FlaskClient
) -> None:
    """A failed forecast lookup should not break the current-weather page."""
    mocker.patch("server.get_current_weather", return_value=WEATHER_OK)
    mocker.patch("server.get_five_day_forecast", return_value={"cod": "400"})

    response = client.get("/weather", query_string={"city": "Nashville"})

    assert response.status_code == 200
    assert "5-Day Forecast" not in response.get_data(as_text=True)


def test_weather_route_forecast_included_by_default(
    mocker: MockerFixture, client: FlaskClient
) -> None:
    """With no forecast param, the forecast section should be visible."""
    mocker.patch("server.get_current_weather", return_value=WEATHER_OK)
    mocker.patch("server.get_five_day_forecast", return_value=FORECAST_OK)

    response = client.get("/weather", query_string={"city": "Nashville"})
    body = response.get_data(as_text=True)

    assert 'id="forecast-section"' in body
    assert "display:none" not in body


def test_weather_route_forecast_hidden_when_false(
    mocker: MockerFixture, client: FlaskClient
) -> None:
    """forecast=false should render the forecast section hidden."""
    mocker.patch("server.get_current_weather", return_value=WEATHER_OK)
    mocker.patch("server.get_five_day_forecast", return_value=FORECAST_OK)

    response = client.get(
        "/weather", query_string={"city": "Nashville", "forecast": "false"}
    )

    assert "display:none" in response.get_data(as_text=True)


@pytest.mark.parametrize(
    ("actual_temp", "feels_like_temp", "expect_feels_like"),
    [
        (75.0, 75.0, False),
        (75.0, 68.0, True),
    ],
)
def test_weather_route_feels_like_shown_only_past_threshold(
    mocker: MockerFixture,
    client: FlaskClient,
    actual_temp: float,
    feels_like_temp: float,
    expect_feels_like: bool,
) -> None:
    """Feels-like should only render when it differs from actual by >5 degrees."""
    weather_data = {
        **WEATHER_OK,
        "main": {"temp": actual_temp, "feels_like": feels_like_temp},
    }
    mocker.patch("server.get_current_weather", return_value=weather_data)
    mocker.patch("server.get_five_day_forecast", return_value=FORECAST_OK)

    response = client.get("/weather", query_string={"city": "Nashville"})

    assert ("Feels like" in response.get_data(as_text=True)) is expect_feels_like


@pytest.mark.parametrize(
    ("feels_like_temp", "expected_image"),
    [
        (95.0, "hot.png"),
        (85.0, "warm.png"),
        (50.0, "cool.png"),
        (20.0, "cold.png"),
        (70.0, None),
    ],
)
def test_weather_route_temperature_image_thresholds(
    mocker: MockerFixture,
    client: FlaskClient,
    feels_like_temp: float,
    expected_image: str | None,
) -> None:
    """The rendered temperature image should match the feels-like bucket."""
    weather_data = {
        **WEATHER_OK,
        "main": {"temp": feels_like_temp, "feels_like": feels_like_temp},
    }
    mocker.patch("server.get_current_weather", return_value=weather_data)
    mocker.patch("server.get_five_day_forecast", return_value=FORECAST_OK)

    response = client.get("/weather", query_string={"city": "Nashville"})
    body = response.get_data(as_text=True)

    if expected_image:
        assert expected_image in body
    else:
        for image in ("hot.png", "warm.png", "cool.png", "cold.png"):
            assert image not in body


def test_weather_route_non_us_territory_resolves_country_name(
    mocker: MockerFixture, client: FlaskClient
) -> None:
    """Non-US cities should resolve to a country name via territories/countries."""
    weather_data = {**WEATHER_OK, "name": "Tokyo", "sys": {"country": "JP"}}
    mocker.patch("server.get_current_weather", return_value=weather_data)
    mocker.patch("server.get_five_day_forecast", return_value=FORECAST_OK)

    response = client.get("/weather", query_string={"city": "Tokyo"})

    assert "Japan" in response.get_data(as_text=True)


def test_weather_route_rate_limits_after_threshold(
    mocker: MockerFixture, client: FlaskClient
) -> None:
    """The (RATE_LIMIT_REQUESTS + 1)th request in the window should get a 429."""
    mocker.patch("server.get_current_weather", return_value=WEATHER_OK)
    mocker.patch("server.get_five_day_forecast", return_value=FORECAST_OK)

    for _ in range(server.RATE_LIMIT_REQUESTS):
        response = client.get("/weather", query_string={"city": "Nashville"})
        assert response.status_code == 200

    response = client.get("/weather", query_string={"city": "Nashville"})

    assert response.status_code == 429
    assert b"Too many requests" in response.data
