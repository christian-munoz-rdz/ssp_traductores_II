class Token:
    def __init__(self, tipo=None, valor=None, numero=None):
        self.tipo = tipo
        self.valor = valor
        self.numero = numero
    
    def set(self, tipo, valor, numero):
        self.tipo = tipo
        self.valor = valor
        self.numero = numero

    def __repr__(self):
        return f"{self.tipo} {self.valor} {self.numero}"

def es_letra(c):
    return c.isalpha()

def es_digito(c):
    return c.isdigit()

def es_identificador(input):
    if input[0].isalpha():
        for char in input[1:]:
            if not (char.isalpha() or char.isdigit()):
                return False
        return True
    return False

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

def es_cadena(input):
    if input[0] == '"' and input[-1] == '"':
        return True
    return False

def es_espacio(c):
    return c in ' \t\n\r'

def obtener_tokens(codigo):
    tokens = {
        ";": (";", ";", 12), ",": (",", ",", 13), "(": ("(", "(", 14), ")": (")", ")", 15),
        "{": ("{", "{", 16), "}": ("}", "}", 17), "=": ("=", "=", 18),
        "if": ("if", "if", 19), "while": ("while", "while", 20),
        "return": ("return", "return", 21), "else": ("else", "else", 22),
        "+": ("opSuma", "+", 5), "-": ("opSuma", "-", 5),
        "||": ("opOr", "||", 8), "&&": ("opAnd", "&&", 9), "!": ("opNot", "!", 10),
        "*": ("opMul", "*", 6), "/": ("opMul", "/", 6),
        "==": ("Operador Igualdad", "==", 11), "!=": ("opIgualdad", "!=", 11), "<": ("opRelac", "<", 7),
        "<=": ("opRelac", "<=", 7), ">": ("opRelac", ">", 7), ">=": ("opRelac", ">=", 7),
        "$": ("Fin de Archivo", "$", 23)
    }
    tipos_de_dato = ["int", "float", "void"]

    i = 0
    longitud = len(codigo)
    tokens_identificados = []

    while i < longitud:
        if es_espacio(codigo[i]):
            i += 1
            continue
        
        temp = ""
        temp_token = Token()
        
        if codigo[i] == '"':  # Inicio de cadena
            inicio_cadena = i
            i += 1
            while i < longitud and codigo[i] != '"':
                temp += codigo[i]
                i += 1
            if i < longitud and codigo[i] == '"':  # Cerrar cadena correctamente
                temp = codigo[inicio_cadena:i+1]
                temp_token.set("cadena", temp, 3)
                tokens_identificados.append(temp_token)
                i += 1
            else:
                # Error: cadena no cerrada
                temp = codigo[inicio_cadena:i+1]
                temp_token.set("Error: Cadena no cerrada", temp, -1)
                tokens_identificados.append(temp_token)
        
        elif es_letra(codigo[i]):  # Inicio de identificador o palabra reservada
            inicio_token = i
            while i < longitud and (es_letra(codigo[i]) or es_digito(codigo[i])):
                temp += codigo[i]
                i += 1
            
            if not es_identificador(temp):  # Si el identificador no es válido
                temp_token.set("Error: Identificador no válido", temp, -1)
                tokens_identificados.append(temp_token)
            elif temp in tipos_de_dato:
                temp_token.set("tipo", temp, 4)
                tokens_identificados.append(temp_token)
            elif temp in tokens:
                temp_token.set(tokens[temp][0], temp, tokens[temp][2])
                tokens_identificados.append(temp_token)
            else:
                temp_token.set("identificador", temp, 0)
                tokens_identificados.append(temp_token)
        
        elif es_digito(codigo[i]):  # Inicio de constante numérica
            inicio_numero = i
            while i < longitud and (es_digito(codigo[i]) or codigo[i] == '.'):
                temp += codigo[i]
                i += 1
            
            if not es_entero(temp) and not es_real(temp):  # Si el número no es válido
                temp_token.set("Error: Número no válido", codigo[inicio_numero:i], -1)
                tokens_identificados.append(temp_token)
            elif es_entero(temp):
                temp_token.set("entero", temp, 1)
                tokens_identificados.append(temp_token)
            elif es_real(temp):
                temp_token.set("real", temp, 2)
                tokens_identificados.append(temp_token)
        
        else:  # Otros caracteres (operadores, delimitadores) o errores
            temp += codigo[i]
            if i + 1 < longitud:
                temp_doble = temp + codigo[i + 1]
                if temp_doble in tokens:  # Verificar operadores de dos caracteres
                    temp_token.set(tokens[temp_doble][0], temp_doble, tokens[temp_doble][2])
                    tokens_identificados.append(temp_token)
                    i += 2
                    continue
            if temp in tokens:
                temp_token.set(tokens[temp][0], temp, tokens[temp][2])
                tokens_identificados.append(temp_token)
            else:
                # Error: caracter no reconocido
                temp_token.set("Error: Caracter no reconocido", temp, -1)
                tokens_identificados.append(temp_token)
            i += 1

    return tokens_identificados

