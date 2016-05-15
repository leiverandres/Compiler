# mpascheck.py
# -*- coding: utf-8 -*-
'''
Proyecto 3 : Chequeo del Programa
=================================
En este proyecto es necesario realizar comprobaciones semánticas en su programa.
Hay algunos aspectos diferentes para hacer esto.

En primer lugar, tendrá que definir una tabla de símbolos que haga un seguimiento
de declaraciones de identificadores previamente declarados.  Se consultará la
tabla de símbolos siempre que el compilador necesite buscar información sobre
variables y declaración de constantes.

A continuación, tendrá que definir los objetos que representen los diferentes
tipos de datos incorporados y registrar información acerca de sus capacidades.
Revise el archivo types.py.

Por último, tendrá que escribir código que camine por el AST y haga cumplir un
conjunto de reglas semánticas.  Aquí está una lista completa de todo los que
deberá comprobar:

1.  Nombres y símbolos:

Todos los identificadores deben ser definidos antes de ser usados.  Esto incluye variables,
constantes y nombres de tipo.  Por ejemplo, esta clase de código genera un error:

a = 3;              // Error. 'a' no está definido.
var a int;

Nota: los nombres de tipo como "int", "float" y "string" son nombres incorporados que
deben ser definidos al comienzo de un programa (función).

2.  Tipos de constantes

A todos los símbolos constantes se le debe asignar un tipo como "int", "float" o "string".
Por ejemplo:

const a = 42;         // Tipo "int"
const b = 4.2;        // Tipo "float"
const c = "forty";    // Tipo "string"

Para hacer esta asignación, revise el tipo de Python del valor constante y adjunte el
nombre de tipo apropiado.

3.  Chequeo de tipo operación binaria.

Operaciones binarias solamente operan sobre operandos del mismo tipo y produce un
resultado del mismo tipo.  De lo contrario, se tiene un error de tipo.  Por ejemplo:

var a int = 2;
var b float = 3.14;

var c int = a + 3;    // OK
var d int = a + b;    // Error.  int + float
var e int = b + 4.5;  // Error.  int = float

4.  Chequeo de tipo operador unario.

Operadores unarios retornan un resultado que es del mismo tipo del operando.

5.  Operadores soportados

Estos son los operadores soportados por cada tipo:

int:      binario { +, -, *, /}, unario { +, -}
float:    binario { +, -, *, /}, unario { +, -}
string:   binario { + }, unario { }

Los intentos de usar operadores no soportados debería dar lugar a un error.
Por ejemplo:

var string a = "Hello" + "World";     // OK
var string b = "Hello" * "World";     // Error (op * no soportado)

6.  Asignación.

Los lados izquierdo y derecho de una operación de asignación deben ser
declarados del mismo tipo.

Los valores sólo se pueden asignar a las declaraciones de variables, no
a constantes.

Para recorrer el AST, use la clase NodeVisitor definida en pasAST.py.
Un caparazón de código se proporciona a continuación.
'''

import sys, re, string
# from types import *
from errors import error
from pasAST import *
import paslex
import pasAST

class MpasType(object):
	'''
	Clase que representa un tipo en el lemguaje mpascal.  Los tipos
	son declarados como instancias singleton de este tipo.
	'''
	def __init__(self, name, bin_ops=set(), un_ops=set()):
		'''
		Deber� ser implementada por usted y averiguar que almacenar
		'''
		self.name = name
		self.bin_ops = bin_ops
		self.un_ops = un_ops

int_type = MpasType("int",
    set(('+', '-', '*', '/',
         '<=', '<', '==', '!=', '>', '>=')),
    set(('+', '-')),
    )
