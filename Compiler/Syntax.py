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
        """variable_def : DEF ID EQUALTHAN expression SEMICOLON"""
        p[0] = VariableDef()
        pass

    def p_put(self, p):
        """put : PUT ID EQUALTHAN expression SEMICOLON"""
        p[0] = Put()
        pass

    def p_add(self, p):
        """add : ADD LBRACKET ID COMMA expression RBRACKET SEMICOLON"""
        p[0] = Add()

    def p_add_one(self, p):
        """add : ADD LBRACKET ID RBRACKET SEMICOLON"""
        p[0] = Add()

    def p_continue(self, p):
        """continue : CONTINUEUP expression SEMICOLON
            | CONTINUEDOWN expression SEMICOLON
            | CONTINUERIGHT expression SEMICOLON
            | CONTINUELEFT expression SEMICOLON"""
        p[0] = Continue()
        pass

    def p_pos(self, p):
        """pos : POS LBRACKET expression COMMA expression RBRACKET SEMICOLON"""
        p[0] = Pos()
        pass

    def p_posX(self, p):
        """pos : POSX expression SEMICOLON"""
        p[0] = Pos()
        pass

    def p_posY(self, p):
        """pos : POSY expression SEMICOLON"""
        p[0] = Pos()
        pass

    def p_useColor(self, p):
        """usecolor : USECOLOR expression SEMICOLON"""
        p[0] = UseColor()
        pass

    def p_elevation(self, p):
        """elevation : UP SEMICOLON
                     | DOWN SEMICOLON"""
        p[0] = Elevation()
        pass

    def p_begin(self, p):
        """begin : BEGIN SEMICOLON"""
        p[0] = Begin()
        pass

    def p_speed(self, p):
        """speed : SPEED expression SEMICOLON"""
        p[0] = Speed()
        pass

    def p_run(self, p):
        """run : RUN LBRACKET compound_procedure RBRACKET SEMICOLON"""
        p[0] = Run()
        pass

    def p_repeat(self, p):
        """repeat : REPEAT expression LBRACKET compound_procedure RBRACKET SEMICOLON"""
        p[0] = Repeat()
        pass

    def p_if(self, p):
        """if : IF condition LBRACKET compound_procedure RBRACKET SEMICOLON"""
        p[0] = If()
        pass

    def p_elif(self, p):
        """elif : ELIF condition LBRACKET compound_procedure RBRACKET LBRACKET compound_procedure RBRACKET SEMICOLON"""
        p[0] = Elif()
        pass

    def p_until(self, p):
        """until : UNTIL LBRACKET compound_procedure RBRACKET LBRACKET condition RBRACKET SEMICOLON"""
        p[0] = Until()
        pass

    def p_while(self, p):
        """while : WHILE LBRACKET condition RBRACKET LBRACKET compound_procedure RBRACKET SEMICOLON"""
        p[0] = While()
        pass

    def p_condition(self, p):
        """condition : LPAREN condition RPAREN"""
        p[0] = p[2]
        pass

    def p_condition_operator(self, p):
        """condition : condition EQUALTHAN condition
                     | condition GREATERTHAN condition
                     | condition LESSTHAN condition
                     | expression"""
        try:
            if p[2] == "==":
                p[0] = p[1] == p[3]
            elif p[2] == ">":
                p[0] = p[1] > p[3]
            elif p[2] == "<":
                p[0] = p[1] < p[3]
        except IndexError:
            p[0] = p[1]
        pass

    def p_boolean(self, p):
        """boolean : AND LPAREN expression COMMA expression RPAREN SEMICOLON
                   | OR LPAREN expression COMMA expression RPAREN SEMICOLON
                   | GREATER LPAREN expression COMMA expression RPAREN SEMICOLON
                   | SMALLER LPAREN expression COMMA expression RPAREN SEMICOLON
                   | EQUAL LPAREN expression COMMA expression RPAREN SEMICOLON"""
        if p[1] == "And":
            p[0] = p[3] and p[5]
        elif p[1] == "Or":
            p[0] = p[3] or p[5]
        elif p[1] == "Greater":
            p[0] = p[3] > p[5]
        elif p[1] == "Less":
            p[0] = p[3] < p[5]
        elif p[1] == "Equal":
            p[0] = p[3] == p[5]
        pass

    def p_boolean_not(self, p):
        """boolean : NOT LPAREN expression RPAREN SEMICOLON"""
        p[0] = not p[3]
        pass

    def p_arithmetic(self, p):
        """arithmetic : MULTIPLY LPAREN expression COMMA expression RPAREN SEMICOLON
                      | DIVIDE LPAREN expression COMMA expression RPAREN SEMICOLON
                      | POWER LPAREN expression COMMA expression RPAREN SEMICOLON
                      | ADDITION LPAREN expression COMMA expression RPAREN SEMICOLON
                      | SUBTRACT LPAREN expression COMMA expression RPAREN SEMICOLON"""
        if p[1] == "Multiply":
            p[0] = p[3] * p[5]
        elif p[1] == "Divide":
            p[0] = p[3] // p[5]
        elif p[1] == "Power":
            p[0] = p[3] ** p[5]
        elif p[1] == "Addition":
            p[0] = p[3] + p[5]
        elif p[1] == "Subtract":
            p[0] = p[3] - p[5]
