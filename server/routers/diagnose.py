from typing import Callable


def diagnose(
    function: Callable,
    pre_function: Callable,
    post_function: Callable,
) -> Callable:
    def diagnosed_function(*args, **kwargs):
        pre_function()
        results = function(*args, **kwargs)
        post_function(results)
    return diagnosed_function


def print_diagnose(
    function: Callable,
    print_function: Callable = print,
) -> Callable:
    def diagnosed_function(*args, **kwargs):
        print("=================================")
        results = function(*args, **kwargs)
        print_function(results)
        print("=================================")
    return diagnosed_function
