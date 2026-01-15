from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

import numpy as np

from looqbox import ObjColumn, ObjRow, ObjText
from looqbox.objects.component_utility.css_option import CssOption
from looqbox.objects.looq_object import LooqObject
from looqbox.utils.utils import format
from looqbox_commons import KeyCreator, DataHolder
from looqbox_commons.src.main.utils.collection_utils import let_or_default
from looqbox_components import Colors


class BarType(Enum):
    INLINE = "INLINE"
    MULTILINE = "MULTILINE"
    AUTO = "AUTO"


class Lines(Enum):
    COMPOSITE = "COMPOSITE"
    ONE = "ONE"
    ONE_FULL = "ONE-FULL"


@dataclass
class Segment:
    value: float
    text: str = ""
    color: Optional[Colors | str] = None
    percent_format: str = "percent:0"
    thickness: str = "1.4em"
    border_radius: str = "2em"
    colored_text: bool = False


@KeyCreator.delegate
class Keys:
    """
    Yes, I'm going to perform a mini flow here.
    I'm going to use `get_or_raise` a lot here, because we are the ones doing the offerings and they must exist.
    """
    IDX: int
    SEGMENT: Segment
    SEGMENTS: List[Segment]
    CONTAINER: List[LooqObject]
    FORMATTED_PERCENT: str
    MAXED_FORMATTED_PERCENT: str


