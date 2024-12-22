from unittest.mock import patch, MagicMock
from night_sky_pi.entry import night_sky_pi


@patch("argparse.ArgumentParser.parse_args")
@patch("night_sky_pi.entry.run")
def test_night_sky_pi(mock_run, mock_parse_args):
    # Arrange
    mock_args = MagicMock()
    mock_args.configuration = "test_config"
    mock_parse_args.return_value = mock_args

    # Act
    night_sky_pi()

    # Assert
    mock_parse_args.assert_called_once_with(None)
    mock_run.assert_called_once_with(mock_args)
