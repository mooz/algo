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
    tree.insert(13)
    tree.insert(17)
    tree.insert(19)
    tree.insert(14)
    tree.insert(12)
    tree.insert(9)
    tree.insert(113)
    tree.insert(117)
    tree.insert(119)
    tree.insert(114)
    tree.insert(112)
    tree.insert(213)
    tree.insert(217)
    tree.insert(219)
    tree.insert(214)
    tree.insert(212)
    tree.insert(29)
    tree.insert(2113)
    tree.insert(2117)
    tree.insert(2119)
    tree.insert(2114)
    tree.insert(2112)
    eq_(tree.delete(13), True)
    eq_(tree.delete(7), True)
    eq_(tree.delete(17), True)
    eq_(tree.delete(12), True)
    eq_(tree.delete(14), True)
    eq_(tree.delete(19), True)

if __name__ == "__main__":
    import nose
    nose.main(argv=["nose", "-vv", __file__])
