from src.app.utilities import conversions
import math


def test_microseconds_to_hundredth_second():
    microseconds = 10000
    seconds = conversions.microsecond_to_seconds(microseconds)
    assert math.isclose(seconds,0.01)



def test_microseconds_to_tenth_second():
    microseconds = 100000
    seconds = conversions.microsecond_to_seconds(microseconds)
    assert math.isclose(seconds,0.1)



def test_simple_micro_to_seconds():
    microseconds = 1000000
    seconds = conversions.microsecond_to_seconds(microseconds)
    assert math.isclose(seconds,1.0)
