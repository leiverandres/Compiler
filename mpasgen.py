# -*- coding: utf-8 -*-
import pasAST
import StringIO
import sys

##########################################################
# Register
##########################################################
class Register(object):
    def __init__(self):
        self.local_count = 0 # next local register for stack
        self.tmp_count = 0 # registros "derramados" en memoria
        self.sp_count = 64
        self.oldest = 0
        self.stack = [False for i in xrange(0,8)]
        # l_cont = 0
        # t_cont = 0

    def getFree(self):
        return self.stack.index(False)

    def push(self, file):
        # print "Stack: ", self.stack
        if False in self.stack:
            # self.local_count +=1
            self.local_count = self.getFree()
            local_reg = "%l" + str(self.local_count)
            self.stack[self.local_count] = True
            print "last free used: ", self.local_count
        else:
            # derramar registro mas viejo en memoria
            self.stack[self.oldest] = False
            print >> file, "     st %s, [%%fp - %d]  ! spill %s" % (self.oldest, self.sp_count, self.oldest)
            self.oldest = (self.oldest + 1) % 8
            self.sp_count +=4
            self.tmp_count += 1
            # try push again:
            local_reg = self.push(file)
            # self.local_count = self.getFree()
            # local_reg = '%l'+str(self.local_count)
            # self.stack[self.local_count] = True
        print "push state(local, tmp, sp): (%d, %d, %d)" % (self.local_count, self.tmp_count, self.sp_count)
        return local_reg
        if self.local_count < 8 and self.tmp_count != 8:
            l = '%l'+str(self.local_count)
            self.local_count +=1
        else:
            if self.local_count == 8:
                self.local_count = 0
                self.tmp_count = 8
            l = '%l'+str(self.local_count)
            print >> file, "     st %s, [%%fp -%d]" % (l, self.sp_count)
            self.sp_count +=4
            self.local_count +=1
        return l

    def pop(self, file): # falta: cuando hacer recovery?
        # local_reg = "None"
        # print "pop state(local, tmp, sp): (%d, %d, %d)" % (self.local_count, self.tmp_count, self.sp_count)
        # if True in self.stack:
        #     local_reg = '%l'+str(self.local_count)
        #     self.stack[self.local_count] = False
        #     self.local_count = ((self.local_count - 1) % 8 + 8 ) % 8 # aritmetica modular
        # if self.stack.count(False) > 0 and self.tmp_count > 0:
        #     self.tmp_count -= 1
        #     self.local_count = self.getFree()
        #     print >>file, "     ld [%%fp - %d], %s" % (self.sp_count, self.local_count)
        #     self.stack[self.local_count] = True
        #     self.sp_count -= 4
        # return local_reg
        if self.local_count >= 0 and self.tmp_count == 0:
            self.local_count -=1
            l = '%l'+str(self.local_count)
        else:
            self.local_count = self.tmp_count
            self.tmp_count = 0
            self.local_count -=1
            l = '%l'+str(self.local_count)
        return l

##########################################################
# Register
##########################################################
data = StringIO.StringIO()
var_locals = None
var_argms  = None
reg = Register()
label_index = 1

def generate(file, root_ast):
    print >>file, "! Creado por %s" % sys.argv[0]
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
    global var_locals
    global var_argms
    old_var_locals = var_locals
    f = StringIO.StringIO()
    ret_label = new_label()
    frame_size = 64 # the stack frame should have at least this size
    statements = func.statements.statements
    decl_locals = func.localslist.locals

    # calculate stack frame size
    frame_size += allocate_locals(file, func)
    frame_size += frame_size % 8 # size must be multiply of 8
    reg.sp_count = frame_size
    old_frame_size = frame_size
    var_locals = decl_locals
    var_argms = func.arglist.arguments
    for stm in statements:
        if isinstance(stm, pasAST.Return):
            emit_return(f, stm, ret_label)
        else:
            emit_statement(f, stm)
    var_locals = old_var_locals
    frame_size = old_frame_size
    reg.sp_count = old_frame_size

    print >>file, "\n! function: %s (start)" % func.id
    print >>file, "\n       .global %s" % func.id
    print >>file, "%s:" % func.id
    print >>file, "     save %%sp, -%d, %%sp" % frame_size
    print >>file, f.getvalue()
    print >>file, "%s:" % ret_label
    if (func.id == 'main'):
        print >>file, "        mov 0, %o0      ! solamente aparece en main"
        print >>file, "        call _exit      ! solamente aparece en main"
        print >>file, "        nop     ! solamente aparece en main"
    print >>file, "        ret"
    print >>file, "        restore"
    print >>file, "\n! function: %s (end)" % func.id

