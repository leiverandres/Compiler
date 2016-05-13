import re

p = re.compile('[a-z]+')
p2 = re.compile(r'ab*', re.IGNORECASE)
pDigits = re.compile(r'\d+')
#multiplos de 3 en binario
binariMul = re.compile('([0-9]*|[0-7]*|[0-9a-fA-F]*)')


m = p.match("hola")
mD = pDigits.findall('12 drummers drumming, 11 pipers piping, 10 lords a-leaping')
if (m):
  print "It matches"
else:
  print "Bad luck this time"

if (mD):
  print "It matches with"
  for i in mD:
    print i
else:
  print "Bad luck with digits"
