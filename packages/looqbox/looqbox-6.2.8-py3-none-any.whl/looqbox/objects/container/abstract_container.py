from abc import abstractmethod
from typing import Optional, List, Collection, cast

from looqbox.objects.component_utility.css_option import CssOption
from looqbox.objects.looq_object import LooqObject
from looqbox.render.abstract_render import BaseRender


class AbstractContainer(LooqObject):
    children: List[LooqObject]

    def __init__(
            self,
            *children: Collection[LooqObject] | LooqObject,
            value: str = "",
            render_condition: bool = True,
            tab_label: str = "",
            css_options: Optional[List[CssOption]] = None,
            obj_class: Optional[List[str]] = None
    ):
        """
        :param children: Children to be contained.
        """
        super().__init__(
            value=value,
            render_condition=render_condition,
            tab_label=tab_label,
            css_options=css_options,
            obj_class=obj_class
        )

        if isinstance(children, LooqObject):
            raise TypeError(f"Could not parse provided children as a list of looq objects, provided type was: {children.__class__.__name__}")

        casted_children = list(children)
        self._check_content_size(casted_children)

        if isinstance(casted_children[0], list):
            casted_children = casted_children[0]

        self.children = casted_children


    @staticmethod
    def _check_content_size(children: Collection[LooqObject]):
        if not children:
            # With this we avoid breaking the frontend rendering
            raise IndexError("A positional container must have at least one element.")

    @abstractmethod
    def to_json_structure(self, visitor: BaseRender):
        """
        Convert python objects into json to Front-End render
        """

    def __eq__(self, other):
        return self.children.__class__ == other.children.__class__ and vars(self) == vars(other)

    def __hash__(self):
        return hash((self.__class__, str(vars(self).items())))
