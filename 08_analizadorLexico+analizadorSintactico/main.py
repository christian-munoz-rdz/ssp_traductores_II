import pandas as pd

csv_path = "compilador.csv"
lr_table = pd.read_csv(csv_path)

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