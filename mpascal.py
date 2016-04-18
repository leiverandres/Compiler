from pasAST import *
import paslex
import pasparser
from pasparser import *
import re
import sys

if __name__ == "__main__":
    if (len(sys.argv) < 2 or len(sys.argv) > 4):
        print "Usage: python %s [-ast] [-lex] <pascal_file>" % sys.argv[0]
    elif (re.match(r'.*\.pas', sys.argv[-1])):
        try:
            file = open(sys.argv[-1])
            data = file.read()

            if ("-lex" in sys.argv):
                paslex.run_lexer(data)
            elif ("-ast" in sys.argv):
                parser = pasparser.make_parser()
                result = parser.parse(data)
                if result:
                    dump_tree(result)
            else:
                parser = pasparser.make_parser()
                result = parser.parse(data)

        except IOError:
            print "Error: The file does not exist"
            print "Usage: python %s [-ast] [-lex] <pascal_file>" % sys.argv[0]
    else:
        print "Please put the name of your pascal file at the end of the command"
