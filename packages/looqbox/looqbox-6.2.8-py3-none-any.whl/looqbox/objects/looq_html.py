from typing import Optional, List

from looqbox import CssOption
from looqbox.objects.looq_object import LooqObject
from looqbox.render.abstract_render import BaseRender
from looqbox.render.chatbot.components.text import _remove_html_tags


class ObjHTML(LooqObject):
    """
    Wraps an HTML code in a Looqbox object to be used in the interface.
    """

    def __init__(
        self,
        html: str,
        value: str = "",
        render_condition: bool = True,
        tab_label: str = "",
        css_options: Optional[List[CssOption]] = None,
        obj_class: Optional[List[str]] = None
    ):
        """
        Args:
            html (str): Html code that will be wrapped.
            tab_label (str): Set the name of the tab in the frame.

        Examples:
            >>> HTML = ObjHTML("<div> Hello Worlds </div>")
        """
        super().__init__(
            value=value,
            render_condition=render_condition,
            tab_label=tab_label,
            css_options=css_options,
            obj_class=obj_class
        )

        self.html = html
        self.tab_label = tab_label
        self.value = value

    def to_json_structure(self, visitor: BaseRender):
        return visitor.html_render(self)

    def __repr__(self):
        tags = _remove_html_tags(self.html)
        if tags is None:
            return ""
        return tags + self.value
