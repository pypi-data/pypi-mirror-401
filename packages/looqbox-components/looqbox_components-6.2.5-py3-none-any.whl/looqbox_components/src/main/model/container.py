from typing import Collection

from looqbox import CssOption as Css
from looqbox import ObjColumn
from looqbox import ObjLine
from looqbox import ObjRow
from looqbox import ObjSwitch
from looqbox import ObjText
from looqbox import ObjTooltip
from looqbox.objects.container.positional.abstract_positional_container import AbstractPositionalContainer
from looqbox.objects.looq_object import LooqObject
from looqbox.render.abstract_render import BaseRender


class Container(AbstractPositionalContainer):
    """
    This class represents a customizable and dynamic container that can be used to group other LooqObjects or components.
    """

    def __init__(self, *children: Collection[LooqObject] | LooqObject, **properties):
        """
            Args:
                *content: The content to be added to the container.
                **properties: Optional properties for the container configuration. Supported properties are:
                    height (str, optional): Height of the container. Defaults to '50px'.
                    use_border (bool, optional): If the container should have a border. Defaults to True.
                    line (bool, optional): If the container should have a side line. Defaults to False.
                    line_thickness (str, optional): Thickness of the side line. Defaults to '5px'.
                    tooltip (str, optional): Tooltip text. Displayed if not empty. Defaults is not having it.
                    title (str): Title of the container.
                    subtitle (str): Subtitle of the container.
                    line_color (str, optional): Color of the side line. Defaults to '#40db62'.
                    tooltip_spacing (str): Margin of the tooltip against the container.
                    tooltip_size (str, optional): Size of the tooltip. Defaults to '15px'.
                    css_options (list, optional): Additional CSS options to apply to the container.
        """
        super().__init__(*children)

        self.properties = properties

        self.obj_container_args = [
            "height",
            "use_border",
            "line",
            "line_thickness",
            "tooltip",
            "title",
            "subtitle",
            "line_color",
            "title_spacing",
            "tooltip_spacing",
            "tooltip_size"
        ]
        self.abs_container_args = [
            "value",
            "render_condition",
            "tab_label",
            "obj_class"
        ]

        self._default_style = [
            Css.TextAlign("left"),
            Css.Height("100%"),
            Css.Width("100%")
        ]
        self._children_style = [
            Css.JustifyContent("flex-start"),
            Css.Padding("15px"),
            Css.TextAlign("left"),
            Css.Height("100%"),
            Css.Width("100%")
        ]
        self._container_style = [
            Css.Overflow("hidden"),
            Css.Position("relative"),
            Css.Width("100%"),
            Css.Height("100%"),
            Css.FlexWrap("nowrap")
        ]
        self._line_style = [
            Css.Margin(0),
            Css.Position("absolute"),
            Css.Height("100%"),
        ]
        self._tooltip_style = [
            Css.Position("absolute"),
            Css.Right(self.properties.get("tooltip-spacing", "5px")),
            Css.Width(self.properties.get("tooltip-size", "15px")),
            Css.Height(self.properties.get("tooltip-size", "15px"))
        ]
        self.parent_properties = self._get_parent_properties(self.properties)
        vars(self).update(self.parent_properties)

    def _get_parent_properties(self, properties):
        return {property_name: property_value for property_name, property_value in properties.items()
                if property_name not in self.obj_container_args}

    def _get_container(self) -> ObjRow:
        content = self._get_content()
        extra_properties = {
            prop: value
            for prop, value in vars(self).items()
            if prop in self.abs_container_args
        }
        return ObjRow(content, css_options=[Css.Padding("5px")], **extra_properties)

    def _get_content(self) -> ObjRow:

        _header = self._get_header()
        _is_single_container = self.is_single_switch(self.children)

        if _is_single_container and _header:
            self._insert_header_on_switch(_header)

        children_container = ObjColumn(self.children, **self._get_positional_args()).set_main_alignment_center
        children_container = self._add_default_style(children_container, self._default_style)

        _container_content = [
            ObjColumn(
               (_header if not _is_single_container and _header else []) + [children_container],
               css_options=self._children_style,
            )
        ]

        if self.properties.get("line", False):
            _container_content.insert(0,self._get_line())

        if self.properties.get("tooltip", False):
            _container_content.append(self._get_container_tooltip())

        container_row = ObjRow(
            *_container_content,
            css_options=self._container_style,
        ).set_cross_alignment_center

        if self.properties.get("use_border", True):
            container_row.add_border


        return container_row

    def _insert_header_on_switch(self, _header):
        first_container = self.children[0].children

        for idx, column in enumerate(first_container):
            updated_column = ObjColumn(*_header, column, tab_label=column.tab_label)
            first_container[idx] = updated_column

    def _get_header(self):
        _header = [
            self._get_title(),
            self._get_subtitle()
        ]
        _header = [header_text_content for header_text_content in _header if not header_text_content.empty()]
        return _header

    @staticmethod
    def is_single_switch(content):
        return len(content) == 1 and isinstance(content[0], ObjSwitch)

    @staticmethod
    def _add_default_style(container, default_style):
        for current_content in default_style:
            container.css_options = (Css.add(container.css_options, current_content))
        return container

    def _get_line(self) -> ObjLine:
        line_obj = ObjLine(
            css_options=self._line_style,
            render_condition=self.properties.get("line", False)
        ) \
            .set_thickness(self.properties.get("line_thickness", "3px")) \
            .set_size("100%") \
            .set_color(self.properties.get("line_color", "#40db62")) \
            .set_alignment_center

        return line_obj

    def _get_title(self) -> ObjText:
        return title if isinstance(title := self.properties.get("title"), ObjText) else \
            ObjText(
                title or "",
                css_options=[Css.Color("#333"), Css.FontSize("16px")],
                render_condition=self.properties.get("title")
            )

    def _get_subtitle(self) -> ObjText:
        return subtitle if isinstance(subtitle := self.properties.get("subtitle"), ObjText) else \
            ObjText(
                subtitle or "",
                css_options=[Css.Color("#b0b0b0"), Css.FontSize("14px"), Css.FontWeight("500")],
                render_condition=self.properties.get("subtitle")
            )

    def _get_positional_args(self) -> dict:
        return {
            properties: value for properties, value in self.properties.items()
            if properties not in self.obj_container_args
        }

    def _get_container_tooltip(self) -> ObjTooltip:
        container_tooltip = ObjTooltip(
            text=self.properties.get("tooltip", ""),
            render_condition=self.properties.get("tooltip"),
            css_options=self._tooltip_style
        )

        return container_tooltip

    def to_json_structure(self, visitor: BaseRender):
        content_obj = self._get_container()
        content = content_obj.to_json_structure(visitor)
        return content
