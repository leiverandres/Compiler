# coding: utf-8
import ply.yacc as yacc
import ply.lex as lex
from paslex import tokens
from pasAST import *
import paslex
import re
import sys
green = '\033[01;32m'
red = '\033[01;31m'

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'NOT'),
    ('left', 'LT', 'LE', 'GT', 'GE', 'NE'),
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),
    ('right', 'ELSE')
)

hasErrors = False

def p_program(p):
    "program : funlist"
    p[0] = p[1]

def p_error_program(p):
    "program : empty" # error al menos una function
    p[0] = Node("Error")
    p[0].lineno = p.lineno(1)
    sys.stderr.write(green+"Warning: File problem\n")

def p_fun_list(p):
    "funlist : funlist function"
    p[1].append(p[2])
    p[0] = p[1]
    p[0].lineno = p.lineno(2)

def p_funList_function(p):
    "funlist : function"
    p[0] = Node("Program", [p[1]])
    p[0].lineno = p.lineno(1)

def p_function(p):
    "function : FUN ID '(' arglist ')' localslist BEGIN statementBlock END"
    p[0] = Node("Function", [p[4], p[6], p[8]], p[2])
    p[0].lineno = p.lineno(2)

def p_error_function(p):
    "function : FUN '(' arglist ')' localslist BEGIN statementBlock END"
    p[0] = Node("Error")
    p[0].lineno = p.lineno(1)
    global hasErrors
    hasErrors = True
    sys.stderr.write(red+"Error line %d: Function indentifier missing\n" % p.lineno(1))

def p_error_function2(p):
    "function : FUN ID '(' arglist ')' localslist BEGIN statementBlock ';' END"
    p[0] = Node("Error")
    p[0].lineno = p.lineno(9)
    sys.stderr.write(red+"Error line %d: bad ';' before END\n" % (p.lineno(9)))

def p_arglist(p):
    "arglist : args"
    p[0] = p[1]

def p_arglist_empty(p):
    "arglist : empty"
    p[0] = p[1] # may be or not??
    p[0].lineno = p.lineno(1)

def p_args_argument(p):
    "args : var_decl"
    p[0] = Node("Argument List", [p[1]])
    p[0].lineno = p[1].lineno

def p_args(p):
    "args : args ',' var_decl"
    p[1].append(p[3])
    p[0] = p[1]

def p_error_args(p):
    "args : args var_decl"
    p[0] = Node("Error")
    p[0].lineno = p[2].lineno
    sys.stderr.write(red+"Error line %d: ',' missing before argument declaration\n" % (p[2].lineno))

def p_localList_locals(p):
    "localslist : locals"
    p[0] = p[1]

def p_localList_empty(p):
    "localslist : empty"
    p[0] = p[1]

def p_locals_var(p):
    "locals : locals var_decl ';'"
    p[1].append(p[2])
    p[0] = p[1]

def p_locals_fun(p):
    "locals : locals function ';'"
    p[1].append(p[2])
    p[0] = p[1]

def p_locals_localDecl(p):
    "locals : var_decl ';'"
    p[0] = Node("Locals List", [p[1]])
    p[0].lineno = p[1].lineno

def p_locals_localFun(p):
    "locals : function ';'"
    p[0] = Node("Locals List", [p[1]])
    p[0].lineno = p[1].lineno

def p_error_locals1(p):
    "locals : locals var_decl"
    p[0] = Node("Error")
    p[0].lineno = p[2].lineno
    sys.stderr.write(red+"Error line %d: ';' missing after local declaration\n" % (p[2].lineno))

def p_error_locals2(p):
    "locals : var_decl"
    p[0] = Node("Error")
    p[0].lineno = p[1].lineno
    sys.stderr.write(red+"Error line %d: ';' missing after local declaration\n" % (p[1].lineno))

def p_error_locals3(p):
    "locals : locals function"
    p[0] = Node("Error")
    p[0].lineno = p[2].lineno
    sys.stderr.write(red+"Error line %d: ';' missing after local function\n" % (p[2].lineno))

