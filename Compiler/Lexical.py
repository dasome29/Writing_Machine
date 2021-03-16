import lex


class Lexer(object):
    errors = []

    def __init__(self):
        self.lexer = lex.lex(object=self)

    reserved = {
        'START': 'START',
        'END': 'END',
        'Def': 'DEF',
        'Put': 'PUT',
        'Add': 'ADD',
        'ContinueUp': 'CONTINUEUP',
        'ContinueDown': 'CONTINUEDOWN',
        'ContinueRight': 'CONTINUERIGHT',
        'ContinueLeft': 'CONTINUELEFT',
        'Pos': 'POS',
        'PosX': 'POSX',
        'PosY': 'POSY',
        'UseColor': 'USECOLOR',
        'Down': 'DOWN',
        'Up': 'UP',
        'Begin': 'BEGIN',
        'Speed': 'SPEED',
        'Run': 'RUN',
        'Repeat': 'REPEAT',
        'If': 'IF',
        'Elif': 'ELIF',
        'Until': 'UNTIL',
        'While': 'WHILE',
        'Equal': 'EQUAL',
        'And': 'AND',
        'Or': 'OR',
        'Not': 'NOT',
        'Greater': 'GREATER',
        'Smaller': 'SMALLER',
        'Subtract': 'SUBTRACT',
        'Multiply': 'MULTIPLY',
        'Power': 'POWER',
        'Divide': 'DIVIDE',
        'Addition': 'ADDITION',
        'Random': 'RANDOM'
    }
    tokens = [
                 'WHITESPACE',
                 'LPAREN',
                 'RPAREN',
                 'LBRACKET',
                 'RBRACKET',
                 'COMMA',
                 'GREATERTHAN',
                 'LESSTHAN',
                 'EQUALTHAN',
                 'SEMICOLON',
                 'INTEGER',
                 'STRING',
                 'BOOL',
                 'ID',
                 'COMMENT'
             ] + list(reserved.values())

    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_COMMA = r'[,]'
    t_GREATERTHAN = r'\>'
    t_LESSTHAN = r'\<'
    t_EQUALTHAN = r'\='
    t_SEMICOLON = r'\;'
    t_ignore = r' '

    def input(self, data):
        self.lexer.input(data)

    def build(self, **kwargs):
        self.lexer = lex.lex(object=self, **kwargs)

    def token(self):
        return self.lexer.token()

    def t_WHITESPACE(self, t):
        r"""[ ]+"""
        pass

    def t_INTEGER(self, t):
        r"""\d+"""
        try:
            t.value = int(t.value)
        except ValueError:
            print("Integer value too large %d", t.value)
            t.value = 0
        return t

    def t_BOOL(self, t):
        r"""True|False"""
        try:
            if t.value == "True":
                t.value = True
            else:
                t.value = False
        except ValueError:
            print("Didn't find a boolean")
            t.value = False

        return t

    def t_STRING(self, t):
        r"""["]{1}[^"]*["]{1}"""
        t.value = str(t.value).replace('\n', " ")
        return t

    def t_ID(self, t):
        r"""[a-zA-Z][a-zA-Z0-9_@&?]*"""
        temp = self.reserved.get(t.value, 'ID')
        if temp == "ID":
            if not t.value[0].islower():
                self.t_error(t)
        t.type = temp
        return t

    def t_COMMENT(self, t):
        r"""\--.*"""
        pass

    def t_newline(self, t):
        r"""[\n]"""
        t.lexer.lineno += len(t.value)
        pass

    def t_error(self, t):
        self.errors.append(f'Found illegal character in line {t.lexer.lineno}: \n"{t.value}"')
        t.lexer.skip(1)
        pass

    def run(self, data):
        self.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break


# data = """
# Def var1 = "Hello";
# Def var2 = 2;
# START procedure []
#     Put var1 = "Bye";
#     Add[var2, 5];
#     PosX 20;
# END
# """

# lexer = Lexer()
# lexer.input(data)
# while True:
#     tok = lexer.lexer.token()
#     if not tok:
#         break
#     print(tok)
