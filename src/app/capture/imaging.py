from ..configuration.configuration import ObservatoryConfig
from ..configuration.core_configuration import MQTTConfig
from ..observation.data import Observation
from .reporting import create_json_file
from .exposure import calculate_next_exposure_value
from datetime import datetime
import logging as log
from time import sleep, time
import subprocess
from ..configuration.nsp_configuration import Capture
from ..utilities.mqtt_client import publish_message


def perform_observation(
    observation: Observation, configuration: ObservatoryConfig
) -> None:
    log.info("starting observation capture period")
    log.debug("creating initial exposure values from configuration")
    capture_configuration: Capture = configuration.nsp.capture
    mqtt_config = configuration.device.mqtt
    while observation.period.within_observation_period(datetime.now()):
        log.debug("within observation starting processes to capture single image")
        capture_configuration = __capture_image(
            observation, capture_configuration, mqtt_config
        )
        delay = configuration.nsp.capture.exposure.delay
        log.debug("sleeping for %s seconds", delay)
        sleep(delay)
    log.info("completed observation capture period")


def __capture_image(
    observation: Observation, capture: Capture, mqtt_config: MQTTConfig
) -> Capture:
    log.debug("starting image capture")
    log.debug("capturing image for observation %s", observation.period.date)
    image_name = f"{round(time())}"
    image_format = ".jpg"
    filename = (
        f"{observation.data_config.observation_image_path}{image_name}{image_format}"
    )
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
        json = create_json_file(observation, capture, image_name, image_format)
        publish_message(config=mqtt_config, topic="nsp/image-captured", payload=json)
        calculate_next_exposure_value(filename, capture)
    except Exception as e:
        log.error(e)

    return capture
