# Testing regular expression

## A RegExp to validate integer numbers in C (decimal, octal, hex, binary)

```python
r'([1-9][0-9]*(ull|llu|uLL|LLu)?|0[0-7]*|0[xX][0-9a-fA-F]+|0[bB][01]+)'

```
### Tested with:

* decimal 42;
* octal 052;
* hex 0x2a;
* hex 0X2A;
* binary 0b101010;

## A RegExp to check email address

```python
r'[a-zA-z0-9\-_\.]+@[a-zA-Z]+\.[a-zA-Z]+'
```
### Tested with:

* leiverandres04p@hotmail.com
* leiver_andres-0.4@gmail.com
* leiver%Andres#@bad@hotmail.com (_doesn't match_)
* leiverandres@mistake@bad#-domain.com (_doesn't match_)

## A RegExp to validate a multiple of 3 in binary

```python
r'(0(1*0)*1)*'
```

## A RegExp to validate a IPv4 address

```python
r'((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
```

## A RegExp to validate Roman Numerals

```python
r'M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})'
```

## A RegExp to validate string like in C language

```python
r'\"(.|\\[a-zA-Z])*\"'
```

## A RegExp to validate numbers with miles point (e.g 123.101)

```python
r'[1-9][0-9]{0,2}\.[0-9]{3}'
```

### Tested with
* 12.152
* 1.000
* 1423.545 (doesn't match)
* 12.45 (doesn't match)

## A RegExp to validate the java comments
* _/\* comment \*/_
* _//comment_
* _/\***/_

```python
r'(//.*|/\*.*\*/|/\*\n?(\*.*\n?)*\*/)'
```

### Tested with

* //This is a comment
* /\*hola\*/
* And:  
```text
  /*
   *foo
   *bar
  */
```

## A RegExp to validate numbers with no leading zeros

```python
r'([1-9][0-9]*|0)'
```


## A RegExp to validate spanish words

Proper Names has no '?'
```python
r'[A-ZÁÉÍÓÚ]?[a-záéíóúñ]*'
```
