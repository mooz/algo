# -*- coding: utf-8 -*-

from node import Node

class Btree(object):
    def __init__(self, t=2):
        self.t = t
        self.root = Node(t=t)

    def add_pair(self, key, value):
        pass

    def search(self, key):
        return self.root.search(key)

    @property
    def height(self):
        return self.root.height
