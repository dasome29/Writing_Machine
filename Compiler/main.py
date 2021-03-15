from Lexical import *
from Syntax import *
from Semantic import *


class Compiler:
    def compile(self, data):
        lexer = Lexer()
        parser = Parser(Lexer())
        lexer.run(data)
        if lexer.errors:
            print(lexer.errors[0])
            pass
        else:
            parsed = parser.parse(data)
            if parser.errors:
                print(parser.errors[0])
                pass
            else:
                semantic = Semantic()
                result = semantic.analyze(parsed)
                if semantic.errors:
                    print(semantic.errors[0])
                    pass
                else:
                    return result

        return None


val2 = ""

val = """
Def var1 = "Hello";
Def var2 = 2;
Def var3 = 4;
Pos [var2, 0];
START procedure [] 
    Put var1 = "Bye"; 
    Add[var2, Multiply(3, 5);]; 
    PosX 20;
    PosY 2;
    ContinueUp var2;
    ContinueDown var3;
    Begin;
    Speed var3;
END
START myFunc [num1, num2] 
    PosX 40;
    PosY 5;
    ContinueUp num1;
    ContinueDown num2;
    Speed 50;
    Repeat var3 [procedure [];];
END
myFunc [10, 40];
"""

compiler = Compiler()
output = compiler.compile(val2)

if output:
    for i in output:
        print(i)
