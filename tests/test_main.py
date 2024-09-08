from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from freezegun import freeze_time
from src.app.main import run


@patch("src.app.main.build_configuration")
@patch("src.app.main.get_observation")
@patch("src.app.main.setup_observation_filesystem")
@patch("src.app.main.perform_observation")
@patch("src.app.main.perform_housekeeping")
@patch("src.app.main.perform_packaging")
@patch("src.app.main.sleep")
@patch("src.app.main.datetime")
def test_run_within_observation_period(
    mock_datetime,
    mock_sleep,
    mock_perform_packaging,
    mock_perform_housekeeping,
    mock_perform_observation,
    mock_setup_observation_filesystem,
    mock_get_observation,
    mock_build_configuration,
):
    mock_datetime.now.return_value = datetime(2022, 1, 1, 12, 0, 0)
    arguments = MagicMock()
    arguments.configuration = "config.json"
    arguments.test_mode = True

    config = MagicMock()
    mock_build_configuration.return_value = config

    observation = MagicMock()
    observation.period.within_observation_period.return_value = True
    mock_setup_observation_filesystem.return_value = observation
    mock_get_observation.return_value = observation

    run(arguments)

    mock_build_configuration.assert_called_once_with(arguments.configuration)
    mock_get_observation.assert_called_once_with(config, datetime(2022, 1, 1, 12, 0, 0))
    mock_setup_observation_filesystem.assert_called_once_with(observation)
    mock_perform_observation.assert_called_once_with(observation, config)
    mock_sleep.assert_called_once_with(config.nsp.observation_cooldown * 60)
    mock_perform_housekeeping.assert_not_called()
    mock_perform_packaging.assert_not_called()


@patch("src.app.main.build_configuration")
@patch("src.app.main.get_observation")
@patch("src.app.main.setup_observation_filesystem")
@patch("src.app.main.perform_observation")
@patch("src.app.main.perform_housekeeping")
@patch("src.app.main.perform_packaging")
@patch("src.app.main.sleep")
@patch("src.app.main.datetime")
def test_run_not_within_observation_period(
    mock_datetime,
    mock_sleep,
    mock_perform_packaging,
    mock_perform_housekeeping,
    mock_perform_observation,
    mock_setup_observation_filesystem,
    mock_get_observation,
    mock_build_configuration,
):
    mock_datetime.now.return_value = datetime(2022, 1, 1, 12, 0, 0)
    arguments = MagicMock()
    arguments.configuration = "config.json"
    arguments.test_mode = True
    config = MagicMock()
    mock_build_configuration.return_value = config

    observation = MagicMock()
    observation.period.within_observation_period.return_value = False
    observation.period.calculate_wait_till_observation.return_value = 1
    mock_get_observation.return_value = observation

    with freeze_time("2022-01-01 12:00:00"):
        run(arguments)

    mock_build_configuration.assert_called_once_with("config.json")
    mock_get_observation.assert_called_once_with(config, datetime(2022, 1, 1, 12, 0, 0))
    mock_setup_observation_filesystem.assert_not_called()
    mock_perform_observation.assert_not_called()
    mock_sleep.assert_called_once_with(1)
    mock_perform_housekeeping.assert_called_once_with(config)
    mock_perform_packaging.assert_called_once_with(config)
