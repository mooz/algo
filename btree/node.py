# -*- coding: utf-8 -*-

class Node():
    def __init__(self, t, parent = None, is_leaf = True,
                 keys = None, children = None):
        if (t < 2):
            raise Exception("t have to be greater than 1")

        self.parent   = parent
        self.is_leaf  = is_leaf
        self.t        = t
        self.keys     = [] if keys is None else keys
        self.children = [None] if children is None else children

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

    def find_proper_child_index(self, key):
        for i, known_key in enumerate(self.keys):
            if key <= known_key:
                break
        else:
            i = len(self.keys)          # len(self.children) - 1
        return i

    def insert(self, key, value = None):
        if (self.is_full):
            raise Exception("Do not call insert for full-node")

        i = self.find_proper_child_index(key)

        if self.is_leaf:
            # do insert
            self.keys.insert(i, key)
            self.children.append(None)
        else:
            if self.children[i].is_full:
                self.split_child(i)
            #
            #    [4][9]
            #      |
            #  [5][6][7]
            #
            # after insertion, keys[i] becomes 6.
            #
            #    [4][6][9]
            #       / \
            # (i) [5] [7] (i+1)
            #
            if key > self.keys[i]:
                i = i + 1
            return self.children[i].insert(key, value)

    def search(self, key):
        i = self.find_proper_child_index(key)

        if i < len(self.keys) and key == self.keys[i]:
            return (key, i)
        elif self.is_leaf:
            return None
        else:
            return self.children[i].search(key)

    def split_child(self, pos):
        child = self.children[pos]

        if not child.is_full:
            raise Exception("Tring to split non-full node")

        med_idx = child.median_key_index

        median_key = child.keys[med_idx]

        left_keys  = child.keys[0:med_idx]
        right_keys = child.keys[med_idx + 1:]

        left_children  = child.children[0:med_idx + 1]
        right_children = child.children[med_idx + 1:]

        left_node = Node(t = child.t, keys = left_keys, children = left_children)
        right_node = Node(t = child.t, keys = right_keys, children = right_children)

        self.keys.insert(pos, median_key)
        self.children.insert(pos, right_node)
        self.children.insert(pos, left_node)

        child.is_leaf = False

    def detach(self):
        """
        Detach from parent node
        """
        pass
