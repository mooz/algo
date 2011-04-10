# -*- coding: utf-8 -*-

from node import Node

from debug import log, plog

class Btree(object):
    def __init__(self, t = 2):
        self.t = t
        self.root = Node(t = t)

    @property
    def height(self):
        return self.root.height

    def insert(self, key, value = None):
        log("--------------------")
        log("insert {0}".format(key))
        if self.root.is_full:
            old_root  = self.root
            self.root = Node(t = self.t, is_leaf = False, children = [old_root])
            self.root.split_child(0)
        self.root.insert(key, value)
        log(self)

    def search(self, key):
        return self.root.search(key)

    def delete(self, key):
        log("--------------------")
        log("delete {0}".format(key))
        deleted = self.root.delete(key)
        log(self)
        return deleted

    def __str__(self):
        info = {}
        self.root.set_pp_info(info)
        buf = []
        for level in sorted(info.iterkeys(), reverse = True):
            stack = info[level]
            buf.append(("   " * (level - 1)) + " ".join(stack))
        return "\n".join(buf)
