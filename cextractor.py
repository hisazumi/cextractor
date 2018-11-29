import sys
import re
import clang.cindex
from clang.cindex import Index, Cursor

def function_decl(node):
    def camel_case_split(identifier):
        matches = re.finditer(
                '.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
        return [m.group(0) for m in matches]

    def function_name_split(identifier):
        ls = sum([i.split('_') for i in camel_case_split(identifier)], [])
        return '|'.join(ls)

    function_name = node.displayname[:node.displayname.index('(')]
    print("%s : %s" % (node.kind.name, function_name_split(function_name)))

def print_node_tree(node, offset):
    print("%s%s : %s" % (offset, node.kind.name, node.displayname))
    for child in node.get_children():
        if child.kind.name == 'FUNCTION_DECL':
            function_decl(child)

if __name__ == "__main__":
    index = Index.create()
    tu = index.parse("testdata/interrupt.c")
    print_node_tree(tu.cursor, "")