action_table = {
    (0, 'tipo'): ('s', 5),
    (0, '$'): ('r', 'R2'),
    (1, '$'): ('r', 'R0'),
    (2, '$'): ('r', 'R1'),
    (3, 'tipo'): ('s', 5),
    (3, '$'): ('r', 'R2'),
    (4, 'tipo'): ('r', 'R4'),
    (4, '$'): ('r', 'R4'),
    (5, 'identificador'): ('s', 8),
    (6,  'tipo'): ('r', 'R5'),
    (6, '$'): ('r', 'R5'),
    (7, '$'): ('r', 'R3'),
    (8, ';'): ('r', 'R7'),
    (8, ','): ('s', 10),
    (8, '('): ('s', 11),
    (9, ';'): ('s', 12),
    (10, 'identificador'): ('s', 13),
    (11, 'tipo'): ('s', 15),
    (11, ')'): ('r', 'R10'),
    (12, 'identificador'): ('r', 'R6'),
    (12, 'tipo'): ('r', 'R6'),
    (12, '}'): ('r', 'R6'),
    (12, 'if'): ('r', 'R6'),
    (12, 'while'): ('r', 'R6'),
    (12, 'return'): ('r', 'R6'),
    (12, '$'): ('r', 'R6'),
    (13, ';'): ('r', 'R7'),
    (13, ','): ('s', 10),
    (14, ')'): ('s', 17),
    (15, 'identificador'): ('s', 18),
    (16, ';'): ('r', 'R8'),
    (17, '{'): ('s', 20),
    (18, ','): ('s', 22),
    (18, ')'): ('r', 'R12'),
    (19, 'tipo'): ('r', 'R9'),
    (19, '$'): ('r', 'R9'),
    (20, 'identificador'): ('s', 27),
    (20, 'tipo'): ('s', 5),
    (20, '}'): ('r', 'R15'),
    (20, 'if'): ('s', 28),
    (20, 'while'): ('s', 29),
    (20, 'return'): ('s', 30),
    (21, ')'): ('r', 'R11'),
    (22, 'tipo'): ('s', 32),
    (23, '}'): ('s', 33),
    (24, 'identificador'): ('s', 27),
    (24, 'tipo'): ('s', 5),
    (24, '}'): ('r', 'R15'),
    (24, 'if'): ('s', 28),
    (24, 'while'): ('s', 29),
    (24, 'return'): ('s', 30),
    (25, 'identificador'): ('r', 'R17'),
    (25, 'tipo'): ('r', 'R17'),
    (25, '}'): ('r', 'R17'),
    (25, 'if'): ('r', 'R17'),
    (25, 'while'): ('r', 'R17'),
    (25, 'return'): ('r', 'R17'),
    (26, 'identificador'): ('r', 'R18'),
    (26, 'tipo'): ('r', 'R18'),
    (26, '}'): ('r', 'R18'),
    (26, 'if'): ('r', 'R18'),
    (26, 'while'): ('r', 'R18'),
    (26, 'return'): ('r', 'R18'),
    (27, '('): ('s', 36),
    (27, '='): ('s', 35),
    (28, '('): ('s', 37),
    (29, '('): ('s', 38),
    (30, 'identificador'): ('s', 46),
    (30, 'entero'): ('s', 47),
    (30, 'real'): ('s', 48),
    (30, 'cadena '): ('s', 49),
    (30, 'opSuma '): ('s', 42),
    (30, 'opNot '): ('s', 43),
    (30, ';'): ('r', 'R29'),
    (30, '('): ('s', 41),
    (31, ';'): ('s', 50),
    (31, 'identificador'): ('s', 51),
    (33, 'tipo'): ('r', 'R14'),
    (33, '$'): ('r', 'R14'),
    (34, '}'): ('r', 'R16'),
    (35, 'identificador'): ('s', 46),
    (35, 'entero'): ('s', 47),
    (35, 'real'): ('s', 48),
    (35, 'cadena'): ('s', 49),
    (35, 'opSuma'): ('s', 42),
    (35, 'opNot'): ('s', 43),
    (35, '('): ('s', 41),
    (36, 'identificador'): ('s', 46),
    (36, 'entero'): ('s', 47),
    (36, 'real'): ('s', 48),
    (36, 'cadena'): ('s', 49),
    (36, 'opSuma'): ('s', 42),
    (36, 'opNot'): ('s', 43),
    (36, '('): ('s', 41),
    (36, ')'): ('r', 'R31'),
    (37, 'identificador'): ('s', 46),
    (37, 'entero'): ('s', 47),
    (37, 'real'): ('s', 48),
    (37, 'cadena'): ('s', 49),
    (37, 'opSuma'): ('s', 42),
    (37, 'opNot'): ('s', 43),
    (37, '('): ('s', 41),
    (38, 'identificador'): ('s', 46),
    (38, 'entero'): ('s', 47),
    (38, 'real'): ('s', 48),
    (38, 'cadena'): ('s', 49),
    (38, 'opSuma'): ('s', 42),
    (38, 'opNot'): ('s', 43),
    (38, '('): ('s', 41),
    (39, ';'): ('s', 57),
    (40, 'opSuma'): ('s', 59),
    (40, 'opMul'): ('s', 58),
    (40, 'opRelac'): ('s', 60),
    (40, 'opOr'): ('s', 63),
    (40, 'opAnd'): ('s', 62),
    (40, 'opIgualdad'): ('s', 61),
    (40, ';'): ('r', 'R30'),
    (41, 'identificador'): ('s', 46),
    (41, 'entero'): ('s', 47),
    (41, 'real'): ('s', 48),
    (41, 'cadena'): ('s', 49),
    (41, 'opSuma'): ('s', 42),
    (41, 'opNot'): ('s', 43),
    (41, '('): ('s', 41),
    (42, 'identificador'): ('s', 46),
    (42, 'entero'): ('s', 47),
    (42, 'real'): ('s', 48),
    (42, 'cadena'): ('s', 49),
    (42, 'opSuma'): ('s', 42),
    (42, 'opNot'): ('s', 43),
    (42, '('): ('s', 41),
    (43, 'identificador'): ('s', 46),
    (43, 'entero'): ('s', 47),
    (43, 'real'): ('s', 48),
    (43, 'cadena'): ('s', 49),
    (43, 'opSuma'): ('s', 42),
    (43, 'opNot'): ('s', 43),
    (43, '('): ('s', 41),
    (44, 'opSuma'): ('r', 'R52'),
    (44, 'opMul'): ('r', 'R52'),
    (44, 'opRelac'): ('r', 'R52'),
    (44, 'opOr'): ('r', 'R52'),
    (44, 'opAnd'): ('r', 'R52'),
    (44, 'opIgualdad'): ('r', 'R52'),
    (44, ';'): ('r', 'R52'),
    (44, ','): ('r', 'R52'),
    (44, ')'): ('r', 'R52'),
    (45, 'opSuma'): ('r', 'R35'),
    (45, 'opMul'): ('r', 'R35'),
    (45, 'opRelac'): ('r', 'R35'),
    (45, 'opOr'): ('r', 'R35'),
    (45, 'opAnd'): ('r', 'R35'),
    (45, 'opIgualdad'): ('r', 'R35'),
    (45, ';'): ('r', 'R35'),
    (45, ','): ('r', 'R35'),
    (45, ')'): ('r', 'R35'),
    (46, 'opSuma'): ('r', 'R36'),
    (46, 'opMul'): ('r', 'R36'),
    (46, 'opRelac'): ('r', 'R36'),
    (46, 'opOr'): ('r', 'R36'),
    (46, 'opAnd'): ('r', 'R36'),
    (46, 'opIgualdad'): ('r', 'R36'),
    (46, ';'): ('r', 'R36'),
    (46, ','): ('r', 'R36'),
    (46, '('): ('s', 36),
    (46, ')'): ('r', 'R36'),
    (47, 'opSuma'): ('r', 'R37'),
    (47, 'opMul'): ('r', 'R37'),
    (47, 'opRelac'): ('r', 'R37'),
    (47, 'opOr'): ('r', 'R37'),
    (47, 'opAnd'): ('r', 'R37'),
    (47, 'opIgualdad'): ('r', 'R37'),
    (47, ';'): ('r', 'R37'),
    (47, ','): ('r', 'R37'),
    (47, ')'): ('r', 'R37'),
    (48, 'opSuma'): ('r', 'R38'),
    (48, 'opMul'): ('r', 'R38'),
    (48, 'opRelac'): ('r', 'R38'),
    (48, 'opOr'): ('r', 'R38'),
    (48, 'opAnd'): ('r', 'R38'),
    (48, 'opIgualdad'): ('r', 'R38'),
    (48, ';'): ('r', 'R38'),
    (48, ','): ('r', 'R38'),
    (48, ')'): ('r', 'R38'),
    (49, 'opSuma'): ('r', 'R39'),
    (49, 'opMul'): ('r', 'R39'),
    (49, 'opRelac'): ('r', 'R39'),
    (49, 'opOr'): ('r', 'R39'),
    (49, 'opAnd'): ('r', 'R39'),
    (49, 'opIgualdad'): ('r', 'R39'),
    (49, ';'): ('r', 'R39'),
    (49, ','): ('r', 'R39'),
    (49, ')'): ('r', 'R39'),
    (50, 'identificador'): ('r', 'R25'),
    (50, 'tipo'): ('r', 'R25'),
    (50, '}'): ('r', 'R25'),
    (50, 'if'): ('r', 'R25'),
    (50, 'while'): ('r', 'R25'),
    (50, 'return'): ('r', 'R25'),
    (50, 'else'): ('r', 'R25'),
    (51, ','): ('s', 22),
    (51, ')'): ('r', 'R12'),
    (52, 'opSuma'): ('s', 59),
    (52, 'opMul'): ('s', 58),
    (52, 'opRelac'): ('s', 60),
    (52, 'opOr'): ('s', 63),
    (52, 'opAnd'): ('s', 62),
    (52, 'opIgualdad'): ('s', 61),
    (52, ';'): ('s', 68),
    (53, ')'): ('s', 69),
    (54, 'opSuma'): ('s', 59),
    (54, 'opMul'): ('s', 58),
    (54, 'opRelac'): ('s', 60),
    (54, 'opOr'): ('s', 63),
    (54, 'opAnd'): ('s', 62),
    (54, 'opIgualdad'): ('s', 61),
    (54, ','): ('s', 71),
    (54, ')'): ('r', 'R33'),
    (55, 'opSuma'): ('s', 59),
    (55, 'opMul'): ('s', 58),
    (55, 'opRelac'): ('s', 60),
    (55, 'opOr'): ('s', 63),
    (55, 'opAnd'): ('s', 62),
    (55, 'opIgualdad'): ('s', 61),
    (55, ')'): ('s', 72),
    (56, 'opSuma'): ('s', 59),
    (56, 'opMul'): ('s', 58),
    (56, 'opRelac'): ('s', 60),
    (56, 'opOr'): ('s', 63),
    (56, 'opAnd'): ('s', 62),
    (56, 'opIgualdad'): ('s', 61),
    (56, ')'): ('s', 73),
    (57, 'identificador'): ('r', 'R24'),
    (57, 'tipo'): ('r', 'R24'),
    (57, '}'): ('r', 'R24'),
    (57, 'if'): ('r', 'R24'),
    (57, 'while'): ('r', 'R24'),
    (57, 'return'): ('r', 'R24'),
    (57, 'else'): ('r', 'R24'),
    (58, 'identificador'): ('s', 46),
    (58, 'entero'): ('s', 47),
    (58, 'real'): ('s', 48),
    (58, 'cadena'): ('s', 49),
    (58, 'opSuma'): ('s', 42),
    (58, 'opNot'): ('s', 43),
    (58, '('): ('s', 41),
    (59, 'identificador'): ('s', 46),
    (59, 'entero'): ('s', 47),
    (59, 'real'): ('s', 48),
    (59, 'cadena'): ('s', 49),
    (59, 'opSuma'): ('s', 42),
    (59, 'opNot'): ('s', 43),
    (59, '('): ('s', 41),
    (60, 'identificador'): ('s', 46),
    (60, 'entero'): ('s', 47),
    (60, 'real'): ('s', 48),
    (60, 'cadena'): ('s', 49),
    (60, 'opSuma'): ('s', 42),
    (60, 'opNot'): ('s', 43),
    (60, '('): ('s', 41),
    (61, 'identificador'): ('s', 46),
    (61, 'entero'): ('s', 47),
    (61, 'real'): ('s', 48),
    (61, 'cadena'): ('s', 49),
    (61, 'opSuma'): ('s', 42),
    (61, 'opNot'): ('s', 43),
    (61, '('): ('s', 41),
    (62, 'identificador'): ('s', 46),
    (62, 'entero'): ('s', 47),
    (62, 'real'): ('s', 48),
    (62, 'cadena'): ('s', 49),
    (62, 'opSuma'): ('s', 42),
    (62, 'opNot'): ('s', 43),
    (62, '('): ('s', 41),
    (63, 'identificador'): ('s', 46),
    (63, 'entero'): ('s', 47),
    (63, 'real'): ('s', 48),
    (63, 'cadena'): ('s', 49),
    (63, 'opSuma'): ('s', 42),
    (63, 'opNot'): ('s', 43),
    (63, '('): ('s', 41),
    (64, 'opSuma'): ('s', 59),
    (64, 'opMul'): ('s', 58),
    (64, 'opRelac'): ('s', 60),
    (64, 'opOr'): ('s', 63),
    (64, 'opAnd'): ('s', 62),
    (64, 'opIgualdad'): ('s', 61),
    (64, ')'): ('s', 80),
    (65, 'opSuma'): ('r', 'R44'),
    (65, 'opMul'): ('r', 'R44'),
    (65, 'opRelac'): ('r', 'R44'),
    (65, 'opOr'): ('r', 'R44'),
    (65, 'opAnd'): ('r', 'R44'),
    (65, 'opIgualdad'): ('r', 'R44'),
    (65, ';'): ('r', 'R44'),
    (65, ','): ('r', 'R44'),
    (65, ')'): ('r', 'R44'),
    (66, 'opSuma'): ('r', 'R45'),
    (66, 'opMul'): ('r', 'R45'),
    (66, 'opRelac'): ('r', 'R45'),
    (66, 'opOr'): ('r', 'R45'),
    (66, 'opAnd'): ('r', 'R45'),
    (66, 'opIgualdad'): ('r', 'R45'),
    (66, ';'): ('r', 'R45'),
    (66, ','): ('r', 'R45'),
    (66, ')'): ('r', 'R45'),
    (67, ')'): ('r', 'R13'),
    (68, 'identificador'): ('r', 'R21'),
    (68, 'tipo'): ('r', 'R21'),
    (68, '}'): ('r', 'R21'),
    (68, 'if'): ('r', 'R21'),
    (68, 'while'): ('r', 'R21'),
    (68, 'return'): ('r', 'R21'),
    (68, 'else'): ('r', 'R21'),
    (69, 'opSuma'): ('r', 'R40'),
    (69, 'opMul'): ('r', 'R40'),
    (69, 'opRelac'): ('r', 'R40'),
    (69, 'opOr'): ('r', 'R40'),
    (69, 'opAnd'): ('r', 'R40'),
    (69, 'opIgualdad'): ('r', 'R40'),
    (69, ';'): ('r', 'R40'),
    (69, ','): ('r', 'R40'),
    (69, ')'): ('r', 'R40'),
    (70, ')'): ('r', 'R32'),
    (71, 'identificador'): ('s', 46),
    (71, 'entero'): ('s', 47),
    (71, 'real'): ('s', 48),
    (71, 'cadena'): ('s', 49),
    (71, 'opSuma'): ('s', 42),
    (71, 'opNot'): ('s', 43),
    (71, '('): ('s', 41),
    (72, 'identificador'): ('s', 27),
    (72, '{'): ('s', 85),
    (72, 'if'): ('s', 28),
    (72, 'while'): ('s', 29),
    (72, 'return'): ('s', 30),
    (73, '{'): ('s', 85),
    (74, 'opSuma'): ('r', 'R46'),
    (74, 'opMul'): ('r', 'R46'),
    (74, 'opRelac'): ('r', 'R46'),
    (74, 'opOr'): ('r', 'R46'),
    (74, 'opAnd'): ('r', 'R46'),
    (74, 'opIgualdad'): ('r', 'R46'),
    (74, ';'): ('r', 'R46'),
    (74, ','): ('r', 'R46'),
    (74, ')'): ('r', 'R46'),
    (75, 'opSuma'): ('r', 'R47'),
    (75, 'opMul'): ('s', 58),
    (75, 'opRelac'): ('r', 'R47'),
    (75, 'opOr'): ('r', 'R47'),
    (75, 'opAnd'): ('r', 'R47'),
    (75, 'opIgualdad'): ('r', 'R47'),
    (75, ';'): ('r', 'R47'),
    (75, ','): ('r', 'R47'),
    (75, ')'): ('r', 'R47'),
    (76, 'opSuma'): ('s', 59),
    (76, 'opMul'): ('s', 58),
    (76, 'opRelac'): ('r', 'R48'),
    (76, 'opOr'): ('r', 'R48'),
    (76, 'opAnd'): ('r', 'R48'),
    (76, 'opIgualdad'): ('r', 'R48'),
    (76, ';'): ('r', 'R48'),
    (76, ','): ('r', 'R48'),
    (76, ')'): ('r', 'R48'),
    (77, 'opSuma'): ('s', 59),
    (77, 'opMul'): ('s', 58),
    (77, 'opRelac'): ('s', 60),
    (77, 'opOr'): ('r', 'R49'),
    (77, 'opAnd'): ('r', 'R49'),
    (77, 'opIgualdad'): ('r', 'R49'),
    (77, ';'): ('r', 'R49'),
    (77, ','): ('r', 'R49'),
    (77, ')'): ('r', 'R49'),
    (78, 'opSuma'): ('s', 59),
    (78, 'opMul'): ('s', 58),
    (78, 'opRelac'): ('s', 60),
    (78, 'opOr'): ('r', 'R50'),
    (78, 'opAnd'): ('r', 'R50'),
    (78, 'opIgualdad'): ('s', 61),
    (78, ';'): ('r', 'R50'),
    (78, ','): ('r', 'R50'),
    (78, ')'): ('r', 'R50'),
    (79, 'opSuma'): ('s', 59),
    (79, 'opMul'): ('s', 58),
    (79, 'opRelac'): ('s', 60),
    (79, 'opOr'): ('r', 'R51'),
    (79, 'opAnd'): ('s', 62),
    (79, 'opIgualdad'): ('s', 61),
    (79, ';'): ('r', 'R51'),
    (79, ','): ('r', 'R51'),
    (79, ')'): ('r', 'R51'),
    (80, 'opSuma'): ('r', 'R43'),
    (80, 'opMul'): ('r', 'R43'),
    (80, 'opRelac'): ('r', 'R43'),
    (80, 'opOr'): ('r', 'R43'),
    (80, 'opAnd'): ('r', 'R43'),
    (80, 'opIgualdad'): ('r', 'R43'),
    (80, ';'): ('r', 'R43'),
    (80, ','): ('r', 'R43'),
    (80, ')'): ('r', 'R43'),
    (81, 'opSuma'): ('s', 59),
    (81, 'opMul'): ('s', 58),
    (81, 'opRelac'): ('s', 60),
    (81, 'opOr'): ('s', 63),
    (81, 'opAnd'): ('s', 62),
    (81, 'opIgualdad'): ('s', 61),
    (81, ','): ('s', 71),
    (81, ')'): ('r', 33),
    (82, 'identificador'): ('r', 'R26'),
    (82, 'tipo'): ('r', 'R26'),
    (82, '}'): ('r', 'R26'),
    (82, 'if'): ('r', 'R26'),
    (82, 'while'): ('r', 'R26'),
    (82, 'return'): ('r', 'R26'),
    (82, 'else'): ('s', 89),
    (83, 'identificador'): ('r', 'R41'),
    (83, 'tipo'): ('r', 'R41'),
    (83, '}'): ('r', 'R41'),
    (83, 'if'): ('r', 'R41'),
    (83, 'while'): ('r', 'R41'),
    (83, 'return'): ('r', 'R41'),
    (83, 'else'): ('r', 'R41'),
    (84, 'identificador'): ('r', 'R42'),
    (84, 'tipo'): ('r', 'R42'),
    (84, '}'): ('r', 'R42'),
    (84, 'if'): ('r', 'R42'),
    (84, 'while'): ('r', 'R42'),
    (84, 'return'): ('r', 'R42'),
    (84, 'else'): ('r', 'R42'),
    (85, 'identificador'): ('s', 27),
    (85, '}'): ('r', 'R19'),
    (85, 'if'): ('s', 28),
    (85, 'while'): ('s', 29),
    (85, 'return'): ('s', 30),
    (86, 'identificador'): ('r', 'R23'),
    (86, 'tipo'): ('r', 'R23'),
    (86, '}'): ('r', 'R23'),
    (86, 'if'): ('r', 'R23'),
    (86, 'while'): ('r', 'R23'),
    (86, 'return'): ('r', 'R23'),
    (86, 'else'): ('r', 'R23'),
    (87, ')'): ('r', 'R34'),
    (88, 'identificador'): ('r', 'R22'),
    (88, 'tipo'): ('r', 'R22'),
    (88, '}'): ('r', 'R22'),
    (88, 'if'): ('r', 'R22'),
    (88, 'while'): ('r', 'R22'),
    (88, 'return'): ('r', 'R22'),
    (88, 'else'): ('r', 'R22'),
    (89, 'identificador'): ('s', 27),
    (89, '{'): ('s', 85),
    (89, 'if'): ('s', 28),
    (89, 'while'): ('s', 29),
    (89, 'return'): ('s', 30),
    (90, '}'): ('s', 93),
    (91, 'identificador'): ('s', 27),
    (91, '}'): ('r', 'R19'),
    (91, 'if'): ('s', 28),
    (91, 'while'): ('s', 29),
    (91, 'return'): ('s', 30),
    (92, 'identificador'): ('r', 'R27'),
    (92, 'tipo'): ('r', 'R27'),
    (92, '}'): ('r', 'R27'),
    (92, 'if'): ('r', 'R27'),
    (92, 'while'): ('r', 'R27'),
    (92, 'return'): ('r', 'R27'),
    (93, 'identificador'): ('r', 'R28'),
    (93, 'tipo'): ('r', 'R28'),
    (93, '}'): ('r', 'R28'),
    (93, 'if'): ('r', 'R28'),
    (93, 'while'): ('r', 'R28'),
    (93, 'return'): ('r', 'R28'),
    (93, 'else'): ('r', 'R28'),
    (94, '}'): ('r', 'R20')
}

