class SyntacticAnalyzer:
    def __init__(self):
        # Define the parsing table, states, and actions
        self.action = {
            (0, 'id'): ('s', 2),
            (1, '$'): ('acc', ''),
            (2, '+'): ('s', 3),
            (2, '$'): ('r', 'E -> id'),
            (3, 'id'): ('s', 2),
            (4, '$'): ('r', 'E -> id + E')  # Correct action for state 4
        }
        self.goto = {
            (0, 'E'): 1,
            (3, 'E'): 4
        }

        # The grammar rules for reduction
        self.grammar = {
            'E -> id': ('E', 1),       # E -> id reduces 1 item from stack
            'E -> id + E': ('E', 3)    # E -> id + E reduces 3 items from stack
        }

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

# Instantiate the corrected analyzer
analyzer_corrected = SyntacticAnalyzer()

# Tokenize the input string 'a+b+c+d+e+f' and parse it
tokens_corrected = tokenize('a+b+c+d+e+')  # The tokenize_extended function can still be used
result_corrected = analyzer_corrected.parse(tokens_corrected)

