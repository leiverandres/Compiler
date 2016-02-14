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

## A RegExp to check email addres

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

##
