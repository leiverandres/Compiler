import ply.lex as lex
from errors import error
import re

reserved = {
    'fun' : 'FUN',
    'int': 'INT',
    'float': 'FLOAT',
    'while': 'WHILE',
    'do': 'DO',
    'begin': 'BEGIN',
    'end': 'END',
    'if': 'IF',
    'else': 'ELSE',
    'then': 'THEN',
    'write': 'WRITE',
    'read': 'READ',
    'print': 'PRINT',
    'return': 'RETURN',
    'skip': 'SKIP',
    'break': 'BREAK',
    'and': 'AND',
    'or': 'OR',
    'not': 'NOT'
}

tokens = [
    'ID',
    'ASIGN',
    'EQUAL',
    'INTEGER',
    'FLOATNUM',
    'STRING',
    'NEWLINE',
    'LT', # less than
    'LE', # less and equal than
    'GT', # greater than
    'GE', # greater and equal than
    'NE', # not-equal
] + list(reserved.values())

literals = '+-*/,;:()[]'
'''
  literals are useful to define simplier grammars like

  expression : expression '+' term

  instead

  expression : expression PLUS term
'''

t_ASIGN = r':='
t_EQUAL = r'=='
t_STRING = r'\".*?\"'
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_NE = r'!='

def t_ID(t):
    r'[a-zA-Z_][\w]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_FLOATNUM(t):
    r'([1-9]\d*|0)(\.\d+(e[+-]?\d+)?|e[+-]?\d+)'
    try:
        t.value = float(t.value)
    except:
        print ("Line %d: Error with number %s " % (t.lineno, t.value))
    return t

def t_INTEGER(t):
    r'([1-9]\d*|0)'
    try:
        t.value = int(t.value)
    except:
        print ("Line %d: Number is %s too large for a INTEGER" % (t.lineno, t.value))
        t.value = 0
    return t

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

# completely ignored characters
t_ignore = ' \t'

# Discarded tokens
def t_COMMENT(t):
    r'\/\*(.|\n)*\*\/'
    t.lexer.lineno += t.value.count('\n') # just take lines

def find_colum(input, token):
    last_cr = input.rfind('\n', 0, token.lexpos) # pos last \n before token we want to find
    if last_cr < 0:
        last_ct = 0
    column = (token.lexpos - last_cr) + 1
    return column

def t_error(t):
    error(t.lineno, "Illegal character %s" % (repr(t.value[0])))
    # print("Illegal character %s line: %d col: %d" % (repr(t.value[0]), t.lineno, find_colum(lexer.lexdata, t)))
    t.lexer.skip(1)

def make_lexer():
    lexer = lex.lex(debug=0)
    return lexer

def run_lexer(data):
    import sys
    from errors import subscribe_errors
    lexer = make_lexer()
    with subscribe_errors(lambda msg: sys.stderr.write(msg+"\n")):
        lexer.input(data)
        for tok in iter(lexer.token, None):
            if tok:
                print(tok)


if __name__ == '__main__':
    import sys
    if (len(sys.argv) == 2):
        data = open(sys.argv[1]).read()
        run_lexer(data)
    else:
        print ("Usage: python %s <file.pas>" % sys.argv[0])
