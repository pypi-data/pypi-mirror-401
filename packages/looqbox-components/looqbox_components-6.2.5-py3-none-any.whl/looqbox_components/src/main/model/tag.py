from dataclasses import dataclass
from math import inf
from typing import List, Optional

from looqbox import CssOption, ObjRow, ObjText, format, ObjColumn, ObjHTML
from looqbox.objects.looq_object import LooqObject
from looqbox_commons import Range, parse_float_or_none
from looqbox_components import Colors
from looqbox_components.src.main.utils.texts import obj_texts_from

"""
Fill free to add some static constants here!!!
"""
DOWN_SYMBOL = "↓"
UP_SYMBOL = "↑"

DEFAULT_UP_COLOR = Colors.DEFAULT_POSITIVE
DEFAULT_DOWN_COLOR = Colors.COLOR_RED_ERROR_600


@dataclass
class TagRule:
    """
    Please provide a str or ObjHTML at symbol...
    It wasn't specifically typed because of our current LazyLoad structure
    """

    range: Range
    text: Optional[str] = None
    symbol: Optional[str | LooqObject] = None
    color: Optional[Colors | str] = None
    size: Optional[int] = None
    value_format: Optional[str] = "percent:1"


@dataclass
class TagContent:
    """
    You can format the value yourself or use the value format parameter.
    """

    value: Optional[str | int | float] = None
    text: Optional[str] = None
    rule_by_range: Optional[List[TagRule]] = None
    value_format: Optional[str] = "percent:1"
    size: Optional[int] = None
    color: Optional[Colors | str] = None
    text_spacing: Optional[float] = None
    height: Optional[str] = None
    width: Optional[str] = None


