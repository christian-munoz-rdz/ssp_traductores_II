class SyntacticAnalyzer:
    def __init__(self, action_table, goto_table, grammar_rules):
        self.action = action_table
        self.goto = goto_table
        self.grammar = grammar_rules


    def parse(self, tokens):
        stack = [0]  # Stack initialization with starting state
        cursor = 0   # Points to the current symbol in the input

        while True:
            state = stack[-1]  # Current state
            symbol = tokens[cursor] if cursor < len(tokens) else '$'  # Current symbol

            if (state, symbol) in self.action:
                action, value = self.action[(state, symbol)]

                if action == 's':  # Shift action
                    stack.append(symbol)  # Shift symbol
                    stack.append(value)   # Shift state
                    cursor += 1  # Move to next symbol

                elif action == 'r':  # Reduce action
                    # Apply the grammar rule
                    rule_length = self.grammar[value][1]
                    # Pop the rule length times 2 from the stack to remove states and symbols
                    for _ in range(rule_length * 2):
                        stack.pop()

                    non_terminal = self.grammar[value][0]
                    # Push non_terminal and goto state
                    stack.append(non_terminal)
                    stack.append(self.goto[(stack[-2], non_terminal)])

                elif action == 'acc':  # Accept action
                    print("The input string is accepted by the grammar.")
                    return True

            else:
                print("The input string is not accepted by the grammar.")
                return False

# Function to tokenize the input string
def tokenize(input_string):
    tokens = []
    current_token = ''
    for char in input_string:
        if char.isalpha() or char.isdigit():
            current_token += char
        else:
            if current_token:
                tokens.append('id')
                current_token = ''
            if char == '+':
                tokens.append(char)
    if current_token:
        tokens.append('id')
    tokens.append('$')  # End of input
    return tokens

# Define the parsing table, states, and actions
action_table1 = {
    (0, 'id'): ('s', 2),
    (1, '$'): ('acc', ''),
    (2, '+'): ('s', 3),
    (3, 'id'): ('s', 4),
    (4, '$'): ('r', 'E -> id + id')
}
goto_table1 = {
            (0, 'E'): 1
}

# The grammar rules for reduction
grammar_rules1 = {
    'E -> id + id': ('E', 3)  # E -> id + id reduces 3 items from stack
}

action_table2 = {
    (0, 'id'): ('s', 2),
    (1, '$'): ('acc', ''),
    (2, '+'): ('s', 3),
    (2, '$'): ('r', 'E -> id'),
    (3, 'id'): ('s', 2),
    (4, '$'): ('r', 'E -> id + E')  # Correct action for state 4
}

goto_table2 = {
    (0, 'E'): 1,
    (3, 'E'): 4
}

grammar_rules2 = {
    'E -> id': ('E', 1),       # E -> id reduces 1 item from stack
    'E -> id + E': ('E', 3)    # E -> id + E reduces 3 items from stack
}

# Analizamos la primera gramática
analyzer = SyntacticAnalyzer(action_table1, goto_table1, grammar_rules1)
tokens = tokenize('hola+mundo')
result = analyzer.parse(tokens)

# Analizamos la segunda gramática
analyzer = SyntacticAnalyzer(action_table2, goto_table2, grammar_rules2)
tokens = tokenize('a+b+c+d+e+f')
result = analyzer.parse(tokens)

#Revisar el algoritmo de parsing para el ejemplo 1 y 2 a ver sis on similares 