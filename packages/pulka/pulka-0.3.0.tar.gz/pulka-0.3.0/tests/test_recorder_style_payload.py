from pulka import theme
from pulka.render.style_resolver import (
    StyleComponents,
    get_active_style_resolver,
    reset_style_resolver_cache,
)
from pulka.theme import ThemeConfig


def test_render_line_styles_payload_roundtrip() -> None:
    original_theme = theme.THEME

    config = ThemeConfig(primary="#f06595", secondary="#63e6be")

    try:
        theme.set_theme(config)
        reset_style_resolver_cache()
        resolver = get_active_style_resolver()

        classes = ("table", "table.header")
        components = resolver.resolve(classes)
        payload = {
            "component": "table_control",
            "theme_epoch": theme.theme_epoch(),
            "lines": [
                {
                    "line_index": 0,
                    "plain_text": " header ",
                    "segments": [
                        {
                            "text": "header",
                            "classes": list(classes),
                            "foreground": components.foreground,
                            "background": components.background,
                            "extras": list(components.extras),
                        }
                    ],
                }
            ],
        }

        first_segment = payload["lines"][0]["segments"][0]
        round_trip = StyleComponents(
            foreground=first_segment["foreground"],
            background=first_segment["background"],
            extras=tuple(first_segment["extras"]),
        )
        style_str = round_trip.to_prompt_toolkit()
        assert "fg:#ffffff" in style_str

        style = theme.THEME.prompt_toolkit_style()
        attrs = style.get_attrs_for_style_str(style_str)
        assert attrs.color == "ffffff"
    finally:
        theme.set_theme(original_theme)
        reset_style_resolver_cache()
