
from looqbox import CssOption, ObjColumn, ObjIcon, ObjRow, ObjText

from typing import Optional
from looqbox_components.src.main.model.tag import Tag, TagContent


class Card:
    """
    This creates a card with the following structure:
    ```
    +------------------------------------+
    + |##| Meta Loja           Yoy: 10%  +
    + |##| R$ 4250,00                    +
    +------------------------------------+
    ```

    With |##| representing an Icon space

    When creating your Icon, priorize doing it by using Icon.of(IconName.YOUR_ICON_NAME)

    If you want a more complex Icon, consider copying this base implementation:
    ```
    ```

    Use examples:
    ```py
    Card.of(title="Total de Produtos", value="97", icon=Icon.of(IconName.PAYMENT)),
    Card.of(title="Total de Venda Perdida", value=lq.format(464819.01, "currency:R$"), icon=Icon.of(IconName.PAYMENT)),
    ```
    """

    @staticmethod
    def of(
        title: str,
        value: str,
        icon: Optional[ObjIcon] = None,
        tag: Optional[TagContent] = None,
        width: Optional[str] = None,
        height: Optional[str] = None,
    ):
        """
        This creates a card with the following structure:
        ```
        +------------------------------------+
        + |##| Meta Loja           Yoy: 10%  +
        + |##| R$ 4250,00                    +
        +------------------------------------+
        ```

        With |##| representing an Icon space

        When creating your Icon, priorize doing it by using Icon.of(IconName.YOUR_ICON_NAME)

        Use examples:
        ```py
        Card.of(title="Total de Produtos", value="97", icon=Icon.of(IconName.PAYMENT)),
        Card.of(title="Total de Venda Perdida", value=lq.format(464819.01, "currency:R$"), icon=Icon.of(IconName.PAYMENT)),
        ```

        If you want a more complex Icon, consider copying this base implementation:
        ```
         ObjColumn(
            ObjRow(
                icon or HorizontalSpace(size=0),
                ObjColumn(
                    ObjText(title).set_as_title(5),
                    ObjText(value).set_as_title(3),
                    css_options=[CssOption.JustifyContent("space-around")]
                ),
                (tag and Tag.of(tag)) or HorizontalSpace(size=0),
            ).set_horizontal_child_spacing("1em"),
            css_options=[
                CssOption.TextAlign("left"),
                CssOption.Padding("1em"),
            ]
        ).add_border
        ```
        """
        return ObjColumn(
            ObjRow(
                icon or ObjText(""),
                ObjColumn(
                    ObjText(title).set_as_title(5),
                    ObjText(value).set_as_title(3),
                    css_options=[CssOption.JustifyContent("space-around")],
                ),
                (tag and Tag.of(tag)) or ObjText(""),
                css_options=[
                    CssOption.AlignItems("center"),
                    CssOption.FlexWrap("nowrap")
                ],
            ).set_horizontal_child_spacing("1em"),
            css_options=[
                CssOption.TextAlign("left"),
                CssOption.Padding("1em"),
                CssOption.Height(height or "fit-content"),
                CssOption.Width(width or "fit-content"),
                CssOption.FlexWrap("nowrap"),
            ],
        ).add_border
