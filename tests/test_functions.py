"""Tests for functions.py: weather description aggregation helpers."""

from pytest_mock import MockerFixture

import functions


def test_get_weather_descriptions_counts_each_description() -> None:
    """Should tally how many times each description appears."""
    weather_data = {
        "weather": [
            {"description": "clear sky"},
            {"description": "clear sky"},
            {"description": "light rain"},
        ]
    }

    result = functions.get_weather_descriptions(weather_data)

    assert result == {"clear sky": 2, "light rain": 1}


def test_get_weather_descriptions_missing_weather_key_returns_empty() -> None:
    """Should return an empty dict when there is no 'weather' key."""
    assert functions.get_weather_descriptions({}) == {}


def test_get_weather_descriptions_skips_entries_without_description() -> None:
    """Should ignore weather entries that have no description."""
    weather_data = {"weather": [{}]}
    assert functions.get_weather_descriptions(weather_data) == {}


def test_get_all_weather_descriptions_aggregates_across_cities(
    mocker: MockerFixture,
) -> None:
    """Should merge descriptions collected for every city."""
    mocker.patch("functions.cities.world_cities", ["Nashville", "Tokyo"])
    mocker.patch(
        "functions.get_current_weather",
        side_effect=[
            {"weather": [{"description": "clear sky"}]},
            {"weather": [{"description": "light rain"}]},
        ],
    )
    mock_sleep = mocker.patch("functions.time.sleep")

    result = functions.get_all_weather_descriptions()

    assert result == {"clear sky": None, "light rain": None}
    mock_sleep.assert_not_called()


def test_get_all_weather_descriptions_sleeps_between_batches(
    mocker: MockerFixture,
) -> None:
    """Should pause BATCH_DELAY seconds once a batch boundary is crossed."""
    mocker.patch("functions.BATCH_SIZE", 1)
    mocker.patch("functions.cities.world_cities", ["Nashville", "Tokyo"])
    mocker.patch(
        "functions.get_current_weather",
        return_value={"weather": [{"description": "clear sky"}]},
    )
    mock_sleep = mocker.patch("functions.time.sleep")

    functions.get_all_weather_descriptions()

    mock_sleep.assert_called_once_with(functions.BATCH_DELAY)
