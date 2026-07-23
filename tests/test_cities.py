"""Tests for cities.py: city catalogue and derived world_cities list."""

import cities


def test_world_cities_is_flattened_from_regions() -> None:
    """world_cities should be every region's cities in one flat list."""
    expected = [city for region in cities.cities.values() for city in region]
    assert cities.world_cities == expected


def test_no_duplicate_cities_within_a_region() -> None:
    """A region's own list should not repeat a city name."""
    for region, region_cities in cities.cities.items():
        assert len(region_cities) == len(set(region_cities)), region


def test_world_cities_all_non_empty_strings() -> None:
    """Every entry should be a non-blank string."""
    assert all(isinstance(city, str) and city.strip() for city in cities.world_cities)
