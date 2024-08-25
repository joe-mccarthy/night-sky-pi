import os
from unittest.mock import MagicMock
from src.app.observation.filesystem import setup_observation_filesystem


def test_setup_observation_filesystem_directory_exists(mocker):
    observation = MagicMock()
    observation.data_config.path = "/data/path"
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("os.makedirs")

    result = setup_observation_filesystem(observation)

    assert os.path.exists.called_with("/data/path")
    assert not os.makedirs.called
    assert result == observation


def test_setup_observation_filesystem_directory_not_exists(mocker):
    observation = MagicMock()
    observation.data_config.path = "/data/path"
    mocker.patch("os.path.exists", return_value=False)
    mocker.patch("os.makedirs")

    result = setup_observation_filesystem(observation)

    assert os.path.exists.called_with("/data/path")
    assert os.makedirs.called_with("/data/path")
    assert result == observation
