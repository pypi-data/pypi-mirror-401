import re
from abc import abstractmethod
from typing import Optional, List, Collection

from looqbox.objects.component_utility.css_option import CssOption
from looqbox.objects.container.abstract_container import AbstractContainer
from looqbox.objects.looq_object import LooqObject
from looqbox.render.abstract_render import BaseRender
from looqbox_commons import parse_float_or_none

NUMBER_REGEX = r"[0-9\.,]+"


class AbstractPositionalContainer(AbstractContainer):
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
            *children,
            value=value,
            render_condition=render_condition,
            tab_label=tab_label,
            css_options=css_options,
            obj_class=obj_class
        )

    def __str__(self):
        children_content = ", ".join(str(c) for c in self.children)
        return f"{self.__class__.__name__}({children_content})"

    def __repr__(self):
        return self.__str__()

    @abstractmethod
    def to_json_structure(self, visitor: BaseRender):
        """
        Convert python objects into json to Front-End render
        """

    @property
    def set_main_alignment_start(self):
        self.css_options = CssOption.add(self.css_options, CssOption.JustifyContent.flex_start)
        return self

    @property
    def set_cross_alignment_start(self):
        self.css_options = CssOption.add(self.css_options, CssOption.AlignContent.flex_start)
        self.css_options = CssOption.add(self.css_options, CssOption.AlignItems.flex_start)
        return self

    @property
    def set_main_alignment_space_around(self):
        self.css_options = CssOption.add(self.css_options, CssOption.JustifyContent.space_around)
        return self

    @property
    def set_cross_alignment_space_around(self):
        self.css_options = CssOption.add(self.css_options, CssOption.AlignContent.space_around)
        self.css_options = CssOption.add(self.css_options, CssOption.AlignItems.stretch)
        return self

    @property
    def set_main_alignment_space_between(self):
        self.css_options = CssOption.add(self.css_options, CssOption.JustifyContent.space_between)
        return self

    @property
    def set_cross_alignment_space_between(self):
        self.css_options = CssOption.add(self.css_options, CssOption.AlignContent.space_between)
        self.css_options = CssOption.add(self.css_options, CssOption.AlignItems.stretch)
        return self

    @property
    def set_main_alignment_space_evenly(self):
        self.css_options = CssOption.add(self.css_options, CssOption.JustifyContent.space_evenly)
        return self

    @property
    def set_cross_alignment_space_evenly(self):
        self.css_options = CssOption.add(self.css_options, CssOption.AlignContent.space_evenly)
        self.css_options = CssOption.add(self.css_options, CssOption.AlignItems.stretch)
        return self

    @property
    def set_main_alignment_center(self):
        self.css_options = CssOption.add(self.css_options, CssOption.JustifyContent.center)
        return self

    @property
    def set_cross_alignment_center(self):
        self.css_options = CssOption.add(self.css_options, CssOption.AlignContent.center)
        self.css_options = CssOption.add(self.css_options, CssOption.AlignItems.stretch)
        return self

    @property
    def set_main_alignment_end(self):
        self.css_options = CssOption.add(self.css_options, CssOption.JustifyContent.flex_end)
        return self

    @property
    def set_cross_alignment_end(self):
        self.css_options = CssOption.add(self.css_options, CssOption.AlignContent.flex_end)
        self.css_options = CssOption.add(self.css_options, CssOption.AlignItems.stretch)
        return self

    @property
    def add_border(self):
        self.css_options = CssOption.add(self.css_options, CssOption.Border("1px solid #DBDBDB"))
        self.css_options = CssOption.add(self.css_options, CssOption.BoxShadow("0px 4px 6px rgb(31 70 88 / 4%)"))
        self.css_options = CssOption.add(self.css_options, CssOption.BorderRadius("10px"))
        return self

    @staticmethod
    def _divide_value(value) -> str:
        tokens = value.split()
        new_tokens = []
        for token in tokens:
            found_number = re.search(str(NUMBER_REGEX), token)
            if found_number is None or not (first_value := found_number.group()):
                continue
            number = parse_float_or_none(first_value)
            if number is None:
                continue
            new_number = round(number / 2, 4)
            new_value = value.replace(first_value, str(new_number))
            new_tokens.append(new_value)
        return " ".join(new_tokens)

    def _add_inbetween_pars(self, first_par, second_par):
        num_children = len(self.children)
        for idx in range(num_children):
            not_first = idx > 0
            not_last = idx < num_children - 1
            current_child = self.children[idx]

            if not_first:
                current_child.css_options = CssOption.add(current_child.css_options, first_par)

            if not_last:
                current_child.css_options = CssOption.add(current_child.css_options, second_par)

    def set_horizontal_child_spacing(self, value):

        value = self._divide_value(value)
        margin_left = CssOption.Margin.left("{value}".format(value=value))
        margin_right = CssOption.Margin.right("{value}".format(value=value))

        self._add_inbetween_pars(margin_left, margin_right)
        return self

    def set_vertical_child_spacing(self, value):

        value = self._divide_value(value)
        margin_top = CssOption.Margin.top("{value}".format(value=value))
        margin_bottom = CssOption.Margin.bottom("{value}".format(value=value))

        self._add_inbetween_pars(margin_top, margin_bottom)

        return self

    def set_to_all_child(self, css_option):
        for child in self.children:
            child.css_options = CssOption.add(child.css_options, css_option)
        return self

    def _remove_constraint(self, constraint):
        self.obj_class = [e for e in self.obj_class or [] if constraint not in e]

    def _set_single_constraint(self, value, constraint):
        if value not in list(range(1, 13)):
            raise ValueError("Invalid constraint, must be between 1 and 12 - Received: {value}".format(value=value))
        self.obj_class = (self.obj_class or []) + [constraint + "-" + str(value)]
        self.css_options = CssOption.add(self.css_options, CssOption.Padding("0px"))

    def _set_constraints(self, value, constraint):
        self._remove_constraint(constraint)
        self._set_single_constraint(value, constraint)
        return self

    def set_size(self, value, constraints=("col-md", "col-sm", "col-xs")):
        for constraint in constraints:
            self._set_constraints(value, constraint)
        return self

    def set_desktop_size(self, value):
        return self.set_size(value, constraints=["col-md"])

    def set_tablet_size(self, value):
        return self.set_size(value, constraints=["col-sm"])

    def set_mobile_size(self, value):
        return self.set_size(value, constraints=["col-xs"])
