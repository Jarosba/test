from collections import OrderedDict
from more_itertools import unique_everseen
import typing as tp


# complexity O(n), so as dict in Python it is hashtable with open addressing
# work only if in items only hashable types

def odict(items: tp.List[tp.Any]):
    return list(OrderedDict.fromkeys(items))


# with hashable O(n)
# https://github.com/more-itertools/more-itertools/blob/master/more_itertools/recipes.py
# Sequences with a mix of hashable and unhashable items can be used.
# The function will be slower (i.e., `O(n^2)`) for unhashable items.

def ouniqea(items: tp.List[tp.Any]):
    return list(unique_everseen(items))


# this function clean dublicates but compare elements not in values , but references
# work with O(n^2)
def clean_references(items: tp.List[tp.Any]):
    unique = []

    for i in range(len(items)):
        f = 1
        for k in unique:
            if k is items[i]:
                f = 0
                break
        if f:
            unique.append(items[i])
    return unique
