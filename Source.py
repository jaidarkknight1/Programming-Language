class Interpreter:
    def __init__(self):
        self.varmap = {}
        self.validExpression = ['BARABAR', 'LIKHO', 'AGAR', 'JABTAK', 'KELIYE', 'SAMAPT_JABTAK', 'SAMAPT_AGAR']
        self.validOperators = ['=', '+', '-', '*', '/', '%', '>', '<', '==', '&']
        self.total_lines_interpreted = 0

    def my_for(self, init, condition, iteration, block):
        self.interpret(init)
        while self.evaluate_expression(condition):
            self.interpret(block)
            self.interpret(iteration)

    def my_if_else(self, condition, if_block, else_block):
        condition = condition[1:]
        result = self.evaluate_expression(condition)
        if result:
            self.interpret(if_block)
        else:
            self.interpret(else_block)

    def my_while(self, condition, block):
        condition = condition[1:]
        while self.evaluate_expression(condition):
            self.interpret(block)

    def my_assign(self, words_Arr):
        if len(words_Arr) <= 2:
            print("Invalid assignment statement")
            return

        var_name = words_Arr[1]
        expr = words_Arr[2:]

        result = self.evaluate_expression(expr)

        if result is not None:
            self.varmap[var_name] = result
        else:
            print("Invalid expression")

    def my_print(self, statement):
        var_name = statement.split()[1]
        if '"' in var_name:
            quoteIndex = statement.index('"')
            endIndex = statement.index('"', quoteIndex + 1)
            print(statement[quoteIndex + 1:endIndex])
        elif var_name in self.varmap:
            print(self.varmap[var_name])
        else:
            print("Variable is not defined")

    def evaluate_expression(self, expr):
        if not expr:
            return None

        stack = []
        for element in expr:
            if element.isdigit():
                stack.append(float(element))
            elif element in self.validOperators:
                if len(stack) < 2:
                    return None
                b = stack.pop()
                a = stack.pop()

                if element == '+':
                    stack.append(a + b)
                elif element == '-':
                    stack.append(a - b)
                elif element == '*':
                    stack.append(a * b)
                elif element == '/':
                    stack.append(a / b)
                elif element == '%':
                    stack.append(a % b)
                elif element == '<':
                    stack.append(a < b)
                elif element == '>':
                    stack.append(a > b)
                elif element == '==':
                    stack.append(a == b)
                elif element == '&':
                    stack.append(a and b)
            elif element in self.varmap:
                stack.append(self.varmap[element])
            else:
                return None

        return stack[0] if stack else None

    def interpret(self, program):
        if program is None:
            return
        stmts = program.split("\n")
        skip = False
        for index, line in enumerate(stmts):
            self.total_lines_interpreted += 1
            lineArr = line.split()
            if skip:
                skip = False
                continue
            if not lineArr:
                continue

            if not lineArr[0] in self.validExpression:
                print("Statement not defined in grammar")
                continue

            if lineArr[0] == 'BARABAR':
                self.my_assign(lineArr)
            elif lineArr[0] == 'LIKHO':
                self.my_print(line)
            elif lineArr[0] == 'AGAR':
                end_index = -1
                for i in range(len(stmts)-1, index, -1):
                    if(stmts[i] == 'SAMAPT_AGAR'):
                        end_index = i
                        break

                if_block = "\n".join(stmts[stmts.index(line) + 1:end_index])
                else_block = None
                if 'ELSE' in if_block:
                    else_index = if_block.index('ELSE')
                    else_block = if_block[else_index + 5:]
                    if_block = if_block[:else_index]
                skip = True
                self.my_if_else(lineArr, if_block, else_block)
            elif lineArr[0] == 'JABTAK':
                condition = line.split('JABTAK', 1)[1].strip()
                end_index = stmts.index('SAMAPT_JABTAK', stmts.index(line))
                block = "\n".join(stmts[stmts.index(line) + 1:end_index])
                self.my_while(condition, block)
            elif lineArr[0] == 'KELIYE':
                init_index = lineArr.index('TO')
                init = "BARABAR " + " ".join(lineArr[1:init_index])
                condition = [lineArr[1], lineArr[4], '<']
                iteration = "BARABAR " + lineArr[1] + " " + lineArr[1] + " 1 +"
                end_index = stmts.index('SAMAPT_KELIYE', stmts.index(line))
                block = "\n".join(stmts[stmts.index(line) + 1:end_index])
                self.my_for(init, condition, iteration, block)

# Sample Programs
#program1 = """
#LIKHO "PROGRAM 1"
#BARABAR x 10
#BARABAR y 20
#LIKHO x
#LIKHO y
#AGAR x y >
 #   LIKHO "x zyada hai y se"
#WARNA
 #   LIKHO "y zyada hai x se"
#SAMAPT_AGAR
#"""

program2 = """
LIKHO "PROGRAM 2"
BARABAR x 0
JABTAK x 5 <
    LIKHO x
    BARABAR x x 1 +
SAMAPT_JABTAK
"""




'''Program3 = """
LIKHO "ChidiUdd"
BARABAR limit 100
BARABAR i 1
JABTAK i limit <
    AGAR i 3 % 0 ==
        LIKHO "chidi"
SAMAPT_AGAR
    AGAR i 5 % 0 ==
        LIKHO "udd"
SAMAPT_AGAR
    AGAR i 3 % 0 == ! i 5 % 0 == ! &
        LIKHO i
SAMAPT_AGAR
    BARABAR i i 1 +
SAMAPT_JABTAK
"""'''

my_interpreter = Interpreter()
#print("for program 1")
#my_interpreter.interpret(program1)
print("for program 2")
my_interpreter.interpret(program2)

#print("for program 3")
#my_interpreter.interpret(Program3)

#print("Total lines interpreted:", my_interpreter.total_lines_interpreted)
