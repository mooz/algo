# -*- coding: utf-8 -*-

from debug import log, plog

class Node():
    def __init__(self, t, parent = None, is_leaf = True,
                 keys = None, values = None, children = None):
        if (t < 2):
            raise Exception("t have to be greater than 1")

        self.parent   = parent
        self.is_leaf  = is_leaf
        self.t        = t
        self.keys     = [] if keys is None else keys
        self.values   = [] if values is None else values
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
    def min_key_count(self):
        return 1 if self.is_root else self.t - 1

    @property
    def max_child_count(self):
        return self.max_key_count + 1

    @property
    def min_child_count(self):
        return 1 if self.is_root else self.min_key_count + 1

    @property
    def is_full(self):
        return self.key_count == self.max_key_count

    @property
    def height(self):
        return 1 if self.is_leaf else 1 + self.children[0].height

    @property
    def median_key_index(self):
        return self.t - 1

    def find_child_node_pos(self, key):
        for i, known_key in enumerate(self.keys):
            if key <= known_key:
                break
        else:
            i = len(self.keys)          # len(self.children) - 1
        return i

    def insert(self, key, value = None):
        if (self.is_full):
            raise Exception("Do not call insert for full-node")

        i = self.find_child_node_pos(key)

        if i < len(self.keys) and self.keys[i] == key:
            self.values[i] = value      # update value
            return

        if self.is_leaf:
            # do insert
            self.keys.insert(i, key)
            self.values.insert(i, value)
            self.children.append(None)
        else:
            if self.children[i].is_full:
                self.split_child(i)
            if i < len(self.keys) and key == self.keys[i]:
                self.values[i] == value # update value
            else:
                self.children[i].insert(key, value)

    def search(self, key):
        i = self.find_child_node_pos(key)

        if i < len(self.keys) and key == self.keys[i]:
            return (key, self.values[i])
        elif self.is_leaf:
            return None
        else:
            return self.children[i].search(key)

    def split_child(self, pos):
        child = self.children[pos]

        if not child.is_full:
            raise Exception("Trying to split non-full node")

        med_idx = child.median_key_index

        left_node = Node(t        = child.t,
                         is_leaf  = child.is_leaf,
                         keys     = child.keys[0:med_idx],
                         values   = child.values[0:med_idx],
                         children = child.children[0:med_idx + 1])
        right_node = Node(t        = child.t,
                          is_leaf  = child.is_leaf,
                          keys     = child.keys[med_idx + 1:],
                          values   = child.values[med_idx + 1:],
                          children = child.children[med_idx + 1:])

        self.keys.insert(pos, child.keys[med_idx])
        self.values.insert(pos, child.values[med_idx])
        self.children[pos] = right_node
        self.children.insert(pos, left_node)

    def delete(self, key):
        if (self.is_leaf):
            return self.delete_internal_leaf(key)
        else:
            raise Exception("Not implemented yet")

    def delete_internal_leaf(self, key):
        assert(self.is_leaf)

        try:
            i = self.keys.index(key)
            self.delete_at(i)
            return True                 # found and deleted
        except ValueError:
            return False                # not found

    def delete_at(self, pos, left = False):
        self.keys.pop(pos)
        self.values.pop(pos)
        if left:
            child_pos = pos             # delete left child for key[pos]
        else:
            child_pos = pos + 1         # delete right child for key[pos]
        return self.children.pop(pos)

    def set_pp_info(self, map):
        if not self.height in map:
            map[self.height] = []
        map[self.height].append("[{0}]".format(",".join([str(k) for k in self.keys])))
        if not self.is_leaf:
            for child in self.children:
                child.set_pp_info(map)
