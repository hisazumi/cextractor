import sys
import re
import itertools
import clang.cindex
from clang.cindex import Index, Cursor

class Function:
    def __init__(self, cindex):
        self.funcdecl = cindex.displayname
        self.function_def = Function.cindex2node(False, 0, cindex)
        self.leaves = self.function_def.get_leaves()
        self.pairs = self.enumerate_all_combination_of_leaves()

    def enumerate_all_combination_of_leaves(self):
        return [Pair(x) for x in itertools.combinations(self.leaves, 2)]

    def function_name(self):
        def camel_case_split(identifier):
            matches = re.finditer(
                    '.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
            return [m.group(0) for m in matches]
        
        identifier = self.funcdecl[:self.funcdecl.index('(')]
        ls = sum([i.split('_') for i in camel_case_split(identifier)], [])
        return '|'.join(ls)

    def to_str(self):
        out = self.function_name()
        for p in self.pairs:
            out = out + ' ' + p.to_str()
        return out

    @classmethod
    def cindex2node(klass, parent, level, current):
        node = Node(parent, level, current.kind.name, current.displayname)
        children = []
        for child in current.get_children():
            children.append(Function.cindex2node(node, level+1, child))
        node.set_children(children)
        return node

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

class Pair:
    def __init__(self, combi):
        self.combination = combi

    def find_path(self):
        combi = self.combination

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
            endbuf.insert(0, end.to_str())
            end = end.parent
            
        return startbuf + endbuf

    def to_str(self):
        path = self.find_path()
        return "%s,%d,%s" % (path[0], hash('|'.join(path[1:-2])), path[-1])

def file2function_array(file):
    tu = Index.create().parse(file)
    return [Function(child) for child in tu.cursor.get_children() \
                if child.kind.name == 'FUNCTION_DECL']

if __name__ == "__main__":
    fa = file2function_array("testdata/interrupt.c")
    for f in fa:
        print(f.to_str())
        print()
