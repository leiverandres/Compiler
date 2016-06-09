# Compiler for UTP course IS753

Implementacion de un compilador para lenguaje minipascal

Desarrolladores:

* Leiver Andres Campeón
* Juan Pablo Florez

Descripción:

Este compilador fue desarrollado en python usando la libreria ply, la cual ayuda a crear el
analizador lexico y el sintáctico. Para construir el arbol de sintaxis abstracto(AST) y hacer el analizador semántico se empleo el patrón visitante, lo cual redujo en gran medida la complejidad y mejoro la estructura del código. Finalmente para la generación de código intermedio de la arquitectura SPARC V8 se implementarón varias funcionalidades en el archivo mpasgen que realizan el manejo de registros, alocación de memoria, entre otras cosas.

En resumen:
El archivo paslex.py contruye el analizador lexico. puede ejecutarse este paso con el comando.
```python
python paslex.py <file_name.pas>
```

El archivo pasAST.py contiene la definicion de las clases de nodos del AST y la definición del nodeVisitor.
El archivo pasparser.py realiza el analisis sintactico y construye el AST.
```python
python pasparser.py <file_name.pas>
```
El archivo check.py se encarga del analisis semantico, el cual valida los tipos de las variables y operaciones.
```python
python check.py <file_name.pas>
```
El archivo mpasgen.py genera el código maquina para ser ejecutado en la arquitectura SPARC V8.
Finalmente el archivo mpascal.py permite ejecutar el compilador completo y asegurarse de que no hayan errores en archivo.pas. Además provee dos opciones: una para ejecutar solamente el analizador lexico(-lex) y la otra para compilar y mostrar por consola el AST(-ast).
```python
python mpascal.py [-lex | -ast]  <file_name.pas>
```



