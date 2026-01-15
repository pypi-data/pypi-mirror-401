from dataclasses import dataclass
from typing import cast

from looqbox.objects.component_utility.css import Css
from looqbox.objects.component_utility.flex_css import FlexCss
from looqbox.objects.component_utility.layout_css import LayoutCss
from looqbox.objects.component_utility.positional_css import PositionalCss
from looqbox.objects.component_utility.self_positional import SelfPositional
from looqbox.objects.component_utility.text_css import TextCss

"""
Draft with use example

import CssOptions as css

css_properties = [css.TextAlignLeft, css.BackgroundColor("Black")]

for p in css_properties:
    print(p.property + " : " + p.value)
    
"""


@dataclass(slots=True)
class CssOption(Css):
    AlignContent = cast("CssOption", PositionalCss("alignContent", "center"))
    AlignItems = cast("CssOption", PositionalCss("alignItems", "center"))
    AlignSelf = cast("CssOption", SelfPositional("alignSelf", "center"))
    Animation = cast("CssOption", Css("animation", None))
    Background = cast("CssOption", Css("background", None))
    BackgroundColor = cast("CssOption", Css("backgroundColor", None))
    BackgroundImage = cast("CssOption", Css("backgroundImage", None))
    Border = cast("CssOption", LayoutCss("border", None))
    BorderColor = cast("CssOption", Css("borderColor", None))
    BorderRadius = cast("CssOption", Css("borderRadius", None))
    BorderStyle = cast("CssOption", Css("borderStyle", None))
    BorderWidth = cast("CssOption", Css("borderWidth", None))
    Bottom = cast("CssOption", Css("bottom", None))
    BoxShadow = cast("CssOption", Css("boxShadow", None))
    BoxSizing = cast("CssOption", Css("boxSizing", None))
    Color = cast("CssOption", Css("color", None))
    Display = cast("CssOption", Css("display", None))
    Flex = cast("CssOption", Css("flex", None))
    FlexDirection = cast("CssOption", FlexCss("flexDirection", None))
    FlexWrap = cast("CssOption", Css("flexWrap", None))
    FontFamily = cast("CssOption", Css("fontFamily", None))
    FontSize = cast("CssOption", Css("fontSize", None))
    FontWeight = cast("CssOption", Css("fontWeight", None))
    Height = cast("CssOption", Css("height", None))
    JustifyContent = cast("CssOption", PositionalCss("justifyContent", "space-between"))
    Left = cast("CssOption", Css("left", None))
    LetterSpacing = cast("CssOption", Css("letterSpacing", None))
    LineHeight = cast("CssOption", Css("lineHeight", None))
    Margin = cast("CssOption", LayoutCss("margin", None))
    MaxHeight = cast("CssOption", Css("maxHeight", None))
    MaxWidth = cast("CssOption", Css("maxWidth", None))
    MinHeight = cast("CssOption", Css("minHeight", None))
    MinWidth = cast("CssOption", Css("minWidth", None))
    Overflow = cast("CssOption", Css("overflow", None))
    Padding = cast("CssOption", LayoutCss("padding", None))
    Position = cast("CssOption", Css("position", None))
    Right = cast("CssOption", Css("right", None))
    Scale = cast("CssOption", Css("scale", None))
    TextAlign = cast("CssOption", TextCss("textAlign", "start"))
    TextDecoration = cast("CssOption", Css("textDecoration", None))
    TextOverflow = cast("CssOption", Css("textOverflow", None))
    Top = cast("CssOption", Css("top", None))
    Transform = cast("CssOption", Css("transform", None))
    TransformOrigin = cast("CssOption", Css("transformOrigin", None))
    WhiteSpace = cast("CssOption", Css("whiteSpace", None))
    Width = cast("CssOption", Css("width", None))
    ZIndex = cast("CssOption", Css("zIndex", None))

    def __call__(self, *args, **kwargs) -> "CssOption":
        return super.__call__(*args, **kwargs)

    @classmethod
    def export(cls, css_options):
        if css_options is None:
            return []
        return {
            css.property: css.value
            for css in css_options if css.value is not None
        }

    @classmethod
    def add(cls, css_options, option):
        if css_options is None:
            css_options = [option]
        else:
            css_options = list(set(css_options).union({option}))
        return css_options

    @classmethod
    def clear(cls, css_options, option):
        if css_options is None:
            return css_options
        css_options = list(set(css_options).difference(set(option)))
        return css_options
