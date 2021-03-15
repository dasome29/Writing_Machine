from Utilities import *


class Semantic:
    errors = []

    def analyze(self, program):
        program.solve()
        if program.errors:
            self.errors = program.errors
        else:
            return program.output_list


class Procedure:
    table = []
    global_table = []
    program = None

    def __init__(self):
        pass

    def solve(self, program, table):
        pass


class Program:
    errors = []
    output_list = []
    colors = 3

    def __init__(self, procedures):
        super().__init__()
        self.procedures = procedures
        self.table = []
        self.scope_table = []
        self.scope_table.append(self.table)

    def solve(self):
        for i in self.procedures:
            if i:
                i.solve(self, self.scope_table)
            else:
                self.error("Semantic", "main", "Null procedure",
                           "It's possible that a null object was found while compiling, check if your file was not empty")
            if self.errors:
                return self.errors[0]
        for i in self.output_list:
            print(i)
        return self.output_list

    def error(self, error_type, method, title, detail):
        self.errors.append(f'{error_type} Error: {title} in {method} method\n--- {detail}')

    def output(self, instruction):
        self.output_list.append(instruction)


class Function(Procedure):
    def __init__(self, name, parameters, procedures):
        super().__init__()
        self.name = name
        self.parameters = parameters
        self.procedures = procedures

    def solve(self, program, scope_table):
        self.program = program
        self.global_table = scope_table + [self.table]
        self.global_table[::-1][1].append({'name': self.name, 'value': self})


class FunctionCall(Procedure):
    def __init__(self, name, parameters):
        super().__init__()
        self.parameters = parameters
        self.name = name

    def setParameters(self, parameter_names):
        temp = []
        for i in range(len(parameter_names)):
            value = self.parameters[i]
            if isinstance(value, Expression):
                value = value.solve(self.program, self.global_table)
            temp.append({'name': parameter_names[i], 'value': value})
        self.table += temp

    def solve(self, program, scope_table):
        self.program = program
        self.global_table = scope_table + [self.table]
        if variableExist(self.global_table, self.name):
            temp = getValue(self.global_table, self.name)
            if isinstance(temp, Function):
                f_parameters = temp.parameters
                if len(f_parameters) == len(self.parameters):
                    self.setParameters(f_parameters)
                    for i in temp.procedures:
                        i.solve(program, self.global_table)
                else:
                    self.program.error("Semantic", f'{self.name}', "Invalid parameters",
                                       f"""Didn't provide de same amount of parameters as in the definition""")
            else:
                self.program.error("Semantic", f'{self.name}', "Wrong variable type",
                                   f'Expected variable type Function, found {type(temp)}')
        else:
            self.program.error("Semantic", f'{self.name}', "Variable not found",
                               f'Variable {self.name} is not declared.')


class VariableDef(Procedure):
    def __init__(self, name, value):
        self.name = name
        self.value = value
        super().__init__()

    def solve(self, program, scope_table):
        self.program = program
        self.global_table = scope_table + [self.table]
        if isinstance(self.value, Expression):
            self.value = self.value.solve(self.program, self.global_table)
        self.global_table[::-1][1].append({'name': self.name, 'value': self.value})


class Put(Procedure):
    def __init__(self, var1, var2):
        super().__init__()
        self.var2 = var2
        self.var1 = var1

    def solve(self, program, scope_table):
        self.program = program
        self.global_table = scope_table + [self.table]
        if variableExist(self.global_table, self.var1):
            temp = getValue(self.global_table, self.var2)
            if isinstance(temp, Expression):
                temp = temp.solve(self.program, self.global_table)
            if type(temp) != Procedure:
                if isinstance(temp, type(self.var1)):
                    changeValue(self.global_table, self.var1, temp)
                else:
                    self.program.error("Semantic", "Put", "Wrong variable type",
                                       f'Expected {type(self.var1)}, found {type(temp)}')
            else:
                self.program.error("Semantic", "Put", "Wrong variable type", "New value must be a simple expression")
        else:
            self.program.error("Semantic", "Put", "Variable not found", f'Variable {self.var1} is not declared')


