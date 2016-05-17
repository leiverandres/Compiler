# coding: utf-8
import ply.yacc as yacc
import ply.lex as lex
from paslex import tokens
from pasAST import *
from errors import *
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

def p_program(p):
    "program : funlist"
    p[0] = Program(p[1])

def p_error_program(p):
    "program : error"
    error(p.lineno(1), green+"Warning: File problem\n")

def p_fun_list(p):
    "funlist : funlist function"
    p[1].append(p[2])
    p[0] = p[1]
    p[0].lineno = p.lineno(2)

def p_funList_function(p):
    "funlist : function"
    p[0] = FunList([p[1]], lineno=p.lineno(1))

def p_function(p):
    "function : FUN ID '(' arglist ')' localslist beginEndBlock"
    p[0] = Function(p[2], p[4], p[6], p[7], lineno=p.lineno(2), type_argms=[])

def p_error_function0(p):
    "function : FUN ID '(' error ')' localslist beginEndBlock"
    error(p.lineno(2), "Error: something wrong with function parameters")

def p_error_function1(p):
    "function : FUN error '(' arglist ')' localslist beginEndBlock"
    error(p.lineno(1), red+"Error: Function indentifier missing\n");

def p_error_function2(p):
    "function : FUN ID '(' arglist ')' error beginEndBlock"
    error(p.lineno(2), "Error: something wrong with function locals")

def p_beginEndBlock(p):
    "beginEndBlock : BEGIN statementBlock END"
    p[0] = p[2]

def p_error_block1(p):
    "beginEndBlock : BEGIN statementBlock ';' END"
    p[0] = p[2]
    error(p.lineno(3), red+"Warning: bad ';' after last statement of BEGIN-END block\n")

def p_error_block2(p):
    "beginEndBlock : BEGIN END"
    error(p.lineno(1), red+"Error: empty Begin-End block")

def p_error_beginEndBlock2(p):
    "beginEndBlock : BEGIN error END"
    error(p.lineno(1), "Error: something wrong with function statements")

def p_arglist(p):
    "arglist : args"
    p[0] = p[1]

def p_arglist_empty(p):
    "arglist : empty"
    p[0] = ArgList([p[1]], lineno=p.lineno(1))

def p_error_arglist(p):
    "arglist : args ','"
    p[0] = p[1]
    error(p.lineno(1), red+"Warning: Bad ',' after parameter")

def p_args_argument(p):
    "args : var_decl"
    p[0] = ArgList([p[1]], lineno=p[1].lineno)

def p_args(p):
    "args : args ',' var_decl"
    p[1].append(p[3])
    p[0] = p[1]

def p_error_args(p):
    "args : args var_decl"
    p[1].append(p[2])
    p[0] = p[1]
    error(p.lineno(2), red+"Error: ',' missing before parameter\n")

def p_localList_locals(p):
    "localslist : locals"
    p[0] = p[1]

def p_localList_empty(p):
    "localslist : empty"
    p[0] = LocalsList([p[1]], lineno=p.lineno(1))

def p_locals(p):
    "locals : locals var_or_fun"
    p[1].append(p[2])
    p[0] = p[1]

def p_var_or_fun_decl(p):
    '''
    var_or_fun : var_decl ';'
               | function ';'
    '''
    p[0] = p[1]

def p_locals_var2(p):
    "locals : var_decl ';'"
    p[0] = LocalsList([p[1]], lineno=p[1].lineno)

def p_locals_fun2(p):
    "locals : function ';'"
    p[0] = LocalsList([p[1]])
    p[0].lineno = p[1].lineno

def p_error_locals1(p):
    "locals : var_decl"
    p[0] = LocalsList([p[1]], lineno=p[1].lineno)
    error(p[1].lineno, red+"Error: ';' missing after local declaration")

def p_error_locals2(p):
    "var_or_fun : var_decl error"
    p[0] = p[1]
    error(p[1].lineno, red+"Error: ';' missing after local declaration")

def p_error_locals3(p):
    "locals : function"
    p[0] = Node("Error")
    p[0].lineno = p[1].lineno
    error(p[1].lineno, red+"Error: ';' missing after local function")

def p_error_locals4(p):
    "var_or_fun : function error"
    p[0] = p[1]
    error(p.lineno(2), red+"Error: ';' missing after local function")

def p_var_decl(p):
    "var_decl : ID ':' type_specifier"
    p[0] = VarDeclaration(p[1], p[3], lineno=p.lineno(1))

def p_error_var_decl(p):
    '''
    var_decl : ID type_specifier
             | ID ASIGN type_specifier
    '''
    p[0] = VarDeclaration(p[1], p[3], lineno=p.lineno(1))
    error(p.lineno(1), red+"Error: bad Assigment. ':' missing")

