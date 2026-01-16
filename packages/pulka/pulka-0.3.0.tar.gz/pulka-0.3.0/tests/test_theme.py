from pulka.theme import ThemeConfig


def test_prompt_toolkit_style_uses_hex_white_for_headers() -> None:
    config = ThemeConfig(primary="#f06595", secondary="#63e6be")

    style = config.prompt_toolkit_style()
    attrs = style.get_attrs_for_style_str("class:table.header")
    assert attrs.color == "ffffff"