class Add(Procedure):
    def __init__(self, name, value=None):
        self.name = name
        self.value = value
        super().__init__()

    def solve(self, program, scope_table):
        self.program = program
        self.global_table = scope_table + [self.table]
        if variableExist(self.global_table, self.name):
            value = getValue(self.global_table, self.name)
            if isinstance(value, int):
                if self.value:
                    temp = self.value
                    if variableExist(self.global_table, temp):
                        temp = getValue(self.global_table, temp)
                    if isinstance(temp, Expression):
                        temp = temp.solve(self.program, self.global_table)
                    if isinstance(temp, int):
                        changeValue(self.global_table, self.name, value + temp)
                    else:
                        self.program.error("Semantic", "Add", "Wrong type in second variable",
                                           f'value must be an integer')
                else:
                    changeValue(self.global_table, self.name, value + 1)
            else:
                self.program.error("Semantic", "Add", "Wrong variable type", f'value must be an integer')
        else:
            self.program.error("Semantic", "Add", "Variable not found", f'Variable {self.name} is not declared')


class Continue(Procedure):
    def __init__(self, name, value):
        self.name = name
        self.value = value
        super().__init__()

    def solve(self, program, scope_table):
        self.program = program
        self.global_table = scope_table + [self.table]
        error = ""
        temp = getValue(self.global_table, self.value)
        if not variableExist(self.global_table, self.value):
            error = "and was not found"
        if isinstance(temp, Expression):
            temp = temp.solve(self.program, self.global_table)
        if isinstance(temp, int):
            self.program.output(f'{self.name} {temp}')
        else:
            self.program.error("Semantic", f'{self.name}', "Invalid parameter",
                               f'Variable {self.value} is not accepted {error}')


class Pos(Procedure):
    def __init__(self, value_x, value_y):
        self.value_x = value_x
        self.value_y = value_y
        super().__init__()

    def solve(self, program, scope_table):
        self.program = program
        self.global_table = scope_table + [self.table]
        error = []
        buffer = [False, False]
        temp_x = getValue(self.global_table, self.value_x)
        if not variableExist(self.global_table, self.value_x):
            error.append(f'{self.value_x}')
        if isinstance(temp_x, Expression):
            temp_x = temp_x.solve(self.program, self.global_table)
        if isinstance(temp_x, int):
            buffer[0] = True
        temp_y = getValue(self.global_table, self.value_y)
        if not variableExist(self.global_table, self.value_y):
            error.append(f'{self.value_y}')
        if isinstance(temp_y, Expression):
            temp_y = temp_y.solve(self.program, self.global_table)
        if isinstance(temp_y, int):
            buffer[1] = True
        if buffer[0] and buffer[1]:
            self.program.output(f'Pos {temp_x} {temp_y}')
        else:
            if error:
                try:
                    error = f', {error[0]} and {error[1]} were not found'
                except IndexError:
                    error = f', {error[0]} was not found'
            error = ""
            self.program.error("Semantic", f'Pos', "Wrong variable type",
                               f'values must be integers {error}')


class PosAxis(Procedure):
    def __init__(self, name, value):
        super().__init__()
        self.name = name
        self.value = value

    def solve(self, program, scope_table):
        self.program = program
        self.global_table = scope_table + [self.table]
        error = ""
        temp = getValue(self.global_table, self.value)
        if not variableExist(self.global_table, self.value):
            error = "and was not found"
        if isinstance(temp, Expression):
            temp = temp.solve(self.program, self.global_table)
        if isinstance(temp, int):
            self.program.output(f'{self.name} {temp}')
        else:
            self.program.error("Semantic", f'{self.name}', "Invalid value",
                               f'Variable {self.value} is not accepted {error}')


