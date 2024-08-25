"""
This module contains functions for performing housekeeping tasks on the data generated by the observatory.

The main function in this module is `perform_housekeeping`, which checks if housekeeping is enabled and if so, deletes files older than a certain age from the data location.

Functions:
    perform_housekeeping(config: ObservatoryConfig) -> None:
        Perform housekeeping tasks if enabled in the configuration. This includes deleting files older than a certain age from the data location.

    is_housekeeping_enabled(config: ObservatoryConfig) -> bool:
        Check if housekeeping is enabled in the configuration. Returns True if enabled, False otherwise.
"""

import logging as log
import os
import time

import magic

from .configuration.configuration import ObservatoryConfig
from typing import List


def perform_housekeeping(config: ObservatoryConfig) -> None:
    """
    Perform housekeeping tasks if enabled in the configuration.

    This function checks if housekeeping is enabled and if so, deletes files older than a certain age from the data location.
    The age of the files and the data location are specified in the configuration.

    Args:
        config (ObservatoryConfig): The configuration object containing the housekeeping settings.

    Returns:
        None
    """
    log.debug("entering house keeping")
    if not is_housekeeping_enabled(config):
        log.debug("house keeping is disabled")
        return
    log.debug("house keeping is enabled")

    data_location = f"{config.data.path}/{config.nsp.data.path}"
    age = config.nsp.data.house_keeping.get_age()
    for item in get_files_for_deletion(data_location, age):
        log.debug("file %s will be deleted", item)
        os.remove(item)
        log.info("deleted file %s", item)

    log.info("house keeping completed")


def is_housekeeping_enabled(config: ObservatoryConfig) -> bool:
    """
    Check if housekeeping is enabled in the configuration.

    This function checks if the data root path exists and if housekeeping is enabled in the configuration.

    Args:
        config (ObservatoryConfig): The configuration object containing the housekeeping settings.

    Returns:
        bool: True if housekeeping is enabled and the data root path exists, False otherwise.
    """
    log.debug("checking if house keeping is enabled")
    data_location = f"{config.data.path}/{config.nsp.data.path}"
    if not os.path.exists(data_location):
        log.warn("data root path %s does not exist", data_location)
        return False

    return config.nsp.data.house_keeping


def get_files_for_deletion(date_location, older_than) -> List[str]:
    """
    Get a list of files that are older than a certain age.

    This function scans the given directory and returns a list of files that are older than the specified age.
    Only files with a MIME type of "application/zip" are considered.

    Args:
        date_location (str): The directory to scan for files.
        older_than (int): The age in seconds. Files older than this age will be included in the returned list.

    Returns:
        List[str]: A list of file paths that are older than the specified age.
    """
    log.debug("getting files for deletion")

    files = []

    with os.scandir(date_location) as listOfEntries:
        for entry in listOfEntries:
            if entry.is_dir():
                log.debug("skipping check on %s it's a directory", entry.name)
                continue
            if magic.from_file(entry.path, mime=True) == "application/zip":
                age = time.time() - entry.stat().st_mtime
                log.debug("file %s has age %d ", entry.name, age)
                if age > older_than:
                    log.debug("file %s will be deleted", entry.name)
                    files.append(entry.path)
                    continue
                log.debug("file %s is not old enough for deletion", entry.name)

    log.debug("returning %d files for deletion", len(files))

    return files