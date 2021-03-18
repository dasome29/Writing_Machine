from Lexical import *
from Syntax import *
from Semantic import *



class Compiler:

    def compile(self, data):
        lexer = Lexer()
        parser = Parser(Lexer())
        lexer.run(data)
        if lexer.errors:
            return(lexer.errors[0])
        else:
            parsed = parser.parse(data)
            if parser.errors:
                return(parser.errors[0])
            else:
                semantic = Semantic()
                result = semantic.analyze(parsed)
                if semantic.errors:
                    return(semantic.errors[0])
                else:
                    return result


# val2 = ""

# val = """
# Def var1 = 10;
# Def var2 = False;
# START myFunc [num1, num2] 
#     While [Smaller(num1, num2);] [
#         Elif Equal(num1, Multiply(3, 5);); [PosX num1;] [PosY num1;];
#         Add[num1];
#         -- Pinga
#     ];
# END
# myFunc [10, 20];
# """

# compiler = Compiler()
# output = compiler.compile(val)

# if output:
#     for i in output:
#         print(i)