float_type = MpasType("float",
    set(('+', '-', '*', '/',
         '<=', '<', '==', '!=', '>', '>=')),
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

class SymbolTable(object):
    '''
    Clase que representa una tabla de símbolos.  Debe proporcionar funcionabilidad
    para agregar y buscar nodos asociados con identificadores.
    '''

    class SymbolDefinedError(Exception):
        '''
        Exception disparada cuando el codigo trara de agregar un simbol
        a la tabla de simbolos, y este ya esta definido
        '''
        error(None, "")
        pass

    class SymbolConflictError(Exception):
        '''
        '''
        pass

    def __init__(self, parent=None):
        '''
        Crea una tabla de simbolos vacia con la tabla padre dada
        '''
        self.symtab = {}
        self.parent = parent
        if self.parent != None:
            self.parent.children.append(self)
        self.children = []

    def add(self, a, v):
        '''
        Agrega un simbol con el valor dado a la tabla de simbolos

        func foo(x:int, y:int)
        x:float;
        v is a vector?
        '''
        if self.symtab.has_key(a):
            if type(self.symtab[a]) != type(v):
                raise SymbolTable.SymbolConflictError()
            else:
                raise SymbolTable.SymbolDefinedError()
        self.symtab[a] = v

    def lookup(self, a):
        if self.symtab.has_key(a):
            return self.symtab[a]
        else:
            if self.parent != None:
                return self.parent.lookup(a)
            else:
                return None

    #just for function tables
    def update_datatype(self, a, value):
        if self.symtab.has_key(a):
            self.symtab[a]['datatype'] = value
        else:
            if self.parent != None:
                self.parent.update_datatype(a, value)

class CheckProgramVisitor(NodeVisitor):
    '''
    Clase de Revisión de programa.  Esta clase usa el patrón cisitor como está
    descrito en pasAST.py.  Es necesario definir métodos de la forma visit_NodeName()
    para cada tipo de nodo del AST que se desee procesar.

    Nota: Usted tendrá que ajustar los nombres de los nodos del AST si ha elegido
    nombres diferentes.
    '''


    def __init__(self):
        '''
        Inicializa la tabla de simbolos
        '''
        self.global_symtab = SymbolTable()
        self.local_symtab = None
        self.current_function = None
        self.has_return = False
        self.in_while = False
        # Agrega nombre de tipos incorporados ((int, float, string) a la tabla de simbolos
        self.symtab_add('int', int_type)
        self.symtab_add('float', float_type)
        self.symtab_add('string', string_type)
        self.symtab_add('bool', boolean_type)

    def symtab_add(self, name, values):
        if self.local_symtab:
            self.local_symtab.add(name, values)
        else:
            self.global_symtab.add(name, values)

    def symtab_lookup(self, name):
        result = None
        if self.local_symtab:
            result = self.local_symtab.lookup(name)
        else:
            result = self.global_symtab.lookup(name)
        return result

    def update_datatype(self, name, new_value):
        if self.local_symtab:
            self.local_symtab.update_datatype(name, new_value)
        else:
            self.global_symtab.update_datatype(name, new_value)

    def push_symtab(self, node):
        self.local_symtab = SymbolTable(self.local_symtab)
        node.symtab = self.local_symtab

    def pop_symbol(self):
        self.local_symtab = self.local_symtab.parent

    def find_fun_type(self, function):
        queue = []
        for item in function.statements.statements:
            queue.append(item)
        while queue:
            cur = queue.pop(0)
            if isinstance(cur, pasAST.Return):
                self.visit(cur.value)
                return cur.value.datatype
            for i in xrange(0, len(cur._fields)):
                att = getattr(cur, cur._fields[i])
                if isinstance(att, pasAST.AST):
                    queue.append(att)

    def visit_Program(self, node):
        self.local_symtab = self.global_symtab
        # self.push_symtab(node)
        # self.symtab_add()
        # 1. Visita todas las funciones
        # 2. Registra la tabla de simbolos asociada
        self.visit(node.funList)
        if not self.symtab_lookup('main'):
            error(0, "main function missing")
        # print "\nGlobal", self.global_symtab.symtab

    def visit_Function(self, node):
        # Asegurarse que tenga return
        self.has_return = False
        if self.symtab_lookup(node.id):
            error(node.lineno, "Function %s already defined" % node.id)
        else:
            v = {
                'datatype': None,
                'lineno' : node.lineno,
                'cant_argms' : len(node.arglist.arguments),
                'type_argms' : [],
                'fun_instance' : node
            }
            self.symtab_add(node.id, v)
            self.push_symtab(node)

            self.current_function = node

            if self.current_function.id == 'main':
                if not isinstance(node.arglist.arguments[0], pasAST.Empty):
                    error(node.lineno, "Function 'main' should not have arguments")
                else:
                    self.local_symtab.parent.symtab[node.id]['cant_argms'] = 0
            else:
                node.type_argms = self.visit(node.arglist)
            self.local_symtab.parent.symtab[node.id]['type_argms'] = node.type_argms

            self.visit(node.localslist)
            self.visit(node.statements)

            if not self.has_return:
                error(node.lineno, "Return was not found. Function mush have return.")

            node.symtab = self.local_symtab.symtab

            self.pop_symbol()
            self.local_symtab.symtab[node.id]['table'] = node.symtab
            # print self.local_symtab.symtab, '\n'

    def visit_ArgList(self, node):
        type_argms = []
        # print "Arguments", node.arguments
        for arg in node.arguments:
            self.visit(arg)
            type_argms.append(arg.datatype)
        return type_argms

    def visit_LocalsList(self, node):
        for local in node.locals:
            if isinstance(local, Function):
                old_function = self.current_function
                self.visit(local)
                self.current_function = old_function
            else:
                self.visit(local)

    def visit_Statements(self, node):
        for stm in node.statements:
            self.visit(stm)

    def visit_VarDeclaration(self,node):
        # 1. Revise que el nombre de la variable no se ha definido
        if self.symtab_lookup(node.id):
            self.visit(node.type)
            node.datatype = node.type.datatype
            error(node.lineno, "Variable %s already defined" % node.id)
        # 2. Agrege la entrada a la tabla de símbolos
        else:
            current = self.local_symtab.symtab
            self.symtab_add(node.id, {'datatype': None})
            self.visit(node.type)
            if isinstance(node.type, Type):
                #simple type
                current[node.id]['varClass'] = 'simple_var'
            else:
                # Vector
                current[node.id]['varClass'] = 'vector'
                current[node.id]['size'] = node.type.size

            node.datatype = node.type.datatype
            current[node.id]['datatype'] = node.datatype
            current[node.id]['lineno'] = node.lineno

    # simple type
    def visit_Type(self, node):
        node.datatype = self.global_symtab.symtab[node.name]

    # vector type
    def visit_Vector(self, node):
        self.visit(node.type)
        node.datatype = node.type.datatype

    def visit_WhileStatement(self, node):
        self.in_while = True
        self.visit(node.condition)
        if not node.condition.datatype == boolean_type:
            error(node.lineno, "Wrong Type for While condition")
        else:
            self.visit(node.body)
        self.in_while = False

    def visit_UnaryOp(self, node):
        # 1. Asegúrese que la operación es compatible con el tipo
        # 2. Ajuste el tipo resultante al mismo del operando
        self.visit(node.right)
        if not node.op in node.right.datatype.un_ops:
            error(node.lineno, "Operación no soportada con este tipo")
        node.datatype = node.right.datatype

    def visit_RelationalOp(self, node):
        self.visit(node.left)
        self.visit(node.right)
        if not node.left.datatype == node.right.datatype:
            error(node.lineno, "Operandos de relación no son del mismo tipo")
        elif not node.op in node.left.datatype.bin_ops:
            error(node.lineno, "Operación no soportada con este tipo")
        elif not node.op in node.right.datatype.bin_ops:
            error(node.lineno, "Operación no soportada con este tipo")
        node.datatype = self.symtab_lookup('bool')

    def visit_BinaryOp(self, node):
        # 1. Asegúrese que los operandos left y right tienen el mismo tipo
        # 2. Asegúrese que la operación está soportada
        # 3. Asigne el tipo resultante
        self.visit(node.left)
        self.visit(node.right)
        if not node.left.datatype == node.right.datatype:
            error(node.lineno, "Operandos de operacionn no son del mismo tipo")
        elif not node.op in node.left.datatype.bin_ops:
            error(node.lineno, "Operación no soportada con este tipo")
        elif not node.op in node.right.datatype.bin_ops:
            error(node.lineno, "Operación no soportada con este tipo")
        node.datatype = node.left.datatype

    def visit_IfStatement(self, node):
        self.visit(node.condition)
        if not node.condition.datatype == boolean_type:
            error(node.lineno, "Tipo incorrecto para condición if")
        else:
            self.visit(node.then_b)
            if node.else_b:
                self.visit(node.else_b)

    def visit_AssignmentStatement(self,node):
        # 1. Asegúrese que la localización de la asignación está definida
        self.visit(node.location)
        sym = self.symtab_lookup(node.location.id)
        if not sym:
            error(node.lineno, "Asignado a un symbol desconocido")
        # 2. Revise que los tipos coincidan.
        else:
            self.visit(node.value)
            if node.location.datatype == node.value.datatype:
                node.datatype = sym['datatype']
            else:
                error(node.lineno, "expression cannot be assigned to a %s variable" \
                      % (sym['datatype'].name))

    def visit_LocationId(self, node):
        # 1. Revisar que la localización es una variable válida
        # 2. Asigne el tipo de la localización al nodo
        var_values = self.symtab_lookup(node.id)
        if not var_values:
            node.datatype = None
            error(node.lineno, "variable %s is not defined" % node.id)
        else:
            node.datatype = var_values['datatype']

    def visit_LocationVectorAsign(self, node):
        # 1. Revisar que la localización cargada es válida.
        # 2. Asignar el tipo apropiado
        # 3. index debe ser entero
        var_values = self.symtab_lookup(node.id)
        if not var_values:
            error(node.lineno, "Assigment invalid, variable '%s' is not defined" % node.id)
        else:
            node.datatype = var_values['datatype']
            self.visit(node.index)
            if isinstance(node.index, Literal) and node.index.datatype == int_type:
                if not (node.index.value >= 0 and node.index.value <= var_values['size']):
                    error(node.lineno, "Vector index out of range")
            else:
                error(node.lineno, "Index of vector '%s' must be INTEGER" % node.id)

    def visit_LocationVector(self, node):
        # 1. Revisar que la localización cargada es válida.
        # 2. Asignar el tipo apropiado
        var_values = self.symtab_lookup(node.id)
        if not var_values:
            error(node.lineno, "Access invalid, variable '%s' is not defined" % node.id)
        else:
            self.visit(node.index)
            node.datatype = var_values['datatype']
            if not node.index.datatype == int_type:
                error(node.lineno, "Access invalid, index of vector must be INTEGER")

    def visit_Literal(self,node):
        # Adjunte un tipo apropiado a la constante
        if isinstance(node.value, bool):
            node.datatype = self.symtab_lookup("bool")
        elif isinstance(node.value, int):
            node.datatype = self.symtab_lookup("int")
        elif isinstance(node.value, float):
            node.datatype = self.symtab_lookup("float")
        elif isinstance(node.value, basestring):
            node.datatype = self.symtab_lookup("string")

    def visit_Print(self, node):
        pass

    def visit_Write(self, node):
        self.visit(node.expr)

    def visit_Read(self, node):
        self.visit(node.location)

    def visit_FunCall(self, node):
        # 1.Revisar que la funcion exista
        # 2.Comparar cantidad de paramentros y sus tipos
        # por ahora
        #si no tiene tipo aun, es por que esta definida despues o es un llamado recursivo
        #entonces buscamos el tipo en los statements de la instancia
        sym = self.symtab_lookup(node.id)

        if sym['datatype'] == None:
            datatype = self.find_fun_type(sym['fun_instance'])
            self.update_datatype(node.id, datatype)
        sym = self.symtab_lookup(node.id) #update

        if not sym:
            error(node.lineno, "Function '%s' is not defined" % node.id)
        else:
            if not node.id == 'main':
                node.datatype = sym['datatype']
                if sym['cant_argms'] == len(node.params.expressions):
                    type_params = self.visit(node.params)
                    type_argms = sym['type_argms']

                    for i in xrange(0, sym['cant_argms']):
                        if not type_argms[i] == type_params[i]:
                            error(node.lineno, "Arguments must have same type")
                            break
                else:
                    error(node.lineno, "Function '%s' takes exactly %d arguments %d given" \
                          % (node.id, sym['cant_argms'], len(node.params.expressions)))
            else:
                error(node.lineno, "You can not call main function")

    def visit_ExprList(self, node):
        type_params = []
        for expr in node.expressions:
            self.visit(expr)
            type_params.append(expr.datatype)
        return type_params

    def visit_Casting(self, node):
        node.datatype = self.symtab_lookup(node.type)
        self.visit(node.expr)

    def visit_Break(self, node):
        if not self.in_while:
            error(node.lineno, "Break statement is not inside a While loop")

    def visit_Return(self, node):
        if not isinstance(node.value, pasAST.Empty):
            self.visit(node.value)
            cur_fun = self.current_function
            if self.has_return:
                # verificar el tipo de todos los return
                sym = self.symtab_lookup(cur_fun.id)
                if not node.value.datatype == sym['datatype']:
                    error(node.lineno, "Conflic with function type and return expressions type")
            else:
                self.has_return = True
                self.local_symtab.parent.symtab[cur_fun.id]['datatype'] = node.value.datatype
        else:
            self.has_return = True
            error(node.lineno, "Return can not be empty")

    def visit_Empty(self, node):
        node.datatype = None

def check_program(ast_root):
    '''
    Comprueba el programa suministrado (en forma de un AST)
    '''
    checker = CheckProgramVisitor()
    checker.visit(ast_root)

def main():
    import pasparser
    import sys
    from errors import subscribe_errors
    lexer = paslex.make_lexer()
    parser = pasparser.make_parser()
    with subscribe_errors(lambda msg: sys.stdout.write(msg+"\n")):
        program = parser.parse(open(sys.argv[1]).read())
        # Revisa el programa
        check_program(program)

if __name__ == '__main__':
    main()
'''
* Que hacer con funciones que todavia no tienen return, y visito
un llamado recursivo a esa funcion
'''