def p_type_specifier1(p):
    "type_specifier : simple_type"
    p[0] = p[1]

def p_type_specifier2(p):
    "type_specifier : simple_type '[' INTEGER ']'"
    p[0] = Vector(p[1], p[3], lineno=p[1].lineno, size=p[3])

def p_type_int(p):
    "simple_type : INT"
    p[0] = Type("int", lineno=p.lineno(1))

def p_type_float(p):
    "simple_type : FLOAT"
    p[0] = Type("float", lineno=p.lineno(1))

def p_statementBlock(p):
    "statementBlock : statementBlock ';' statement"
    p[1].append(p[3])
    p[0] = p[1]

def p_statement(p):
    "statementBlock : statement"
    p[0] = Statements([p[1]])

def p_error_comma_stm(p):
    "statementBlock : statementBlock statement"
    p[1].append(p[2])
    p[0] = p[1]
    error(p[2].lineno, red+"Error: ';' expected before statement")

def p_statement_while(p):
    "statement : WHILE relation DO statement"
    p[0] = WhileStatement(p[2], p[4], lineno=p.lineno(1))

def p_statement_ifthen(p):
    "statement : ifthen"
    p[0] = p[1]

def p_statement_ifThenElse(p):
    "statement : ifthenelse"
    p[0] = p[1]

def p_statement_assign(p):
    "statement : location ASIGN expression"
    p[0] = AssignmentStatement(p[1], p[3], lineno=p.lineno(2))

def p_statement_inOutExpr(p):
    "statement : inOutExpr"
    p[0] = p[1]

def p_statement_return(p):
    "statement : RETURN '(' expression ')'"
    p[0] = Return(p[3], lineno=p.lineno(1))

def p_statement_return2(p):
    "statement : RETURN '(' empty ')'"
    p[0] = Return(p[3], lineno=p.lineno(1))

def p_error_return1(p):
    'statement : RETURN error'
    error(p.lineno(1), "Error: return expression should be between parenthesis")

def p_statement_call(p):
    "statement : functionCall"
    p[0] = p[1]

def p_statement_skip(p):
    "statement : SKIP"
    p[0] = Skip(lineno=p.lineno(1))

def p_statement_break(p):
    "statement : BREAK"
    p[0] = Break(lineno=p.lineno(1))

def p_statement_block(p):
    "statement : beginEndBlock"
    p[0] = p[1]

def p_ifthen(p):
    "ifthen : IF relation THEN statement %prec ELSE"
    p[0] = IfStatement(p[2], p[4], None, lineno=p.lineno(1))

def p_ifthenelse(p):
    "ifthenelse : IF relation THEN statement ELSE statement"
    p[0] = IfStatement(p[2], p[4], p[6], lineno=p.lineno(1))

def p_error_ifthen(p):
    "ifthen : IF relation statement"
    p[0] = IfStatement(p[2], p[3], None, lineno=p.lineno(1))
    error(p[2].lineno, red+"Warning: 'Then' missing before statement")

def p_error_ifthen2(p):
    "ifthenelse : IF relation error statement ELSE statement"
    p[0] = IfStatement(p[2], p[4], p[6], lineno=p.lineno(1))
    error(p[2].lineno, red+"Warning: 'Then' missing before statement")

def p_functionCall(p):
    "functionCall : ID '(' paramslistop ')' %prec UMINUS"
    p[0] = FunCall(p[1], p[3], lineno=p.lineno(1), datatype=None)

def p_paramsListOp1(p):
    "paramslistop : paramList"
    p[0] = p[1]

def p_paramsListOp2(p):
    "paramslistop : empty"
    p[0] = ExprList([p[1]])

def p_paramList1(p):
    "paramList : paramList ',' expression"
    p[1].append(p[3])
    p[0] = p[1]

def p_paramList2(p):
    "paramList : expression"
    p[0] = ExprList([p[1]])

def p_inOutExpr1(p):
    "inOutExpr : PRINT '(' STRING ')'"
    p[0] = Print(p[3], lineno=p.lineno(1))

def p_inOutExpr2(p):
    "inOutExpr : WRITE '(' expression ')'"
    p[0] = Write(p[3], lineno=p.lineno(1))

def p_inOutExpr3(p):
    "inOutExpr : READ '(' location ')'"
    p[0] = Read(p[3], lineno=p.lineno(1))

def p_location1(p):
    "location : ID"
    p[0] = LocationId(p[1], lineno=p.lineno(1), _leaf=True)

def p_location2(p):
    "location : ID '[' expression ']'"
    p[0] = LocationVectorAsign(p[1], p[3], lineno=p.lineno(1))

def p_relationop1(p):
    "relation : relation OR relation"
    p[0] = RelationalOp(p[2], p[1], p[3], lineno=p.lineno(2))

