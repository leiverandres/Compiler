# coding: utf-8

import ply.yacc as yacc
from paslex import tokens

precedence = (
  ('left', 'OR'),
  ('left', 'AND'),
  ('left', 'NOT'),
  ('left', 'PLUS', 'MINUS'),
  ('left', 'TIMES', 'DIVIDE'),
  ('right', 'UMINUS')
)

def p_program(p):
  "program: funlist"
  pass

def p_fun_list(p):
  "funlist: funlist function"
  pass

def p_funList_function(p):
  "funlist: function"
  pass

def p_function(p):
  "function: FUN ID '(' arglist ')' locals BEGIN statementBlock END"

def p_arglist(p):
  "arglist: arglist ',' argument"
  pass

def p_arglist_argument(p):
  "arglist: argument"
  pass

def p_arglist_empty(p):
  "arglist: empty"
  pass

def p_empty(p):
  "empty :"
  pass;

'''
... refactor
? ask

program: fun_list

fun_list: fun_list fun
        | fun

fun: FUN ID LPAREN arglist RPAREN localsList BEGIN statementBlock END

arglist: arglist COMMA argument
       | argument
       | empty

->
argument: ID ':' type_specifier

declaration: ID ':' type_specifier

type_specifier: INT LSQUARE INTEGER RSQUARE
              | FLOAT LSQUARE INTEGER RSQUARE
              | type

type: INT
    | FLOAT

localsList: declaration_local ';'
          | localsList declaration_local ';'
          | empty

declaration_local: declaration
        | fun

statementBlock : statement_list ';' statement
          | statement
          | ¿ empty ?

statement: WHILE relationop DO statement
         |  IF relation THEN statement // if then ...
         |  IF relation THEN statement ELSE statement // if then else ...
         |  assigment
         |  inOutExpr
         |  RETURN expression
         |  name ( exprlist )
         |  SKIP
         |  BREAK
         |  BEGIN ¿ statements/statementBlock ? END

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

expression: expression '+' expression
          | expression '-' expression
          | expression '*' expression
          | expression '/' expression
          | '-' expression
          | '+' expression
          | LPAREN expression RPAREN
          | ID
          | number
          | INT LPAREN expression RPAREN // casting
          | FLOAT LPAren expression RPAREN
          | ID LSQUARE expression RSQUARE
          | ID LPAREN arglist RPAREN // function call

number: INTEGER
      | FLOATNUM

assigment : location ASIGN expression

location: ID
        | ID LSQUARE INTEGER RSQUARE //errors: index must be int, type errors

inOutExpr: PRINT LPAREN STRING RPAREN
         | WRITE LPAREN expression RPAREN
         | READ LPAREN location RPAREN
'''
