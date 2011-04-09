# -*- coding: utf-8 -*-

import set_libpath

from btree import btree
from nose.tools import eq_

def setup_tree(t=2, values=None):
    tree = btree.Btree(t=t)

    if not values is None:
        for key, value in values:
            tree.add_pair(key, value)
    return tree

def test_btree_create_instance():
    """
    インスタンスが作成可能か
    """
    tree = setup_tree()
    pass

def test_btree_add_key_value():
    """
    キーと値のペアを格納可能か
    """
    tree = setup_tree((("foo", "bar"), ("baz", "qux")))
    eq_(tree.height, 1)

if __name__ == "__main__":
    import nose
    nose.main(argv=["nose", "-vv", __file__])
