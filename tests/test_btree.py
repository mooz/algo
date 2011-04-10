# -*- coding: utf-8 -*-

import set_libpath

from btree.btree import Btree
from nose.tools import eq_
from btree.debug import plog, log

def setup_tree(t=2, values=None):
    tree = Btree(t=t)

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

def test_btree_insert():
    """
    キーと値のペアを格納可能か
    """
    log("=====================================")
    tree = Btree()
    tree.insert(4)
    tree.insert(7)
    tree.insert(10)
    eq_(tree.height, 1)
    tree.insert(13)
    eq_(tree.height, 2)
    tree.insert(14)
    tree.insert(12)
    tree.insert(9)
    tree.insert(10)
    tree.insert(10)
    tree.insert(20)
    tree.insert(29)
    tree.insert(18)
    tree.insert(16)
    tree.insert(15, "foo")
    eq_(tree.search(15), (15, "foo"))
    tree.insert(15, "bar")
    eq_(tree.search(15), (15, "bar"))
    tree.insert(15)
    eq_(tree.height, 3)

def test_btree_delete():
    """
    キー指定による値の削除
    """
    log("=====================================")
    tree = Btree()
    tree.insert(4)
    tree.insert(7)
    tree.insert(10)
    eq_(tree.delete(10), True)

if __name__ == "__main__":
    import nose
    nose.main(argv=["nose", "-vv", __file__])
