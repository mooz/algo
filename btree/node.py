# -*- coding: utf-8 -*-

class Node():
    def __init__(self, t, parent=None, is_leaf=True):
        if (t < 2):
            raise Exception("t have to be greater than 1")

        self.parent   = parent
        self.is_leaf  = is_leaf
        self.t        = t
        self.keys     = []
        self.children = []

    @property
    def is_root(self):
        return self.parent is None

    @property
    def key_count(self):
        return len(self.keys)

    @property
    def max_key_count(self):
        return 2 * self.t - 1

    @property
    def max_child_count(self):
        return self.max_key_count + 1

    @property
    def first_child(self):
        return self.children[0]

    @property
    def last_child(self):
        return self.children[-1]

    @property
    def is_full(self):
        return self.key_count == self.max_key_count

    @property
    def height(self):
        return 1 if self.is_leaf else 1 + self.first_child.height

    def find_proper_key_index(self, key):
        for i, known_key in enumerate(self.keys):
            if key <= known_key:
                break
        else:
            i += 1
        return i

    def add_pair(self, key, value):
        if self.is_full:
            raise Exception("Split is not supported yet")
        i = self.find_proper_key_index(key)
        # self.keys[]

    def search(self, key):
        i = self.find_proper_key_index(key)

        if i < len(self.keys) and key == self.keys[i]:
            return (key, i)
        elif self.is_leaf:
            return None
        else:
            return self.children[i].search(key)

    def detach(self):
        """
        Detach from parent node
        """
        pass
