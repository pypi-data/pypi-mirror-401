from dataclasses import dataclass, asdict, field
from typing import Optional, List, Tuple

import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

from looqbox_components import Colors


@dataclass
class Font:
    size: int = 12
    family: str = "Inter"
    color: Optional[str] = field(default_factory=lambda: Colors.parse_or_none(Colors.GRAY_500))


# noinspection SpellCheckingInspection
@dataclass
class Annotation:
    text: str
    x: float
    y: float
    xref: str = "x"
    yref: str = "y"
    xanchor: str = "center"
    yanchor: str = "middle"
    align: str = "center"
    arrowcolor: str = "#000"
    arrowhead: int = 0
    arrowside: str = "end"
    arrowsize: float = 1
    arrowwidth: int = 1
    borderwidth: int = 1
    borderpad: int = 1
    bordercolor: str = "#000"
    bgcolor: str = "#fff"
    font: Font = field(default_factory=Font)
    height: int = 30
    width: int = 100
    visible: bool = True


@dataclass
class Pad:
    t: int = 0
    r: int = 0
    b: int = 0
    l: int = 0


# noinspection SpellCheckingInspection
@dataclass
class Title:
    text: str
    font: Font = field(default_factory=Font)
    pad: Pad = field(default_factory=Pad)
    x: float = 0.5
    y: float = 0.9
    xanchor: str = "auto"
    xref: str = "x"
    yref: str = "y"


# noinspection SpellCheckingInspection
@dataclass
class Legend:
    bgcolor: str = "#fff"
    bordercolor: Optional[str] = None
    borderwidth: Optional[int] = None
    font: Font = field(default_factory=Font)
    title: Optional[Title] = None
    yanchor: str = "bottom"
    xanchor: str = "center"
    y: float = -0.15
    x: float = 0.5
    orientation: str = "h"


# noinspection SpellCheckingInspection
@dataclass
class ColorScale:
    diverging: Optional[List[Tuple[str]]] = None
    sequential: Optional[List[str]] = None
    sequentialminus: Optional[List[str]] = None


# noinspection SpellCheckingInspection
@dataclass
class Axis:
    title: Optional[str] = None
    titlefont: Font = field(default_factory=Font)
    tickfont: Font = field(default_factory=Font)
    gridwidth: int = 1
    linewidth: int = 1
    tickmode: str = "auto"
    nticks: int = 0
    tick0: int = 0
    dtick: int = 1
    ticklen: int = 5
    tickwidth: int = 1
    tickangle: int = 0
    showticklabels: bool = True
    showgrid: bool = True
    zeroline: bool = False
    showline: bool = False
    mirror: bool = False
    showspikes: bool = False
    tickprefix: Optional[str] = None
    ticksuffix: Optional[str] = None
    gridcolor: Optional[str] = field(default_factory=lambda: Colors.parse_or_none(Colors.GRAY_200))
    linecolor: Optional[str] = field(default_factory=lambda: Colors.parse_or_none(Colors.GRAY_500))
    tickcolor: Optional[str] = field(default_factory=lambda: Colors.parse_or_none(Colors.BLACK))


# noinspection SpellCheckingInspection
@dataclass
class Layout:
    title: Optional[Title] = None
    xaxis: Axis = field(default_factory=Axis)
    yaxis: Axis = field(default_factory=Axis)
    yaxis2: Axis = field(default_factory=lambda: Axis(showgrid=False))
    showlegend: bool = True
    legend: Legend = field(default_factory=Legend)
    margin: Pad = field(default_factory=lambda: Pad(10, 10, 10, 10))
    paper_bgcolor: str = "#fff"
    plot_bgcolor: str = "#fff"
    colorscale: Optional[ColorScale] = None
    colorway: Optional[List[str]] = field(default_factory=lambda:Colors.default_color_list())
    hovermode: str = "x unified"
    shapes: Optional[List[str]] = None
    barmode: str = "group"

    def round_corners(self):
        return self

    @staticmethod
    def get_shape_by_path(path: str):
        return dict(
            type='path',
            path=path,
            fillcolor='rgba(128, 0, 128, 0.7)',
            layer='above',
            line=dict(color='rgba(128, 0, 128, 0.7)', width=0.5)
        )

    def as_dict(self):
        return asdict(self)


class PlotlyFigure:
    def __init__(self, data: pd.DataFrame, layout=Layout()):
        self.layout = layout
        self.fig = make_subplots(specs=[[{"secondary_y": True}]])
        self.data = data

    def add_annotation(self, annotation: Annotation):
        self.fig.add_annotation(asdict(annotation))
        return self

    def add_bar(
        self,
        x_name: str,
        y_name: str,
        secondary_y: bool = False,
        color: Optional[Colors | str] = None,
        **extra_bar_parameters
    ):
        color = Colors.parse_or_none(color)
        self.fig.add_trace(
            go.Bar(
                name=y_name + (4 * " "),
                x=self.data[x_name],
                y=self.data[y_name],
                marker=dict(color=color),
                **extra_bar_parameters
            ),
            secondary_y=secondary_y
        )

    def add_scatter(
        self,
        x_name: str,
        y_name: str,
        secondary_y: bool = False,
        color: Optional[Colors | str] = None,
        **extra_scatter_parameters
    ):
        color = Colors.parse_or_none(color)
        self.fig.add_trace(
            go.Scatter(
                name=y_name + (4 * " "),
                x=self.data[x_name],
                y=self.data[y_name],
                line=dict(color=color),
                **extra_scatter_parameters
            ),
            secondary_y=secondary_y
        )

    def render(self):
        self.fig.update_layout(self.layout.as_dict())
        return self.fig
