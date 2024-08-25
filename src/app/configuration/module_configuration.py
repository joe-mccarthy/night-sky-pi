from dataclasses import dataclass
from typing import Optional
from dataclass_wizard import JSONWizard
from .core_configuration import LoggingConfig, DataConfig


@dataclass
class ModuleLoggingConfig(LoggingConfig):
    file: Optional[str] = None

    def merge(self, loggingConfig: LoggingConfig):
        if not self.path:
            self.path = loggingConfig.path
        if not self.level:
            self.level = loggingConfig.level
        if not self.format:
            self.format = loggingConfig.format
        if not self.rotation:
            self.rotation = loggingConfig.rotation


@dataclass
class HouseKeeping(JSONWizard):
    delete_after: int
    unit: Optional[str] = "DAYS"

    def __post_init__(self):
        if self.delete_after < 1.0:
            raise ValueError("Delete after must be greater or equal than 1.0")

    def get_age(self) -> int:
        if self.unit == "DAYS":
            return self.delete_after * 86400


@dataclass
class ModuleDataConfig(DataConfig):
    house_keeping: Optional[HouseKeeping] = None
