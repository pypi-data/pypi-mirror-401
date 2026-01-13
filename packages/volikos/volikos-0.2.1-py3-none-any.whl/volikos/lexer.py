from rply import LexerGenerator

class Lexer:
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        # Keywords
        self.lexer.add('PRINT', r'print')
        self.lexer.add('FUNC', r'func')
        self.lexer.add('RETURNS', r'returns')
        self.lexer.add('RETURN', r'return')
        self.lexer.add('VAR', r'var')
        self.lexer.add('CONST', r'const')
        self.lexer.add('REPEAT', r'repeat')
        self.lexer.add('AS', r'as')
        self.lexer.add('IF', r'if')
        self.lexer.add('ELSE', r'else')
        self.lexer.add('IS', r'is')
        self.lexer.add('OR', r'or')

        # Types
        self.lexer.add('TYPE_INT', r'int')
        self.lexer.add('TYPE_FLOAT', r'float')
        self.lexer.add('TYPE_STRING', r'string')

        # Symbols
        self.lexer.add('OPEN_PAREN', r'\(')
        self.lexer.add('CLOSE_PAREN', r'\)')
        self.lexer.add('OPEN_CURLY', r'\{')
        self.lexer.add('CLOSE_CURLY', r'\}')
        self.lexer.add('OPEN_BRACKET', r'\[')
        self.lexer.add('CLOSE_BRACKET', r'\]')
        self.lexer.add('DOT', r'\.')
        self.lexer.add('SEMI_COLON', r'\;')
        self.lexer.add('COLON', r'\:')
        self.lexer.add('COMMA', r'\,')
        self.lexer.add('EQUALS', r'\=')

        # Comparators
        self.lexer.add('EQ', r'\=\=')
        self.lexer.add('NEQ', r'\!\=')
        self.lexer.add('GTE', r'\>\=')
        self.lexer.add('LTE', r'\<\=')
        self.lexer.add('GT', r'\>')
        self.lexer.add('LT', r'\<')

        # Operators
        self.lexer.add('SUM', r'\+')
        self.lexer.add('SUB', r'\-')
        self.lexer.add('MUL', r'\*')
        self.lexer.add('DIV', r'\/')

        # Literals
        self.lexer.add('NUMBER', r'\d+(\.\d+)?')
        self.lexer.add('STRING_LITERAL', r'\".*?\"')
        self.lexer.add('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*')

        # Ignore spaces and comments
        self.lexer.ignore(r'\s+')
        self.lexer.ignore(r'\#.*')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()