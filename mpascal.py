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
    from errors import subscribe_errors, errors_reported

    if (len(sys.argv) < 2 or len(sys.argv) > 3):
        show_usage(sys.argv[0])
        raise SystemExit(1)
    elif (re.match(r'.*\.pas', sys.argv[-1])):
        try:
            file = open(sys.argv[-1])
            data = file.read()

            if ("-lex" in sys.argv):
                paslex.run_lexer(data)
            else:
                parser = pasparser.make_parser()
                try:
                    with subscribe_errors(lambda msg: sys.stdout.write(msg+"\n")):
                        result = parser.parse(data)
                    errors = errors_reported();
                    if errors == 0:
                        if ("-ast" in sys.argv):
                            dump_class_tree(result)
                    else:
                        sys.stderr.write("Number of errors: %d" % errors)
                except parseError as e:
                    sys.stderr.write("Program couldn't be compiled\n")

        except IOError:
            sys.stderr.write("Error: The file does not exist")
            raise SystemExit(1)
    else:
        print "Please put the name of your pascal file at the end of the command"
        raise SystemExit(1)
