# -----------------------------------------------
# AST structure
# -----------------------------------------------
class Node:
    def __init__(self, name, children=None, leaf=None):
        self.name = name
        if children:
            self.children = children
        else:
            self.children = []
        self.leaf = leaf

    def append(self, node):
        self.children.append(node)

    def __str__(self):
        return "<%s>" % self.name

    def __repr__(self):
        return "<%s>" % self.name

# -----------------------------------------------
#
# -----------------------------------------------

# ===================================
# Imprimir AST
# ===================================

def dump_tree(n, indent = ""):
    if not hasattr(n, "datatype"):
        datatype = ""
    else:
        datatype = n.datatype

    if not n.leaf:
        print "%s%s %s" % (indent, n.name, datatype)
    else:
        print "%s%s (%s) %s" % (indent, n.name, n.leaf, datatype)

    indent = indent.replace("-"," ")
    indent = indent.replace("+"," ")

    for i in range(len(n.children)):
        c = n.children[i]
        if i == len(n.children)-1:
            dump_tree(c, indent + "+-- ")
        else:
            dump_tree(c, indent + "|-- ")

# ===================================
# Imprimir AST