def p_relationop2(p):
    "relation : relation AND relation"
    p[0] = RelationalOp(p[2], p[1], p[3], lineno=p.lineno(2))

def p_relationop3(p):
    "relation : NOT relation"
    p[0] = UnaryOp(p[1], p[2], lineno=p.lineno(1))

def p_relationop4(p):
    "relation : '(' relation ')'"
    p[0] = p[2]

def p_relation_LT(p):
    "relation : expression LT expression"
    p[0] = RelationalOp('<', p[1], p[3], lineno=p.lineno(2))

def p_relation_LE(p):
    "relation : expression LE expression"
    p[0] = RelationalOp('<=', p[1], p[3], lineno=p.lineno(2))

def p_relation_GT(p):
    "relation : expression GT expression"
    p[0] = RelationalOp('>', p[1], p[3], lineno=p.lineno(2))

def p_relation_GE(p):
    "relation : expression GE expression"
    p[0] = RelationalOp('>=', p[1], p[3], lineno=p.lineno(2))

def p_relation_NE(p):
    "relation : expression NE expression"
    p[0] = RelationalOp('!=', p[1], p[3], lineno=p.lineno(2))

def p_relation_equal(p):
    "relation : expression EQUAL expression"
    p[0] = RelationalOp('==', p[1], p[3], lineno=p.lineno(2))

def p_expr_plus(p):
    "expression : expression '+' expression"
    p[0] = BinaryOp(p[2], p[1], p[3], lineno=p.lineno(2))

def p_expr_minus(p):
    "expression : expression '-' expression"
    p[0] = BinaryOp(p[2], p[1], p[3], lineno=p.lineno(2))

def p_expr_times(p):
    "expression : expression '*' expression"
    p[0] = BinaryOp(p[2], p[1], p[3], lineno=p.lineno(2))

def p_expr_div(p):
    "expression : expression '/' expression"
    p[0] = BinaryOp(p[2], p[1], p[3], lineno=p.lineno(2))

def p_expr_uminus(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = UnaryOp(p[1], p[2], lineno=p[2].lineno)

def p_expr_uplus(p):
    "expression : '+' expression %prec UMINUS"
    p[0] = p[2]

def p_expr_parens(p):
    "expression : '(' expression ')'"
    p[0] = p[2]

def p_expr_id(p):
    "expression : ID"
    p[0] = LocationId(p[1], lineno=p.lineno(1), _leaf=True)

def p_expr_num(p):
    "expression : number"
    p[0] = p[1]

def p_expr_ubication(p):
    "expression : ID '[' expression ']'"
    p[0] = LocationVector(p[1], p[3], lineno=p.lineno(1))

def p_expr_casting(p):
    "expression : casting"
    p[0] = p[1]

def p_expr_funcall(p):
    "expression : functionCall"
    p[0] = p[1]

def p_casting_int(p):
    "casting : INT '(' expression ')'"
    p[0] = Casting('int', p[3], lineno=p.lineno(1))

def p_casting_float(p):
    "casting : FLOAT '(' expression ')'"
    p[0] = Casting('float', p[3], lineno=p.lineno(1))

def p_number_int(p):
    "number : INTEGER"
    p[0] = Literal(p[1], lineno=p.lineno(1), typename='int', _leaf=True)

def p_number_float(p):
    "number : FLOATNUM"
    p[0] = Literal(p[1], lineno=p.lineno(1), typename='float', _leaf=True)

def p_empty(p):
    "empty : "
    p[0] = Empty()

def p_error(p):
    if p:
        print " i'm in error rule with", p.type
        error(p.lineno, red+"Syntax error before:  %s -> %s\n" % (p.type , p.value ))
        # raise parseError()


def make_parser():
    lexer = paslex.make_lexer()
    parser = yacc.yacc(debug=1)
    return parser

class parseError(Exception):
    # def __init__(self, value):
    #     self.value = value
    # def __str__(self):
    #         return repr(self.value)
    pass

if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print green+"Usage: python %s <pascal_file>" % sys.argv[0]
    elif (re.match(r'.*\.pas', sys.argv[1])):
        try:
            file = open(sys.argv[-1])
            data = file.read()
            parser = pasparser.make_parser()
            with subscribe_errors(lambda msg: sys.stdout.write(msg+"\n")):
                result = parser.parse(data)
            if errors_reported() == 0:
                dump_class_tree(result)

        except IOError:
            print red+"Error: The file does not exist"
            print green+"Usage: python %s <pascal_file>" % sys.argv[0]
    else:
        print "Please put the name of your pascal file at the end of the command"

'''
NOTAS:

2. # errores: warning / fatal
Preguntas:
Como asignar el datatype, un string o una instancia de type----
'''
