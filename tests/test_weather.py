"""Tests for weather.py: the OpenWeatherMap API client functions."""

from pytest_mock import MockerFixture

import weather


def test_get_current_weather_returns_parsed_json(mocker: MockerFixture) -> None:
    """Should return the JSON body of the current-weather API response."""
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"cod": 200, "main": {"temp": 72.0}}
    mock_get = mocker.patch("weather.requests.get", return_value=mock_response)

    result = weather.get_current_weather("Nashville")

    assert result == {"cod": 200, "main": {"temp": 72.0}}
    _, kwargs = mock_get.call_args
    assert kwargs["params"]["q"] == "Nashville"
    assert kwargs["params"]["units"] == "imperial"


def test_get_five_day_forecast_returns_parsed_json(mocker: MockerFixture) -> None:
    """Should return the JSON body of the five-day forecast API response."""
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"cod": "200", "list": []}
    mock_get = mocker.patch("weather.requests.get", return_value=mock_response)

    result = weather.get_five_day_forecast("Tokyo")

    assert result == {"cod": "200", "list": []}
    _, kwargs = mock_get.call_args
    assert kwargs["params"]["q"] == "Tokyo"
