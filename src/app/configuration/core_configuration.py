from dataclasses import dataclass, field
from typing import Optional
from dataclass_wizard import JSONWizard


@dataclass
class LocationConfig(JSONWizard):
    latitude: float
    longitude: float

    def __post_init__(self):
        if self.latitude > 90 or self.latitude < -90:
            raise ValueError("Invalid Location:Latitude")
        if self.longitude > 180 or self.longitude < -180:
            raise ValueError("Invalid Location:Longitude")

    def data(self):
        return self.latitude, self.longitude


@dataclass
class DeviceConfig(JSONWizard):
    name: str
    location: LocationConfig


@dataclass
class LoggingFormatConfig(JSONWizard):
    date: str
    output: str


@dataclass
class LoggingRotationConfig(JSONWizard):
    size: int
    backup: int


@dataclass
class LoggingConfig(JSONWizard):
    path: Optional[str] = None
    level: Optional[str] = None
    format: Optional[LoggingFormatConfig] = None
    rotation: Optional[LoggingRotationConfig] = None


@dataclass
class DataConfig(JSONWizard):
    path: str