class UseColor(Procedure):
    def __init__(self, value):
        self.value = value
        super().__init__()

    def solve(self, program, scope_table):
        self.program = program
        self.global_table = scope_table + [self.table]
        temp = getValue(self.global_table, self.value)
        error = ""
        if not variableExist(self.global_table, self.value):
            error = "and was not found"
        if isinstance(temp, Expression):
            temp = temp.solve(self.program, self.global_table)
        if isinstance(temp, int):
            if 0 < temp <= self.program.colors:
                self.program.output(f'UseColor {self.value}')
            else:
                self.program.error("Semantic", f'UseColor', "Invalid value",
                                   f'Value must be an integer between 0 and {self.program.colors}')
        else:
            self.program.error("Semantic", f'UseColor', "Invalid parameter",
                               f'Variable {self.value} is not integer {error}')


class Elevation(Procedure):
    def __init__(self, value):
        self.value = value
        super().__init__()

    def solve(self, program, scope_table):
        self.program = program
        self.global_table = scope_table + [self.table]
        self.program.output(self.value)


class Begin(Procedure):
    def __init__(self):
        super().__init__()

    def solve(self, program, scope_table):
        self.program = program
        self.global_table = scope_table + [self.table]
        self.program.output("Pos 0 0")


class Speed(Procedure):
    def __init__(self, value):
        self.value = value
        super().__init__()

    def solve(self, program, scope_table):
        self.program = program
        self.global_table = scope_table + [self.table]
        error = ""
        temp = getValue(self.global_table, self.value)
        if not variableExist(self.global_table, self.value):
            error = "and was not found"
        if isinstance(temp, Expression):
            temp = temp.solve(self.program, self.global_table)
        if isinstance(temp, int):
            self.program.output(f'Speed {temp}')
        else:
            self.program.error("Semantic", f'Speed', "Invalid value",
                               f'Variable {self.value} is not accepted {error}')


class Run(Procedure):
    def __init__(self, procedures):
        self.procedures = procedures
        super().__init__()

    def solve(self, program, scope_table):
        self.program = program
        self.global_table = scope_table + [self.table]
        for i in self.procedures:
            i.solve(self.program, self.global_table)


class Repeat(Procedure):
    def __init__(self, value, procedures):
        self.value = value
        self.procedures = procedures
        super().__init__()

    def solve(self, program, scope_table):
        self.program = program
        self.global_table = scope_table + [self.table]
        error = ""
        temp = getValue(self.global_table, self.value)
        if variableExist(self.global_table, self.value):
            error = "and was not found"
        if isinstance(temp, Expression):
            temp = temp.solve(self.program, self.global_table)
        if isinstance(temp, int):
            for i in range(temp):
                for j in self.procedures:
                    j.solve(self.program, self.global_table)
        else:
            self.program.error("Semantic", f'Repeat', "Invalid parameter",
                               f'Variable {self.value} is not accepted {error}')


class If(Procedure):
    def __init__(self, condition, procedures):
        self.condition = condition
        self.procedures = procedures
        super().__init__()

    def solve(self, program, scope_table):
        self.program = program
        self.global_table = scope_table + [self.table]
        if self.condition:
            for i in self.procedures:
                i.solve(self.program, self.global_table)


class Elif(Procedure):
    def __init__(self, condition, procedures_1, procedures_2):
        self.condition = condition
        self.procedures_1 = procedures_1
        self.procedures_2 = procedures_2
        super().__init__()

    def solve(self, program, scope_table):
        self.program = program
        self.global_table = scope_table + [self.table]
        temp = self.procedures_1
        if not self.condition:
            temp = self.procedures_2
        for i in temp:
            i.solve(self.program, self.global_table)


class Until(Procedure):
    def __init__(self, condition, procedures):
        self.condition = condition
        self.procedures = procedures
        super().__init__()

    def solve(self, program, scope_table):
        self.program = program
        self.global_table = scope_table + [self.table]
        while True:
            for i in self.procedures:
                i.solve(self.program, self.global_table)
            if self.condition:
                break


class While(Procedure):
    def __init__(self, condition, procedures):
        self.condition = condition
        self.procedures = procedures
        super().__init__()

    def solve(self, program, scope_table):
        self.program = program
        self.global_table = scope_table + [self.table]
        while self.condition:
            for i in self.procedures:
                i.solve(self.program, self.global_table)


class Expression:
    def __init__(self):
        pass

    def solve(self, program, scope_table):
        pass


