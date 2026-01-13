from rply import ParserGenerator
from . import ast_nodes as nodes

class Parser:
    def __init__(self):
        self.pg = ParserGenerator(
            # Token List
            ['NUMBER', 'STRING_LITERAL', 'IDENTIFIER', 
             'PRINT', 'FUNC', 'RETURNS', 'VAR', 'CONST', 
             'REPEAT', 'AS', 'IF', 'ELSE', 'IS', 'OR',
             'TYPE_INT', 'TYPE_FLOAT', 'TYPE_STRING',
             'OPEN_PAREN', 'CLOSE_PAREN', 'OPEN_CURLY', 'CLOSE_CURLY',
             'OPEN_BRACKET', 'CLOSE_BRACKET', 'DOT',
             'SEMI_COLON', 'COLON', 'COMMA', 'EQUALS',
             'SUM', 'SUB', 'MUL', 'DIV',
             'GT', 'LT', 'EQ', 'NEQ', 'GTE', 'LTE', 'RETURN'], # Added RETURN
            
            # Precedence (Lowest to Highest)
            precedence=[
                ('left', ['OR']),
                ('left', ['EQ', 'NEQ', 'GT', 'LT', 'GTE', 'LTE', 'IS']),
                ('left', ['SUM', 'SUB']),
                ('left', ['MUL', 'DIV']),
            ]
        )

    def parse(self):
        @self.pg.production('program : statement_list')
        def program(p):
            return p[0]

        @self.pg.production('statement_list : statement_list statement')
        def statement_list(p):
            return p[0] + [p[1]]

        @self.pg.production('statement_list : statement')
        def statement_list_single(p):
            return [p[0]]

        # --- Statements (Must end with SEMI_COLON unless compound) ---
        
        @self.pg.production('statement : VAR IDENTIFIER COLON type_name EQUALS expression SEMI_COLON')
        def var_decl(p):
            return nodes.VarDecl(p[1].getstr(), p[3], p[5], is_mutable=True)

        @self.pg.production('statement : CONST IDENTIFIER COLON type_name EQUALS expression SEMI_COLON')
        def const_decl(p):
            return nodes.VarDecl(p[1].getstr(), p[3], p[5], is_mutable=False)

        @self.pg.production('statement : IDENTIFIER EQUALS expression SEMI_COLON')
        def assignment(p):
            return nodes.Assign(p[0].getstr(), p[2])

        @self.pg.production('statement : PRINT OPEN_PAREN expression CLOSE_PAREN SEMI_COLON')
        def print_stmt(p):
            return nodes.Print(p[2])
            
        @self.pg.production('statement : IDENTIFIER OPEN_BRACKET expression CLOSE_BRACKET EQUALS expression SEMI_COLON')
        def array_set(p):
            return nodes.ArraySet(p[0].getstr(), p[2], p[5])

        @self.pg.production('statement : IDENTIFIER DOT IDENTIFIER OPEN_PAREN expr_list CLOSE_PAREN SEMI_COLON')
        def method_call(p):
            return nodes.MethodCall(p[0].getstr(), p[2].getstr(), p[4])

        # NEW: Return Statement
        @self.pg.production('statement : RETURN expression SEMI_COLON')
        def return_stmt(p):
            # We need a Return Node. For now, we can reuse Assign or make a new one.
            # Let's assume we add a Return node to ast_nodes.py
            return nodes.Return(p[1])

        # --- Compound Statements (No Semicolon) ---
        @self.pg.production('statement : FUNC IDENTIFIER OPEN_PAREN CLOSE_PAREN block')
        def func_void(p):
            return nodes.FunctionDef(p[1].getstr(), [], "void", p[4])

        # Func with args
        @self.pg.production('statement : FUNC IDENTIFIER OPEN_PAREN arg_list CLOSE_PAREN block')
        def func_void_args(p):
            return nodes.FunctionDef(p[1].getstr(), p[3], "void", p[5])

        @self.pg.production('statement : FUNC IDENTIFIER OPEN_PAREN arg_list CLOSE_PAREN RETURNS type_name block')
        def func_ret_args(p):
            return nodes.FunctionDef(p[1].getstr(), p[3], p[6], p[7])
            
        @self.pg.production('statement : REPEAT expression AS IDENTIFIER block')
        def repeat(p):
            return nodes.RepeatLoop(p[1], p[3].getstr(), p[4])

        @self.pg.production('statement : IF expression block')
        def if_std(p):
             return nodes.IfStatement(p[1], p[2])

        @self.pg.production('statement : IF expression block ELSE block')
        def if_else(p):
            return nodes.IfStatement(p[1], p[2], p[4])

        # --- Comma Syntax (Specific Rules) ---
        # We explicitly define the allowed "small statements" inside comma syntax
        # to avoid conflicts with the main statement logic.
        
        @self.pg.production('comma_stmt : PRINT OPEN_PAREN expression CLOSE_PAREN')
        def comma_print(p):
            return nodes.Print(p[2])
            
        @self.pg.production('comma_stmt : IDENTIFIER EQUALS expression')
        def comma_assign(p):
            return nodes.Assign(p[0].getstr(), p[2])

        @self.pg.production('statement : IF expression COMMA comma_stmt COMMA ELSE comma_stmt SEMI_COLON')
        def if_comma_else(p):
            return nodes.IfStatement(p[1], [p[3]], [p[6]])

        @self.pg.production('statement : IF expression COMMA comma_stmt SEMI_COLON')
        def if_comma(p):
            return nodes.IfStatement(p[1], [p[3]])

        # --- Function Arguments ---
        @self.pg.production('arg_list : IDENTIFIER COLON type_name')
        def arg_single(p):
            return [(p[0].getstr(), p[2])]

        @self.pg.production('arg_list : arg_list COMMA IDENTIFIER COLON type_name')
        def arg_multi(p):
            return p[0] + [(p[2].getstr(), p[4])]
            
        # --- Blocks ---
        @self.pg.production('block : OPEN_CURLY statement_list CLOSE_CURLY')
        def block(p):
            return p[1]

        # --- Expressions ---
        @self.pg.production('expression : expression IS expression OR expression')
        def smart_or(p):
            cond1 = nodes.BinaryOp("==", p[0], p[2])
            cond2 = nodes.BinaryOp("==", p[0], p[4])
            return nodes.BinaryOp("OR", cond1, cond2)

        @self.pg.production('expression : expression SUM expression')
        @self.pg.production('expression : expression SUB expression')
        @self.pg.production('expression : expression MUL expression')
        @self.pg.production('expression : expression DIV expression')
        @self.pg.production('expression : expression OR expression')
        @self.pg.production('expression : expression GT expression')
        @self.pg.production('expression : expression LT expression')
        @self.pg.production('expression : expression EQ expression')
        @self.pg.production('expression : expression NEQ expression')
        @self.pg.production('expression : expression IS expression')
        @self.pg.production('expression : expression GTE expression')
        @self.pg.production('expression : expression LTE expression')
        def binop(p):
            op = p[1].gettokentype()
            if op == 'IS': op = '==' 
            elif op == 'EQ': op = '=='
            elif op == 'NEQ': op = '!='
            elif op == 'GT': op = '>'
            elif op == 'LT': op = '<'
            elif op == 'GTE': op = '>='
            elif op == 'LTE': op = '<='
            elif op == 'SUM': op = '+'
            elif op == 'SUB': op = '-'
            elif op == 'MUL': op = '*'
            elif op == 'DIV': op = '/'
            elif op == 'OR': op = 'OR'
            return nodes.BinaryOp(op, p[0], p[2])

        @self.pg.production('expression : OPEN_BRACKET expr_list CLOSE_BRACKET')
        def array_lit(p):
            return nodes.ArrayLiteral(p[1])

        @self.pg.production('expression : IDENTIFIER OPEN_BRACKET expression CLOSE_BRACKET')
        def array_access(p):
            return nodes.ArrayAccess(p[0].getstr(), p[2])

        @self.pg.production('expr_list : expression')
        def expr_list_single(p):
            return [p[0]]
        @self.pg.production('expr_list : expr_list COMMA expression')
        def expr_list_multi(p):
            return p[0] + [p[2]]

        @self.pg.production('expression : NUMBER')
        def number(p):
            return nodes.Number(p[0].getstr())
        @self.pg.production('expression : STRING_LITERAL')
        def string_lit(p):
            return nodes.String(p[0].getstr()[1:-1])
        
        # FIX: Explicit rule for Variable Access
        @self.pg.production('expression : IDENTIFIER')
        def ident(p):
            return nodes.Identifier(p[0].getstr())
            
        @self.pg.production('type_name : TYPE_INT')
        @self.pg.production('type_name : TYPE_FLOAT')
        @self.pg.production('type_name : TYPE_STRING')
        def typename(p):
            return p[0].getstr()
        
        @self.pg.production('type_name : TYPE_INT OPEN_BRACKET CLOSE_BRACKET')
        def type_int_array(p):
            return "int[]"

        @self.pg.error
        def error_handle(token):
            raise ValueError(f"Syntax Error: Unexpected token '{token.gettokentype()}' at position {token.source_pos}")

        return self.pg.build()