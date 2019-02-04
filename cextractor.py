import sys
import re
import itertools
import clang.cindex
from clang.cindex import Index, Cursor

class Node:
    def __init__(self, parent, type, content):
        self.parent = parent
        self.type = type
        self.content = content

    def set_child(self, child):
        self.child = child

    def pp(self, offset):
        print("%s%s : %s" % (offset, self.type, self.content))
        for child in self.child:
            child.pp(offset+' ')

def cindex2node(parent, current):
    node = Node(parent, current.kind.name, current.displayname)
    children = []
    for child in current.get_children():
        children.append(cindex2node(node, child))
    node.set_child(children)
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
            cindex2node(False, child).pp('')

if __name__ == "__main__":
    index = Index.create()
    tu = index.parse("testdata/interrupt.c")
    print_node_tree(tu.cursor)
