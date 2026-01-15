import json
import os
from importlib import resources as impresources
from typing import List, Optional

from looqbox_components import Colors

from looqbox import CssOption, ObjHTML, ObjRow, ObjText
from looqbox.objects.component_utility.icon_name import IconName, IconType
from looqbox.objects.looq_object import LooqObject
from looqbox.render.abstract_render import BaseRender

from ... import resources


class ObjIcon(LooqObject):
    resources_path = str(impresources.files(resources) / "ant_icons.json")
    with open(resources_path, "r") as f:
        icon_resources = json.load(f)

    def __init__(
        self,
        icon_name: IconName | str,
        icon_type: IconType = IconType.OUTLINED,
        color: Colors | str = Colors.DEFAULT_POSITIVE,
        size: str = "1.5em",
        css_options: Optional[List[CssOption]] = None,
    ):
        super().__init__(css_options=css_options)
        color = Colors.parse(color)
        self.color = color
        self.size = size
        self.css_options = CssOption.add(css_options, CssOption.FontSize(size))
        self.icon_type = icon_type.value

        rendered_name = getattr(icon_name, "value", None) or str(icon_name)
        if not isinstance(rendered_name, str):
            raise RuntimeError(
                "Something went wrong while rendering icon name.\nExpected a string or IconName but got: "
                + str(icon_name)
            )
        self.icon_name = rendered_name

    def to_json_structure(self, visitor: BaseRender):
        temp_square = ObjRow(
            ObjText(""),
            css_options=[
                CssOption.Width("2em"),
                CssOption.Height("2em"),
                CssOption.Background(Colors.parse(Colors.DEFAULT_POSITIVE)),
            ],
        )
        key_name = self.icon_name.replace("_", "-").lower()
        temp_svg = self.icon_resources.get(key_name)
        if temp_svg is None:
            return visitor.row_render(temp_square)
        text = f"""
            <div class="temp-icon" style="font-size: {self.size}; padding: 0.4em 0.4em 0.25em 0.4em; line-height: 1; color: white; background: {self.color}; border-radius: 0.2em;">
                {temp_svg}
            </div>
        """
        obj_html = ObjHTML(text)
        return visitor.html_render(obj_html)
        # return visitor.icon_render(self)
