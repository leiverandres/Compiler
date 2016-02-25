import ply.lex as lex

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
  'EQUALs',
  'INTEGER',
  'FLOAT',
  'CONST',
  'MINUS',
  'PLUS',
  'TIMES',
  'DIVIDE',
  'STRING',
  'NEWLINE',
  'LPAREN', # '('
  'RPAREN', # ')'
  'LSQUARE', # left square bracket '['
  'RSQUARE', # right square brecket ']'
  'LT',
  'LE',
  'GT',
  'GE',
  'NE',
  'COMMA',
  'SEMI',
  'COLM'
] + list(reserved.values())

# completely ignored characters
t_ignore = ' \t'

def t_NEWLINE(t):
  r'\n+'
  t.lexer.lineno += t.value.count("\n")

def t_ID():
  pass

# Discarded tokens
def t_COMMENT(t):
  r'\/\*(.|\n)*\*\/'
  pass

def t_error(t):
  print("Illegal character %s foo %d" % repr(t.value[0]))
  t.lexer.skip(1)
