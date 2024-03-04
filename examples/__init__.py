import glob
import importlib
import os
from typing import Callable
from inspect import getmembers, isfunction

__authors__ = ["Joseph Hwang", "Pawel Zadrozny"]
__copyright__ = "Copyright (c) 2024, Joseph Hwang. Originally written by Pawel Zadrozny"


def fetch_all_examples_for_testing() -> list[Callable]:
    """Fetch all functions from every module in example package.

    This list of functions will be used in test_example module running by py.test.
    This helps to include all examples automatically.

    Returns:
        List of example functions
    """
    example_func = []
    for f in glob.glob(os.path.dirname(__file__) + "/*.py"):
        if os.path.isfile(f) and not os.path.basename(f).startswith("_"):
            mod = importlib.import_module(
                "examples.{}".format(os.path.basename(f)[:-3])
            )
            example_func.extend([o[1] for o in getmembers(mod) if isfunction(o[1])])

    return example_func
