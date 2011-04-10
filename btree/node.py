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
    def is_deletion_delegable(self):
        # XXX: Is this correct for root node?
        return self.key_count >= self.t

    @property
    def height(self):
        return 1 if self.is_leaf else 1 + self.children[0].height

    @property
    def median_key_index(self):
        return self.t - 1

    def find_proper_child_index(self, key):
        for pos, known_key in enumerate(self.keys):
            if key <= known_key:
                break
        else:
            pos = len(self.keys)          # len(self.children) - 1
        return pos

    def insert_at(self, pos, key, value, child = None):
        self.keys.insert(pos, key)
        self.values.insert(pos, value)
        self.children.insert(pos + 1, child)

    def insert(self, key, value = None):
        assert(not self.is_full)

        pos = self.find_proper_child_index(key)

        if pos < len(self.keys) and self.keys[pos] == key:
            self.values[pos] = value      # update value
            return

        if self.is_leaf:
            # do insert
            self.insert_at(pos, key, value)
        else:
            if self.children[pos].is_full:
                self.split_child(pos)
            key_pos = min(pos, len(self.keys) - 1)
            hoisted = self.keys[key_pos]
            if key == hoisted:
                self.values[key_pos] == value # update value
            else:
                if key > hoisted and pos < len(self.keys):
                    # adjust pos (because self.keys was modified)
                    pos += 1
                self.children[pos].insert(key, value)

    def search(self, key):
        pos = self.find_proper_child_index(key)

        if pos < len(self.keys) and key == self.keys[pos]:
            return (key, self.values[pos])
        elif self.is_leaf:
            return None
        else:
            return self.children[pos].search(key)

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

        try:
            pos = self.keys.index(key)
        except ValueError:
            # pattern 3-{a, b}
            return self.delete_internal_descending(key)
        else:
            # pattern 2-{a, b, c}
            return self.delete_internal_restructuring(key, pos)

    def delete_internal_leaf(self, key):
        assert(self.is_leaf)

        try:
            pos = self.keys.index(key)
        except ValueError:
            return False                # not found
        else:
            self.delete_at(pos)
            return True                 # found and deleted

    def delete_internal_restructuring(self, key, pos):
        left_child  = self.children[pos]
        right_child = self.children[pos + 1]

        if (left_child.is_deletion_delegable):
            return self.delete_from_child(left_child, -1, pos) # pattern 2-a
        elif (right_child.is_deletion_delegable):
            return self.delete_from_child(right_child, 0, pos) # pattern 2-b
        else:
            return self.merge_and_delete_from_child(left_child, right_child, key, pos)

    def delete_from_child(self, child, del_pos, replace_pos):
        # save
        del_key = child.keys[del_pos]
        del_value = child.values[del_pos]
        # delete recursively
        deleted = child.delete(del_key)
        # replace
        self.keys[replace_pos] = del_key
        self.values[replace_pos] = del_value
        return deleted

    def merge_nodes(self, left, right, key, value):
        left.keys.append(key)
        left.keys.extend(right.keys)
        left.values.append(value)
        left.values.extend(right.values)
        left.children.extend(right.children)
        return left

    def merge_and_delete_from_child(self, left_child, right_child, key, pos):
        # merge target (key, value) and right_child into left_child
        self.merge_nodes(left_child, right_child, key, self.values[pos])
        # delete target from self
        self.delete_at(pos)
        # delete target from child
        return left_child.delete(key)

    def delete_internal_descending(self, key):
        pos = self.find_proper_child_index(key)
        child = self.children[pos]
        if not child.is_deletion_delegable:
            child = self.ensure_descending_node_is_delegable(pos)
        return child.delete(key)

    def get_child_at(self, pos):
        try:
            return self.children[pos]
        except IndexError:
            return None

    def ensure_descending_node_is_delegable(self, pos):
        child = self.children[pos]

        left_sibling = self.get_child_at(pos - 1)
        if left_sibling and left_sibling.is_deletion_delegable:
            self.rotate_tree(pos, child, left_sibling, clockwise = True)
            return child

        right_sibling = self.get_child_at(pos + 1)
        if right_sibling and right_sibling.is_deletion_delegable:
            self.rotate_tree(pos, child, right_sibling, clockwise = False)
            return child

        # merge children
        if left_sibling:
            left  = left_sibling
            right = child
        else:
            left  = child
            right = right_sibling

        my_pos = min(pos, len(self.keys) - 1)
        merged = self.merge_nodes(left, right, self.keys[my_pos], self.values[my_pos])

        self.delete_at(my_pos)

        return merged

    def rotate_tree(self, pos, target, sibling, clockwise = True):
        # save self key-value
        my_key = self.keys[pos]
        my_value = self.values[pos]

        # carry parts from sibling
        sib_del_pos = -1 if clockwise else 0
        sib_key = sibling.keys[sib_del_pos]
        sib_value = sibling.values[sib_del_pos]
        sib_child = sibling.children[sib_del_pos]
        sibling.delete_at(sib_del_pos, delete_right = clockwise)

        # set carried key-value to self
        self.keys[pos] = sib_key
        self.values[pos] = sib_value

        # give self key-value and sibling child to target
        tar_ins_pos = 0 if clockwise else len(target.keys)
        target.insert_at(tar_ins_pos, my_key, my_value, sib_child)

    def delete_at(self, pos, delete_right = True):
        if pos < 0:
            pos = len(self.keys) + pos
        self.keys.pop(pos)
        self.values.pop(pos)
        if delete_right:
            child_pos = pos + 1         # delete right child for key[pos]
        else:
            child_pos = pos             # delete left child for key[pos]
        return self.children.pop(child_pos)

    def set_pp_info(self, map):
        if not self.height in map:
            map[self.height] = []
        map[self.height].append("[{0}]".format(",".join([str(k) for k in self.keys])))
        if not self.is_leaf:
            for child in self.children:
                child.set_pp_info(map)
