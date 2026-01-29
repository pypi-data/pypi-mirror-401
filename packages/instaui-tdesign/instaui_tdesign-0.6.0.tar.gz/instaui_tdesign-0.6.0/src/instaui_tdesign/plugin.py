import contextvars
from instaui import custom
from instaui_tdesign import resources, symbol

_registered = contextvars.ContextVar("_registered", default=False)


def register_tdesign_once():
    if not _registered.get():
        _register_tdesign()
        _registered.set(True)

        custom.on_page_exit(lambda: _registered.set(False))


def _register_tdesign():
    theme = custom.CssAsset(
        resources.THEME_CSS_DIR / "theme-default.css",
        namespace=symbol.THEME_CSS_SYMBOL,
        role=custom.CssRole.THEME,
    )

    tdesign_css = custom.CssAsset(
        resources.tdesign_css,
        role=custom.CssRole.BASE,
    )

    instaui_tdesign_css = custom.CssAsset(
        resources.instaui_tdesign_css,
        role=custom.CssRole.BASE,
    )

    custom.register_plugin(
        "InstauiTDesign",
        esm=resources.instaui_tdesign_esm_js,
        externals={
            "tdesign-vue-next": resources.tdesign_esm_js,
        },
        css=[tdesign_css, instaui_tdesign_css, theme],
    )