class Arithmetic(Expression):
    solved = False

    def __init__(self, value1, value2):
        super().__init__()
        self.value1 = value1
        self.value2 = value2

    def solve(self, program, scope_table):
        if not self.solved:
            self.value1 = self.getValue(program, scope_table, self.value1)
            self.value2 = self.getValue(program, scope_table, self.value2)

    def getValue(self, program, scope_table, value):
        error = ""
        temp = getValue(scope_table, value)
        if not variableExist(scope_table, value):
            error = "and was not found"
        if isinstance(temp, Arithmetic):
            temp = temp.solve(program, scope_table)
        if isinstance(temp, int):
            return temp
        else:
            program.error("Semantic", f'Speed', "Invalid value",
                          f'Variable {value} is not accepted {error}')
        return 1


class Addition(Arithmetic):
    def __init__(self, value1, value2):
        super().__init__(value1, value2)

    def solve(self, program, scope_table):
        super(Addition, self).solve(program, scope_table)
        return self.value1 + self.value2


class Subtract(Arithmetic):
    def __init__(self, value1, value2):
        super().__init__(value1, value2)

    def solve(self, program, scope_table):
        super(Subtract, self).solve(program, scope_table)
        return self.value1 - self.value2


class Multiply(Arithmetic):
    def __init__(self, value1, value2):
        super().__init__(value1, value2)

    def solve(self, program, scope_table):
        super(Multiply, self).solve(program, scope_table)
        return self.value1 * self.value2


class Power(Arithmetic):
    def __init__(self, value1, value2):
        super().__init__(value1, value2)

    def solve(self, program, scope_table):
        super(Power, self).solve(program, scope_table)
        return self.value1 * self.value2


class Divide(Arithmetic):
    def __init__(self, value1, value2):
        super().__init__(value1, value2)

    def solve(self, program, scope_table):
        super(Divide, self).solve(program, scope_table)
        if not self.value2:
            program.error("Semantic", "Divide", "Division by zero", "value2 ended up been zero")
            return 1
        return self.value1 // self.value2


class Boolean(Expression):
    solved = False

    def __init__(self, value1, value2):
        super().__init__()
        self.value1 = value1
        self.value2 = value2

    def solve(self, program, scope_table):
        if not self.solved:
            self.value1 = self.getValue(program, scope_table, self.value1)
            self.value2 = self.getValue(program, scope_table, self.value2)

    def getValue(self, program, scope_table, value):
        error = ""
        temp = getValue(scope_table, value)
        if isinstance(temp, Boolean):
            temp = temp.solve(program, scope_table)
        if not variableExist(scope_table, value):
            error = "and was not found"
        if isinstance(temp, bool):
            return temp
        else:
            program.error("Semantic", f'Speed', "Invalid value",
                          f'Variable {value} is not accepted {error}')
        return 1


class And(Boolean):
    def __init__(self, value1, value2):
        super().__init__(value1, value2)

    def solve(self, program, scope_table):
        super(And, self).solve(program, scope_table)
        return self.value1 and self.value2


class Or(Boolean):
    def __init__(self, value1, value2):
        super().__init__(value1, value2)

    def solve(self, program, scope_table):
        super(Or, self).solve(program, scope_table)
        return self.value1 or self.value2


class Greater(Boolean):
    def __init__(self, value1, value2):
        super().__init__(value1, value2)

    def solve(self, program, scope_table):
        super(Greater, self).solve(program, scope_table)
        return self.value1 > self.value2


class Less(Boolean):
    def __init__(self, value1, value2):
        super().__init__(value1, value2)

    def solve(self, program, scope_table):
        super(Less, self).solve(program, scope_table)
        return self.value1 < self.value2


class Equal(Boolean):
    def __init__(self, value1, value2):
        super().__init__(value1, value2)

    def solve(self, program, scope_table):
        super(Equal, self).solve(program, scope_table)
        return self.value1 == self.value2


class Not(Boolean):
    def __init__(self, value1):
        super().__init__(value1, None)

    def solve(self, program, scope_table):
        self.value1 = self.getValue(program, scope_table)
        return not self.value1
