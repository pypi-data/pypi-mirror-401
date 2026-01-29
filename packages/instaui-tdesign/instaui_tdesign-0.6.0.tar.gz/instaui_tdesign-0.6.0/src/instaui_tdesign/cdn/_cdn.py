from pathlib import Path
from typing import Optional
from instaui.cdn.options import CdnResourceOption
from instaui_tdesign import resources


def override(
    *,
    tdesign_vue_next_js: Optional[str] = None,
    tdesign_vue_next_css: Optional[str] = None,
) -> CdnResourceOption:
    if not tdesign_vue_next_js and not tdesign_vue_next_css:
        return default_override()

    import_maps = {}
    if tdesign_vue_next_js:
        import_maps["tdesign-vue-next"] = tdesign_vue_next_js

    css_links: dict[Path, str] = {}
    if tdesign_vue_next_css:
        css_links[resources.tdesign_css] = tdesign_vue_next_css

    return CdnResourceOption(import_maps=import_maps, css_links=css_links)


def default_override() -> CdnResourceOption:
    return override(
        tdesign_vue_next_js=resources.TDESIGN_VUE_ESM_JS_CDN,
        tdesign_vue_next_css=resources.TDESIGN_VUE_CSS_CDN,
    )
