class Node:
    pass

class Number(Node):
    def __init__(self, value):
        self.value = value

class String(Node):
    def __init__(self, value):
        self.value = value

class BinaryOp(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class VarDecl(Node):
    def __init__(self, name, var_type, value, is_mutable=True):
        self.name = name
        self.var_type = var_type
        self.value = value
        self.is_mutable = is_mutable

class Assign(Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Identifier(Node):
    def __init__(self, name):
        self.name = name

class Print(Node):
    def __init__(self, expression):
        self.expression = expression

class FunctionDef(Node):
    def __init__(self, name, args, return_type, body):
        self.name = name
        self.args = args
        self.return_type = return_type
        self.body = body

class RepeatLoop(Node):
    def __init__(self, count, iterator_name, body):
        self.count = count
        self.iterator_name = iterator_name
        self.body = body

class IfStatement(Node):
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body

class Return(Node):
    def __init__(self, value):
        self.value = value

# --- Arrays & Methods ---
class ArrayLiteral(Node):
    def __init__(self, elements):
        self.elements = elements

class ArrayAccess(Node):
    def __init__(self, name, index):
        self.name = name
        self.index = index

class ArraySet(Node):
    def __init__(self, name, index, value):
        self.name = name
        self.index = index
        self.value = value

class MethodCall(Node):
    def __init__(self, obj_name, method_name, args):
        self.obj_name = obj_name
        self.method_name = method_name
        self.args = args
