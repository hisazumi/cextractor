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

    def to_str(self):
        if self.content == '':
            return self.type
        else:
            return self.content
#        return self.type + '|' + self.content

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

def enumerate_all_combination_of_leaves(leaves):
    return [x for x in itertools.combinations(leaves, 2)]

def find_path(combi):
    start = combi[0]
    startbuf = []
    end = combi[1]
    endbuf = []

    # adjust level
    if start.level > end.level:
        for i in range(start.level - end.level):
            startbuf.append(start.to_str())
            start = start.parent

    if start.level < end.level:
        for i in range(end.level - start.level):
            endbuf.append(end.to_str())
            end = end.parent

    # up until match
    for i in range(start.level):
        if start == end:
            break
        startbuf.append(start.to_str())
        start = start.parent
        endbuf.append(end.to_str())
        end = end.parent
        
    return startbuf + endbuf

def to_str(combi):
    path = find_path(combi)
    return "%s,%d,%s" % (path[0], hash('|'.join(path[1:-2])), path[-1])

def print_node_tree(node):
    for child in node.get_children():
        if child.kind.name == 'FUNCTION_DECL':
            sys.stdout.write(function_name_split(child.displayname[:child.displayname.index('(')]) + " ")
            tree = cindex2node(False, 0, child)
            leaves = tree.get_leaves()
            combis = enumerate_all_combination_of_leaves(leaves)
            for c in combis:
                sys.stdout.write(to_str(c) + " ")
            print
                            
if __name__ == "__main__":
    index = Index.create()
    tu = index.parse("testdata/interrupt.c")
    print_node_tree(tu.cursor)
