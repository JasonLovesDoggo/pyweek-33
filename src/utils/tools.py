import os
import sys
from random import randint


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


def offsetToCenter(loc: tuple, size=(20, 24)):
    return (loc[0], loc[1] - size[0] / 2)



def centerToOffset(loc: tuple, size=(20, 24)):
    return (loc[0] - size[0] / 2, loc[1] - size[1] / 2)


def quicksort(array):
    if len(array) < 2:
        return array

    low, same, high = [], [], []

    pivot = array[randint(0, len(array) - 1)]

    for item in array:
        if item[0] < pivot[0]:
            low.append(item)
        elif item[0] == pivot[0]:
            same.append(item)
        elif item[0] > pivot[0]:
            high.append(item)

    return quicksort(low) + same + quicksort(high)


def sortFartestToClosest(tile_layers, tmxdata, reverse=False):
    scores = []
    for z, layer in enumerate(tile_layers):
        for y, row in enumerate(layer.data):
            for x in range(len(row)):
                scores.append([x + y + z, (x, y, z)])

    out = [item[1] for item in quicksort(scores)]

    return out.reverse() if reverse else out
