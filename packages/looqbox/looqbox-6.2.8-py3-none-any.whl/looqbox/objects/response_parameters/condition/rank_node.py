from typing import Optional

import numpy as np
from pydantic.dataclasses import dataclass

from looqbox.config.pydantic_configuration import PydanticConfiguration
from looqbox.objects.nodes.node import Node
from looqbox.objects.nodes.numeric.methematical_operation_node import MathematicalOperationNode
from looqbox.objects.nodes.numeric.number_node import NumberNode
from looqbox.objects.response_parameters.condition.commons.sort_direction import SortDirection
from looqbox.objects.response_parameters.condition.condition import Condition
from looqbox.objects.response_parameters.condition.condition_type import ConditionType
from looqbox_commons.src.main.logger.logger import RootLogger

log = RootLogger().get_new_logger("python_package")


@dataclass(config=PydanticConfiguration.Config)
class RankNode(Condition):
    condition_type: ConditionType = ConditionType.RANK
    text: Optional[str] = None
    direction: SortDirection = SortDirection.DESCENDING
    reference: Optional[Node] = None
    limit: Optional[NumberNode | MathematicalOperationNode] = None
    parameterName: Optional[str] = None
    id: Optional[int] = None

    def as_sql_filter(self, column_name: str) -> str:
        return ""

    def get_entity_type(self) -> str | None:
        return "$topn"

    def _retrieve_value(self) -> int:
        value = 10
        try:
            value = np.safe_eval(str(self.limit))
        except ValueError as e:
            log.warning(f"Error while retrieving value from node (defaulted to 10):\n{self.limit}\nError:\n{e}")
        return value
