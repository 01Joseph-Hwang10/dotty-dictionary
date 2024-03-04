#!/usr/bin/env python
# -*- coding: utf-8 -*-

__authors__ = ["Joseph Hwang", "Pawel Zadrozny"]
__copyright__ = "Copyright (c) 2024, Joseph Hwang. Originally written by Pawel Zadrozny"


def custom_separator():
    from dotty_dictionary import Dotty

    dot = Dotty(
        {"deep": {"deeper": {"harder": "faster"}}}, separator="$", esc_char="\\"
    )

    assert dot["deep$deeper$harder"] == "faster"
    # end of custom_separator


def custom_escape_char():
    from dotty_dictionary import Dotty

    dot = Dotty({"deep.deeper": {"harder": "faster"}}, separator=".", esc_char="#")

    assert dot["deep#.deeper.harder"] == "faster"
    # end of custom_escape_char
