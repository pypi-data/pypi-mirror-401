from typing import Dict
from instaui.internal.ui.element import Element
from instaui.internal.ui.event import EventMixin
from instaui.internal.ui.bindable import is_bindable


def handle_props(props: Dict, *, model_value=None):
    props = {
        k.replace("_", "-"): v
        for k, v in props.items()
        if not isinstance(v, EventMixin)
    }
    if model_value is not None:
        props["modelValue"] = model_value
    return props


def handle_event_from_props(element: Element, props: Dict):
    for k, v in props.items():
        if isinstance(v, EventMixin):
            # 'on_click' -> 'click'
            element.on(k.replace("on_", ""), v)


def try_setup_vmodel(
    element: Element,
    value,
    *,
    prop_name: str = "value",
):
    if value is None:
        return
    if is_bindable(value):
        element.vmodel(value, prop_name=prop_name)
        return

    element.props({prop_name: value})
