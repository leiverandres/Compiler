# -*- coding: utf-8 -*-
import pasAST
import StringIO
data = StringIO.StringIO()
label_index = 1

def generate(file, root_ast):
    print >>file, "! Creado por mpasca.py"
    print >>file, "! Leiver Andres Campeón, Juan Pablo Florez, IS744 (2016‐1)"
    print >>file, '\n     .section  ".text"'
    print >>data, '\n     .section  ".rodata"'
    emit_program(file, root_ast)
    print >>file, data.getvalue()

def emit_program(file, program):
    print >>file, "\n! program"
    funclist = program.funList.functions
    for fun in funclist:
        emit_function(file, fun)

def emit_function(file, func):
    print >>file, "\n! function: %s (start)" % func.id
    print >>file, "\n       .global %s" % func.id
    print >>file, "%s:" % func.id
    statements = func.statements.statements
    for stm in statements:
        emit_statement(file, stm)
    print >>file, "\n! function: %s (end)" % func.id

def emit_statement(file, stm):
    if isinstance(stm, pasAST.WhileStatement):
        emit_while(file, stm)
    elif isinstance(stm, pasAST.IfStatement):
        emit_ifthen(file, stm)
    elif isinstance(stm, pasAST.AssignmentStatement):
        emit_assing(file, stm)
    elif isinstance(stm, pasAST.Print):
        emit_print(file, stm)
    elif isinstance(stm, pasAST.Write):
        emit_write(file, stm)
    elif isinstance(stm, pasAST.Read):
        emit_read(file, stm)
    elif isinstance(stm, pasAST.Return):
        emit_return(file, stm)
    elif isinstance(stm, pasAST.FunCall):
        emit_funcall(file, stm)
    elif isinstance(stm, pasAST.Skip):
        emit_skip(file, stm)
    elif isinstance(stm, pasAST.Break):
        emit_break(file, stm)
    elif isinstance(stm, pasAST.Statements):
        emit_block(file, stm)

def emit_while(file, while_stm):
    test = new_label()
    done = new_label()
    print >>file, "\n! while (start)"
    print >>file, "\n%s:\n" % test

    condition = while_stm.condition
    body = while_stm.body

    eval_relation(file, condition)
    print >>file, "!   relop := pop"
    print >>file, "!   if not relop: goto %s" % done
    if not isinstance(body, pasAST.Skip):
        emit_block(file, while_stm.body);
    else:
        emit_skip(file, body)
    print >>file, "! goto %s" % test
    print >>file, "\n%s:" % done
    print >>file, "\n! while (end)"

def emit_ifthen(file, ifthen_stm):
    done = new_label()
    else_label = new_label() if ifthen_stm.else_b else None
    print >>file, "\n! ifthen (start)"

    eval_relation(file, ifthen_stm.condition)
    if else_label == None:
        print >>file, "! if not relop: goto %s  ! done" % done
    else:
        print >>file, "! if not relop: goto %s  ! else" % else_label

    if not isinstance(ifthen_stm.then_b, pasAST.Skip):
        emit_block(file, ifthen_stm.then_b)
    else:
        emit_skip(file, ifthen_stm.then_b)

    print >>file, "! goto %s    ! goto end" % done
    if ifthen_stm.else_b:
        print >>file, "%s:    ! else:" % else_label
        if not isinstance(ifthen_stm.then_b, pasAST.Skip):
            emit_block(file, ifthen_stm.then_b)
        else:
            emit_skip(file, ifthen_stm.then_b)

    print >>file, "\n%s:  ! done:" % done
    print >>file, "\n! ifthen (end)"

def emit_assing(file, assign_stm):
    print >>file, "\n! Assigment (start)"
    eval_expr(file, assign_stm.value)
    loc = assign_stm.location
    if isinstance(loc, pasAST.LocationId):
        print >>file, "!   %s := pop" % loc.id
    else: # LocationVectorAsign
        print >>file, "!  %s[index] := pop" % loc.id
    print >>file, "! Assigment (end)"

