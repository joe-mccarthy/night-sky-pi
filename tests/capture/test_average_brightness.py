import unittest
from unittest.mock import patch, MagicMock
from PIL import Image
from src.app.capture.exposure import calculate_average_brightness


@patch("src.app.capture.exposure.Image.open")
def test_completely_dark_image(mock_open):
    # Arrange
    mock_image = MagicMock()
    mock_image.convert.return_value.histogram.return_value = [100] + [0] * 255
    mock_open.return_value = mock_image

    # Act
    average_brightness = calculate_average_brightness("dummy_path")

    # Assert
    assert average_brightness == 0


@patch("src.app.capture.exposure.Image.open")
def test_completely_bright_image(mock_open):
    # Arrange
    mock_image = MagicMock()
    mock_image.convert.return_value.histogram.return_value = [0] * 255 + [100]
    mock_open.return_value = mock_image

    # Act
    average_brightness = calculate_average_brightness("dummy_path")

    # Assert
    assert average_brightness == 1.0


@patch("src.app.capture.exposure.Image.open")
def test_mid_tone_image(mock_open):
    # Arrange
    mock_image = MagicMock()
    mock_image.convert.return_value.histogram.return_value = (
        [0] * 128 + [100] + [0] * 127
    )
    mock_open.return_value = mock_image

    # Act
    average_brightness = calculate_average_brightness("dummy_path")

    # Assert
    assert average_brightness == 0.5