def emit_statement(file, stm):
    if isinstance(stm, pasAST.WhileStatement):
        emit_while(file, stm)
    elif isinstance(stm, pasAST.IfStatement):
        emit_ifthen(file, stm)
    elif isinstance(stm, pasAST.AssignmentStatement):
        emit_assign(file, stm)
    elif isinstance(stm, pasAST.Print):
        emit_print(file, stm)
    elif isinstance(stm, pasAST.Write):
        emit_write(file, stm)
    elif isinstance(stm, pasAST.Read):
        emit_read(file, stm)
    elif isinstance(stm, pasAST.FunCall):
        emit_funcall(file, stm)
    elif isinstance(stm, pasAST.Skip):
        emit_skip(file, stm)
    elif isinstance(stm, pasAST.Break):
        emit_break(file, stm)
    elif isinstance(stm, pasAST.Statements):
        emit_block(file, stm)

def emit_while(file, while_stm):
    test_label = new_label()
    done_label = new_label()
    print >>file, "\n! while (start)"
    print >>file, "\n%s:\n" % test_label

    condition = while_stm.condition
    body = while_stm.body

    eval_relation(file, condition)
    result = reg.pop(file)
    print >>file, "!    relop := pop"
    print >>file, "     cmp %s, %%g0 !if not relop: goto done" % result
    print >>file, "     be  %s" % done_label
    print >>file, "     nop"
    if not isinstance(body, pasAST.Skip):
        emit_block(file, while_stm.body);
    else:
        emit_skip(file, body)
    print >>file, "     ba %s    ! goto %s" % (test_label, test_label)
    print >>file, "     nop"
    print >>file, "\n%s:" % done_label
    print >>file, "\n! while (end)"

def emit_ifthen(file, ifthen_stm):
    print >>file, "\n! ifthen (start)"
    done_label = new_label()
    else_label = new_label() if ifthen_stm.else_b else None

    eval_relation(file, ifthen_stm.condition)
    result = reg.pop(file)
    print >>file, "     cmp %s, %%g0" % result
    if else_label == None:
        print >>file, "     be %s" % done_label
        print >>file, "     ! if not relop: goto done"
    else:
        print >>file, "     be %s" % else_label
        print >>file, "     ! if not relop: goto else"
    print >>file, "     nop"
    print >>file, "! then: "
    if not isinstance(ifthen_stm.then_b, pasAST.Skip):
        emit_block(file, ifthen_stm.then_b)
    else:
        emit_skip(file, ifthen_stm.then_b)

    print >>file, "     ba %s" % done_label
    print >>file, "     ! goto done"
    if ifthen_stm.else_b:
        print >>file, "%s:    ! else:" % else_label
        if not isinstance(ifthen_stm.then_b, pasAST.Skip):
            emit_block(file, ifthen_stm.then_b)
        else:
            emit_skip(file, ifthen_stm.then_b)

    print >>file, "\n%s:  ! done:" % done_label
    print >>file, "\n! ifthen (end)"

def emit_assign(file, assign_stm):
    print >>file, "\n! Assignment (start)"
    eval_expr(file, assign_stm.value)
    result = reg.pop(file)
    loc = assign_stm.location
    print "last: ",  loc.id
    offset = -find_offset(loc) #falta: offset es positivo? negativo
    if isinstance(loc, pasAST.LocationId):
        print >>file, "     st %s, [%%fp - %d]" % (result, offset)
        print >>file, "!   %s := pop" % loc.id
    else: # LocationVectorAsign
        eval_expr(file, loc.index)
        result = reg.pop(file)
        ans_push = reg.push(file)
        offset = -find_offset(loc)
        print >>file, "     sll %s, 2, %s" % (result,result)
        print >>file, "     add %%fp, %s, %s" % (result, result)
        print >>file, "     ld [%s - %d], %s" % (result, offset, ans_push)
    print >>file, "! Assigment (end)"

def emit_print(file, print_stm):
    print >>file, "\n! print (start)"
    value = print_stm.str
    label = new_label()

    print >>file, " ! call hlprint()"
    print >>file, "     sethi %%hi(%s), %%o0" % label
    print >>file, "     or    %%o0, %%lo(%s), %%o0" % label
    print >>file, "     call hlprint"
    print >>file, "     nop"
    print >>data, '%s:   .asciz  "%s"' % (label, value)
    print >>file, "! print (end)"

def emit_write(file, write_stm):
    value = write_stm.expr
    eval_expr(file, value)
    lm = reg.pop(file)
    print >>file, "\n! write (start)"
    if value.datatype.name == 'int':
        print >>file, '! call flwritei(int)'
        print >>file, "     mov %s, %%o0" % lm
        print >>file, "     call flwritei"
        print >>file, "     nop"
    else:
        print >>file, '! call flwritef(float)'
        print >>file, "     mov %s, %%o0" % lm
        print >>file, "     call flwritef" ## <- el cambio
        print >>file, "     nop"
    # print >>file, "!   write(expr)"
    # print >>file, "!   expr := pop"
    print >>file, "! write (end)"