goto_table = {
    (0, 'programa'): 1,
    (0, 'Definiciones'): 2,
    (0, 'Definicion'): 3,
    (0, 'DefVar'):4,
    (0, 'DefFunc'):6,
    (3, 'Definiciones'): 7,
    (3, 'Definicion'): 3,
    (3, 'DefVar'):4,
    (3, 'DefFunc'):6,
    (8, 'ListaVar'): 9,
    (11, 'Parametros'): 14,
    (13, 'ListaVar'): 16,
    (17, 'BloqFunc'): 19,
    (18, 'ListaParam'): 21,
    (20, 'DefVar'): 25,
    (20, 'DefLocales'): 23,
    (20, 'DefLocal'): 24,
    (20, 'Sentencia'): 26,
    (20, 'LlamadaFunc'): 31,
    (24, 'DefVar'): 25,
    (24, 'DefLocales'): 34,
    (24, 'DefLocal'): 24,
    (24, 'Sentencia'): 26,
    (24, 'LlamadaFunc'): 31,
    (30, 'ValorRegresa'): 39,
    (30, 'Termino'): 44,
    (30, 'LlamadaFunc'): 45,
    (30, 'Expresion'): 40,
    (35, 'Termino'): 44,
    (35, 'LlamadaFunc'): 45,
    (35, 'Expresion'): 52,
    (36, 'Argumentos'): 53,
    (36, 'Termino'): 44,
    (36, 'LlamadaFunc'): 45,
    (36, 'Expresion'): 54,
    (37, 'Termino'): 44,
    (37, 'LlamadaFunc'): 45,
    (37, 'Expresion'): 55,
    (38, 'Termino'): 44,
    (38, 'LlamadaFunc'): 45,
    (38, 'Expresion'): 56,
    (41, 'Termino'): 44,
    (41, 'LlamadaFunc'): 45,
    (41, 'Expresion'): 64,
    (42, 'Termino'): 44,
    (42, 'LlamadaFunc'): 45,
    (42, 'Expresion'): 65,
    (43, 'Termino'): 44,
    (43, 'LlamadaFunc'): 45,
    (43, 'Expresion'): 66,
    (51, 'ListaParam'): 67,
    (54, 'ListaArgumentos'): 70,
    (58, 'Termino'): 44,
    (58, 'LlamadaFunc'): 45,
    (58, 'Expresion'): 74,
    (59, 'Termino'): 44,
    (59, 'LlamadaFunc'): 45,
    (59, 'Expresion'): 75,
    (60, 'Termino'): 44,
    (60, 'LlamadaFunc'): 45,
    (60, 'Expresion'): 76,
    (61, 'Termino'): 44,
    (61, 'LlamadaFunc'): 45,
    (61, 'Expresion'): 77,
    (62, 'Termino'): 44,
    (62, 'LlamadaFunc'): 45,
    (62, 'Expresion'): 78,
    (63, 'Termino'): 44,
    (63, 'LlamadaFunc'): 45,
    (63, 'Expresion'): 79,
    (71, 'Termino'): 44,
    (71, 'LlamadaFunc'): 45,
    (71, 'Expresion'): 81,
    (72, 'Sentencia'): 83,
    (72, 'Bloque'): 84,
    (72, 'LlamadaFunc'): 31,
    (72, 'SentenciaBloque'): 82,
    (72, 'Bloque'): 86,
    (81, 'ListaArgumentos'): 87,
    (82, 'Otro'): 88,
    (85, 'Sentencias'): 90,
    (85, 'Sentencia'): 91,
    (85, 'LlamadaFunc'): 31,
    (89, 'Sentencia'): 83,
    (89, 'Bloque'): 84,
    (89, 'LlamadaFunc'): 31,
    (89, 'SentenciaBloque'): 92,
    (91, 'Sentencias'): 94,
    (91, 'Sentencia'): 91,
    (91, 'LlamadaFunc'): 31
}

