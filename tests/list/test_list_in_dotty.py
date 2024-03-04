import pytest
from dotty_dictionary import dotty


@pytest.fixture
def dot():
    return dotty(
        {
            "field1": "Value of F1",
            "field2": "Value of F2",
            "field3": [
                {
                    "subfield1": "Value of subfield1 (item 0)",
                    "subfield2": "Value of subfield2 (item 0)",
                },
                {
                    "subfield1": "Value of subfield1 (item 1)",
                    "subfield2": "Value of subfield2 (item 1)",
                },
            ],
            "field4": "Not wanted",
            "field5": [
                {"subfield1": [{"subsubfield": "Value of sub subfield (item 0)"}]}
            ],
            "field6": ["a", "b"],
        }
    )


def test_root_level_list_element(dot):
    assert dot["field6.0"] == "a"


def test_access_subfield1_of_field3(dot):
    assert dot["field3.0.subfield1"] == "Value of subfield1 (item 0)"
    assert dot["field3.1.subfield1"] == "Value of subfield1 (item 1)"


def test_access_sub_sub_field(dot):
    assert dot["field5.0.subfield1.0.subsubfield"] == "Value of sub subfield (item 0)"


def test_access_multidimensional_lists():
    dot = dotty(
        {
            "field": [
                [{"subfield": "Value of subfield (item 0,0)"}],
                [{"subfield": "Value of subfield (item 0,1)"}],
            ]
        }
    )
    assert dot["field.1.0.subfield"] == "Value of subfield (item 0,1)"


def test_dotty_contains_subfield_of_field(dot):
    assert "field3.0.subfield2" in dot


def test_dotty_not_contains_out_of_range_subfield(dot):
    assert "field3.3.subfield1" not in dot


def test_assert_key_error_if_index_is_not_integer(dot):
    with pytest.raises(KeyError):
        val = dot["field3.subfield1"]  # noqa


def test_assert_index_error_if_index_is_out_of_range(dot):
    with pytest.raises(IndexError):
        val = dot["field3.4.subfield1"]  # noqa


def test_assert_get_returns_default_if_index_is_out_of_range(dot):
    val = dot.get("field3.4.subfield1")
    assert val is None


def test_set_subfield_in_list():
    dot = dotty()

    dot["field.0.subfield"] = "Value of subfield (item 0)"
    dot["field.1.subfield"] = "Value of subfield (item 1)"
    dot["field.1.subfield2"] = "Value of subfield2 (item 1)"

    assert dot.to_dict() == {
        "field": [
            {"subfield": "Value of subfield (item 0)"},
            {
                "subfield": "Value of subfield (item 1)",
                "subfield2": "Value of subfield2 (item 1)",
            },
        ],
    }


def test_update_subfield_in_list():
    dot = dotty(
        {
            "field": [
                {"subfield": "Value of subfield (item 0)"},
                {
                    "subfield": "Value of subfield (item 1)",
                    "subfield2": "Value of subfield2 (item 1)",
                },
            ],
        }
    )

    dot["field.0.subfield"] = "updated value"

    assert dot.to_dict() == {
        "field": [
            {"subfield": "updated value"},
            {
                "subfield": "Value of subfield (item 1)",
                "subfield2": "Value of subfield2 (item 1)",
            },
        ],
    }


def test_delete_subfield():
    dot = dotty(
        {
            "field": [
                {
                    "subfield1": "Value of subfield1 (item 0)",
                    "subfield2": "Value of subfield2 (item 0)",
                },
            ]
        }
    )

    del dot["field.0.subfield2"]

    assert dot.to_dict() == {
        "field": [
            {"subfield1": "Value of subfield1 (item 0)"},
        ]
    }


def test_list_as_return_value():
    dot = dotty({"field": ["list_field0", "list_field1"]})

    assert dot["field.0"] == "list_field0"
    assert dot["field.1"] == "list_field1"
    assert "field.0" in dot
    assert "field.1" in dot
    assert "field.2" not in dot


def test_root_level_field_is_none():
    dot = dotty(
        {
            "field": None,
        }
    )

    assert dot["field.0"] is None
