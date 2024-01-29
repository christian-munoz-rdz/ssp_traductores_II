def es_entero(input):
    if input[0].isdigit():
        for char in input[1:]:
            if not char.isdigit():
                return False
        return True
    return False

def es_real(input):
    if not input[0].isdigit():
        return False
    elif input[0].isdigit:
        pos=1
        for char in input[1:]:
            if not (char.isdigit() or char == '.'):
                return False
            elif char == '.':
                if '.' in input[pos+1:]:
                    return False
            pos += 1
        if input[-1] == '.':
            return False
        return True

# Definición de tokens
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f'Token({self.type}, {repr(self.value)})'

# Lista de tokens para el resultado
tokens = []

# La entrada que vamos a analizar
input_text = """int variable+1=5;float variable2=3.14+5;
if (variable1 > 1 && variable2 == variable1) {
    variable1 = variable1 * 2;
    while (variable1 <= 10) {
        return variable1 + variable2;
    }
} else {
    variable2 = variable1 / 2.0;
    return variable2;
}"""

# Variables auxiliares para guardar estados y valores
current_token = ""
reserved_words = ['int', 'float', 'void' 'if', 'while', 'return', 'else']
operators = ['+', '-', '*', '/', '=', '<', '>', '<=', '>=', '!=', '==', '&&', '||', '!']
delimiters = [' ', '\n', '(', ')', '{', '}', ';']

# Función para agregar el token actual a la lista de tokens
def add_token(token_type, token_value):
    tokens.append(Token(token_type, token_value))

# Analizador léxico
for idx, char in enumerate(input_text):
    if char in delimiters:
        if current_token:
            # Aquí es donde determinaríamos si es un tipo de dato, un identificador o un número
            if current_token in reserved_words:
                add_token('RESERVED_WORD', current_token)
            elif es_entero(current_token):
                add_token('INTEGER', int(current_token))
            elif es_real(current_token):
                add_token('FLOAT', float(current_token))
            else:
                add_token('IDENTIFIER', current_token)
            current_token = ""
        if char.strip():
            add_token('DELIMITER', char)
    elif char in operators:
        if char + input_text[idx+1] in operators:
            if current_token:
                add_token('IDENTIFIER', current_token)
                current_token = ""
            add_token('OPERATOR', char + input_text[idx+1])
            continue
        if current_token:
            add_token('IDENTIFIER', current_token)
            current_token = ""
        add_token('OPERATOR', char)
    else:
        current_token += char

# Mostrar los tokens encontrados
for token in tokens:
    print(token)