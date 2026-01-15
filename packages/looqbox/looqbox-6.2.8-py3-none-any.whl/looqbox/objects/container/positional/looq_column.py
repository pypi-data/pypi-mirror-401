from typing import List, Optional, Collection

from looqbox.objects.component_utility.css_option import CssOption
from looqbox.objects.container.positional.abstract_positional_container import AbstractPositionalContainer
from looqbox.objects.looq_object import LooqObject
from looqbox.render.abstract_render import BaseRender


class ObjColumn(AbstractPositionalContainer):
    """
    Class to create a column container. Children will be displayed vertically.
    """

    def __init__(
            self,
            *children: Collection[LooqObject] | LooqObject,
            value: str = "",
            render_condition: bool = True,
            tab_label: str = "",
            css_options: Optional[List[CssOption]] = None,
            obj_class: Optional[List[str]] = None  # pyright: ignore [reportUndefinedVariable]
    ):
        # noinspection PyUnresolvedReferences
        """
                :param children: Children to be contained.

                Examples:
                    >>> ObjColumn(
                    >>>     ObjPlotly(chart_1),
                    >>>     ObjPlotly(chart_2)
                    >>> )
        """
        super().__init__(
            *children,
            value=value,
            render_condition=render_condition,
            tab_label=tab_label,
            css_options=css_options,
            obj_class=obj_class
        )


    def to_json_structure(self, visitor: BaseRender):
        return visitor.column_render(self)
