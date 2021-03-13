import yacc
from Semantic import *


class Parser(object):
    start = "program"

    def __init__(self, lexer):
        self.parser = None
        self.lexer = lexer
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self, start=self.start)

    def parse(self, data):
        self.parser.parse(data, self.lexer)

    def p_program(self, p):
        """program : compound_procedure"""
        p[0] = p[1]
        pass

    def p_compound_procedure(self, p):
        """compound_procedure : procedure_set"""
        p[0] = p[1]
        pass

    def p_procedure_set(self, p):
        """procedure_set : procedure procedure_set
                        | procedure"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]
        pass

    def p_procedure(self, p):
        """procedure : function
                     | variable_def
                     | put
                     | add
                     | continue
                     | pos
                     | useColor
                     | elevation
                     | begin
                     | speed
                     | run
                     | repeat
                     | if
                     | elif
                     | until
                     | while
                     | empty"""
        p[0] = p[1]
        pass

    def p_expression(self, p):
        """expression : condition
                      | boolean
                      | arithmetic
                      | INTEGER
                      | BOOL
                      | STRING
                      | ID
                      | empty"""
        p[0] = p[1]
        pass

    def p_expression_set(self, p):
        """expression_set : expression expression_set
                          | expression"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]
        pass

    def p_parameters(self, p):
        """parameters : parameter_set"""
        p[0] = p[1]
        pass

    def p_parameter_set(self, p):
        """parameter_set : ID COMMA parameter_set
                         | ID
                         | empty"""
        try:
            p[0] = [p[1]] + p[3]
        except IndexError:
            p[0] = [p[1]]
        pass

    def p_function(self, p):
        """function : START ID parameters compound_procedure END"""
        p[0] = Function()
        pass

    def p_variable_def(self, p):
        """variable_def : Def ID EQUALTHAN expression SEMICOLON"""
        p[0] = VariableDef()
        pass

    def p_put(self, p):
        """put : Put ID EQUALTHAN expression SEMICOLON"""
        p[0] = Put()
        pass

    def p_add(self, p):
        """add : Add LBRACKET ID COMMA expression RBRACKET SEMICOLON"""
        p[0] = Add()

    def p_add_one(self, p):
        """add : Add LBRACKET ID RBRACKET SEMICOLON"""
        p[0] = Add()

    def p_continue(self, p):
        """continue : ContinueUp expression SEMICOLON
            | ContinueDown expression SEMICOLON
            | ContinueRight expression SEMICOLON
            | ContinueLeft expression SEMICOLON"""
        p[0] = Continue()

    def p_pos(self, p):
        """pos : Pos LBRACKET expression COMMA expression RBRACKET SEMICOLON"""
        p[0] = Pos()
        pass

    def p_posX(self, p):
        """pos : PosX expression SEMICOLON"""
        p[0] = Pos()
        pass

    def p_posY(self, p):
        """pos : PosY expression SEMICOLON"""
        p[0] = Pos()
        pass

    def p_useColor(self, p):
        """usecolor : UseColor expression SEMICOLON"""
        p[0] = UseColor()
        pass

    def p_elevation(self, p):
        """elevation : Up SEMICOLON
                     | Down SEMICOLON"""
        p[0] = Elevation()
        pass

    def p_begin(self, p):
        """begin : Begin SEMICOLON"""
        p[0] = Begin()
        pass

    def p_speed(self, p):
        """speed : Speed expression SEMICOLON"""
        p[0] = Speed()
        pass

    def p_run(self, p):
        """run : Run LBRACKET compound_procedure RBRACKET SEMICOLON"""
        p[0] = Run()
        pass

    def p_repeat(self, p):
        """repeat : Repeat expression LBRACKET compound_procedure RBRACKET SEMICOLON"""
        p[0] = Repeat()
        pass

    def p_if(self, p):
        """if : If condition LBRACKET compound_procedure RBRACKET SEMICOLON"""
        p[0] = If()
        pass

    def p_elif(self, p):
        """elif : Elif condition LBRACKET compound_procedure RBRACKET LBRACKET compound_procedure RBRACKET SEMICOLON"""
        p[0] = Elif()
        pass

    def p_until(self, p):
        """until : Until LBRACKET compound_procedure RBRACKET LBRACKET condition RBRACKET SEMICOLON"""
        p[0] = Until()
        pass

    def p_while(self, p):
        """while : While LBRACKET condition RBRACKET LBRACKET compound_procedure RBRACKET SEMICOLON"""
        p[0] = While()
        pass
