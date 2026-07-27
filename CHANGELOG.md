# Changelog

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]
### Added
- Populated CHANGELOG.md with project history
- pytest suite covering `server.py`, `weather.py`, `functions.py`, and the static data modules, with mocked HTTP calls and 100% coverage on tested modules
- Per-IP rate limiting and city input length validation on `/weather`
### Changed
- Corrected README.md setup instructions and feature list
- OpenWeatherMap requests now use encoded query params over HTTPS instead of raw f-string URLs
- `.gitignore` now excludes coverage.py output (`.coverage`, `.coverage.*`, `htmlcov/`)
### Fixed
- Removed "San Salvador" duplicate entry incorrectly listed under South America in `cities.py`
- Uniform forecast card height regardless of status text length
- Forecast toggle touch target now meets WCAG 2.1 AA 44x44px minimum

## [0.2.1] - 2026-04-30
### Fixed
- 5-day forecast card sizing and mobile layout

## [0.2.0] - 2026-04-26
### Added
- 5-day forecast with toggle control; state persists across page reloads
- Screen-reader accessibility for forecast toggle and icons
### Fixed
- API response validation (200 OK check)

## [0.1.0] - 2025-02-15
### Added
- Current weather lookup by city name (OpenWeatherMap)
- Conditional display of US state or country based on location
- "Feels like" temperature shown when >5&deg; different from actual
- Mobile-friendly responsive styling and icon set
### Fixed
- Expanded/corrected city and US state lists; corrected icon references
