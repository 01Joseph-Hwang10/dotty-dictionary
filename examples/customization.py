"""
*************
Customization
*************

By default Dotty uses dot as keys separator and backslash as escape character.
In special occasions you may want to use different set of chars.

Customization require using Dotty class directly instead of factory function.
"""

__authors__ = ["Joseph Hwang", "Pawel Zadrozny"]
__copyright__ = "Copyright (c) 2024, Joseph Hwang. Originally written by Pawel Zadrozny"


def custom_separator():
    """
    Custom separator
    ================

    In fact any valid string can be used as separator.
    """
    from dotty_dictionary import Dotty

    dot = Dotty(
        {"deep": {"deeper": {"harder": "faster"}}}, separator="$", esc_char="\\"
    )

    assert dot["deep$deeper$harder"] == "faster"
    # end of custom_separator


def custom_escape_char():
    """
    Custom escape char
    ==================

    As separator, escape character can be any valid string
    not only single character.
    """
    from dotty_dictionary import Dotty

    dot = Dotty({"deep.deeper": {"harder": "faster"}}, separator=".", esc_char="#")

    assert dot["deep#.deeper.harder"] == "faster"
    # end of custom_escape_char