grammar_rules = {
    #'E -> id + id': ('E', 3)
    'programa -> Definiciones': ,
    'Definiciones -> \e': ,
    'Definiciones -> Definicion Definiciones': ,
    'Definicion -> DefVar': ,
    'Definicion -> DefFunc': ,
    'DefVar -> tipo identificador ListaVar ;': ,
    'ListaVar -> \e': ,
    'ListaVar -> , identificador ListaVar': ,
    'DefFunc -> tipo identificador ( Parametros ) BloqFunc': ,
    'Parametros -> \e': ,
    'Parametros -> tipo identificador ListaParam': ,
    'ListaParam -> \e': ,
    'ListaParam -> , tipo identificador ListaParam': ,
    'BloqFunc -> { DefLocales }': ,
    'DefLocales -> \e': ,
    'DefLocales -> DefLocal DefLocales': ,
    'DefLocal -> DefVar': ,
    'DefLocal -> Sentencia': ,
    'Sentencias -> \e': ,
    'Sentencias -> Sentencia Sentencias': ,
    'Sentencia -> identificador = Expresion ;': ,
    'Sentencia -> if ( Expresion ) SentenciaBloque Otro': ,
    'Sentencia -> while ( Expresion ) Bloque': ,
    'Sentencia -> return ValorRegresa ;': ,
    'Sentencia -> LlamadaFunc ;': ,
    'Otro -> \e': ,
    'Otro -> else SentenciaBloque': ,
    'Bloque -> { Sentencias }': ,
    'ValorRegresa -> \e': ,
    'ValorRegresa -> Expresion': ,
    'Argumentos -> \e': ,
    'Argumentos -> Expresion ListaArgumentos': ,
    'ListaArgumentos -> \e': ,
    'ListaArgumentos -> , Expresion ListaArgumentos': ,
    'Termino -> LlamadaFunc': ,
    'Termino -> identificador': ,
    'Termino -> entero': ,
    'Termino -> real': ,
    'Termino -> cadena': ,
    'LlamadaFunc -> identificador ( Argumentos )': ,
    'SentenciaBloque -> Sentencia': ,
    'SentenciaBloque -> Bloque': ,
    'Expresion -> ( Expresion )': ,
    'Expresion -> opSuma Expresion': ,
    'Expresion -> opNot Expresion': ,
    'Expresion -> Expresion opMul Expresion': ,
    'Expresion -> Expresion opSuma Expresion': ,
    'Expresion -> Expresion opRelac Expresion': ,
    'Expresion -> Expresion opIgualdad Expresion': ,
    'Expresion -> Expresion opAnd Expresion': ,
    'Expresion -> Expresion opOr Expresion': ,
    'Expresion -> Termino': 
}

