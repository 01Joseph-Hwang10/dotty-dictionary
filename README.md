# dotty-dictionary

[![PyPI version](https://badge.fury.io/py/dotty-dictionary.svg)](https://pypi.org/project/dotty-dictionary)
[![Testsuite](https://github.com/01Joseph-Hwang10/dotty-dictionary/workflows/Test%20and%20Lint/badge.svg)](https://github.com/01Joseph-Hwang10/dotty-dictionary/actions?query=workflow%3A"Test+and+Lint")
[![Python version](https://img.shields.io/pypi/pyversions/dotty-dictionary.svg)](https://pypi.org/project/dotty-dictionary)
[![Project Status](https://img.shields.io/pypi/status/dotty-dictionary.svg)](https://pypi.org/project/dotty-dictionary/)
[![Supported Interpreters](https://img.shields.io/pypi/implementation/dotty-dictionary.svg)](https://pypi.org/project/dotty-dictionary/)
[![License](https://img.shields.io/pypi/l/dotty-dictionary.svg)](https://github.com/pawelzny/dotty-dictionary/blob/master/LICENSE)

`dotty-dictionary` is a Python library that provides a dictionary-like object that allows you to access nested dictionaries using dot notation.

`dotty-dictionary` is a fork of [pawelzny/dotty_dict](https://github.com/pawelzny/dotty_dict) that provides additional features and improvements.

## Installation

```bash
pip install dotty-dictionary
```

- Package: <https://pypi.org/project/dotty-dictionary>
- Source: <https://github.com/01Joseph-Hwang10/dotty-dictionary>

## Features

### Provides dot notation acccess to dictionary objects

It provides a simple wrapper around python dictionary and dict like `Mapping` objects. 
You can access deeply nested keys with dot notation.

```py
from dotty_dictionary import dotty
dot = dotty({"deeply": {"nested": {"key": "value"}}})
dot['deeply.nested.key']
'value'
```

### Exposes all dictionary methods (`.get`, `.pop`, `.keys`, ...)

You can use all dictionary methods like `.get`, `.pop`, `.keys` and other.

```py
from dotty_dictionary import dotty
dot = dotty({"deeply": {"nested": {"key": "value"}}})

# View methods
list(dot.keys()) # ["deeply"]
list(dot.values()) # [{"nested": {"key": "value"}}]
list(dot.items()) #[("deeply", {"nested": {"key": "value"}})]

# `.update`
dot.update({"other": "value"})
dot
Dot(dictionary={'deeply': {'nested': {'key': 'value'}}, 'other': 'value'}, separator='.', esc_char='\\')

# `.pop`: Pops nested keys
dot.pop("deeply.nested.key")
"value"

# `.copy`
dot is not dot.copy()
True
```

### Dot notation access support for list objects

You can access dicts in lists by index like: `dot['parents.0.first_name']`.
It also supports multidimensional lists.

```py
from dotty_dictionary import dotty
dot = dotty({"parents": [{"first_name": "John"}, {"first_name": "Jane"}]})
dot['parents.0.first_name']
'John'

dot = dotty({"matrix": [[1, 2, 3], [4, 5, 6], [7, 8, 9]]})
dot['matrix.1.1']
5
```

> [!NOTE]\
> Using integer in dictionary keys will be treated as embedded list index.


### Support for accessing lists with slices

You can access lists with slices like: `dot['parents.0:2']`.

```py
from dotty_dictionary import dotty
dot = dotty({"parents": [{"first_name": "John"}, {"first_name": "Jane"}, {"first_name": "Doe"}]})
dot['parents.0:2']
[{"first_name": "John"}, {"first_name": "Jane"}]

dot['parents.:']
[{"first_name": "John"}, {"first_name": "Jane"}, {"first_name": "Doe"}]
```

### Flattening and Unflattening

You can utilize `to_flat_dict` and `from_flat_dict` to convert dotty to and from flat dictionary.

```py
from dotty_dictionary import Dotty
dot = Dotty.from_flat_dict({'very.deeply.nested.thing': 'spam', 'very.deeply.spam': 'indeed'})
dot
Dotty(dictionary={'very': {'deeply': {'nested': {'thing': 'spam'}, 'spam': 'indeed'}}}, separator='.', esc_char='\\')

dot.to_flat_dict()
{'very.deeply.nested.thing': 'spam', 'very.deeply.spam': 'indeed'}
```

### Custom Types && Encoders

By default, `dotty-dictionary` only considers `dict` as a mapping type, and `list` as a sequence type and will provide a dot notation access for them. However, you can also provide custom types to be considered as mapping or sequence types.

```py
from collections.abc import MutableMapping
from dataclasses import dataclass
from dotty_dictionary import Dotty, DottyEncoder


@dataclass
class User(MutableMapping):
    name: str
    age: int

    # Implementations are skipped for brevity

class CustomJSONEncoder(DottyEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            return {"name": obj.name, "age": obj.age}
        return super().default(obj)

dictionary = {
    "a": { 
        "b": { "c": 1, "d": 2 },
        "e": (3, {"f": 4}, (5, 6, 7)), # Has Tuple
    },
    "g": 8,
    "h": User(name="John", age=25), # Has Custom Dataclass
}
dot = Dotty(
    dictionary,
    mapping_types=(dict, User),
    sequence_types=(list, tuple),
    json_encoder=CustomJSONEncoder,
)

dot["a.e.1.f"]
4

dot["h.name"]
"John"

dot["h.age"] = 26
dot["h.age"]
26
```

Full example can be found on [tests/test_dotty_custom_types.py](https://github.com/01Joseph-Hwang10/dotty-dictionary/tree/master/tests/test_dotty_custom_types.py)

## More Examples

More examples can be found in the [examples](https://github.com/01Joseph-Hwang10/dotty-dictionary/tree/master/examples) and [tests](https://github.com/01Joseph-Hwang10/dotty-dictionary/tree/master/tests) directory.

## Contributing

Any contribution is welcome! Check out [CONTRIBUTING.md](https://github.com/01Joseph-Hwang10/dotty-dictionary/blob/master/.github/CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](https://github.com/01Joseph-Hwang10/dotty-dictionary/blob/master/.github/CODE_OF_CONDUCT.md) for more information on how to get started.

## License

`dotty-dictionary` is licensed under a [MIT License](https://github.com/01Joseph-Hwang10/dotty-dictionary/blob/master/LICENSE).
