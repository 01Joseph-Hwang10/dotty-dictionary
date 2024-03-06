import pytest
from collections.abc import MutableMapping
from dataclasses import dataclass
from dotty_dictionary import Dotty, DottyEncoder


@dataclass
class User(MutableMapping):
    name: str
    age: int

    def __getitem__(self, key):
        if key not in self.__dict__:
            raise KeyError(key)
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __delitem__(self, key):
        if key not in self.__dict__:
            raise KeyError(key)
        delattr(self, key)

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __repr__(self):
        return f"User(name={self.name}, age={self.age})"

    def __str__(self):
        return f"User(name={self.name}, age={self.age})"

    def __eq__(self, other):
        return isinstance(other, User) and self.__dict__ == other.__dict__


class CustomJSONEncoder(DottyEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            return {"name": obj.name, "age": obj.age}
        return super().default(obj)


@pytest.fixture
def dot():
    return Dotty(
        {
            "a": {
                "b": {
                    "c": 1,
                    "d": 2,
                },
                "e": (3, {"f": 4}, (5, 6, 7)),
            },
            "g": 8,
            "h": User(name="John", age=25),
        },
        mapping_types=(dict, User),
        sequence_types=(list, tuple),
        json_encoder=CustomJSONEncoder,
    )


@pytest.fixture
def dot_serialized():
    return {
        "a": {
            "b": {
                "c": 1,
                "d": 2,
            },
            "e": [3, {"f": 4}, [5, 6, 7]],
        },
        "g": 8,
        "h": {"name": "John", "age": 25},
    }


def test_dotty_get_custom_types(dot: Dotty):
    # Access to dict keys
    assert dot.get("a.b.c") == 1

    # Access to tuple keys
    assert dot.get("a.e.0") == 3
    assert dot.get("a.e.1.f") == 4
    assert dot.get("a.e.2.0") == 5

    # Access to keys of custom types
    assert dot.get("h.name") == "John"


def test_dotty_set_custom_types(dot: Dotty):
    # Set dict keys
    dot["a.b.c"] = 10
    assert dot.get("a.b.c") == 10

    # Set tuple keys: fails as tuples are immutable
    with pytest.raises(TypeError):
        dot["a.e.0"] = 30
        assert dot.get("a.e.0") == 30

    # Set keys of custom types
    dot["h.name"] = "Jane"
    assert dot.get("h.name") == "Jane"


def test_dotty_del_custom_types(dot: Dotty):
    # Delete dict keys
    del dot["a.b.c"]
    assert dot.get("a.b.c") is None

    # Delete tuple keys: fails as tuples are immutable
    with pytest.raises(TypeError):
        del dot["a.e.0"]
        assert dot.get("a.e.0") == 3

    # Delete keys of custom types
    del dot["h.name"]
    assert dot.get("h.name") is None


def test_dotty_to_dict(dot: Dotty, dot_serialized):
    assert dot.to_dict() == dot_serialized
