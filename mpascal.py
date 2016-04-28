from pasAST import *
import paslex
import pasparser
from pasparser import *
import re
import sys

def show_usage(programName):
    sys.stderr.write(
    '''Usage: python %s [option] <pascal_file>
Options:
-lex   : show all tokens of lexer
-ast   : show abstract syntax tree
    ''' % programName)

if __name__ == "__main__":
    import sys
    from errors import subscribe_errors

    if (len(sys.argv) < 2 or len(sys.argv) > 3):
        show_usage(sys.argv[0])
        raise SystemExit(1)
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
                    dump_class_tree(result)
            else:
                parser = pasparser.make_parser()
                result = parser.parse(data)

        except IOError:
            sys.stderr.write("Error: The file does not exist")
            raise SystemExit(1)
    else:
        print "Please put the name of your pascal file at the end of the command"
        raise SystemExit(1)

# with subscribe_errors(lambda msg: sys.stderr.write(msg+"\n")):
# 		lexer.input(open(sys.argv[1]).read())
# 		for tok in iter(lexer.token, None):
# 			sys.stdout.write("%s\n" % tok)
