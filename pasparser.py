# coding: utf-8
import ply.yacc as yacc
import re
from paslex import tokens
import sys

# -----------------------------------------------
# AST
# -----------------------------------------------
class Node:
    def __init__(self, name, children=None, leaf=None):
        self.name = type
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
# Parser
# -----------------------------------------------

# ===================================
# Imprimir AST
# ===================================

def dump_tree(n, indent = ""):
    print "hi"
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
# ===================================

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'NOT'),
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),
    ('right', 'ELSE')
)

def p_program(p):
    "program : funlist"
    p[0] = Node("program", [p[1]])

def p_fun_list(p):
    "funlist : funlist function"
    p[1].append(p[2])
    p[0] = p[1]

def p_funList_function(p):
    "funlist : function"
    p[0] = Node("Funlist", [p[1]])

def p_function(p):
    "function : FUN ID '(' arglist ')' localslist BEGIN statementBlock END"
    p[0] = Node("Function", [p[4], p[6], p[8]], p[2])

def p_arglist(p):
    "arglist : args"
    p[0] = Node("ArgList", [p[1]])

def p_arglist_empty(p):
    "arglist : empty"
    p[0] = p[1] # may be or not??

def p_args(p):
    "args : args ',' var_decl"
    p[1].append(p[3])
    p[0] = p[1]

def p_args_argument(p):
    "args : var_decl"
    p[0] = Node("Args", [p[1]])

def p_localList_locals(p):
    "localslist : locals"
    p[0] = p[1]

def p_localList_empty(p):
    "localslist : empty"
    p[0] = p[1]

def p_locals(p):
    "locals : locals declaration_local ';'"
    p[1].append(p[2])
    p[0] = p[1]

def p_locals_localDecl(p):
    "locals : declaration_local ';'"
    p[0] = p[1]

def p_localDecl_varDecl(p):
    "declaration_local : var_decl"
    p[0] = Node("Locals declaration", [p[1]])

def p_localDecl_fun(p):
    "declaration_local : function"
    p[0] = Node("Locals Declaration", [p[1]])

def p_var_decl(p):
    "var_decl : ID ':' type_specifier"
    p[0] = Node("VarDecl", [p[3]], p[1])

def p_type_specifier1(p):
    "type_specifier : simple_type"
    p[0] = p[1]

def p_type_specifier2(p):
    "type_specifier : simple_type '[' INTEGER ']'"
    p[0] = Node("Array[index]", [p[1]],leaf=p[3])

# def p_type_specifier3(p):
#     "type_specifier : INT '[' INTEGER ']'"
#     p[0] = Node("Int[index]", leaf=p[3])

def p_type_int(p):
    "simple_type : INT"
    p[0] = Node("INT")

def p_type_float(p):
    "simple_type : FLOAT"
    p[0] = Node("FLOAT")

def p_statementBlock(p):
    "statementBlock : statementBlock ';' statement"
    p[1].append(p[3])
    p[0] = p[1]

def p_statement(p):
    "statementBlock : statement"
    p[0] = Node("Statement Block", [p[1]])

def p_statement_while(p):
    "statement : WHILE relation DO statement"
    p[0] = Node("While", [p[2], p[4]])

def p_statement_ifthen(p):
    "statement : ifthen"
    p[0] = p[1]

def p_statement_ifThenElse(p):
    "statement : ifthenelse"
    p[0] = p[1]

def p_statement_assign(p):
    "statement : location ASIGN expression"
    p[0] = Node("Assigment", [p[1], p[3]])

def p_statement_inOutExpr(p):
    "statement : inOutExpr"
    p[0] = p[1]

def p_statement_return(p):
    "statement : RETURN expression"
    p[0] = Node("RETURN", [p[2]])

def p_statement_call(p):
    "statement : functionCall"
    p[0] = p[1]

def p_statement_skip(p):
    "statement : SKIP"
    p[0] = Node("Skip")

def p_statement_break(p):
    "statement : BREAK"
    p[0] = Node("Break")

def p_statement_block(p):
    "statement : BEGIN statementBlock END"
    p[0] = Node("BeginEnd Block", [p[2]])

def p_ifthen(p):
    'ifthen : IF relation THEN statement %prec ELSE'
    p[0] = Node("If then", [p[2], p[4]])

