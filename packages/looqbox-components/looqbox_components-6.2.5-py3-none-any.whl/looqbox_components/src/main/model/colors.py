from __future__ import annotations

from enum import Enum
from typing import Optional


class Colors(Enum):
    """
    Tip: If you are using JetBrains IDEs, download color highlighter (from atom material) plugin to see the colors in the code.
    """
    DEFAULT_POSITIVE = "#00C899"
    DEFAULT_NEGATIVE = "#D94804"
    PRIMARY_GREEN_50 = "#E6FFF5"
    PRIMARY_GREEN_100 = "#A0FAD9"
    PRIMARY_GREEN_200 = "#72EDC4"
    PRIMARY_GREEN_300 = "#48E0B3"
    PRIMARY_GREEN_400 = "#24D4A4"
    PRIMARY_GREEN_500 = "#00C899"
    PRIMARY_GREEN_600 = "#00A181"
    PRIMARY_GREEN_700 = "#007A66"
    PRIMARY_GREEN_800 = "#005449"
    PRIMARY_GREEN_900 = "#002E29"
    SECONDARY_ORANGE_50 = "#FFF3E6"
    SECONDARY_ORANGE_100 = "#FFD9B5"
    SECONDARY_ORANGE_200 = "#FFC08C"
    SECONDARY_ORANGE_300 = "#FFA463"
    SECONDARY_ORANGE_400 = "#FF863B"
    SECONDARY_ORANGE_500 = "#FF6311"
    SECONDARY_ORANGE_600 = "#D94804"
    SECONDARY_ORANGE_700 = "#833300"
    SECONDARY_ORANGE_800 = "#8C2300"
    SECONDARY_ORANGE_900 = "#661600"
    TERTIARY_PURPLE_50 = "#F9F0FF"
    TERTIARY_PURPLE_100 = "#EFDBFF"
    TERTIARY_PURPLE_200 = "#D3ADF7"
    TERTIARY_PURPLE_300 = "#B37FEB"
    TERTIARY_PURPLE_400 = "#9254DE"
    TERTIARY_PURPLE_500 = "#722ED1"
    TERTIARY_PURPLE_600 = "#531DAB"
    TERTIARY_PURPLE_700 = "#391085"
    TERTIARY_PURPLE_800 = "#22075E"
    TERTIARY_PURPLE_900 = "#120338"
    WARNING_GOLD_50 = "#FFFBE6"
    WARNING_GOLD_100 = "#FFF1B8"
    WARNING_GOLD_200 = "#FFE58F"
    WARNING_GOLD_300 = "#FFD666"
    WARNING_GOLD_400 = "#FFC53D"
    WARNING_GOLD_500 = "#FAAD14"
    WARNING_GOLD_600 = "#D48806"
    WARNING_GOLD_700 = "#AD6800"
    WARNING_GOLD_800 = "#874000"
    WARNING_GOLD_900 = "#613400"
    WHITE = "#FFFFFF"
    GRAY_50 = "#FAFAFA"
    GRAY_100 = "#F5F5F5"
    GRAY_200 = "#F0F0F0"
    GRAY_300 = "#BFBFBF"
    GRAY_400 = "#8C8C8C"
    GRAY_500 = "#595959"
    GRAY_600 = "#434343"
    GRAY_700 = "#262626"
    GRAY_800 = "#141414"
    BLACK = "#000000"
    COLOR_RED_ERROR_50 = "#FFF1F0"
    COLOR_RED_ERROR_100 = "#FFCCC7"
    COLOR_RED_ERROR_200 = "#FFA39E"
    COLOR_RED_ERROR_300 = "#FF7875"
    COLOR_RED_ERROR_400 = "#FF4D4F"
    COLOR_RED_ERROR_500 = "#F5222D"
    COLOR_RED_ERROR_600 = "#CF1322"
    COLOR_RED_ERROR_700 = "#A8071A"
    COLOR_RED_ERROR_800 = "#820014"
    COLOR_RED_ERROR_900 = "#5C0011"

    @staticmethod
    def parse(color: Optional[Colors | str]) -> str:
        if color is None:
            return ""
        return getattr(color, "value", None) or str(color)

    @staticmethod
    def parse_or_none(color: Optional[Colors | str]) -> Optional[str]:
        if color is None:
            return None
        return getattr(color, "value", None) or str(color)

    @classmethod
    def parse_list(cls, colors: list[Colors | str]) -> list[str]:
        return [cls.parse(color) for color in colors if color is not None]

    @classmethod
    def default_color_list(cls):
        return cls.parse_list([cls.GRAY_400, cls.PRIMARY_GREEN_700, cls.PRIMARY_GREEN_300, cls.PRIMARY_GREEN_500])

    @classmethod
    def sample_color_list(cls):
        return cls.parse_list([cls.PRIMARY_GREEN_600, cls.SECONDARY_ORANGE_400, cls.WARNING_GOLD_500, cls.TERTIARY_PURPLE_400, cls.GRAY_400])
