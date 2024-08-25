import logging as log
from typing import List
from .configuration.configuration import ObservatoryConfig
import os, shutil
import pathlib


def perform_packaging(config: ObservatoryConfig) -> None:
    log.debug("starting the packaging process")
    data_location = f"{config.data.path}/{config.nsp.data.path}"

    if not is_packaging_required(data_location):
        log.debug("no packaging required")
        log.info("packaging processes completed")
        return

    for item in data_directory_contents(config):
        log.info("packaging item %s", item)
        folder_name = pathlib.PurePath(item).name
        __zip_folder(item, data_location, folder_name)
        __delete_folder(item)
        log.info("packaging of %s completed", item)

    log.info("packaging processes completed")


def data_directory_contents(config: ObservatoryConfig) -> List[str]:
    log.debug("scanning data directory for folders to compress")
    data_location = f"{config.data.path}/{config.nsp.data.path}"
    log.debug("data directory set to %s", data_location)
    directories = []
    for path in sorted(os.listdir(data_location)):
        log.debug("checking item %s for compression", path)
        if os.path.isdir(os.path.join(data_location, path)):
            log.debug("%s is a directory directory will be compressed", path)
            directories.append(os.path.join(data_location, path))

    log.debug("found %s directories that need compression", len(directories))
    return directories


def is_packaging_required(data_location: str) -> bool:

    if not os.path.exists(data_location):
        log.warning("data root path %s does not exist", data_location)
        return False

    log.debug("checking if packaging is required")
    log.debug("checking root folder %s", data_location)

    processing_required = False
    for path in sorted(os.listdir(data_location)):
        log.debug("checking item %s for processing", path)
        if os.path.isdir(os.path.join(data_location, path)):
            log.debug("%s is a directory processing will be required", path)
            processing_required = True

    return processing_required


def __zip_folder(source, root, base) -> None:
    log.debug("about to compress directory %s into %s.zip", base, base)
    shutil.make_archive(source, "zip", root, base)
    log.info("completed compression of %s into %s.zip", base, base)


def __delete_folder(path: str) -> None:
    log.debug("deleting %s", path)
    shutil.rmtree(path)
    log.debug("directory %s has been deleted", path)
