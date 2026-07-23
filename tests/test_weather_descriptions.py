"""Tests for weather_descriptions.py: description-to-icon mapping."""

from weather_descriptions import weather_descriptions


def test_all_keys_are_lowercase() -> None:
    """Lookup keys must be lowercase to match the .capitalize()/.lower() call sites."""
    assert all(key == key.lower() for key in weather_descriptions)


def test_all_values_are_png_filenames() -> None:
    """Every mapped icon should be a .png filename."""
    assert all(value.endswith(".png") for value in weather_descriptions.values())
