import pytest
from unittest.mock import MagicMock
from datetime import datetime
from night_sky_pi.app.configuration.core_configuration import LocationConfig
from night_sky_pi.app.observation.data import Observation
from night_sky_pi.app.observation.utils import __get_sun_data, get_observation

# Define a list of locations and dates for testing
locations_and_dates = [
    (
        LocationConfig(latitude=51.5074, longitude=-0.1278),
        datetime(2022, 1, 1),
        datetime(2022, 1, 1, 8, 7),
        datetime(2022, 1, 1, 16, 2),
    )  # London on New Year's Day
]


@pytest.mark.parametrize(
    "location,date,expected_sunrise,expected_sunset", locations_and_dates
)
def test_get_sun_data(location, date, expected_sunrise, expected_sunset):
    sunrise, sunset = __get_sun_data(location, date)

    # Check that the function returns datetime objects
    assert isinstance(sunrise, datetime)
    assert isinstance(sunset, datetime)

    # Check that sunrise is before sunset
    assert sunrise < sunset
    assert expected_sunrise == sunrise.replace(tzinfo=None)
    assert expected_sunset == sunset.replace(tzinfo=None)


def test_get_observation():
    # Create a mock configuration
    config = MagicMock()
    config.device.location = LocationConfig(
        latitude=51.5074, longitude=-0.1278
    )  # London

    # Define a datetime for testing
    a_datetime = datetime(2022, 1, 1, 12)  # Noon on New Year's Day

    # Call the function
    observation = get_observation(config, a_datetime)

    # Check that the function returns an Observation object
    assert isinstance(observation, Observation)

    start = observation.period.start.replace(tzinfo=None)
    end = observation.period.end.replace(tzinfo=None)
    # Check that the observation period is reasonable
    assert start < end

    # test date is before the start and end of the observation period
    assert a_datetime <= start <= end


def test_get_observation_while_in_next_day():
    # Create a mock configuration
    config = MagicMock()
    config.device.location = LocationConfig(
        latitude=51.5074, longitude=-0.1278
    )  # London

    # Define a datetime for testing
    a_datetime = datetime(2022, 1, 1, 3)  # 3am on New Year's Day

    # Call the function
    observation = get_observation(config, a_datetime)

    # Check that the function returns an Observation object
    assert isinstance(observation, Observation)

    start = observation.period.start.replace(tzinfo=None)
    end = observation.period.end.replace(tzinfo=None)
    # Check that the observation period is reasonable
    assert start < end
    assert start.day == 31
    assert end.day == 1

    # test date is before end and after start of the observation period
    assert start <= a_datetime <= end
