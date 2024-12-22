import os
from unittest.mock import MagicMock, call
from night_sky_pi.app.observation.filesystem import setup_observation_filesystem


def test_setup_observation_filesystem_directory_exists(mocker):
    observation = MagicMock()
    observation.data_config.path = "/data/path"
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("os.makedirs")

    result = setup_observation_filesystem(observation)

    os.path.exists.assert_called_with("/data/path")
    assert not os.makedirs.called
    assert result == observation


def test_setup_observation_filesystem_directory_not_exists(mocker):
    observation = MagicMock()
    observation.data_config.path = "/data/path"
    observation.data_config.observation_image_path = "/data/path/obs/2021-01-01/image"
    observation.data_config.observation_data_path = "/data/path/obs/2021-01-01"
    mocker.patch("os.path.exists", return_value=False)
    mocker.patch("os.makedirs")

    result = setup_observation_filesystem(observation)

    os.path.exists.assert_called_with("/data/path")
    os.makedirs.assert_has_calls([call("/data/path/obs/2021-01-01/image"), call("/data/path/obs/2021-01-01")])
    assert result == observation