def emit_read(file, read_stm):
    print >>file, "\n! read (start)"
    if read_stm.location.datatype.name == 'int':
        print >>file, "! call flreadi()"
        print >>file, "     call flreadi"
    else: # float
        print >>file, "! call flreadf()"
        print >>file, "     call flreadf"
    print >>file, "     nop"

    if isinstance(read_stm.location, pasAST.LocationId):
        print find_offset(read_stm.location)
    else: # LocationVectorAsign
        print find_offset(read_stm.location)
    # falta: result = reg.pop()?
    print >>file, "     st %%o0, result" # falta: dir result, %fp + offset?
    print >>file, "! read (end)"

def emit_return(file, return_stm, ret_label):
    print >>file, "\n! return (start)"
    eval_expr(file, return_stm.value)
    memdir = reg.pop(file)
    print >>file, "     mov %s, %%o0" % memdir
    print >>file, "     jmp %s" % ret_label
    print >>file, "     nop"
    print >>file, "! return (end)"

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
            for k in (0, len(params.expressions)):
                result = reg.pop(file)
                print >>file, "     store %s, %%o%d" % (result, i)
                i += 1
    push += ")"
    print >>file, "     call %s" % funcall_stm.id
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
        memdir_right = reg.pop(file)
        memdir_left = reg.pop(file)
        memdir_ans = reg.push(file)
        if (expr == 'or'):
            print >>file, "     or %s, %s, %s" % (memdir_left, memdir_right, memdir_ans)
            # print >>file, "!   or"
        elif (expr.op == 'and'):
            print >>file, "     and %s, %s, %s" % (memdir_left, memdir_right, memdir_ans)
            # print >>file, "!   and"
        elif (expr.op == '<'):
            label = new_label()
            print >>file, "     cmp %s, %s" % (memdir_left, memdir_right)
            print >>file, "     bl %s" % label
            print >>file, "     mov 1, %s" % memdir_ans
            print >>file, "     mov 0, %s" % memdir_ans
            print >>file, "%s:" % label
            # print >>file, "!   lt"
        elif (expr.op == '<='):
            label = new_label()
            print >>file, "     cmp %s, %s" % (memdir_left, memdir_right)
            print >>file, "     ble %s" % label
            print >>file, "     mov 1, %s" % memdir_ans
            print >>file, "     mov 0, %s" % memdir_ans
            print >>file, "%s:" % label
            # print >>file, "!   le"
        elif (expr.op == '>'):
            label = new_label()
            print >>file, "     cmp %s, %s" % (memdir_left, memdir_right)
            print >>file, "     bg %s" % label
            print >>file, "     mov 1, %s" % memdir_ans
            print >>file, "     mov 0, %s" % memdir_ans
            print >>file, "%s:" % label
            print >>file, "!   gt"
        elif (expr.op == '>='):
            label = new_label()
            print >>file, "     cmp %s, %s" % (memdir_left, memdir_right)
            print >>file, "     bge %s" % label
            print >>file, "     mov 1, %s" % memdir_ans
            print >>file, "     mov 0, %s" % memdir_ans
            print >>file, "%s:" % label
            # print >>file, "!   ge"
        elif (expr.op == '!='):
            label = new_label()
            print >>file, "     cmp %s, %s" % (memdir_left, memdir_right)
            print >>file, "     be %s" % label
            print >>file, "     mov 1, %s" % memdir_ans
            print >>file, "     mov 0, %s" % memdir_ans
            print >>file, "%s:" % label
            # print >>file, "!   ne"
        elif (expr.op == '=='):
            label = new_label()
            print >>file, "     cmp %s, %s" % (memdir_left, memdir_right)
            print >>file, "     bne %s" % label
            print >>file, "     mov 1, %s" % memdir_ans
            print >>file, "     mov 0, %s" % memdir_ans
            print >>file, "%s:" % label
            # print >>file, "!   eq"
    elif isinstance(expr, pasAST.UnaryOp):
        if (expr.op == 'not'):
            eval_relation(file, expr.right)
            li = reg.pop(file) # parte superior de la pila
            lk = reg.push(file) # tope donde se guarda el valor modificado
            print >>file, "     neg %s, %s" % (li, lk)
    print >>file, "!   relop := pop"

