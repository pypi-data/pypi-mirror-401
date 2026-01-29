from typing import Dict, Union, cast
from instaui import ui
from instaui_tdesign.types import TLocale, TCustomizeLocale
from instaui_tdesign.components.config_provider import ConfigProvider
from instaui_tdesign.locales import get_locale


def configure(*, locale: Union[TLocale, TCustomizeLocale]):
    if isinstance(locale, str):
        locale = get_locale(locale)

    @ui.layout
    def add_config_provider_lifespan():
        with ConfigProvider(global_config=cast(Dict, locale)):
            yield
