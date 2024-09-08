import math
from unittest.mock import patch, MagicMock
from src.app.capture.exposure import calculate_next_exposure_value
from src.app.configuration.nsp_configuration import Capture


@patch("src.app.capture.exposure.calculate_average_brightness")
def test_brightness_below_lower_threshold(mock_calculate_average_brightness):
    # Arrange
    mock_calculate_average_brightness.return_value = 0.17
    capture = MagicMock()
    capture.shutter.fastest = 1
    capture.shutter.current = 100
    capture.shutter.slowest = 10000
    capture.gain.current = 1.0
    capture.gain.highest = 8.0
    capture.gain.lowest = 1.0
    capture.exposure.target = 0.20
    capture.exposure.tolerance = 0.01

    # Act
    calculate_next_exposure_value("dummy_path", capture)

    # Assert
    assert math.isclose(capture.shutter.current, 200, rel_tol=0.5)
    assert math.isclose(capture.gain.current, 1.0)


@patch("src.app.capture.exposure.calculate_average_brightness")
def test_brightness_above_upper_threshold(mock_calculate_average_brightness):
    # Arrange
    mock_calculate_average_brightness.return_value = 0.25
    capture = MagicMock()
    capture.shutter.fastest = 1
    capture.shutter.current = 100
    capture.shutter.slowest = 10000
    capture.gain.current = 1.0
    capture.gain.highest = 8.0
    capture.gain.lowest = 1.0
    capture.exposure.target = 0.20
    capture.exposure.tolerance = 0.02

    # Act
    calculate_next_exposure_value("dummy_path", capture)

    # Assert
    assert math.isclose(capture.shutter.current, 95, rel_tol=0.5)
    assert math.isclose(capture.gain.current, 1.0)


@patch("src.app.capture.exposure.calculate_average_brightness")
def test_brightness_above_upper_threshold_gain(mock_calculate_average_brightness):
    # Arrange
    mock_calculate_average_brightness.return_value = 0.25
    capture = MagicMock()
    capture.shutter.fastest = 1
    capture.shutter.current = 100
    capture.shutter.slowest = 10000
    capture.gain.current = 7.0
    capture.gain.highest = 8.0
    capture.gain.lowest = 1.0
    capture.exposure.target = 0.20
    capture.exposure.tolerance = 0.02

    # Act
    calculate_next_exposure_value("dummy_path", capture)

    # Assert
    assert math.isclose(capture.shutter.current, 100)
    assert math.isclose(capture.gain.current, 6.6, rel_tol=0.5)


@patch("src.app.capture.exposure.calculate_average_brightness")
def test_brightness_below_lower_threshold_gain(mock_calculate_average_brightness):
    # Arrange
    mock_calculate_average_brightness.return_value = 0.05
    capture = MagicMock()
    capture.shutter.fastest = 1
    capture.shutter.current = 10000
    capture.shutter.slowest = 10000
    capture.gain.current = 1.0
    capture.gain.highest = 8.0
    capture.gain.lowest = 1.0
    capture.exposure.target = 0.20
    capture.exposure.tolerance = 0.01

    # Act
    calculate_next_exposure_value("dummy_path", capture)

    # Assert
    assert math.isclose(capture.shutter.current, 10000)
    assert math.isclose(capture.gain.current, 1.1, rel_tol=0.5)


@patch("src.app.capture.exposure.calculate_average_brightness")
def test_brightness_within_tolerance(mock_calculate_average_brightness):
    # Arrange
    mock_calculate_average_brightness.return_value = 0.21
    capture = MagicMock()
    capture.shutter.fastest = 1
    capture.shutter.current = 550
    capture.shutter.slowest = 10000
    capture.gain.current = 3.0
    capture.gain.highest = 8.0
    capture.gain.lowest = 1.0
    capture.exposure.target = 0.20
    capture.exposure.tolerance = 0.02

    # Act
    calculate_next_exposure_value("dummy_path", capture)

    assert math.isclose(capture.shutter.current, 550)
    assert math.isclose(capture.gain.current, 3.0, rel_tol=0.5)
