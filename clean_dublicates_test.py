from clean_dublicates import odict, ouniqea, clean_references
from collections import namedtuple
import pytest

Task = namedtuple("Task", ["dublicates", "result"])
Hashable = [
    Task([], []),
    Task([False], [False]),
    Task([False], [0]),
    Task(['a' * 10, 1, 'a' * 10], ['a' * 10, 1]),
    Task(['a' * 1000, 1, 'a' * 1000], ['a' * 1000, 1]),
    Task([True, True], [True]),
    Task([1, 1, 1], [1]),
    Task([1, 2, 1], [1, 2]),
    Task([1, None, 2, 2, 1, None], [1, None, 2]),
    Task([1, None, 2, (), 2, 1, None], [1, None, 2, ()]),
    Task([1, None, 2, (), (), 2, (), 1, None], [1, None, 2, ()]),
    Task(['a', 'a', 'a'], ['a']),
    Task(['a', 'a', 'b', 'b', 'a'], ['a', 'b']),
    Task(['a', 1, 2, 'a', 'b', 'b', 'a'], ['a', 1, 2, 'b']),
    Task([1, None, 2, (), (), 2, (), 1, None, 'a', 1, 2, 'a', 'b', 'b', 'a'],
         [1, None, 2, (), 'a', 'b'])]


@pytest.mark.parametrize("t", Hashable)
def test_odict(t: Task):
    assert odict(t.dublicates) == t.result


@pytest.mark.parametrize("t", Hashable)
def test_hashable_ouniqea(t: Task):
    assert ouniqea(t.dublicates) == t.result


not_hashable = [
    Task([False, [], 0], [0, []]),
    Task([True, [], 0], [1, [], 0]),
    Task([False, [1], 0], [0, [1]]),
    Task([False, {}, 0], [0, {}]),
    Task([[], [], []], [[]]),
    Task([{}, {}, {}], [{}]),
    Task([{1, 1}, {1, 1}, {1, 1}], [{1, 1}]),
    Task([1, None, 2, (), [], (), 2, (), 1, None],
         [1, None, 2, (), []]),
    Task([1, None, 2, (), {}, [], (), 2, (), 1, None, {}],
         [1, None, 2, (), {}, []]),
    Task([1, None, 2, (), {}, [], (), 2, (), 1, None, {}],
         [1, None, 2, (), {}, []]),
    Task([1, None, 2, (), {1, 1, ()}, [], (), 2, (), 1, None, {1, 1, ()}],
         [1, None, 2, (), {1, 1, ()}, []]),
]


@pytest.mark.parametrize("t", not_hashable)
def test_unhashable_ouniqea(t: Task):
    assert ouniqea(t.dublicates) == t.result


str1 = 'a' * 10
str2 = 'a' * 10
big_str1 = 'a' * 100500
big_str2 = 'a' * 100500
d1 = {}
d2 = {}
l1 = []
l2 = []

references_0 = [
    Task([1, 1, 1, 2, 1], [1, 2]),
    Task([0, 1, 1, 2, 0], [0, 1, 2]),
    Task([True, 0], [True, 0]),
    Task([False, 0], [False, 0]),
    Task([False, l1, 0], [False, l1, 0]),
    Task([True, l1, 0], [True, l1, 0]),
    Task([str1, l1, 0], [str2, l1, 0]),
]

references_len = [
    Task([False, l1, l2, 0], 4),
    Task([False, l1, d1, l2, d2, 0], 6),
    Task([str1, str2], 1),
    Task([big_str1, big_str2], 2),
]

references_rev = [
    Task([0, 1], [1, 0]),
    Task([l1, l2], [l2, l1]),
    Task([d1, d2], [d2, d1]),
    Task([big_str1, big_str2], [big_str2, big_str1]),
]


@pytest.mark.parametrize("t", references_0)
def test_clean_references_0(t: Task):
    f = 1
    ans = clean_references(t.dublicates)
    res = t.result
    for i, k in zip(ans, res):
        if i is not k:
            f = 0
            break
    assert f == 1


@pytest.mark.parametrize("t", references_len)
def test_clean_references_len(t: Task):
    ans = clean_references(t.dublicates)
    assert len(ans) == t.result


@pytest.mark.parametrize("t", references_rev)
def test_clean_references_rev(t: Task):
    f = 1
    ans = clean_references(t.dublicates)
    res = t.result
    res.reverse()
    for i, k in zip(ans, res):
        if i is not k:
            f = 0
            break
    assert f == 1