class ElementoPila:
    pass

class Terminal(ElementoPila):
    def __init__(self, symbol):
        self.symbol = symbol

    def __repr__(self):
        return f"Terminal('{self.symbol}')"

class NoTerminal(ElementoPila):
    def __init__(self, symbol):
        self.symbol = symbol

    def __repr__(self):
        return f"NoTerminal('{self.symbol}')"

class Estado(ElementoPila):
    def __init__(self, state):
        self.state = state

    def __repr__(self):
        return f"Estado({self.state})"

class Pila:
    def __init__(self):
        self.items = []

    def push(self, item):
        if isinstance(item, ElementoPila):
            self.items.append(item)
        else:
            raise TypeError("Only objects of type ElementoPila can be pushed onto the stack.")

    def pop(self):
        if self.items:
            return self.items.pop()

    def top(self):
        if self.items:
            return self.items[-1]

    def __repr__(self):
        return str(self.items)

class SyntacticAnalyzerOO:
    def __init__(self, action_table, goto_table, grammar_rules):
        self.action = action_table
        self.goto = goto_table
        self.grammar = grammar_rules
        self.stack = Pila()
        self.stack.push(Estado(0))

    def parse(self, tokens):
        cursor = 0

        while True:
            #print(self.stack, tokens[cursor:])
            top_state = self.stack.top()
            symbol = tokens[cursor] if cursor < len(tokens) else Terminal('$')
            action_entry = (top_state.state, symbol.symbol)

            if action_entry in self.action:
                action, value = self.action[action_entry]

                if action == 's':  # Shift action
                    self.stack.push(symbol)  # Shift symbol
                    self.stack.push(Estado(value))  # Shift state
                    cursor += 1

                elif action == 'r':  # Reduce action
                    for _ in range(self.grammar[value][1] * 2):
                        self.stack.pop()  # Pop state and symbol
                    non_terminal = NoTerminal(self.grammar[value][0])
                    self.stack.push(non_terminal)
                    goto_state = self.stack.items[-2].state
                    goto_entry = (goto_state, non_terminal.symbol)
                    self.stack.push(Estado(self.goto[goto_entry]))

                elif action == 'acc':  # Accept action
                    print("The input string is accepted by the grammar.")
                    return True

            else:
                print("The input string is not accepted by the grammar.")
                return False

        return False