def emit_print(file, print_stm):
    print >>file, "\n! print (start)"
    value = print_stm.str
    label = new_label()
    print >>data, '%s:   .asciz  "%s"' % (label, value)
    print >>file, "! print (end)"

def emit_write(file, write_stm):
    print >>file, "\n! write (start)"
    eval_expr(file, write_stm.expr)
    print >>file, "!   expr := pop"
    print >>file, "!   write(expr)"
    print >>file, "! write (end)"

def emit_read(file, read_stm):
    print >>file, "\n! read (start)"
    print >>file, "! read (end)"

def emit_return(file, return_stm):
    # print >>file, "\n! return (start)"
    # eval_expr(file, return_stm.value)
    # print >>file, "! return (end)"
    print "return no implemented"

def emit_funcall(file, funcall_stm):
    params = funcall_stm.params
    i = 1
    push = "!   push %s(" % funcall_stm.id
    if isinstance(params, pasAST.ExprList):
        if not isinstance(params.expressions[0], pasAST.Empty):
            for parm in params.expressions:
                eval_expr(file, parm)
                print >>file, "!   arg%d := pop" % i
                push += ", " if i > 1 else ""
                push += "arg" + str(i)
                i += 1
    push += ")"
    print >>file, push

def emit_skip(file, skip_stm):
    print >>file, "\n! skip (start)"
    print >>file, "! skip (end)"

def emit_break(file, break_stm):
    print >>file, "\n! break (start)"
    print >>file, "! break (end)"

def emit_block(file, block_stms):
    if not isinstance(block_stms, pasAST.Statements):
        emit_statement(file, block_stms)
    else:
        for stm in block_stms.statements:
            emit_statement(file, stm)

def eval_relation(file, expr):
    if isinstance(expr, pasAST.RelationalOp):
        eval_expr(file, expr.left)
        eval_expr(file, expr.right)
        if (expr == 'or'):
            print >>file, "!   or"
        elif (expr.op == 'and'):
            print >>file, "!   and"
        elif (expr.op == '<'):
            print >>file, "!   lt"
        elif (expr.op == '<='):
            print >>file, "!   le"
        elif (expr.op == '>'):
            print >>file, "!   gt"
        elif (expr.op == '>='):
            print >>file, "!   ge"
        elif (expr.op == '!='):
            print >>file, "!   ne"
        elif (expr.op == '=='):
            print >>file, "!   eq"
    elif isinstance(expr, pasAST.UnaryOp):
        if (expr == 'not'):
            print >>file, "!   not"
    print >>file, "!   relop := pop"

def eval_expr(file, expr):
    if isinstance(expr, pasAST.BinaryOp):
        eval_expr(file, expr.left)
        eval_expr(file, expr.right)
        if (expr.op == '+'):
            print >>file, "!   add"
        elif (expr.op == '-'):
            print >>file, "!   sub"
        elif (expr.op == '*'):
            print >>file, "!   mul"
        elif (expr.op == '/'):
            print >>file, "!   div"
    elif isinstance(expr, pasAST.UnaryOp):
        print "UnaryOp no implemented"
    elif isinstance(expr, pasAST.LocationId):
        print >>file, "!   push", expr.id
    elif isinstance(expr, pasAST.LocationVector):
        eval_expr(file, expr.index)
        print >>file, "!   push %s[index]" % expr.id
    elif isinstance(expr, pasAST.Literal):
        expr_type = expr.datatype
        if (expr_type.name == 'int'):
            print >>file, "!   push", expr.value
        elif (expr_type.name == 'float'):
            print >>file, "!   push", expr.value
    elif isinstance(expr, pasAST.Casting):
        print "Casting no implemented"
    elif isinstance(expr, pasAST.FunCall):
        emit_funcall(file, expr)

def new_label():
    global label_index
    label = ".L" + str(label_index)
    label_index += 1
    return label

'''
LocationVector y LocationVectorAsign?
'''
