# -*- coding: utf-8 -*-

class Node():
    def __init__(self, t, parent=None, is_leaf=True,
                 keys=None, children=None):
        if (t < 2):
            raise Exception("t have to be greater than 1")

        self.parent   = parent
        self.is_leaf  = is_leaf
        self.t        = t
        self.keys     = [] if keys is None else keys
        self.children = [] if children is None else children

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

    @property
    def median_key_index(self):
        return self.t - 1

    def find_proper_key_index(self, key):
        for i, known_key in enumerate(self.keys):
            if key <= known_key:
                break
        else:
            i = len(self.keys)
        return i

    def add_pair(self, key, value):
        i = self.find_proper_key_index(key)

        if self.is_leaf:
            if self.is_full:
                # split
                # if self.is_root:
                # else:
                #     self.parent.split_child(self)
                pass
            # do insert
            self.keys[:] = self.keys[0:i] + [key] + self.keys[i:]
        else:
            self.children[i].add_pair(key, value)

    def search(self, key):
        i = self.find_proper_key_index(key)

        if i < len(self.keys) and key == self.keys[i]:
            return (key, i)
        elif self.is_leaf:
            return None
        else:
            return self.children[i].search(key)

    def split(self):
        if not self.is_full:
            raise Exception("Tring to split non-full node")

        median_key = self.keys[self.median_key_index]

        left_keys  = self.keys[0:self.median_key_index]
        right_keys = self.keys[self.median_key_index + 1:]

        left_children  = self.children[0:self.median_key_index + 1]
        right_children = self.children[self.median_key_index + 1:]

        left_node = Node(t=self.t, keys=left_keys, children=left_children)
        right_node = Node(t=self.t, keys=right_keys, children=right_children)

    def detach(self):
        """
        Detach from parent node
        """
        pass
