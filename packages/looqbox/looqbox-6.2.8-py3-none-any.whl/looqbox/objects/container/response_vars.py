from dataclasses import field
from typing import Optional, List, Any

from pydantic.dataclasses import dataclass

from looqbox.config.pydantic_configuration import PydanticConfiguration
from looqbox.configuration.popo.response_package_configurations import ResponsePackageConfiguration


@dataclass(config=PydanticConfiguration.Config)
class FeatureFlags:
    file_sync: dict[str, int]
    response_packages_configuration: Optional[ResponsePackageConfiguration] = field(default_factory=ResponsePackageConfiguration)

    def get(self, item, default=None):
        return getattr(self, item, default)


@dataclass(config=PydanticConfiguration.Config)
class ResponseVars:
    test_mode: bool
    home: str
    temp_dir: str
    jdbc_path: str
    response_timeout: int
    response_path: str
    entity_sync_path: str
    feature_flags: Optional[FeatureFlags] = None
    domains: Optional[List[dict]] = None
