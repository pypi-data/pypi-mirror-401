from __future__ import annotations
from typing import Literal, Optional, Sequence, Union

from instaui_tdesign.components._icon_param_utils import make_prefix_icon
from ._base_element import BaseElement
from instaui.internal.ui.event import EventMixin
from typing_extensions import TypedDict, Unpack, Required
from ._utils import handle_props, handle_event_from_props


class Dropdown(BaseElement):
    def __init__(
        self,
        options: Optional[Sequence[Union[DropdownOptionItem, dict]]] = None,
        **kwargs: Unpack[TDropdownProps],
    ):
        """
        Represents a dropdown component that can display a list of selectable options.

        The Dropdown can be configured either by passing a list of option dictionaries
        or by nesting `dropdown_menu` and `dropdown_item` elements within its context.
        It supports various styling, positioning, and interaction behaviors through
        props defined in `TDropdownProps`.

        Args:
            options (Optional[Sequence[Union[DropdownOptionItem, dict]]]): A list of dropdown items.
                Each item must include at least a `content` (str) and a `value` (int).
                Additional optional keys include `active`, `disabled`, `divider`, `theme`,
                and `childred` (note: likely typo for "children").
            prefix_icon (str): Icon to display before the dropdown trigger element.
            direction (Literal["left", "right"]): Direction in which submenus expand.
            disabled (bool): If True, disables the dropdown trigger.
            hide_after_item_click (bool): If True, closes the dropdown panel after an item is clicked.
            max_column_width (Union[float, str]): Maximum width of the dropdown panel column.
            max_height (float): Maximum height of the dropdown panel.
            min_column_width (Union[float, str]): Minimum width of the dropdown panel column.
            panel_bottom_content (str): Content rendered at the bottom of the dropdown panel.
            panel_top_content (str): Content rendered at the top of the dropdown panel.
            placement (Literal["top", "left", "right", "bottom", ...]): Positioning strategy for the dropdown panel relative to the trigger.
            popup_props (dict): Additional props passed to the underlying popup component.
            trigger (Literal["hover", "click", "focus", "context-menu"]): Event that triggers the dropdown visibility.
            on_click (EventMixin): Event handler triggered when a dropdown item is clicked.
                Receives an event object containing at least `content` and `value`.

        Example:
        .. code-block:: python
            selected = ui.state("")
            options = [
                {"content": "foo", "value": 1},
                {"content": "bar", "value": 2},
            ]

            @ui.event(inputs=[ui.event_context.e()], outputs=[selected])
            def on_click(e):
                return e["content"]

            with td.dropdown(options, on_click=on_click):
                ui.text("Dropdown")

            ui.text("selected:" + selected)
        """
        super().__init__("t-dropdown")
        prefix_icon = kwargs.pop("prefix_icon", None)
        self.props({"options": options})
        make_prefix_icon(self, prefix_icon)
        self.props(handle_props(kwargs))  # type: ignore
        handle_event_from_props(self, kwargs)  # type: ignore

    def on_click(
        self,
        handler: EventMixin,
        *,
        extends: Optional[list] = None,
    ):
        self.on(
            "click",
            handler,
            extends=extends,
        )
        return self


class DropdownMenu(BaseElement):
    def __init__(self):
        super().__init__("t-dropdown-menu")


class DropdownItem(BaseElement):
    def __init__(
        self,
        content: Optional[str] = None,
        **kwargs: Unpack[TDropdownItemProps],
    ):
        super().__init__("t-dropdown-item")
        prefix_icon = kwargs.pop("prefix_icon", None)

        self.props({"content": content})
        make_prefix_icon(self, prefix_icon)
        self.props(handle_props(kwargs))  # type: ignore
        handle_event_from_props(self, kwargs)  # type: ignore

    def on_click(
        self,
        handler: EventMixin,
        *,
        extends: Optional[list] = None,
    ):
        self.on(
            "click",
            handler,
            extends=extends,
        )
        return self


class DropdownOptionItem(TypedDict, total=False):
    active: bool
    content: Required[str]
    disabled: bool
    divider: bool
    theme: Literal["default", "success", "warning", "error"]
    value: Required[int]
    childred: Optional[list[DropdownOptionItem]]


class TDropdownProps(TypedDict, total=False):
    prefix_icon: str
    direction: Literal["left", "right"]
    disabled: bool
    hide_after_item_click: bool
    max_column_width: Union[float, str]
    max_height: float
    min_column_width: Union[float, str]
    panel_bottom_content: str
    panel_top_content: str
    placement: Literal[
        "top",
        "left",
        "right",
        "bottom",
        "top-left",
        "top-right",
        "bottom-left",
        "bottom-right",
        "left-top",
        "left-bottom",
        "right-top",
        "right-bottom",
    ]
    popup_props: dict
    trigger: Literal["hover", "click", "focus", "context-menu"]
    on_click: EventMixin


class TDropdownItemProps(TypedDict, total=False):
    prefix_icon: str
    active: bool
    disabled: bool
    divider: bool
    theme: Literal["default", "success", "warning", "error"]
    value: int
    on_click: EventMixin
