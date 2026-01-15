from typing import Optional

from pydantic.dataclasses import dataclass

from looqbox.config.pydantic_configuration import PydanticConfiguration


@dataclass(config=PydanticConfiguration.Config)
class FlowSettings:
    """
    This class holds info and configuration for script and input flows
    """
    stacktrace_level:Optional[int] = 0
