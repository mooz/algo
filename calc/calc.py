#!/usr/bin/env python

class Node(object):
    pass

class OperationNode(Node):
    def __init__(self, operation, left = None, right = None):
        self.operation = operation
        self.left = left
        self.right = right

class OperandNode(Node):
    def __init__(self, value = None):
        self.value = value

class PrefixParser:
    OPERATIONS = {
        "+" : 1,
        "-" : 2,
        "*" : 3,
        "/" : 4,
    }

    def __init__(self):
        pass

    def set_chars(self, chars):
        self.chars = chars
        self.chars_len = len(chars)
        self.pos = 0

    def peek_next_char(self):
        c = self.chars[self.pos]
        return c

    def get_next_char(self):
        c = self.chars[self.pos]
        self.pos += 1
        return c

    def has_next(self):
        return self.pos < self.chars_len

    def skip_spaces(self):
        while True:
            c = self.peek_next_char()
            if not c in (' ', '\n', '\r', '\t'):
                break
            self.get_next_char()        # trash

    def parse(self, chars):
        self.set_chars(chars)
        return self.parse_node()

    def parse_node(self):
        self.skip_spaces()

        if self.peek_next_char() in self.OPERATIONS:
            return self.parse_operation_node()
        else:
            return self.parse_operand_node()

    def parse_operation_node(self):
        return OperationNode(self.get_next_char(), self.parse_node(), self.parse_node())

    def parse_operand_node(self):
        buf = []
        while self.has_next():
            if not self.is_number(self.peek_next_char()):
                break
            buf.append(self.get_next_char())
        if not buf:
            raise Exception("Parse Error: Operand node must have at least 1 numeral char")
        return OperandNode(int("".join(buf)))

    def is_number(self, c):
        return 48 <= ord(c) <= 57

def tree_prefix(node):
    if isinstance(node, OperationNode):
        return " ".join((node.operation,
                         tree_prefix(node.left),
                         tree_postfix(node.right)))
    elif isinstance(node, OperandNode):
        return str(node.value)

def tree_postfix(node):
    if isinstance(node, OperationNode):
        return " ".join((tree_postfix(node.left),
                         tree_postfix(node.right),
                         node.operation))
    elif isinstance(node, OperandNode):
        return str(node.value)

import operator

EVALUATORS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.div,
}

def eval_tree(node):
    if isinstance(node, OperationNode):
        return EVALUATORS[node.operation](
            eval_tree(node.left),
            eval_tree(node.right)
        )
    elif isinstance(node, OperandNode):
        return node.value

if __name__ == "__main__":
    parser = PrefixParser()
    parsed = parser.parse("+ * 3 4 6")
    print(tree_prefix(parsed))
    print(tree_postfix(parsed))
    print("=> " + str(eval_tree(parsed)))
