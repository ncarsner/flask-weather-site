"""Tests for provinces.py: country/territory/state lookup tables."""

import provinces


def test_territories_values_are_two_letter_codes() -> None:
    """Every territories entry should map a city to an ISO-alpha-2 code."""
    assert all(
        isinstance(code, str) and len(code) == 2 and code.isupper()
        for code in provinces.territories.values()
    )


def test_countries_keys_are_two_letter_codes() -> None:
    """Every countries entry should be keyed by an ISO-alpha-2 code."""
    assert all(
        isinstance(code, str) and len(code) == 2 and code.isupper()
        for code in provinces.countries.keys()
    )


def test_countries_values_are_non_empty_strings() -> None:
    """Every country name should be a non-blank string."""
    assert all(
        isinstance(name, str) and name.strip() for name in provinces.countries.values()
    )


def test_us_cities_values_are_non_empty_strings() -> None:
    """Every US city should map to a non-blank state name."""
    assert all(
        isinstance(state, str) and state.strip()
        for state in provinces.us_cities.values()
    )
