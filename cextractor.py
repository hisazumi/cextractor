import sys

import clang.cindex
from clang.cindex import Index
from clang.cindex import Config

def print_node_tree(node, offset):
    print("%s%s : %s" % (offset, node.kind.name, node.displayname))
    for child in node.get_children():
        print_node_tree(child, offset+" ")

if __name__ == "__main__":
    index = Index.create()
    tu = index.parse("testdata/interrupt.c")
    print_node_tree(tu.cursor, "")
