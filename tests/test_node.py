# -*- coding: utf-8 -*-

import set_libpath

from btree.node import Node
from nose.tools import eq_

def test_node_construct():
    node = Node(t=2)
    eq_(node.is_full, False)
    eq_(node.is_leaf, True)
    eq_(node.parent, None)
    eq_(node.key_count, 0)
    eq_(node.max_key_count, 3)

def test_node_search_leaf():
    node = Node(t=2)
    node.keys = [3, 9, 15]
    eq_(node.search(-10), None)
    eq_(node.search(3), (3, 0))
    eq_(node.search(15), (15, 2))
    eq_(node.search(17), None)

def test_find_proper_child_index():
    node = Node(t=2)
    node.keys = [3, 9, 15]
    eq_(node.find_proper_child_index(-10), 0)
    eq_(node.find_proper_child_index(3), 0)
    eq_(node.find_proper_child_index(5), 1)
    eq_(node.find_proper_child_index(9), 1)
    eq_(node.find_proper_child_index(15), 2)
    eq_(node.find_proper_child_index(16), 3)

# def test_split():
#     node = Node(t=3)
#     node.keys = [3, 9, 15, 20, 32]
#     median, left, right = node.split()
#     eq_(left.keys, [3, 9])
#     eq_(median, 15)
#     eq_(right.keys, [20, 32])

def test_insert():
    node = Node(t=3)
    node.insert(20, None)
    node.insert(3, None)
    node.insert(9, None)
    node.insert(32, None)
    node.insert(15, None)
    eq_(node.keys,  [3, 9, 15, 20, 32])

if __name__ == "__main__":
    import nose
    nose.main(argv=["nose", "-vv", __file__])