def p_error_locals4(p):
    "locals : function"
    p[0] = Node("Error")
    p[0].lineno = p[1].lineno
    sys.stderr.write(red+"Error line %d: ';' missing after local function\n" % (p[1].lineno))

def p_var_decl(p):
    "var_decl : ID ':' type_specifier"
    p[0] = Node("Variable", [p[3]], p[1])
    p[0].lineno = p.lineno(1)

def p_error_var_decl(p):
    '''
    var_decl : ID type_specifier
             | ID ASIGN type_specifier
    '''
    p[0] = Node("Error")
    p[0].lineno = p.lineno(1)
    sys.stderr.write(red+"Error line %d: bad Assigment. ':' missing\n" % (p.lineno(1)))

def p_type_specifier1(p):
    "type_specifier : simple_type"
    p[0] = p[1]

def p_type_specifier2(p):
    "type_specifier : simple_type '[' INTEGER ']'"
    p[0] = Node("Array[index]", [p[1]], leaf=p[3])
    p[0].lineno = p[1].lineno

def p_type_int(p):
    "simple_type : INT"
    p[0] = Node("INT", leaf=p[1])
    p[0].lineno = p.lineno(1)

def p_type_float(p):
    "simple_type : FLOAT"
    p[0] = Node("FLOAT", leaf=p[1])
    p[0].lineno = p.lineno(1)

def p_statementBlock(p):
    "statementBlock : statementBlock ';' statement"
    p[1].append(p[3])
    p[0] = p[1]

def p_statement(p):
    "statementBlock : statement"
    p[0] = Node("statement Block", [p[1]])
    p[0] = p[1]

def p_error_comma_stm(p):
    "statementBlock : statementBlock statement"
    p[0] = Node("Error")
    p[1].append(p[2])
    p[0] = p[1]
    sys.stderr.write(red+"Error line %d: ';' expected before statement\n" % (p[2].lineno))

def p_statement_while(p):
    "statement : WHILE relation DO statement"
    p[0] = Node("While", [p[2], p[4]])
    p[0].lineno = p.lineno(1)

def p_statement_ifthen(p):
    "statement : ifthen"
    p[0] = p[1]
    p[0].lineno = p.lineno(1)

def p_statement_ifThenElse(p):
    "statement : ifthenelse"
    p[0] = p[1]
    p[0].lineno = p.lineno(1)

def p_statement_assign(p):
    "statement : location ASIGN expression"
    p[0] = Node("Assigment", [p[1], p[3]])
    p[0].lineno = p.lineno(2)

def p_statement_inOutExpr(p):
    "statement : inOutExpr"
    p[0] = p[1]

def p_statement_return(p):
    "statement : RETURN expression"
    p[0] = Node("RETURN", [p[2]])
    p[0].lineno = p.lineno(1)

def p_statement_return2(p):
    "statement : RETURN"
    p[0] = Node("RETURN empty")
    p[0].lineno = p.lineno(1)

def p_statement_call(p):
    "statement : functionCall"
    p[0] = p[1]

def p_statement_skip(p):
    "statement : SKIP"
    p[0] = Node("Skip")
    p[0].lineno = p.lineno(1)

def p_statement_break(p):
    "statement : BREAK"
    p[0] = Node("Break")
    p[0].lineno = p.lineno(1)

def p_statement_block(p):
    "statement : BEGIN statementBlock END"
    p[0] = Node("Begin-End Block", [p[2]])

def p_error_block(p):
    "statement : BEGIN END"
    p[0] = Node("Error")
    p[0].lineno = p.lineno(1)
    sys.stderr.write(red+"Error line %d: empty Begin-End block\n" % p.lineno(1))

def p_ifthen(p):
    "ifthen : IF relation THEN statement %prec ELSE"
    p[0] = Node("If then", [p[2], p[4]])
    p[0].lineno = p.lineno(1)