def p_ifthenelse(p):
    'ifthenelse : IF relation THEN statement ELSE statement'
    p[0] = Node("If then else", [p[2], p[4], p[5]])

def p_functionCall(p):
    "functionCall : ID '(' paramslistop ')'"
    p[0] = Node("Function Call", [p[3]], leaf=p[1])

def p_paramsListOp1(p):
    "paramslistop : paramList"
    pass

def p_paramsListOp2(p):
    "paramslistop : empty"
    pass

def p_paramList1(p):
    "paramList : paramList ',' expression"
    pass

def p_paramList2(p):
    "paramList : expression"
    pass

def p_inOutExpr1(p):
    "inOutExpr : PRINT '(' STRING ')'"
    p[0] = Node("PRINT", [p[3]])

def p_inOutExpr2(p):
    "inOutExpr : WRITE '(' expression ')'"
    p[0] = Node("WRITE", [p[3]])

def p_inOutExpr3(p):
    "inOutExpr : READ '(' location ')'"
    p[0] = Node("READ", [p[3]])

def p_location1(p):
    "location : ID"
    p[0] = Node("ID")

def p_location2(p):
    "location : ID '[' expression ']'"
    p[0] = Node("Location", [p[3]], p[1])

def p_relationop1(p):
    "relation : relation OR relation"
    p[0] = Node("Relation op", [p[1], p[3]], p[2])

def p_relationop2(p):
    "relation : relation AND relation"
    p[0] = Node("Relation op", [p[1], p[3]], p[2])

def p_relationop3(p):
    "relation : NOT relation"
    p[0] = Node("Relation op", [p[2]], p[1])

def p_relationop4(p):
    "relation : '(' relation ')'"
    p[0] = Node("Relation op", [p[2]])

def p_relation_LT(p):
    "relation : expression LT expression"
    p[0] = Node("Relation", [p[1], p[3]], p[2])

def p_relation_LE(p):
    "relation : expression LE expression"
    p[0] = Node("Relation", [p[1], p[3]], p[2])

def p_relation_GT(p):
    "relation : expression GT expression"
    p[0] = Node("Relation", [p[1], p[3]], p[2])

def p_relation_GE(p):
    "relation : expression GE expression"
    p[0] = Node("Relation", [p[1], p[3]], p[2])

def p_relation_NE(p):
    "relation : expression NE expression"
    p[0] = Node("Relation", [p[1], p[3]], p[2])

def p_relation_equal(p):
    "relation : expression EQUAL expression"
    p[0] = Node("Relation", [p[1], p[3]], p[2])

def p_relation_true(p):
    "relation : TRUE"
    p[0] = Node("True")

def p_relation_false(p):
    "relation : FALSE"
    p[0] = Node("False")

def p_expr_plus(p):
    "expression : expression '+' expression"
    p[0] = Node("Expression", [p[1], p[3]], p[2])

def p_expr_minus(p):
    "expression : expression '-' expression"
    p[0] = Node("Expression", [p[1], p[3]], p[2])

def p_expr_times(p):
    "expression : expression '*' expression"
    p[0] = Node("Expression", [p[1], p[3]], p[2])

def p_expr_div(p):
    "expression : expression '/' expression"
    p[0] = Node("Expression", [p[1], p[3]], p[2])