class Tag(LooqObject):
    """
    This class represents a color tag for displaying values with optional rules for color-coding and formatting.
    """

    def __init__(self, tag_value: int | float | str, **template_options):
        """
        Args:
            tag_value (int | float | str): The value to be displayed in the tag.
            template_options (dict, optional): The options for the tag template. Keys include:
                - tag_rules (list of dict): Rules for color-coding the tag value based on its numerical value. Each dictionary must have:
                    * symbol (str or ObjHTML, optional): Displayed before the tag value.
                    * color (str): Color displayed when the value is within "range".
                    * range (list of [float, float]): Range in which the parameters above will appear.
                - default_color (str, optional): The default text color of the tag if no rule is applicable.
                - tag_format (str, optional): The formatting of the tag value.


        Returns:
            Tag: A tag object.

        Examples:
            >>> rules = [
            >>>     {
            >>>         "symbol": "↓",
            >>>         "color": "#E92C2C",
            >>>         "range": [-np.inf, 40]
            >>>     },
            >>>     {
            >>>         "color": "#DBA800",
            >>>         "symbol": "<div class=\"fa fa-trash-o\"></div>",
            >>>         "range": [40, 80]
            >>>     },
            >>>     {
            >>>         "symbol": "↑",
            >>>         "color": "#00BA34",
            >>>         "range": [80, np.inf]
            >>>     }
            >>> ]
            >>>
            >>> return lq.ResponseFrame(
            >>>     [
            >>>         lq.ObjColumn(
            >>>             Tag(4),
            >>>             Tag(45, tag_rules = regras)
            >>>             )
            >>>     ]
            >>> )
        """

        self.tag_rules = [
            {
                "symbol": "↓",
                "color": "#E92C2C",
                "range": [-inf, 0]
            },
            {
                "symbol": "↑",
                "color": "#00BA34",
                "range": [0, inf]
            },

        ]

        self.tag_must_have_properties = ["default_color", "tag_format", "tag_rules"]

        self.tag_properties = self._get_tag_properties(template_options)

        self.container_properties = self._get_template_properties(template_options)

        super().__init__(**self.container_properties)

        self.tag_value = tag_value or "-"

        self._text_default_style = [
            CssOption.FontSize("14px")
        ]

        self._container_default_style = [
            CssOption.AlignItems.center,
            CssOption.JustifyContent.center,
            CssOption.BorderRadius("6px"),
            CssOption.Border("4px"),
            CssOption.Height("24px"),
            CssOption.Width("fit-content"),
            CssOption.Padding("0px 5px")
        ]

    def _set_tag_style_values(self):
        self.default_color = self.tag_properties.get("default_color", "#797979")
        self.tag_format = self.tag_properties.get("tag_format", "number:1")
        self.tag_rules = self.tag_properties.get("tag_rules", self.tag_rules)

    def _get_template_properties(self, tag_options) -> dict:
        return {property_key: value for property_key, value in tag_options.items() if
                property_key not in self.tag_must_have_properties}

    def _get_tag_properties(self, tag_options) -> dict:

        return {property_key: value for property_key, value in tag_options.items() if
                property_key in self.tag_must_have_properties}

    def _set_element_style(self, element) -> CssOption:
        for style in self._get_defined_style():
            element.css_options = CssOption.add(element.css_options, style)
        return element

    def _get_defined_style(self):
        if self.css_options is None:
            self.css_options = []
        return list(set(self.css_options).union(set(self._container_default_style)))

    @property
    def invert_default_color(self):
        range_list = [e.get("range") for e in self.tag_rules]
        inverse_range_list = list(reversed(range_list))
        for rule, new_rule in zip(self.tag_rules, inverse_range_list):
            rule["range"] = new_rule
        return self

    def set_font_size(self, font_size: int | str):
        self._text_default_style = CssOption.add(self.css_options, CssOption.FontSize(font_size))
        self._container_default_style = CssOption.clear(self._container_default_style,
                                                        [CssOption.Height("24px")])
        self._container_default_style = CssOption.add(self._container_default_style,
                                                      CssOption.Height(10 + font_size))
        return self

    def _is_number(self) -> bool:
        return self.tag_value and not isinstance(self.tag_value, str)

    def _is_in_range(self, rule) -> bool:
        return rule["range"][0] <= self.tag_value <= rule["range"][1]

    def _get_rule_by_range(self) -> dict:
        for rule in self.tag_rules:
            if self._is_number() and self._is_in_range(rule):
                return rule
        return {}

    def _update_container_style(self, color) -> None:
        self._container_default_style += [
            CssOption.BackgroundColor(color + "1a"),
            CssOption.Color(color)
        ]

    def _set_format(self, tag_format: str):
        if self._is_number():
            return format(self.tag_value, tag_format)
        return self.tag_value

    def _get_content(self) -> ObjColumn:

        self._set_tag_style_values()
        rule = self._get_rule_by_range()
        font_size = self._text_default_style[0].value
        symbol = [ObjHTML(f"""<div style="font-size:{font_size}px">{symbol}</div>""")] if (
            symbol := rule.get("symbol")) else []
        self.tag_value = self._set_format(self.tag_format)
        text_obj = ObjText(
            self.tag_value,
            css_options=self._text_default_style
        )
        tag_container = ObjColumn(
            ObjRow(
                symbol + [text_obj],
            ),
            **self.container_properties
        )

        color = rule.get("color") or self.default_color
        self._update_container_style(color)

        tag_container = self._set_element_style(tag_container)
        return tag_container

    def to_json_structure(self, visitor):
        return self._get_content().to_json_structure(visitor)

    """
    The format parameters are also present on each tag rule.
    Priority: TagRule -> TagContent -> Default

    DOWN_SYMBOL and UP_SYMBOL are available as imports.

    Use example:
     ```
    Tag.of(TagContent(
                        14296,
                        text="Faltam",
                        value_format="currency:R$",
                        color=DEFAULT_DOWN_COLOR,
                        height="100%",
                    )
    ```
    """

    default_tag = TagRule(Range(inf, -inf))

    @staticmethod
    def of(tag_content: TagContent, show_border: bool = False) -> ObjRow:
        """
        The format parameters are also present on each tag rule.
        Priority: TagRule -> TagContent -> Default

        DOWN_SYMBOL and UP_SYMBOL are available as imports.

        Use example:
         ```
        Tag.of(TagContent(
                            14296,
                            text="Faltam",
                            value_format="currency:R$",
                            color=DEFAULT_DOWN_COLOR,
                            height="100%",
                        ),
                show_border = True
                )
        Example with tag rules:

        Tag.of(
                TagContent(
                    value=200,
                    value_format="currency:R$",
                    height="100%",
                    rule_by_range=[
                        TagRule(
                            Range(0, np.inf),
                            color=DEFAULT_UP_COLOR,
                            value_format="currency:R$"
                        ),
                        TagRule(
                            Range(-np.inf, 0),
                            color=DEFAULT_DOWN_COLOR,
                            text="Faltam:" + ("<br>" if with_line_break else ""),
                            value_format="currency:R$",
                        ),
                    ],
                )
            )
        ```
        """
        fitting_rule = Tag._get_fitting_rule(tag_content)
        symbol = Tag._assert_symbol_is_obj_html(fitting_rule.symbol)
        text_spacing = tag_content.text_spacing or "0.2em"
        color = fitting_rule.color or tag_content.color or DEFAULT_UP_COLOR
        text_color = fitting_rule.color or tag_content.color or DEFAULT_UP_COLOR
        text_size = fitting_rule.size or tag_content.size or 5
        value_format = fitting_rule.value_format or tag_content.value_format

        color = Colors.parse(color)
        text_color = Colors.parse(text_color)

        color = Tag._lighten(str(color))

        text = fitting_rule.text or tag_content.text or ""
        formatted_value = Tag.formatted(tag_content.value or "", value_format)

        content = [obj_texts_from(f"{text} {formatted_value}", text_size), symbol]

        height = tag_content.height or "fit-content"
        width = tag_content.width or "fit-content"

        return ObjRow(
            content,
            css_options=[
                CssOption.AlignItems("center"),
                CssOption.JustifyContent("space-around"),
                CssOption.Background(color),
                CssOption.Border(f"{int(show_border)}px solid"),
                CssOption.BorderColor(text_color),
                CssOption.Color(text_color),
                CssOption.BorderRadius("6px"),
                CssOption.Height(height),
                CssOption.Width(width),
                CssOption.Padding("0px 0.5em"),
            ],
        ).set_horizontal_child_spacing(text_spacing)

    @staticmethod
    def formatted(value: float | int | str, value_format: str | None) -> str:
        float_value = parse_float_or_none(value)
        if float_value is None:
            return str(value)
        return format(float_value, value_format)

    @staticmethod
    def _get_fitting_rule(tag_content: TagContent) -> TagRule:
        if tag_content is None:
            return Tag.default_tag

        parsed_float = parse_float_or_none(str(tag_content.value))

        if parsed_float is None:
            return Tag.default_tag

        if tag_content.rule_by_range is None:
            if parsed_float >= 0:
                return Tag.default_tag
            return Tag.default_tag

        selected_rule = tag_content.rule_by_range[0]
        for rule in tag_content.rule_by_range:
            if rule.range.is_value_within(parsed_float):
                selected_rule = rule
                break
        return selected_rule

    @staticmethod
    def _lighten(color: str) -> str:
        return color + "1a"

    @staticmethod
    def _assert_symbol_is_obj_html(symbol) -> LooqObject:
        decision_map = {
            "ObjHTML": lambda: symbol,
            "ObjText": lambda: symbol,
            "ObjIcon": lambda: symbol,
            "str": lambda: ObjText(symbol),
        }
        type_name = str(getattr(getattr(symbol, "__class__", None), "__name__", None))
        return decision_map.get(type_name, lambda: ObjText(""))()
