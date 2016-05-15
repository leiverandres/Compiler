```python
'''
program: funlist

funlist: funlist function
        | function

function: FUN ID '(' arglist ')' localslist BEGIN statementBlock END

arglist: args
       | empty

args: args ',' var_decl
    | var_decl

localsList: locals
          | empty

locals: locals declaration_local ';'
      | declaration_local ';'

declaration_local: var_decl
        | function

var_decl: ID ':' type_specifier

type_specifier: simple_type
              | simple_type '[' INTEGER ']' ... expr? // error

simple_type: INT
           | FLOAT

type: INT
    | FLOAT

statementBlock : statementBlock ';' statement
          | statement

statement: WHILE relation DO statement
         |  IF relation THEN statement // ifthen
         |  IF relation THEN statement %prec ELSE statement // ifthenelse
         |  location ASIGN expression
         |  inOutExpr
         |  RETURN expression
         |  functionCall
         |  SKIP
         |  BREAK
         |  BEGIN statementBlock END

functionCall: ID '(' paramslistop ')'

paramslistop: paramList
            | empty

paramList: paramList ',' expression
         | expression

relation: relation OR relation
        | relation AND relation
        | NOT relation
        | '(' relation ')'
        | ID
        | ID '[' expression ']' //errors: type errors
        | expression LT expression
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
          | '(' expression ')'
          | ID // location
          | ID '[' expression ']'
          | number
          | ID LPAREN expression RPAREN
          | casting
          | functionCall

inOutExpr: PRINT LPAREN STRING RPAREN
         | WRITE LPAREN expression RPAREN
         | READ LPAREN location RPAREN

casting: FLOAT '(' expression ')'
       | INT '(' expression ')'

number: INTEGER
      | FLOATNUM
'''
```