def p_expr_uminus(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = Node("Expression", [p[2]], p[1])

def p_expr_uplus(p):
    "expression : '+' expression"
    p[0] = Node("Expression", [p[2]])

def p_expr_parens(p):
    "expression : '(' expression ')'"
    p[0] = Node("Expression", [p[2]])

def p_expr_id(p):
    "expression : ID"
    p[0] = Node("ID")

def p_expr_num(p):
    "expression : number"
    p[0] = p[1]

def p_expr_ubication(p):
    "expression : ID '[' expression ']'"
    p[0] = Node("Expression", [p[3]], p[1])

def p_expr_casting(p):
    "expression : casting"
    p[0] = p[1]

def p_expr_funcall(p):
    "expression : functionCall"
    p[0] = p[1]

def p_casting_int(p):
    "casting : INT '(' expression ')'"
    p[0] = Node("Casting Int", [p[3]], leaf=int(p[3]))

def p_casting_float(p):
    "casting : FLOAT '(' expression ')'"
    p[0] = Node("Casting Float", [p[3]], leaf=float(p[3]))

def p_number_int(p):
    "number : INTEGER"
    p[0] = Node("INTEGER", [p[1]])

def p_number_float(p):
    "number : FLOATNUM"
    p[0] = Node("FLOAT", [p[1]])

def p_empty(p):
    "empty : "
    p[0] = Node("Empty")

def p_error(p):
    print("Error en la entrada!")
    print p

def make_parser():
    parser = yacc.yacc(debug=0)
    return parser

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

# def dump_tree(node, indent = ""):
#     #print node
#     if not hasattr(node, "datatype"):
# 		datatype = ""
#     else:
# 		datatype = node.datatype
#
#     if(node.__class__.__name__ != "str" and node.__class__.__name__ != "list"):
#         print "%s%s  %s" % (indent, node.__class__.__name__, datatype)
#
#     indent = indent.replace("-"," ")
#     indent = indent.replace("+"," ")
#     if hasattr(node,'_fields'):
#         mio = node._fields
#     else:
#         mio = node
#     if(isinstance(mio,list)):
#         for i in range(len(mio)):
#             if(isinstance(mio[i],str) ):
#                 c = getattr(node,mio[i])
#             else:
#              c = mio[i]
#             if i == len(mio)-1:
# 		    	dump_tree(c, indent + "  +-- ")
#             else:
# 		    	dump_tree(c, indent + "  |-- ")
#     else:
#         print indent, mio

# ===================================
# Imprimir AST
# ===================================


if __name__ == "__main__":
    if (len(sys.argv) < 2 or len(sys.argv) > 4):
        print "Usage: python %s [-ast] [-lex] <pascal_file>" % sys.argv[0]
    elif (re.match(r'.*\.pas', sys.argv[-1])):
        try:
            for i in sys.argv:
                if (i == "-ast"):
                    print "Get ast op"
                if (i == "-lex"):
                    print "Get lex op"

            file = open(sys.argv[-1])
            data = file.read()
            parser = make_parser()
            result = parser.parse(data)
            # dump_tree(result)
            print result
        except IOError:
            print "Error: The file does not exist"
            print "Usage: python %s [-ast] [-lex] <pascal_file>" % sys.argv[0]
    else:
        print "Please put the name of your pascal file at the end of the command"

'''
... refactor
? ask

program: fun_list

fun_list: fun_list fun
        | fun

fun: FUN ID '(' arglist ')' localslist BEGIN statementBlock END

arglist: args
       | empty

args: args ',' var_decl
    | var_decl

var_decl: ID ':' type_specifier

type_specifier: INT LSQUARE INTEGER RSQUARE
              | FLOAT LSQUARE INTEGER RSQUARE
              | type

type: INT
    | FLOAT

localsList: locals
          | empty

locals: declaration_local ';'
      | locals declaration_local ';'

declaration_local: var_decl
        | fun

statementBlock : statementBlock ';' statement
          | statement

statement: WHILE relation DO statement
         |  IF relation THEN statement // ifthen
         |  IF relation THEN statement %prec ELSE statement // ifthenelse
         |  assigment
         |  inOutExpr
         |  RETURN expression ...
         |  functionCall
         |  SKIP
         |  BREAK
         |  BEGIN statementBlock END

functionCall: ID LPAREN arglist RPAREN

->
relation: relation OR relation
          | relation AND relation
          | NOT relation
          | LPAREN relation RPAREN
          | relation

relation: expression LT expression
        | expression LE expression
        | expression GT expression
        | expression GE expression
        | expression NE expression
        | expression EQUAL expression
        | TRUE
        | FALSE

expression: expression '+' expression
          | expression '-' expression
          | expression '*' expression
          | expression '/' expression
          | '-' expression
          | '+' expression
          | LPAREN expression RPAREN
          | ID // location
          | ID LSQUARE expression RSQUARE
          | number
          | ID LPAREN expression RPAREN
          | casting
          | functionCall

number: INTEGER
      | FLOATNUM

location: ID
        | ID LSQUARE INTEGER RSQUARE //errors: index must be int, type errors

inOutExpr: PRINT LPAREN STRING RPAREN
         | WRITE LPAREN expression RPAREN
         | READ LPAREN location RPAREN

casting: FLOAT LPAREN expression RPAREN
       | INT LPAREN expression RPAREN
'''