def p_ifthenelse(p):
    "ifthenelse : IF relation THEN statement ELSE statement"
    p[0] = Node("If then else", [p[2], p[4], p[6]])
    p[0].lineno = p.lineno(1)

def p_error_ifthen(p):
    "ifthen : IF relation statement"
    p[0] = Node("Error")
    p[0].lineno = p.lineno(1)
    sys.stderr.write("Error line %d: 'Then' missing before statement\n" % p[2].lineno)

def p_error_ifthen(p):
    "ifthenelse : IF relation statement ELSE statement"
    p[0] = Node("Error")
    p[0].lineno = p.lineno(1)
    sys.stderr.write("Error line %d: 'Then' missing before statement\n" % p[2].lineno)

def p_functionCall(p):
    "functionCall : ID '(' paramslistop ')' %prec UMINUS"
    p[0] = Node("Function Call", [p[3]], leaf=p[1])
    p[0].lineno = p.lineno(1)

def p_paramsListOp1(p):
    "paramslistop : paramList"
    p[0] = p[1]

def p_paramsListOp2(p):
    "paramslistop : empty"
    p[0] = p[1]

def p_paramList1(p):
    "paramList : paramList ',' expression"
    p[1].append(p[3])
    p[0] = p[1]

def p_paramList2(p):
    "paramList : expression"
    p[0] = Node("Param List", [p[1]])
    p[0].lineno = p[1].lineno

def p_inOutExpr1(p):
    "inOutExpr : PRINT '(' STRING ')'"
    p[0] = Node("PRINT", leaf=p[3])
    p[0].lineno = p.lineno(1)

def p_inOutExpr2(p):
    "inOutExpr : WRITE '(' expression ')'"
    p[0] = Node("WRITE", [p[3]])
    p[0].lineno = p.lineno(1)

def p_inOutExpr3(p):
    "inOutExpr : READ '(' location ')'"
    p[0] = Node("READ", [p[3]])
    p[0].lineno = p.lineno(1)

def p_location1(p):
    "location : ID"
    p[0] = Node("ID", leaf=p[1])
    p[0].lineno = p.lineno(1)

def p_location2(p):
    "location : ID '[' expression ']'"
    p[0] = Node("Location", [p[3]], leaf=p[1])
    p[0].lineno = p.lineno(1)

def p_relationop1(p):
    "relation : relation OR relation"
    p[0] = Node("Binary Relation", [p[1], p[3]], p[2])
    p[0].lineno = p.lineno(2)

def p_relationop2(p):
    "relation : relation AND relation"
    p[0] = Node("Binary Relation", [p[1], p[3]], p[2])
    p[0].lineno = p.lineno(2)

def p_relationop3(p):
    "relation : NOT relation"
    p[0] = Node("Relation", [p[2]], p[1])
    p[0].lineno = p.lineno(1)

def p_relationop4(p):
    "relation : '(' relation ')'"
    p[0] = p[2]

def p_relation_LT(p):
    "relation : expression LT expression"
    p[0] = Node("Binary Relation", [p[1], p[3]], p[2])
    p[0].lineno = p.lineno(2)

def p_relation_LE(p):
    "relation : expression LE expression"
    p[0] = Node("Binary Relation", [p[1], p[3]], p[2])
    p[0].lineno = p.lineno(2)

def p_relation_GT(p):
    "relation : expression GT expression"
    p[0] = Node("Binary Relation", [p[1], p[3]], p[2])
    p[0].lineno = p.lineno(2)

def p_relation_GE(p):
    "relation : expression GE expression"
    p[0] = Node("Binary Relation", [p[1], p[3]], p[2])
    p[0].lineno = p.lineno(2)

def p_relation_NE(p):
    "relation : expression NE expression"
    p[0] = Node("Binary Relation", [p[1], p[3]], p[2])
    p[0].lineno = p.lineno(2)

def p_relation_equal(p):
    "relation : expression EQUAL expression"
    p[0] = Node("Binary Relation", [p[1], p[3]], p[2])
    p[0].lineno = p.lineno(2)

