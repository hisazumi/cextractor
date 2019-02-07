import sys
import re
import itertools
import clang.cindex
from clang.cindex import Index, Cursor
from argparse import ArgumentParser

class Function:
    SKIP_KINDNAME = ['PARM_DECL']

    def __init__(self, cindex):
        self.funcdecl = cindex.displayname
        self.function_def = Function.cindex2node(False, 0, cindex)
        self.leaves = self.function_def.get_leaves()
        self.pairs = [p for p in self.enumerate_all_combination_of_leaves() if p.is_valid()]

    def enumerate_all_combination_of_leaves(self):
        return [Pair(x) for x in itertools.combinations(self.leaves, 2)]

    def function_name(self):
        def camel_case_split(identifier):
            matches = re.finditer(
                    '.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
            return [m.group(0) for m in matches]
        
        identifier = self.funcdecl[:self.funcdecl.index('(')]
        normed_id = identifier.strip('_').replace('__', '_')
        ls = sum([i.split('_') for i in camel_case_split(normed_id)], [])
        return '|'.join(ls)

    def has_pair(self):
        return len(self.pairs) > 0

    def print_paths(self):
        print(self.function_name(), end='')
        for p in self.pairs:
            print(' ', end='')
            p.print_paths()

    def get_paths(self):
        return ' '.join([self.function_name()] \
            + [p.get_paths() for p in self.pairs])

    def print_fullpaths(self):
        print(self.function_name(), end='')
        for p in self.pairs:
            print(' ', end='')
            p.print_fullpaths()

    def get_pathdict(self):
        dict = {}
        for p in self.pairs:
            dict[p.pathid] = p.get_fullpaths()
        return dict

    def print_ast(self):
        print(self.function_name())
        self.function_def.print_ast('')

    @classmethod
    def cindex2node(klass, parent, level, current):
        node = Node(parent, level, current)
        children = []
        for child in current.get_children():
            if child.kind.name not in klass.SKIP_KINDNAME:
                children.append(Function.cindex2node(node, level+1, child))
        node.set_children(children)
        return node

class Node:
    def __init__(self, parent, level, cursor):
        self.level = level
        self.parent = parent
        self.type = cursor.kind.name
        self.content = cursor.displayname

    def set_children(self, children):
        self.children = children

    def print_ast(self, offset):
        print("%s%s: %s : %s" % (offset, self.level, self.type, self.content))
        for child in self.children:
            child.print_ast(offset+' ')

    def get_leaves(self):
        if len(self.children) == 0:
            return [self]
        else:
            leaves = []
            for child in self.children:
                leaves.extend(child.get_leaves())
            return leaves

    def to_str(self):
        if self.content == '' or self.type == 'STRING_LITERAL' or len(self.children) > 0:
            return self.type
        else:
            return self.content

class Pair:
    def __init__(self, combi):
        self.combination = combi
        self.path = [p.replace(' ', '_') for p in self.find_path()]
        self.pathid = hash('|'.join(self.path[1:-2]))

    def is_valid(self):
        return len(self.path) >= 3

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
                endbuf.insert(0, end.to_str())
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

    def print_paths(self):
        print(self.get_paths(), end='')

    def get_paths(self):
        return "%s,%d,%s" % (self.path[0], self.pathid, self.path[-1])

    def print_fullpaths(self):
        print(self.get_fullpaths())

    def get_fullpaths(self):
        return ','.join(self.path)

    def get_pathid(self):
        return self.pathid

def file2function_array(file):
    tu = Index.create().parse(file)
    return [Function(child) for child in tu.cursor.get_children() \
                if child.kind.name == 'FUNCTION_DECL']

if __name__ == "__main__":
    # Parse arguments
    usage = 'Usage: python {} FILE [--path] [--help]'\
            .format(__file__)
    argparser = ArgumentParser(usage=usage)
    argparser.add_argument('filename', type=str,
                           help='input file')
    argparser.add_argument('-p', '--path',
                           action='store_true',
                           help='show path information')
    argparser.add_argument('-a', '--ast',
                           action='store_true',
                           help='show AST')
    args = argparser.parse_args()

    # Body
    for f in file2function_array(args.filename):
        if args.path:
            f.print_fullpaths()
        elif args.ast:
            f.print_ast()
        else:
            if f.has_pair():
                f.print_paths()
                print()
