from unittest.mock import MagicMock
from src.app.capture.reporting import create_json_file
import json

def test_create_json_file():
    # Create a mock observation and capture configuration
    observation = MagicMock()
    observation.period.date = "2022-01-01"
    observation.period.start.isoformat.return_value = "2022-01-01T00:00:00"
    observation.period.end.isoformat.return_value = "2022-01-01T01:00:00"
    observation.data_config.path = "./tests/scratch/"
    observation.data_config.root_path = "./tests/scratch/"
    observation.data_config.observation_image_path = "./tests/scratch/"
    observation.data_config.observation_data_path = "./tests/scratch/"

    capture = MagicMock()
    capture.shutter.current = 100
    capture.gain.current = 1
    capture.white_balance.red = 0.5
    capture.white_balance.blue = 0.5

    file_name = "image123"
    image_format = ".jpg"

    # Call the function
    create_json_file(observation, capture, file_name, image_format)

    # Assert that the JSON file was created with the correct data
    expected_json_data = {
        "observation": {
            "date": "2022-01-01",
            "start": "2022-01-01T00:00:00",
            "end": "2022-01-01T01:00:00"
        },
        "data" : {
            "path": "./tests/scratch/",
            "root_path": "./tests/scratch/",
            "observation_image_path":"./tests/scratch/",
            "observation_data_path": "./tests/scratch/"
        },
        "exposure" : {
            "shutter": 0.0001,
            "gain": 1,
            "white_balance": {
                "red": 0.5,
                "blue": 0.5
            }
        },
        "image" : {
            "path": "./tests/scratch/image123.jpg",
            "format": ".jpg",
            "filename": "image123"
        }
    }

    with open("./tests/scratch/image123.json") as json_file:
        actual_json_data = json.load(json_file)

    assert actual_json_data == expected_json_data