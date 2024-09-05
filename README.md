# Night Sky Pi

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/joe-mccarthy/night-sky-pi/build-test.yml?cacheSeconds=1)
![Coveralls](https://img.shields.io/coverallsCoverage/github/joe-mccarthy/night-sky-pi?cacheSeconds=1)
![Sonar Quality Gate](https://img.shields.io/sonar/quality_gate/joe-mccarthy_night-sky-pi?server=https%3A%2F%2Fsonarcloud.io&cacheSeconds=1)
![GitHub Release](https://img.shields.io/github/v/release/joe-mccarthy/night-sky-pi?sort=semver&cacheSeconds=1)
![GitHub commits since latest release](https://img.shields.io/github/commits-since/joe-mccarthy/night-sky-pi/latest?cacheSeconds=1)
![GitHub License](https://img.shields.io/github/license/joe-mccarthy/night-sky-pi?cacheSeconds=1)

## Hardware

## Prerequisites

### Python

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

## Outputs

### MQTT

#### Observation Started

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

```json
{
    "file": "/home/joseph/nsp/data/observations/2024-08-30.zip"
}
```

### Archive Completed

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
