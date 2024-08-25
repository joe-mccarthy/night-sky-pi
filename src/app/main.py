from .configuration.configuration import build_configuration
import logging as log
from datetime import datetime, timezone
from .observation.utils import get_observation
from .observation.filesystem import setup_observation_filesystem
from .housekeeping import perform_housekeeping
from .packaging import perform_packaging
from .capture.imaging import perform_observation

from time import sleep


def run(arguments):

    configuration = build_configuration(arguments.configuration)
    log.debug("entering nsp application")
    while True:
        current_datetime = datetime.now()
        log.debug("starting the root loop")
        log.debug("current datetime is %s", current_datetime)
        observation = get_observation(configuration, current_datetime)

        if observation.period.within_observation_period(current_datetime):
            log.info(
                "currently within an observation period till %s", observation.period.end
            )
            observation = setup_observation_filesystem(observation)
            perform_observation(observation, configuration)
        else:
            log.info(
                "not currently within observation period it will start @ %s",
                observation.period.start,
            )
            perform_housekeeping(configuration)
            perform_packaging(configuration)
            seconds_till_observation = (
                observation.period.calculate_wait_till_observation(datetime.now(timezone.utc))
            )
            log.debug("%s seconds till observation start", seconds_till_observation)
            log.info("waiting for observation period at %s", observation.period.start)
            sleep(seconds_till_observation)
        log.debug("ending the root loop")
