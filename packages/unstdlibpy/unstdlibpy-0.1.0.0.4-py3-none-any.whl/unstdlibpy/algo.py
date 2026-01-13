
"""
This module re-exports selected functions and classes from the standard
libraries `bisect`, `heapq`, and `collections`, along with some custom
algorithmic utilities.
It provides a unified interface for common algorithmic operations.
Functions included:
- binary_search: Perform binary search on a sorted array.
- top_k_elements: Get the top k largest elements from an iterable.
- sliding_window: Generate a sliding window of a specified size over an iterable.

More than these.
Colours are in this. Such as RED, BLACK, PURPLE, CHINESE_RED, MAGIC_COLOR...
"""

from bisect import bisect_left
from heapq import nlargest
from collections import deque
from typing import List, Tuple, Any, Iterable, Deque, Callable
from typing_extensions import Literal

def floatequ(num1: float, num2: float, e: float=1e-10) -> float:
    return abs(num1 - num2) < e * (int(num1 + num2) >> 1)

num2_16: int = 0xFFFF
num2_32: int = 0xFFFFFFFF
num2_64: int = 0xFFFFFFFF_FFFFFFFF
float_inf: float = float('inf')
float_minf: float = float('-inf')
float_zero: float = 0.0

def binary_search(arr: List[Any], target: Any) -> int:
    """
    Perform binary search on a sorted array.
    :param arr: A sorted list of elements.
    :param target: The element to search for.
    :return: The index of the target element if found, otherwise -1.
    """

    index = bisect_left(arr, target)
    if index != len(arr) and arr[index] == target:
        return index
    return -1

def top_k_elements(iterable: Iterable[Any], k: int) -> List[Any]:
    """
    Get the top k largest elements from an iterable.
    :param iterable: An iterable of elements.
    :param k: The number of top elements to retrieve.
    :return: A list of the top k largest elements.
    """

    return nlargest(k, iterable)

def sliding_window(iterable: Iterable[Any], window_size: int) -> Iterable[Tuple[Any, ...]]:
    """
    Generate a sliding window of a specified size over an iterable.
    :param iterable: An iterable of elements.
    :param window_size: The size of the sliding window.
    :return: An iterable of tuples representing the sliding windows.
    """

    if window_size <= 0:
        raise ValueError("window_size must be > 0")

    it = iter(iterable)
    window: Deque[Any] = deque(maxlen=window_size)

    try:
        for _ in range(window_size):
            window.append(next(it))
    except StopIteration:
        # Not enough elements for a full window: yield nothing
        return

    yield tuple(window)

    for elem in it:
        window.append(elem)
        yield tuple(window)

def sort(num: Iterable[Any]) -> Iterable[Any]:
    """
    Sort for a Iterable
    :param num: A function of sorting.
    :type num: Iterable[Any]
    :return: An Iterable of sorting.
    :rtype: Iterable[Any]
    """
    return sorted(num)

def exec(func: Callable, *arg, **kwarg) -> Any:
    return func(*arg, **kwarg)

def printsprint(*values: object, sep: str | None = "", end: str | None = "\n", file: Any | None = None, flush: Literal[False] = False) -> None:
    print(*values, sep=sep, end=end, flush=flush,file=file)

def rgb(string: str, r: int, g: int, b: int, mode: str = 't') -> str:
    assert isinstance(r, int) and isinstance(g, int) and isinstance(b, int) and \
        0 <= r < 256 and 0 <= g < 256 and 0 <= b < 256, f'Bad rgb: {r=}, {g=}, {b=}.'
    if mode == 't': m: int = 38
    elif mode == 'b': m: int = 48
    else: raise NameError(f'Unknown mode: \'{mode}\'.')
    return f'\033[{m};2;{r};{g};{b}m{string}\033[0m'

def make_rgb_mode(r: int, g: int, b: int, mode: str = 't') -> Callable:
    assert isinstance(r, int) and isinstance(g, int) and isinstance(b, int) and \
        0 < r < 256 and 0 < g < 256 and 0 < b < 256, f'Bad rgb: {r=}, {g=}, {b=}.'
    if mode == 't': m: int = 38
    elif mode == 'b': m: int = 48
    else: raise NameError(f'Unknown mode: \'{mode}\'.')
    def wrap(string: str) -> str:
        return f'\033[{m};2;{r};{g};{b}m{string}\033[0m'
    wrap.__name__ = f'rgb({r=}, {g=}, {b=})'
    return wrap

def make_rgb(r: int, g: int, b: int) -> Callable:
    assert isinstance(r, int) and isinstance(g, int) and isinstance(b, int) and \
        0 <= r < 256 and 0 <= g < 256 and 0 <= b < 256, f'Bad rgb: {r=}, {g=}, {b=}.'
    
    def wrap(string: str, mode: str = 't') -> str:
        if mode == 't': m: int = 38
        elif mode == 'b': m: int = 48
        else: raise NameError(f'Unknown mode: \'{mode}\'.')
        return f'\033[{m};2;{r};{g};{b}m{string}\033[0m'
    wrap.__name__ = f'rgb({r=}, {g=}, {b=})'
    return wrap

# some colors.
RED = make_rgb(255, 0, 0)
BLUE = make_rgb(0, 0, 255)
GREEN = make_rgb(0, 255, 0)
YELLOW = make_rgb(255, 255, 0)
ORANGE = make_rgb(255, 128, 0)
CYAN = make_rgb(0, 255, 255)
PURPLE = make_rgb(255, 0, 255)
BLACK = make_rgb(0, 0, 0)
WHITE = make_rgb(255, 255, 255)

# special red
CHINESE_RED = make_rgb(230, 0, 18)
BRIGHT_RED  = make_rgb(255, 0, 36)

# special blue
SKY_BLUE = make_rgb(135, 206, 235)

#special green
EMERALD_GREEN = make_rgb(80, 200, 120)

# ???
MAGIC_COLOR = make_rgb(74, 65, 42)

if __name__ == '__main__':
    print(CHINESE_RED("Water of cow is milk"))
    print(RED        ("Water of cow is milk"))
    print(BRIGHT_RED ("Water of cow is milk"))
    print(MAGIC_COLOR("Water of cow is milk"))

