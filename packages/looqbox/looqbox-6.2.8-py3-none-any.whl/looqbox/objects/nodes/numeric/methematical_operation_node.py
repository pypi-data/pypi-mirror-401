from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic.dataclasses import dataclass

from looqbox.config.pydantic_configuration import PydanticConfiguration
from looqbox.objects.nodes.node import Node
from looqbox.objects.nodes.node_type import NodeType
from looqbox.objects.nodes.numeric.number_node import NumberNode


class ArithmeticOperator(Enum):
    SUM = "+"
    SUBTRACT = "-"
    MULTIPLY = "*"
    DIVIDE = "/"


@dataclass(config=PydanticConfiguration.Config)
class MathematicalOperation:
    function: ArithmeticOperator
    arguments: list[NumberNode | MathematicalOperationNode]

    def __str__(self) -> str:
        return ArithmeticOperator.value.join([str(arg) for arg in self.arguments])


@dataclass(config=PydanticConfiguration.Config)
class MathematicalOperationNode(Node):
    node_type: NodeType = NodeType.MATHEMATICAL_OPERATION
    text: Optional[str] = None
    apply: Optional[MathematicalOperation] = None

    def __str__(self) -> str:
        return str(self.apply)
