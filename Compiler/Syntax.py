import yacc


class Parser(object):
    start = "program"

    def __init__(self, lexer):
        self.parser = None
        self.lexer = lexer
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self, start=self.start)

    def parse(self, data):
        self.parser.parse(data, self.lexer)