def eval_expr(file, expr):
    if isinstance(expr, pasAST.BinaryOp):
        eval_expr(file, expr.left)
        eval_expr(file, expr.right)
        memdir_right = reg.pop(file)
        memdir_left = reg.pop(file)
        memdir_ans = reg.push(file)
        if (expr.op == '+'):
            print >>file, "     add %s, %s, %s" % (memdir_left, memdir_right, memdir_ans)
        elif (expr.op == '-'):
            print >>file, "     sub %s, %s, %s" % (memdir_left, memdir_right, memdir_ans)
        elif (expr.op == '*'):
            memdir_ans = reg.push(file)
            print >>file, "     mov %s, %%o0" % memdir_left
            print >>file, "     call .mul"
            print >>file, "     mov %s, %%o1" % memdir_right
            print >>file, "     mov %%o0 , %s" % memdir_ans
        elif (expr.op == '/'):
            memdir_ans = reg.push(file)
            print >>file, "     mov %s, %%o0" % memdir_left
            print >>file, "     call .div"
            print >>file, "     mov %s, %%o1" % memdir_right
            print >>file, "     mov %%o0, %s" % memdir_ans
    elif isinstance(expr, pasAST.UnaryOp):
        eval_expr(expr.right)
        li = reg.pop(file) # parte superior de la pila
        lk = reg.push(file) # tope donde se guarda el valor modificado
        if expr.op == '-': # minus unary
            print >>file, "     xor %s, 1, %s" % (li, lk)
    elif isinstance(expr, pasAST.LocationId):
        offset = -find_offset(expr) # falta: signo offset?
        ln = reg.push(file)
        print >>file, "     ld [%%fp - %d], %s" % (offset, ln)
        print >>file, "!   push", expr.id
    elif isinstance(expr, pasAST.LocationVector):
        eval_expr(file, expr.index)
        result = reg.pop(file)
        ans_push = reg.push(file)
        offset = find_offset(expr)
        print >>file, "     sll %s, 2, %s" % (result,result)
        print >>file, "     add %%fp, %s, %s" % (result, result)
        print >>file, "     ld [%s - %d], %s" % (result, offset,ans_push)
        print >>file, "!    push %s[index]" % expr.id
    elif isinstance(expr, pasAST.Literal):
        expr_type = expr.datatype.name
        if (expr_type == 'int'):
            memdir = reg.push(file)
            if expr.value >= -4095 and expr.value <= 4095:
                print >>file, "     mov %d, %s         ! push %d" % (expr.value, memdir, expr.value)
            else:
                label = new_label()
                print >>file, "     sethi %%hi(%s), %%g1" % label
                print >>file, "     or    %%g1, %lo(%s), %%g1" % label
                print >>file, "     ld    [%%g1], %s" % memdir
                print >>data, "%s:    .word    %d" % (label, expr.value)

        elif (expr_type == 'float'):
            memdir = reg.push(file)
            if expr.value >= -4095 and expr.value <= 4095:
                print >>file, "     mov %d, %s" % (expr.value, memdir)
                print >>file, "!    push float", expr.value
            else:
                label = new_label()
                print >>file, "     sethi %%hi(%s), %%g1" % label
                print >>file, "     or    %%g1, %lo(%s), %%g1" % label
                print >>file, "     ld    [%%g1], %s" % memdir
                print >>data, "%s:    .float    %d" % (label, expr.value)
    elif isinstance(expr, pasAST.Casting):
        print "Casting no implemented"
    elif isinstance(expr, pasAST.FunCall):
        emit_funcall(file, expr)

def new_label():
    global label_index
    label = ".L" + str(label_index)
    label_index += 1
    return label

def find_offset(var):
    global var_locals
    global var_argms
    found = None
    flag = False
    if not isinstance(var_locals[0], pasAST.Empty):
        for i in var_locals:
            if (i.id == var.id):
                found = i
                flag = True
                break
    if not isinstance(var_argms[0], pasAST.Empty) and not flag:
        for k in var_argms:
            if (k.id == var.id):
                found = k
                break
    if found == None:
        print "problem finding offset"
    # if isinstance(var, pasAST.LocationVectorAsign):
    #     return found.frame_offset + (var.index.value*4)
    # else: # locationID
    #     return found.frame_offset
    return found.frame_offset

def allocate_locals(file, fun):
    frame_size = 0
    decl_argms = fun.arglist.arguments
    decl_locals = fun.localslist.locals
    if not isinstance(decl_argms[0], pasAST.Empty):
        for arg in decl_argms:
            if isinstance(arg.type, pasAST.Vector):
                frame_size += arg.type.size * 4
            else: # simple type
                frame_size += 4
            arg.frame_offset = -(frame_size)

    if not isinstance(decl_locals[0], pasAST.Empty):
        for local in decl_locals:
            if isinstance(local, pasAST.Function):
                emit_function(file, local)
            else: # var declaration
                if isinstance(local.type, pasAST.Vector):
                    frame_size += local.type.size * 4
                else: # simple type
                    frame_size += 4
                local.frame_offset = -(frame_size)
    return frame_size
'''
'''
