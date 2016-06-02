# types.py
# -*- coding: utf-8 -*-
'''
Sistema de Tipos de MPascal
===========================
Este archivo define las clases de representaci�n de tipos.  Esta es una
clase general usada para representar todos los tipos.  Cada tipo es entonces
una instancia singleton de la clase tipo.

class MpasType(object):
    pass

int_type = MpasType("int",...)
float_type = MpasType("float",...)
string_type = MpasType("string", ...)

El contendo de la clase tipo es enteramente suya.  Sin embargo, ser�
m�nimamente necesario el codificar cierta informaci�n sobre:

   a.  Que operaciones son soportadas (+, -, *, etc.).
   b.  Valores por defecto
   c.  ????
   d.  Beneficio!

Una vez que se haya definido los tipos incorporado, se deber� segurar que
sean registrados en la tabla de s�mbolos o c�digo que compruebe los nombres
de tipo en 'mpascheck.py'.
'''

class MpasType(object):
    '''
    Clase que representa un tipo en el lemguaje mpascal.  Los tipos
    son declarados como instancias singleton de este tipo.
    '''
    def __init__(self, name, bin_ops=set(), un_ops=set()):
        '''
        Debera ser implementada por usted y averiguar que almacenar
        '''
        self.name = name
        self.bin_ops = bin_ops
        self.un_ops = un_ops


# Crear instancias especificas de los tipos.  Usted tendr� que adicionar
# los argumentos apropiados dependiendo de su definici�n de MpasType
# int_type = MpasType("int",
# 	set(('PLUS', 'MINUS', 'TIMES', 'DIVIDE',
# 	     'LE', 'LT', 'EQ', 'NE', 'GT', 'GE')),
# 	set(('PLUS', 'MINUS')),
# 	)

int_type = MpasType("int",
    set(('+', '-', '*', '/','<=', '<', '==', '!=', '>', '>=')),
    set(('+', '-')),
    )
float_type = MpasType("float",
    set(('+', '-', '*', '/', '<=', '<', '==', '!=', '>', '>=')),
    set(('+', '-')),
    )
string_type = MpasType("string",
    set(('+',)),
    set(),
    )
boolean_type = MpasType("bool",
    set(('and', 'or', '==', '!=')),
    set(('not',))
    )
