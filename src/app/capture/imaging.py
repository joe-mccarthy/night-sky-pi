from ..configuration.configuration import ObservatoryConfig
from ..observation.data import Observation
from ..utilities.conversions import microsecond_to_seconds
from datetime import datetime
import logging as log
from time import sleep, time
import subprocess
from ..configuration.nsp_configuration import Capture
from PIL import Image
import json


def perform_observation(
    observation: Observation, configuration: ObservatoryConfig
) -> None:
    log.info("starting observation capture period")
    log.debug("creating initial exposure values from configuration")
    capture_configuration: Capture = configuration.nsp.capture
    while observation.period.within_observation_period(datetime.now()):
        log.debug("within observation starting processes to capture single image")
        capture_configuration = __capture_image(observation, capture_configuration)
        delay = configuration.nsp.capture.exposure.delay
        log.debug("sleeping for %s seconds", delay)
        sleep(delay)
    log.info("completed observation capture period")


def __capture_image(observation: Observation, capture: Capture) -> Capture:
    log.debug("starting image capture")
    log.debug("capturing image for observation %s", observation.period.date)
    image_name = f"{round(time())}"
    image_format = ".jpg"
    filename = f"{observation.data_config.observation_image_path}{image_name}{image_format}"
    # Construct the command
    exposure_settings = (
        f"--shutter {capture.shutter.current} --gain {capture.gain.current} "
    )
    white_balance = (
        f"--awbgains {capture.white_balance.red},{capture.white_balance.blue} "
    )
    switches = "-n --immediate --denoise cdn_hq "
    command = "libcamera-still "

    call = f"{command} -o {filename} {exposure_settings} {white_balance} {switches}"

    try:
        log.debug("image capture timeout: %s", capture.timeout)
        subprocess.run(
            call,
            shell=True,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
            timeout=capture.timeout,
        )
        log.info("image capture completed")
        __create_json_file(observation, capture, image_name, image_format)
        calculate_next_exposure_value(filename, capture)
    except Exception as e:
        log.error(e)

    return capture

def __create_json_file(observation: Observation, capture: Capture, file_name: str,image_format: str) -> None:
    json_data = {
        "observation": {
            "date": observation.period.date,
            "start": observation.period.start.isoformat(),
            "end": observation.period.end.isoformat()
        },
        "data" : {
            "path": observation.data_config.path,
            "root_path": observation.data_config.root_path,
            "observation_image_path": observation.data_config.observation_image_path,
            "observation_data_path": observation.data_config.observation_data_path
        },
        "exposure" : {
            "shutter": microsecond_to_seconds(capture.shutter.current),
            "gain": capture.gain.current,
            "white_balance": {
                "red": capture.white_balance.red,
                "blue": capture.white_balance.blue
            }
        },
        "image" : {
            "path": f"{observation.data_config.observation_image_path}{file_name}{image_format}",
            "format": image_format,
            "filename": file_name
        }
    }
    
    output_file = f"{observation.data_config.observation_data_path}{file_name}.json"
    log.debug("Creating JSON file: %s", output_file)
    try:
        with open(output_file, 'w') as json_file:
            json.dump(json_data, json_file)
        log.debug("JSON file created successfully: %s", output_file)
    except Exception as e:
        log.error("Failed to create JSON file: %s", e)
    
def calculate_next_exposure_value(image_path, capture: Capture):

    average_brightness = calculate_average_brightness(image_path)

    log.debug("Average brightness: %s", average_brightness)
    current_shutter_speed = capture.shutter.current
    current_gain = capture.gain.current
    brightness_threshold = capture.exposure.target
    tolerance = capture.exposure.tolerance
    lower_threshold = brightness_threshold - tolerance
    upper_threshold = brightness_threshold + tolerance

    new_gain = current_gain
    new_shutter_speed = current_shutter_speed

    brightness_difference = abs(
        max(
            average_brightness - brightness_threshold,
            brightness_threshold - average_brightness,
        )
    )
    log.debug("Brightness difference: %s", brightness_difference)
    # Calculate adjustments
    if average_brightness < lower_threshold:
        # Image is too dark, increase shutter speed and gain
        log.debug("Image is too dark, increasing shutter speed and gain")
        temp_shutter = min(
            current_shutter_speed + (brightness_difference + current_shutter_speed),
            capture.shutter.slowest,
        )
        if temp_shutter < capture.shutter.slowest:
            new_shutter_speed = temp_shutter
        else:
            new_shutter_speed = capture.shutter.slowest
            new_gain = min(
                current_gain + (brightness_difference * current_gain),
                capture.gain.highest,
            )

    elif average_brightness > upper_threshold:
        log.debug("Image too bright, decreasing shutter speed and increasing gain")
        log.debug("current_gain: %s", current_gain)
        log.debug("capture.gain.lowest: %s", capture.gain.lowest)
        if current_gain == capture.gain.lowest:
            log.debug("Decreasing Shutter Speed")
            new_shutter_speed = max(
                current_shutter_speed - (current_shutter_speed * brightness_difference),
                capture.shutter.fastest,
            )
        else:
            log.debug("Decreasing Gain")
            new_gain = max(
                current_gain - (brightness_difference * current_gain),
                capture.gain.lowest,
            )
    else:
        # Image is within the target range
        log.debug("Image is within the target range, no adjustments needed")
        new_shutter_speed = current_shutter_speed
        new_gain = current_gain

    # Update the capture configuration
    capture.shutter.current = new_shutter_speed
    capture.gain.current = new_gain
    log.debug("New shutter speed: %s", microsecond_to_seconds(capture.shutter.current))
    log.debug("New gain: %s", capture.gain.current)
    log.debug("Next exposure value calculated")


def calculate_average_brightness(image_path):
    log.debug("Calculating next exposure value")
    image = Image.open(image_path, formats=["JPEG"])
    crop = image.convert("L")
    histogram = crop.histogram()
    pixels = sum(histogram)
    brightness = scale = len(histogram)

    for index in range(0, scale):
        ratio = histogram[index] / pixels
        brightness += ratio * (-scale + index)

    average_brightness = 1 if brightness == 255 else round(brightness / scale, 2)
    return average_brightness
