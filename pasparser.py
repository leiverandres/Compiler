# coding: utf-8
import ply.yacc as yacc
from paslex import tokens

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
  pass

def p_fun_list(p):
  "funlist : funlist function"
  pass

def p_funList_function(p):
  "funlist : function"
  pass

def p_function(p):
  "function : FUN ID '(' arglist ')' localslist BEGIN statementBlock END"
  pass

def p_arglist(p):
  "arglist : args"
  pass

def p_arglist_empty(p):
  "arglist : empty"
  pass

def p_args(p):
  "args : args ',' var_decl"
  pass

def p_args_argument(p):
  "args : var_decl"
  pass

def p_var_decl(p):
  "var_decl : ID ':' type_specifier"
  pass

def p_type_specifier1(p):
  "type_specifier : type"
  pass

def p_type_specifier2(p):
  "type_specifier : FLOAT '[' INTEGER ']'"
  pass

def p_type_specifier3(p):
  "type_specifier : INT '[' INTEGER ']'"
  pass

def p_type_int(p):
  "type : INT"
  pass

def p_type_float(p):
  "type : FLOAT"
  pass

def p_localList_locals(p):
  "localslist : locals"
  pass

def p_localList_empty(p):
  "localslist : empty"
  pass

def p_locals(p):
  "locals : locals declaration_local ';'"
  pass

def p_locals_localDecl(p):
  "locals : declaration_local ';'"
  pass

def p_localDecl_varDecl(p):
  "declaration_local : var_decl"
  pass

def p_localDecl_fun(p):
  "declaration_local : function"
  pass

def p_statementBlock(p):
  "statementBlock : statementBlock ';' statement"
  pass

def p_statement(p):
  "statementBlock : statement"
  pass

def p_statement_while(p):
  "statement : WHILE relationop DO statement"
  pass

def p_statement_ifthen(p):
  "statement : ifthen"
  pass

def p_statement_ifThenElse(p):
  "statement : ifthenelse"


def p_statement_assign(p):
  "statement : location ASIGN expression"
  pass

def p_statement_inOutExpr(p):
  "statement : inOutExpr"
  pass

def p_statement_return(p):
  "statement : RETURN expression"
  pass

def p_statement_call(p):
  "statement : functionCall"
  pass

def p_statement_skip(p):
  "statement : SKIP"
  pass

def p_statement_break(p):
  "statement : BREAK"
  pass

def p_statement_block(p):
  "statement : BEGIN statementBlock END"
  pass

def p_ifthen(p):
  'ifthen : IF relationop THEN statement %prec ELSE'
  pass

def p_ifthenelse(p):
  'ifthenelse : IF relationop THEN statement ELSE statement'
  pass

def p_functionCall(p):
  "functionCall : ID '(' arglist ')'"
  pass

def p_relationop1(p):
  "relationop : relationop OR relationop"
  pass

def p_relationop2(p):
  "relationop : relationop AND relationop"
  pass

def p_relationop3(p):
  "relationop : NOT relationop"
  pass

def p_relationop4(p):
  "relationop : '(' relationop ')'"
  pass

def p_relationop5(p):
  "relationop : relation"
  pass

def p_relation_LT(p):
  "relation : expression LT expression"
  pass

def p_relation_LE(p):
  "relation : expression LE expression"
  pass

def p_relation_GT(p):
  "relation : expression GT expression"
  pass

def p_relation_GE(p):
  "relation : expression GE expression"
  pass

def p_relation_NE(p):
  "relation : expression NE expression"
  pass

def p_relation_equal(p):
  "relation : expression EQUAL expression"
  pass

def p_relation_true(p):
  "relation : TRUE"
  pass

def p_relation_false(p):
  "relation : FALSE"
  pass

def p_expr_plus(p):
  "expression : expression '+' expression"
  pass

def p_expr_minus(p):
  "expression : expression '-' expression"
  pass

def p_expr_times(p):
 "expression : expression '*' expression"
 pass

def p_expr_div(p):
  "expression : expression '/' expression"
  pass

def p_expr_uminus(p):
  "expression : '-' expression %prec UMINUS"
  pass

def p_expr_uplus(p):
  "expression : '+' expression"
  pass

def p_expr_parens(p):
  "expression : '(' expression ')'"
  pass

def p_expr_id(p):
  "expression : ID"
  pass

def p_expr_num(p):
  "expression : number"
  pass

def p_expr_id(p):
  "expression : ID"
  pass

def p_expr_ubication(p):
  "expression : ID '[' expression ']'"

def p_expr_casting(p):
  "expression : casting"
  pass

def p_expr_funcall(p):
  "expression : functionCall"
  pass

def p_num_int(p):
  "number : INTEGER"
  pass

def p_num_float(p):
  "number : FLOATNUM"

def p_location1(p):
  "location : ID"
  pass

def p_location2(p):
  "location : ID '[' INTEGER ']'"
  pass

def p_casting_int(p):
  "casting : INTEGER '(' expression ')'"
  pass

def p_casting_float(p):
  "casting : FLOAT '(' expression ')'"
  pass

def p_inOutExpr1(p):
  "inOutExpr : PRINT '(' STRING ')'"
  pass

def p_inOutExpr2(p):
  "inOutExpr : WRITE '(' expression ')'"
  pass

def p_inOutExpr3(p):
  "inOutExpr : READ '(' expression ')'"
  pass

def p_empty(p):
  "empty : "
  pass

def p_error(p):
  print("Error en la entrada!")

parser = yacc.yacc()

while True:
  try:
      s = raw_input('basic > ')
  except EOFError:
      break
  if not s: continue
  result = parser.parse(s)
  print(result)

'''
... refactor
? ask

program: fun_list

fun_list: fun_list fun
        | fun

fun: FUN ID LPAREN arglist RPAREN localslist BEGIN statementBlock END

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

statement: WHILE relationop DO statement ...
         |  IF relation THEN statement // ifthen ...
         |  IF relation THEN statement %prec ELSE statement // ifthenelse ...
         |  assigment
         |  inOutExpr
         |  RETURN expression
         |  functionCall
         |  SKIP
         |  BREAK
         |  BEGIN statementBlock END

functionCall: ID LPAREN arglist RPAREN

->
relationop: relationop OR relationop
          | relationop AND relationop
          | NOT relationop
          | LPAREN relationop RPAREN
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
       | ID LPAREN expression RPAREN
'''
