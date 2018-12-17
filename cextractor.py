import sys
import re
import itertools
import clang.cindex
from clang.cindex import Index, Cursor

# text|extent point,362150388,METHOD_NAME point,714300710,string point,-1248995371,string METHOD_NAME,-1103308019,string METHOD_NAME,1228363196,string METHOD_NAME,713917609,context METHOD_NAME,713917671,string METHOD_NAME,713917702,textextent string,381233612,string string,-1107024650,context string,-1107024588,string string,-1107024557,textextent string,-285930137,context string,-285930075,string string,-285930044,textextent context,2020783594,string string,-1572583797,textextent

#     public Point textExtent(String string) {
#        return context.textExtent(string);
#    }



def function_decl(node):
    def camel_case_split(identifier):
        matches = re.finditer(
                '.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
        return [m.group(0) for m in matches]

    def function_name_split(identifier):
        ls = sum([i.split('_') for i in camel_case_split(identifier)], [])
        return '|'.join(ls)

    def function_decl_print(node, offset):
        print("%s %s %s" % (offset, node.kind.name, node.displayname))
        for child in node.get_children():
            function_decl_print(child, offset + ' ')

    def function_decl_traverse(node):
        def is_finished(node):
            try:
                next(node)
                return False
            except StopIteration:
                return True

        terminals = []

        for child in node.get_children():
            if is_finished(child.get_children()):
                terminals.append(child)
            else:
                terminals.extend(function_decl_traverse(child))

        return terminals

    def get_all_leafs(node):
        terminals = []
        for child in node.get_children():
            terminals.extend(function_decl_traverse(child))
        return terminals

    function_name = node.displayname[:node.displayname.index('(')]
    print("%s : %s" % (node.kind.name, function_name_split(function_name)))

    for child in node.get_children():
        function_decl_print(child, '')

    combinations = [x for x in itertools.combinations(get_all_leafs(node), 2)]

    print("-----")
    for t in combinations:
        print("> %s %s : %s %s" % (t[0].kind.name, t[0].displayname, t[1].kind.name, t[1].displayname))
    print("-----")


def print_node_tree(node, offset):
    print("%s%s : %s" % (offset, node.kind.name, node.displayname))
    for child in node.get_children():
        if child.kind.name == 'FUNCTION_DECL':
            function_decl(child)

if __name__ == "__main__":
    index = Index.create()
    tu = index.parse("testdata/interrupt.c")
    print_node_tree(tu.cursor, "")
