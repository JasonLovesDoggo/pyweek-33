import os
import sys


def is_negative(num):
    return str(num)[0] == "-" and len(str(num)) > 1


class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, "w")

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


def instance_getter(to_count: list, instance: object) -> int:
    count = []
    other = []
    for obj in to_count:
        if isinstance(obj, instance):
            count.append(obj)
        else:
            other.append(obj)
    return count, other


def sizeString(string):
    return f"{string[0]}x{string[1]}"

def offsetToCenter(loc: tuple, size = (20, 24)):
    return (loc[0] - size[0] / 2, loc[1] - size[0] / 2)
