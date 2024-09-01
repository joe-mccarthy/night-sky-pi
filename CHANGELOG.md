# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- [#9](https://github.com/joe-mccarthy/night-sky-pi/issues/9) A configurable cooldown has been added to the end of an observation to allow other processes to possibly complete
- [#3](https://github.com/joe-mccarthy/night-sky-pi/issues/3) Ability to publish messages to an MQTT Broker with supporting documentation.
- [#4](https://github.com/joe-mccarthy/night-sky-pi/issues/4) Observation, Capture, Data and file information stored in data directory for image.
  
### Changed

- [#10](https://github.com/joe-mccarthy/night-sky-pi/issues/10) Modified timeout for the image capture subprocess to be configurable with a default
- [#5](https://github.com/joe-mccarthy/night-sky-pi/issues/5) Resolved Sonar issues from the previous release
- [#6](https://github.com/joe-mccarthy/night-sky-pi/issues/6) Added utility to convert microseconds to seconds for easier to read logs and messages
- [#8](https://github.com/joe-mccarthy/night-sky-pi/issues/8) Configuration for the application is reloaded at the start of every observation rather and application startup
- [#11](https://github.com/joe-mccarthy/night-sky-pi/pull/11) Update dependencies via dependabot, freeze suntime version as known breakage about **1.2.5**

### Fixed

- [#12](https://github.com/joe-mccarthy/night-sky-pi/issues/12) Logging configuration being ignored, introduced by [#8](https://github.com/joe-mccarthy/night-sky-pi/issues/8)

## [0.1.0]

Initial Testing Release

[unreleased]: https://github.com/joe-mccarthy/night-sky-pi/compare/0.1.0...HEAD
[0.1.0]: https://github.com/joe-mccarthy/night-sky-pi/releases/tag/0.1.0