def p_relation_true(p):
    "relation : TRUE"
    p[0] = Node("True")
    p[0].lineno = p.lineno(1)

def p_relation_false(p):
    "relation : FALSE"
    p[0] = Node("False")
    p[0].lineno = p.lineno(1)

def p_expr_plus(p):
    "expression : expression '+' expression"
    p[0] = Node("Binary Operation", [p[1], p[3]], p[2])
    p[0].lineno = p.lineno(2)

def p_expr_minus(p):
    "expression : expression '-' expression"
    p[0] = Node("Binary Operation", [p[1], p[3]], p[2])
    p[0].lineno = p.lineno(2)

def p_expr_times(p):
    "expression : expression '*' expression"
    p[0] = Node("Binary Operation", [p[1], p[3]], p[2])
    p[0].lineno = p.lineno(2)

def p_expr_div(p):
    "expression : expression '/' expression"
    p[0] = Node("Binary Operation", [p[1], p[3]], p[2])
    p[0].lineno = p.lineno(2)

def p_expr_uminus(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = Node("UMINUS expr", [p[2]], p[1])
    p[0].lineno = p[2].lineno

def p_expr_uplus(p):
    "expression : '+' expression %prec UMINUS"
    p[0] = p[2]

def p_expr_parens(p):
    "expression : '(' expression ')'"
    p[0] = p[2]

def p_expr_id(p):
    "expression : ID"
    p[0] = Node("ID", leaf=p[1])
    p[0].lineno = p.lineno(1)

def p_expr_num(p):
    "expression : number"
    p[0] = p[1]

def p_expr_ubication(p):
    "expression : ID '[' expression ']'"
    p[0] = Node("ID[expr]", [p[3]], leaf=p[1])
    p[0].lineno = p.lineno(1)

def p_expr_casting(p):
    "expression : casting"
    p[0] = p[1]

def p_expr_funcall(p):
    "expression : functionCall"
    p[0] = p[1]

def p_casting_int(p):
    "casting : INT '(' expression ')'"
    p[0] = Node("Casting Int", [p[3]], leaf=int(p[3]))
    p[0].lineno = p.lineno(1)

def p_casting_float(p):
    "casting : FLOAT '(' expression ')'"
    p[0] = Node("Casting Float", [p[3]], leaf=float(p[3]))
    p[0].lineno = p.lineno(1)

def p_number_int(p):
    "number : INTEGER"
    p[0] = Node("Literal", leaf=p[1])
    p[0].lineno = p.lineno(1)
    p[0].datatype = Node("Type-Int")

def p_number_float(p):
    "number : FLOATNUM"
    p[0] = Node("Literal", leaf=p[1])
    p[0].lineno = p.lineno(1)
    p[0].datatype = Node("Type-Float")

def p_empty(p):
    "empty : "
    p[0] = Node("Empty")

def p_error(p):
    if p:
        sys.stderr.write (red+"Syntax error line %d:  %s -> %s\n" % (p.lineno, p.type , p.value ))

def make_parser():
    lexer = paslex.make_lexer()
    parser = yacc.yacc(debug=1)
    return parser

if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print green+"Usage: python %s <pascal_file>" % sys.argv[0]
    elif (re.match(r'.*\.pas', sys.argv[1])):
        try:
            file = open(sys.argv[-1])
            data = file.read()
            parser = make_parser()
            result = parser.parse(data)
            if not hasErrors:
                dump_tree(result)

        except IOError:
            print red+"Error: The file does not exist"
            print green+"Usage: python %s <pascal_file>" % sys.argv[0]
    else:
        print "Please put the name of your pascal file at the end of the command"

'''

notes:
fun : FUN ID
    | FUN // error
    // error con id's que no cumplam con nombres validos

esta mpaslex y mpasparser

finalmente solo ejecutar
mpas qsort.pas
resumen de la compilacion
1. mostrar errores dentro del programa
2. # errores: warning / fatal

opciones: -ast
          -lex


preguntas:

Quien debe tener data-type

Que hacer con los shift / reduce
'''
