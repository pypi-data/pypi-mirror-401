from instaui import custom
from instaui_tdesign.plugin import register_tdesign_once


class BaseElement(custom.element):
    def __init__(self, tag: str):
        super().__init__(tag)
        register_tdesign_once()
