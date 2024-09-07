# Night Sky Pi

[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/joe-mccarthy/night-sky-pi/build-test.yml?cacheSeconds=1)](https://github.com/joe-mccarthy/night-sky-pi/actions/workflows/build-test.yml)
[![Coveralls](https://img.shields.io/coverallsCoverage/github/joe-mccarthy/night-sky-pi?cacheSeconds=1)](https://coveralls.io/github/joe-mccarthy/night-sky-pi)
[![Sonar Quality Gate](https://img.shields.io/sonar/quality_gate/joe-mccarthy_night-sky-pi?server=https%3A%2F%2Fsonarcloud.io&cacheSeconds=1)](https://sonarcloud.io/project/overview?id=joe-mccarthy_night-sky-pi)
[![GitHub Release](https://img.shields.io/github/v/release/joe-mccarthy/night-sky-pi?sort=semver&cacheSeconds=1)](https://github.com/joe-mccarthy/night-sky-pi/releases/latest)
[![GitHub commits since latest release](https://img.shields.io/github/commits-since/joe-mccarthy/night-sky-pi/latest?cacheSeconds=1)](https://github.com/joe-mccarthy/night-sky-pi/compare/0.1.0...HEAD)
[![GitHub License](https://img.shields.io/github/license/joe-mccarthy/night-sky-pi?cacheSeconds=1)](LICENSE)

Night Sky Pi is a camera that takes images throughout the night currently from sunset till sunrise. These images are then zipped then the application waits for the next observation period. Along with the images that are taken there are supporting json files for each image with additional information. These data files currently contain the exposure and observation information for the image, allowing for processing off device later.

There could be additional json files created by other supporting applications. The Night Sky Pi can use MQTT to publish events so one could write other applications that respond to these events to complete additional task. One example would be to add weather information to the json file. Note: MQTT is not required for standard operation only for other applications to interact with the data in a timely manner.

## Hardware

Night Sky Pi has been created with certain hardware in mind. Wanting to keep the application simple, small and low cost the hardware that Night Sky Pi has targeted is the __Raspberry Pi Zero 2 W__. That being said any __Raspberry Pi__ more capable than this model should work fine. The camera used and tested is the __Raspberry Pi HQ Camera__, however the standard camera model could be used ensuring that the exposure times within the configuration are kept within the models capabilities.

## Prerequisites

Before deploying the Night Sky Pi it's important to ensure that you have the following configured as there are dependencies. However the installation of an MQTT broker is optional I usually have it installed instead of needing to remember to do it when starting up other applications.

### Python

Night Sky Pi is written in Python and has been tested with the following Python versions:

- Python 3.8
- Python 3.9
- Python 3.10
- Python 3.11

The [nsp.sh](nsp.sh) runs within a virtual environment based on what's on your system path.

### MQTT Broker

Night Sky Pi has the ability to publish events to an MQTT broker. The intent of this is so that other modules can react to the events to complete additional actions. Initially this broker will only run locally therefore only allow clients that reside on the same device as intended. Firstly we need to install MQTT on the Raspberry Pi.

```bash
sudo apt update && sudo apt upgrade
sudo apt install -y mosquitto
sudo apt install -y mosquitto-clients # Optional for testing locally
sudo systemctl enable mosquitto.service
sudo reboot # Just something I like to do, this is optional as well
```

The next step is to configure the Night Sky Pi to use the MQTT broker, as MQTT events are disabled by default.

```json
"device" : {
    "mqtt" : {
        "enabled": true,
        "host": "127.0.0.1"
    }
}
```

## Configuration

All configuration of the Night Sky Pi is done through the [config.json](config.json), which is passed into the Night Sky Pi as an argument. It's best not to update the configuration within the repository but to copy it to another location and use that for running the Night Sky Pi.

### Configuration Items

#### Device

- __name__ : 
- __location__ : 
  - __latitude__ :
  - __longitude__ :
- __mqtt__ :
  - __enabled__ :
  - __host__ :

#### Logging

#### Data

#### NSP

##### Data

##### Logging

##### Capture

## Running Night Sky Pi

## Outputs

### MQTT

If MQTT has been [enabled](#mqtt-broker) on Night Sky Pi, there are a couple of events that are fired through the running of the application.

#### Observation Started

When an observation starts and the file structure has been created Night Sky Pi will fire an event to the "nsp/observation-started" topic, below is an example of what to expect in the message payload.

```json
{
    "observation": {
        "date": "2024-09-04",
        "start": "2024-09-04T19:38:00+01:00",
        "end": "2024-09-05T06:19:00+01:00"
    },
    "data": {
        "path": "/home/joseph/nsp/data/observations/2024-09-04/",
        "root_path": "/home/joseph/nsp/data/observations/",
        "observation_image_path": "/home/joseph/nsp/data/observations/2024-09-04/images/",
        "observation_data_path": "/home/joseph/nsp/data/observations/2024-09-04/data/"
    }
}
```

#### Image Captured

Each and every time that an image has been captured and saved to disk. Night Sky Pi will publish a message to the "nsp/image-captured" topic, below is an example of what to expect in the message payload.

```json
{
    "observation": {
        "date": "2024-09-04",
        "start": "2024-09-04T19:38:00+01:00",
        "end": "2024-09-05T06:19:00+01:00"
    },
    "data": {
        "path": "/home/joseph/nsp/data/observations/2024-09-04/",
        "root_path": "/home/joseph/nsp/data/observations/",
        "observation_image_path": "/home/joseph/nsp/data/observations/2024-09-04/images/",
        "observation_data_path": "/home/joseph/nsp/data/observations/2024-09-04/data/"
    },
    "exposure": {
        "shutter": 0.25,
        "gain": 1,
        "white_balance": {
            "red": 2.8,
            "blue": 1.7
        }
    },
    "image": {
        "path": "/home/joseph/nsp/data/observations/2024-09-04/images/1725490896.jpg",
        "format": ".jpg",
        "filename": "1725490896"
    }
}
```

### Observation Completed

When an observation has reached it's completed datetime Night Sky Pi will fire an event to the "nsp/observation-ended" topic, below is an example of what to expect in the message payload.

```json
{
    "observation": {
        "date": "2024-09-04",
        "start": "2024-09-04T19:38:00+01:00",
        "end": "2024-09-05T06:19:00+01:00"
    },
    "data": {
        "path": "/home/joseph/nsp/data/observations/2024-09-04/",
        "root_path": "/home/joseph/nsp/data/observations/",
        "observation_image_path": "/home/joseph/nsp/data/observations/2024-09-04/images/",
        "observation_data_path": "/home/joseph/nsp/data/observations/2024-09-04/data/"
    }
}
```

### Archive Deleted

During house keeping there is an configuration option to delete zipped archives that are older than a configured number of days. If enabled and an archive is deleted, Night Sky Pi will fire an event to the "nsp/file-deleted" topic, below is an example of what to expect in the message payload.

```json
{
    "file": "/home/joseph/nsp/data/observations/2024-08-30.zip"
}
```

### Archive Completed

After the observation and housekeeping the Night Sky Pi will archive the entire observation folder. This operation can take a while once completed, Night Sky Pi will fire an event to the "nsp/archive-completed" topic, below is an example of what to expect in the message payload.

```json
{
    "name": "2024-09-04",
    "format": "zip",
    "folder" : "/home/joseph/nsp/data/observations/",
    "path": "/home/joseph/nsp/data/observations/2024-09-04.zip"
}
```

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

Don't forget to give the project a star! Thanks again!

1. Fork the Project
1. Create your Feature Branch (git checkout -b feature/AmazingFeature)
1. Commit your Changes (git commit -m 'Add some AmazingFeature')
1. Push to the Branch (git push origin feature/AmazingFeature)
1. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
