from looqbox.objects.looq_object import LooqObject
from looqbox.objects.visual.looq_table import ObjTable
from looqbox.render.abstract_render import BaseRender
from multimethod import overload
from pandas import DataFrame


class TopList(LooqObject):
    """
    Create and render a TopList template.
    """

    @overload
    def __init__(self, data: DataFrame, thickness: int = 1, line_color: str = "#D5DFE9", alignment: str = "center"):
        """
        Args:
            data (pd.DataFrame | lq.ObjTable): A pandas DataFrame or a looqbox ObjTable to be displayed in the list.
            thickness (int, optional): Thickness of the line between rows. Defaults to 1.
            line_color (str, optional): Color of the line between rows. Defaults to "#D5DFE9".
            alignment (str, optional): Text-alignment of the list. Defaults to "center". Can be "left", "right" or "center".
        
        Returns:
            lq.ObjTable: A looqbox table object.
        
        Examples:
            >>> df = pd.DataFrame({'item': ["item1", "item2", "item3", "item4", "item5"],
            >>>     'value_min': [1000, 2000, 3000, 4000, 5000],
            >>>     'value_max': [10000, 20000, 30000, 40000, 50000],
            >>>     'value_avg': [5000, 10000, 15000, 20000, 25000]})
            >>>
            >>> TopList(df, alignment="start", thickness=2, line_color="red")
        """
        super().__init__()
        self.list_content = ObjTable(data)
        self.alignment = alignment
        self.thickness = thickness
        self.line_color = line_color

    @overload
    def __init__(self, data: ObjTable, thickness: int = 1, line_color: str = "#D5DFE9", alignment: str = "center"):
        """
        Args:
            data (pd.DataFrame | lq.ObjTable): A pandas DataFrame or a looqbox ObjTable to be displayed in the list.
            thickness (int, optional): Thickness of the line between rows. Defaults to 1.
            line_color (str, optional): Color of the line between rows. Defaults to "#D5DFE9".
            alignment (str, optional): Text-alignment of the list. Defaults to "center". Can be "left", "right" or "center".
        
        Returns:
            lq.ObjTable: A looqbox table object.
        
        Examples:
            >>> df = pd.DataFrame({'item': ["item1", "item2", "item3", "item4", "item5"],
            >>>     'value_min': [1000, 2000, 3000, 4000, 5000],
            >>>     'value_max': [10000, 20000, 30000, 40000, 50000],
            >>>     'value_avg': [5000, 10000, 15000, 20000, 25000]})
            >>>
            >>> TopList(df, alignment="start", thickness=2, line_color="red")
        """
        super().__init__()
        self.list_content = data
        self.alignment = alignment
        self.thickness = thickness
        self.line_color = line_color

    def _set_list_style(self) -> None:

        for row in range(self.list_content.data.shape[0]):
            self.list_content.row_style[row] = {"background": "white",
                                                "border-bottom": f"{self.thickness}px solid {self.line_color}"}

        self.list_content.show_head = False
        self.list_content.show_option_bar = False
        self.list_content.show_footer = False
        self.list_content.col_style = dict(
            zip(self.list_content.data.columns,
                [{'text-align': self.alignment}] * len(self.list_content.data.columns)))

    def _data_frame_is_empty(self) -> bool:
        return self.list_content.data is None or self.list_content.data.empty

    def to_json_structure(self, visitor: BaseRender):

        if self._data_frame_is_empty():
            raise ValueError("Dataframe is empty")

        self._set_list_style()
        return self.list_content.to_json_structure(visitor)
