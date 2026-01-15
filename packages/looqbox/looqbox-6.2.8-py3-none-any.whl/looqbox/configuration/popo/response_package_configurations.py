from dataclasses import field
from typing import Optional

from pydantic.dataclasses import dataclass

from looqbox.config.pydantic_configuration import PydanticConfiguration
from looqbox.configuration.popo.database_connection import QueryServiceConfiguration
from looqbox.configuration.popo.flow_settings import FlowSettings


@dataclass(config=PydanticConfiguration.Config)
class ResponsePackageConfiguration:
    """
    This class aim to hold remote configuration inject through a NoSQL collection.
    There are three main properties:
    - use_query_caller_as_default (bool) set whether the Query-Executor is the default query method
    - flow_settings (FlowSettings) hold any configuration regard the script or input flows
    - database_configuration (DatabaseConnectionConfiguration) carry configuration for the query feature
    """

    database_configuration: QueryServiceConfiguration = field(default_factory=QueryServiceConfiguration)
    flow_settings: FlowSettings = field(default_factory=FlowSettings)
    use_query_caller_as_default:Optional[bool] = False
