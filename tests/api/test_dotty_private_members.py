from dotty_dictionary import Dotty, dotty


def test_split_separator():
    dot = dotty()
    result = dot._split("chain.of.keys")
    assert result == ["chain", "of", "keys"]


def test_split_with_custom_separator():
    dot = Dotty({}, separator="#", esc_char="\\")
    result = dot._split("chain#of#keys")
    assert result == ["chain", "of", "keys"]
