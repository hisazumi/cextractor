import sys
import re
import itertools
import clang.cindex
from clang.cindex import Index, Cursor

class Node:
    def __init__(self, parent, level, type, content):
        self.level = level
        self.parent = parent
        self.type = type
        self.content = content

    def set_children(self, children):
        self.children = children

    def p(self):
        print("%s : %s" % (self.type, self.content))

    def pp(self, offset):
        print("%s%s: %s : %s" % (offset, self.level, self.type, self.content))
        for child in self.children:
            child.pp(offset+' ')

    def get_leaves(self):
        if len(self.children) == 0:
            return [self]
        else:
            leaves = []
            for child in self.children:
                leaves.extend(child.get_leaves())
            return leaves

def cindex2node(parent, level, current):
    node = Node(parent, level, current.kind.name, current.displayname)
    children = []
    for child in current.get_children():
        children.append(cindex2node(node, level+1, child))
    node.set_children(children)
    return node

def function_name_split(identifier):
    def camel_case_split(identifier):
        matches = re.finditer(
                '.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
        return [m.group(0) for m in matches]
    
    ls = sum([i.split('_') for i in camel_case_split(identifier)], [])
    return '|'.join(ls)

def print_node_tree(node):
    for child in node.get_children():
        if child.kind.name == 'FUNCTION_DECL':
            print("----")
            tree = cindex2node(False, 0, child)
            for leaf in tree.get_leaves():
                leaf.p()

if __name__ == "__main__":
    index = Index.create()
    tu = index.parse("testdata/interrupt.c")
    print_node_tree(tu.cursor)
