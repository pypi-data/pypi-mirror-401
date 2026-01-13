from llvmlite import ir
from . import ast_nodes as nodes

class CodeGen:
    def __init__(self, target_triple="native"):
        self.module = ir.Module(name="volikos_main")
        
        # Configure Target
        if target_triple == "native":
            self.module.triple = "x86_64-pc-linux-gnu" 
        else:
            self.module.triple = target_triple
        
        self.module.data_layout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
        
        self.builder = None
        self.scope_stack = [{}] 
        self.printf = None
        self.malloc = None
        self.realloc = None
        
        # Libc String functions
        self.strlen = None
        self.strcpy = None
        self.strcat = None
        
        # --- Type Definitions ---
        self.int_type = ir.IntType(32)
        self.float_type = ir.FloatType()
        self.void_type = ir.VoidType()
        self.bool_type = ir.IntType(1)
        self.string_type = ir.IntType(8).as_pointer()
        self.long_type = ir.IntType(64)
        
        # Dynamic Array Struct: { int* data, int size, int capacity }
        self.array_struct_ty = ir.LiteralStructType([
            self.int_type.as_pointer(),
            self.int_type,
            self.int_type
        ])
        
        self._init_libc()

    def _init_libc(self):
        # printf(i8* format, ...)
        printf_ty = ir.FunctionType(self.int_type, [self.string_type], var_arg=True)
        self.printf = ir.Function(self.module, printf_ty, name="printf")
        
        # malloc(i64 size)
        malloc_ty = ir.FunctionType(self.string_type, [self.long_type])
        self.malloc = ir.Function(self.module, malloc_ty, name="malloc")
        
        # realloc(i8* ptr, i64 size)
        realloc_ty = ir.FunctionType(self.string_type, [self.string_type, self.long_type])
        self.realloc = ir.Function(self.module, realloc_ty, name="realloc")

        # strlen(i8* str) -> i64
        strlen_ty = ir.FunctionType(self.long_type, [self.string_type])
        self.strlen = ir.Function(self.module, strlen_ty, name="strlen")

        # strcpy(i8* dest, i8* src) -> i8*
        strcpy_ty = ir.FunctionType(self.string_type, [self.string_type, self.string_type])
        self.strcpy = ir.Function(self.module, strcpy_ty, name="strcpy")

        # strcat(i8* dest, i8* src) -> i8*
        strcat_ty = ir.FunctionType(self.string_type, [self.string_type, self.string_type])
        self.strcat = ir.Function(self.module, strcat_ty, name="strcat")

    def _get_var_ptr(self, name):
        for scope in reversed(self.scope_stack):
            if name in scope: return scope[name]
        raise ValueError(f"Undefined variable: {name}")

    def generate(self, node):
        if isinstance(node, list):
            for n in node: self.generate(n)
            return

        # --- Functions ---
        if isinstance(node, nodes.FunctionDef):
            ret_type = self.void_type
            if node.return_type == "int": ret_type = self.int_type
            elif node.return_type == "float": ret_type = self.float_type
            
            arg_types = []
            for arg_name, arg_type in node.args:
                if arg_type == "int": arg_types.append(self.int_type)
                elif arg_type == "float": arg_types.append(self.float_type)
                elif arg_type == "string": arg_types.append(self.string_type)
            
            func_ty = ir.FunctionType(ret_type, arg_types)
            func = ir.Function(self.module, func_ty, name=node.name)
            
            entry = func.append_basic_block(name="entry")
            self.builder = ir.IRBuilder(entry)
            self.scope_stack.append({})
            
            for i, (arg_name, arg_type) in enumerate(node.args):
                ptr = self.builder.alloca(arg_types[i], name=arg_name)
                self.builder.store(func.args[i], ptr)
                self.scope_stack[-1][arg_name] = ptr
            
            self.generate(node.body)
            
            if not self.builder.block.is_terminated:
                if ret_type == self.void_type:
                    self.builder.ret_void()
                else:
                    if ret_type == self.int_type: self.builder.ret(ir.Constant(self.int_type, 0))
                    elif ret_type == self.float_type: self.builder.ret(ir.Constant(self.float_type, 0.0))
            
            self.scope_stack.pop()

        # --- Return ---
        elif isinstance(node, nodes.Return):
            val = self.generate(node.value)
            self.builder.ret(val)

        # --- Variables ---
        elif isinstance(node, nodes.VarDecl):
            if node.var_type == "int[]":
                ptr = self.builder.alloca(self.array_struct_ty, name=node.name)
                val_struct = self.generate(node.value) 
                self.builder.store(val_struct, ptr)
            else:
                typ = self.int_type
                if node.var_type == "float": typ = self.float_type
                elif node.var_type == "string": typ = self.string_type
                
                ptr = self.builder.alloca(typ, name=node.name)
                val = self.generate(node.value)
                
                if node.var_type == "float" and val.type == self.int_type:
                    val = self.builder.sitofp(val, self.float_type)
                    
                self.builder.store(val, ptr)
            
            self.scope_stack[-1][node.name] = ptr

        # --- Array Literal ---
        elif isinstance(node, nodes.ArrayLiteral):
            count = len(node.elements)
            size_bytes = ir.Constant(self.long_type, count * 4)
            raw_ptr = self.builder.call(self.malloc, [size_bytes])
            data_ptr = self.builder.bitcast(raw_ptr, self.int_type.as_pointer())
            
            for i, elem in enumerate(node.elements):
                val = self.generate(elem)
                item_ptr = self.builder.gep(data_ptr, [ir.Constant(self.int_type, i)])
                self.builder.store(val, item_ptr)
            
            struct = ir.Constant(self.array_struct_ty, [None, None, None])
            struct = self.builder.insert_value(struct, data_ptr, 0)
            struct = self.builder.insert_value(struct, ir.Constant(self.int_type, count), 1)
            struct = self.builder.insert_value(struct, ir.Constant(self.int_type, count), 2)
            return struct

        # --- Array Access ---
        elif isinstance(node, nodes.ArrayAccess):
            struct_ptr = self._get_var_ptr(node.name)
            struct = self.builder.load(struct_ptr)
            data_ptr = self.builder.extract_value(struct, 0)
            idx = self.generate(node.index)
            item_ptr = self.builder.gep(data_ptr, [idx])
            return self.builder.load(item_ptr)

        # --- Array Set ---
        elif isinstance(node, nodes.ArraySet):
            struct_ptr = self._get_var_ptr(node.name)
            struct = self.builder.load(struct_ptr)
            data_ptr = self.builder.extract_value(struct, 0)
            idx = self.generate(node.index)
            val = self.generate(node.value)
            item_ptr = self.builder.gep(data_ptr, [idx])
            self.builder.store(val, item_ptr)

        # --- Method Call ---
        elif isinstance(node, nodes.MethodCall):
            if node.method_name == "push":
                struct_ptr = self._get_var_ptr(node.obj_name)
                struct = self.builder.load(struct_ptr)
                
                data_ptr = self.builder.extract_value(struct, 0)
                size = self.builder.extract_value(struct, 1)
                
                new_size = self.builder.add(size, ir.Constant(self.int_type, 1))
                new_size_bytes = self.builder.mul(self.builder.zext(new_size, self.long_type), ir.Constant(self.long_type, 4))
                
                raw_ptr = self.builder.bitcast(data_ptr, self.string_type)
                new_raw_ptr = self.builder.call(self.realloc, [raw_ptr, new_size_bytes])
                new_data_ptr = self.builder.bitcast(new_raw_ptr, self.int_type.as_pointer())
                
                val = self.generate(node.args[0])
                item_ptr = self.builder.gep(new_data_ptr, [size]) 
                self.builder.store(val, item_ptr)
                
                new_struct = self.builder.insert_value(struct, new_data_ptr, 0)
                new_struct = self.builder.insert_value(new_struct, new_size, 1)
                new_struct = self.builder.insert_value(new_struct, new_size, 2)
                self.builder.store(new_struct, struct_ptr)

        # --- Assign ---
        elif isinstance(node, nodes.Assign):
            ptr = self._get_var_ptr(node.name)
            val = self.generate(node.value)
            self.builder.store(val, ptr)

        # --- If / Else ---
        elif isinstance(node, nodes.IfStatement):
            cond = self.generate(node.condition)
            if cond.type != self.bool_type:
                 cond = self.builder.icmp_unsigned('!=', cond, ir.Constant(cond.type, 0))
            
            if node.else_body:
                with self.builder.if_else(cond) as (then, otherwise):
                    with then: self.generate(node.body)
                    with otherwise: self.generate(node.else_body)
            else:
                with self.builder.if_then(cond):
                    self.generate(node.body)

        # --- Loop ---
        elif isinstance(node, nodes.RepeatLoop):
            count_val = self.generate(node.count)
            i_ptr = self.builder.alloca(self.int_type, name=node.iterator_name)
            self.builder.store(ir.Constant(self.int_type, 0), i_ptr)
            
            loop_cond = self.builder.append_basic_block("loop_cond")
            loop_body = self.builder.append_basic_block("loop_body")
            loop_end = self.builder.append_basic_block("loop_end")
            
            self.builder.branch(loop_cond)
            self.builder.position_at_end(loop_cond)
            curr_i = self.builder.load(i_ptr)
            cond = self.builder.icmp_signed('<', curr_i, count_val)
            self.builder.cbranch(cond, loop_body, loop_end)
            
            self.builder.position_at_end(loop_body)
            self.scope_stack.append({})
            self.scope_stack[-1][node.iterator_name] = i_ptr
            self.generate(node.body)
            self.scope_stack.pop()
            
            next_i = self.builder.add(self.builder.load(i_ptr), ir.Constant(self.int_type, 1))
            self.builder.store(next_i, i_ptr)
            self.builder.branch(loop_cond)
            self.builder.position_at_end(loop_end)

        # --- Print ---
        elif isinstance(node, nodes.Print):
            val = self.generate(node.expression)
            fmt = "%d\n\0"
            if val.type == self.float_type:
                fmt = "%f\n\0"
                val = self.builder.fpext(val, ir.DoubleType())
            elif val.type == self.bool_type:
                fmt = "%d\n\0"
            elif val.type == self.string_type:
                fmt = "%s\n\0"
            
            c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)), bytearray(fmt.encode("utf8")))
            global_fmt = ir.GlobalVariable(self.module, c_fmt.type, name=f"fmt_{id(node)}")
            global_fmt.linkage = 'internal'; global_fmt.global_constant = True; global_fmt.initializer = c_fmt
            
            fmt_ptr = self.builder.bitcast(global_fmt, self.string_type)
            self.builder.call(self.printf, [fmt_ptr, val])

        # --- Binary Operations (Includes String Concatenation Fix) ---
        elif isinstance(node, nodes.BinaryOp):
            lhs = self.generate(node.left)
            rhs = self.generate(node.right)
            op = node.op

            # 1. String Concatenation Fix
            if lhs.type == self.string_type and rhs.type == self.string_type:
                if op == "+":
                    # len1 = strlen(lhs)
                    len1 = self.builder.call(self.strlen, [lhs])
                    # len2 = strlen(rhs)
                    len2 = self.builder.call(self.strlen, [rhs])
                    
                    # total = len1 + len2 + 1
                    total_len = self.builder.add(len1, len2)
                    total_alloc = self.builder.add(total_len, ir.Constant(self.long_type, 1))
                    
                    # new_str = malloc(total)
                    new_str = self.builder.call(self.malloc, [total_alloc])
                    
                    # strcpy(new_str, lhs)
                    self.builder.call(self.strcpy, [new_str, lhs])
                    # strcat(new_str, rhs)
                    self.builder.call(self.strcat, [new_str, rhs])
                    
                    return new_str

            # 2. Logic OR
            if op == "OR":
                if lhs.type != self.bool_type:
                    lhs = self.builder.icmp_unsigned('!=', lhs, ir.Constant(lhs.type, 0))
                if rhs.type != self.bool_type:
                    rhs = self.builder.icmp_unsigned('!=', rhs, ir.Constant(rhs.type, 0))
                return self.builder.or_(lhs, rhs)

            # 3. Type Promotion
            is_float = (lhs.type == self.float_type or rhs.type == self.float_type)
            if is_float:
                if lhs.type == self.int_type: lhs = self.builder.sitofp(lhs, self.float_type)
                if rhs.type == self.int_type: rhs = self.builder.sitofp(rhs, self.float_type)

            if op == "+": return self.builder.fadd(lhs, rhs) if is_float else self.builder.add(lhs, rhs)
            if op == "-": return self.builder.fsub(lhs, rhs) if is_float else self.builder.sub(lhs, rhs)
            if op == "*": return self.builder.fmul(lhs, rhs) if is_float else self.builder.mul(lhs, rhs)
            if op == "/": 
                if not is_float:
                    lhs = self.builder.sitofp(lhs, self.float_type)
                    rhs = self.builder.sitofp(rhs, self.float_type)
                return self.builder.fdiv(lhs, rhs)

            if is_float:
                 if op == "==": return self.builder.fcmp_ordered('==', lhs, rhs)
                 if op == "!=": return self.builder.fcmp_ordered('!=', lhs, rhs)
                 if op == ">": return self.builder.fcmp_ordered('>', lhs, rhs)
                 if op == "<": return self.builder.fcmp_ordered('<', lhs, rhs)
                 if op == ">=": return self.builder.fcmp_ordered('>=', lhs, rhs)
                 if op == "<=": return self.builder.fcmp_ordered('<=', lhs, rhs)
            else:
                 if op == "==": return self.builder.icmp_signed('==', lhs, rhs)
                 if op == "!=": return self.builder.icmp_signed('!=', lhs, rhs)
                 if op == ">": return self.builder.icmp_signed('>', lhs, rhs)
                 if op == "<": return self.builder.icmp_signed('<', lhs, rhs)
                 if op == ">=": return self.builder.icmp_signed('>=', lhs, rhs)
                 if op == "<=": return self.builder.icmp_signed('<=', lhs, rhs)

        # --- Literals ---
        elif isinstance(node, nodes.Number):
            if "." in node.value: return ir.Constant(self.float_type, float(node.value))
            return ir.Constant(self.int_type, int(node.value))
        
        elif isinstance(node, nodes.Identifier):
            ptr = self._get_var_ptr(node.name)
            return self.builder.load(ptr, name=node.name)
        
        elif isinstance(node, nodes.String):
            text = node.value + "\0"
            c_str = ir.Constant(ir.ArrayType(ir.IntType(8), len(text)), bytearray(text.encode("utf8")))
            g = ir.GlobalVariable(self.module, c_str.type, name=f"str_{id(node)}")
            g.linkage = 'internal'
            g.global_constant = True
            g.initializer = c_str
            return self.builder.bitcast(g, self.string_type)