class ProgressBar:
    """
    ProgressBar renders itself as an ObjRow
    We are using the static factory method to avoid overrides.
    As a bonus we don't need to extend LooqObject nor implement visitor methods.

    Use examples:

    Run this to check it out!

    ```
     view = lq.ObjColumn(
        lq.ObjText("Multiple elements - Multiline").set_as_title(3),
        lq.ObjLine().set_orientation_horizontal,
        ProgressBar.of([
            Segment(0.4, "Tomate", "tomato"),
            Segment(0.4, "Apples", "red"),
            Segment(0.2, "Banana Prata", "#9f9f00"),
        ]),

        lq.ObjText("One element not full - Inline").set_as_title(3),
        lq.ObjLine().set_orientation_horizontal,
        ProgressBar.of([Segment(0.7, "Tomate", "tomato")], BarType.INLINE),

        lq.ObjText("One element not full - Multiline").set_as_title(3),
        lq.ObjLine().set_orientation_horizontal,
        ProgressBar.of([Segment(0.7, "Tomate", "tomato")], BarType.MULTILINE),

        lq.ObjText("One element full - Inline").set_as_title(3),
        lq.ObjLine().set_orientation_horizontal,
        ProgressBar.of([Segment(1, "Tomate", "tomato")], BarType.INLINE),

        css_options=[
            CssOption.Width("60vw"),
            CssOption.Height("600px")
        ]
    )
    ```
    """

    @staticmethod
    def of(segments: List[Segment], bar_type: Optional[BarType] = None) -> ObjRow:
        """
        ProgressBar renders itself as an ObjRow
        We are using the static factory method to avoid overrides.
        As a bonus we don't need to extend LooqObject nor implement visitor methods.

        Use examples:

        Run this to check it out!
        ```
         view = lq.ObjColumn(
            lq.ObjText("Multiple elements - Multiline").set_as_title(3),
            lq.ObjLine().set_orientation_horizontal,
            ProgressBar.of([
                Segment(0.4, "Tomate", "tomato"),
                Segment(0.4, "Apples", "red"),
                Segment(0.2, "Banana Prata", "#9f9f00"),
            ]),

            lq.ObjText("One element not full - Inline").set_as_title(3),
            lq.ObjLine().set_orientation_horizontal,
            ProgressBar.of([Segment(0.7, "Tomate", "tomato")], BarType.INLINE),

            lq.ObjText("One element not full - Multiline").set_as_title(3),
            lq.ObjLine().set_orientation_horizontal,
            ProgressBar.of([Segment(0.7, "Tomate", "tomato")], BarType.MULTILINE),

            lq.ObjText("One element full - Inline").set_as_title(3),
            lq.ObjLine().set_orientation_horizontal,
            ProgressBar.of([Segment(1, "Tomate", "tomato")], BarType.INLINE),

            css_options=[
                CssOption.Width("60vw"),
                CssOption.Height("600px")
            ]
        )
        ```
        """
        if not segments:
            raise IndexError("Could not instantiate a progress bar because segment list was empty.")

        """
        Yes, I could simplify this a lot, basically we have 2 options till now.
        I chose to leave it this way so we can decouple the behaviours in case we want to modify them in the future.
        """
        flow_map = {
            # bar contains more than one element - INLINE
            "composite-inline": [
                ProgressBar.__assert_percentual_is_greater_than_zero,
                ProgressBar._update_border_radius_by_index,
                ProgressBar._draw_inline_segment,
            ],
            # bar contains more than one element - MULTILINE
            "composite-multiline": [
                ProgressBar.__assert_percentual_is_greater_than_zero,
                ProgressBar._update_border_radius_by_index,
                ProgressBar._draw_multiline_segment,
            ],
            # bar contains only one element and it is not full - INLINE
            "one-inline": [
                ProgressBar.__assert_percentual_is_greater_than_zero,
                ProgressBar._update_border_radius_by_index,
                ProgressBar._draw_inline_segment,
            ],
            # bar contains only one element and it is not full - MULTILINE
            "one-multiline": [
                ProgressBar.__assert_percentual_is_greater_than_zero,
                ProgressBar._update_border_radius_by_index,
                ProgressBar._draw_multiline_segment,
            ],
            # bar contains only one element and it is full - MULTILINE
            "one-full-multiline": [
                ProgressBar.__assert_percentual_is_greater_than_zero,
                ProgressBar._update_border_radius_by_index,
                ProgressBar._draw_multiline_segment,

            ],
            # bar contains only one element and it is full - INLINE
            "one-full-inline": [
                ProgressBar.__assert_percentual_is_greater_than_zero,
                ProgressBar._update_border_radius_by_index,
                ProgressBar._draw_inline_segment,
            ]
        }

        message = DataHolder()
        message[Keys.SEGMENTS] = segments

        flow_type = ProgressBar._get_flow_type(bar_type, message)
        flow = flow_map[flow_type]

        # we first check if there are any segments before
        if len(segments) == 1 and \
            ProgressBar.zero_if_none_or_nan(segments[0].value) < 1:
            message = ProgressBar._fill_till_100_pct(message)

        for idx, segment in enumerate(message.get_or_raise(Keys.SEGMENTS)):
            segment.value = ProgressBar.zero_if_none_or_nan(segment.value)
            message[Keys.IDX] = idx
            message[Keys.SEGMENT] = segment
            message[Keys.FORMATTED_PERCENT] = format(segment.value, segment.percent_format)
            message[Keys.MAXED_FORMATTED_PERCENT] = format(min(segment.value, 1), segment.percent_format)

            for executor in flow:
                message = executor(message)

        rows = message.get_or_raise(Keys.CONTAINER)

        return ObjRow(
            rows,
            css_options=[
                CssOption.MinHeight("fit-content"),
                CssOption.Width("100%"),
                CssOption.FlexWrap("nowrap"),
            ]
        )

    @staticmethod
    def _fill_till_100_pct(message: DataHolder) -> DataHolder:
        segments = message.get_or_raise(Keys.SEGMENTS)
        first_segment = segments[0]
        first_segment.value = ProgressBar.zero_if_none_or_nan(first_segment.value)
        completion = Segment(round(1 - first_segment.value, 2), "--no-text", "#8C8C8C")
        if completion.value == 1:
            completion.text = "--empty"
            message[Keys.SEGMENTS] = [completion]
            return message
        message[Keys.SEGMENTS] = [first_segment, completion]
        return message

    @staticmethod
    def zero_if_none_or_nan(value):
        if value is None or np.isnan(value):
            value = 0
        return value

    @staticmethod
    def _draw_multiline_segment(message: DataHolder) -> DataHolder:
        segment = message.get_or_raise(Keys.SEGMENT)
        maxed_formatted_percentual = message.get_or_raise(Keys.MAXED_FORMATTED_PERCENT)

        drawing = ObjRow(
            ObjText(""),  # Avoiding empty contents
            css_options=[
                CssOption.BackgroundColor(Colors.parse(segment.color)),
                CssOption.Height(segment.thickness),
                CssOption.BorderRadius(segment.border_radius),
            ]
        )

        subtitles = ProgressBar.__get_progress_bar_subtitles(message)

        progress_bar = ObjColumn(
            drawing,
            subtitles,
            css_options=[
                CssOption.Width(maxed_formatted_percentual),
                CssOption.Height("fit-content"),
            ]
        )
        message.append_to_list(Keys.CONTAINER, progress_bar)
        return message

    @staticmethod
    def _draw_inline_segment(message: DataHolder) -> DataHolder:
        segment = message.get_or_raise(Keys.SEGMENT)
        formatted_percentual_text = message.get_or_raise(Keys.FORMATTED_PERCENT)
        maxed_formatted_percent = message.get_or_raise(Keys.MAXED_FORMATTED_PERCENT)

        text = segment.text or ""
        remove_text = False
        if text == "--empty":
            text = ""
            formatted_percentual_text = "0%"
            maxed_formatted_percent = "100%"
        if text == "--no-text":
            remove_text = True

        progress_bar = ObjRow(
            ObjText(str((not remove_text and text) or ""), css_options=[CssOption.ZIndex("1")]),
            ObjText(str((not remove_text and formatted_percentual_text) or "")),  # Avoiding empty contents
            css_options=[
                CssOption.Width(maxed_formatted_percent),
                CssOption.Height(segment.thickness),
                CssOption.BackgroundColor(Colors.parse(segment.color)),
                CssOption.BorderRadius(segment.border_radius),
                CssOption.Color("white"),
                CssOption.JustifyContent("space-between"),
                CssOption.AlignItems("center"),
                CssOption.Padding("0 0.5em"),
                CssOption.FlexWrap("nowrap"),
            ]
        )
        message.append_to_list(Keys.CONTAINER, progress_bar)
        return message

    @staticmethod
    def __get_progress_bar_subtitles(message: DataHolder) -> ObjColumn:
        segment = message.get_or_raise(Keys.SEGMENT)
        formatted_percentual_text = message.get_or_raise(Keys.FORMATTED_PERCENT)

        text_color = let_or_default(segment.colored_text, lambda: [CssOption.Color(Colors.parse(segment.color))], [])
        return ObjColumn(
            ObjText(segment.text).set_as_title(5),
            ObjText(formatted_percentual_text).set_as_title(4),
            css_options=[CssOption.TextAlign("left"), CssOption.Padding("0.2em")] + text_color
        )

    @staticmethod
    def _get_flow_type(bar_type: Optional[BarType], message: DataHolder) -> str:
        segments = message.get_or_raise(Keys.SEGMENTS)
        is_single = len(segments) == 1
        is_full = is_single and segments[0].value == 1
        bar_type = bar_type or BarType.MULTILINE
        lines_type = Lines.COMPOSITE
        if is_single:
            lines_type = Lines.ONE
        if is_full:
            lines_type = Lines.ONE_FULL
        return f"{lines_type.value.lower()}-{bar_type.value.lower()}"

    @staticmethod
    def _update_border_radius_by_index(message: DataHolder):
        segments = message.get_or_raise(Keys.SEGMENTS)
        segment = message.get_or_raise(Keys.SEGMENT)

        if not segment:
            raise StopIteration("There was an error generating the progress bar: Segment cannot be empty.")
        idx = message.get_or_raise(Keys.IDX)
        one_element = len(segments) == 1

        if not one_element and idx == 0:
            segment.border_radius = f"{segment.border_radius} 0 0 {segment.border_radius}"
        elif not one_element and idx == len(segments) - 1:
            segment.border_radius = f"0 {segment.border_radius} {segment.border_radius} 0"
        elif not one_element:
            segment.border_radius = "0"

        message[Keys.SEGMENT] = segment
        return message

    @staticmethod
    def __assert_percentual_is_greater_than_zero(message: DataHolder) -> DataHolder:
        segments = message.get_or_raise(Keys.SEGMENTS)
        total_percent_text = sum(map(lambda it: it.value, segments))
        if total_percent_text <= 0:
            raise ValueError(f"The sum of all the percent texts needs to be greater than zero and was {total_percent_text}.")
        return message
