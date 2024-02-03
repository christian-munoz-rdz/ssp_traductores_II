def es_letra(caracter):
    return caracter.isalpha()

def es_digito(caracter):
    return caracter.isdigit()

# Mapeo de tokens a números según las imágenes proporcionadas.
TOKEN_MAP = {
    'IDENTIFICADOR': 0,
    'ENTERO': 1,
    'REAL': 2,
    'OPSUMA': 5,  # '+', '-'
    'OPMUL': 6,   # '*', '/'
    'OPRELAC': 7, # '<', '>', '<=', '>=', '!=', '=='
    'OPOR': 8,    # '||'
    'OPAND': 9,   # '&&'
    'OPNOT': 10,  # '!'
    'PARENTESIS': 14,  # '(', ')'
    'LLAVE': 16,       # '{', '}'
    'PUNTOYCOMA': 12,  # ';'
    # Para las palabras reservadas, usaremos su representación en mayúsculas como clave
    'IF': 19,
    'WHILE': 20,
    'RETURN': 21,
    'ELSE': 22,
    'INT': 23,
    'FLOAT': 24,
}

# Lista de palabras reservadas para verificación rápida.
PALABRAS_RESERVADAS = {'if', 'while', 'return', 'else', 'int', 'float'}

def obtener_token(cadena, indice):
    token = ''
    longitud = len(cadena)

    # Identificadores y palabras reservadas
    if es_letra(cadena[indice]):
        while indice < longitud and (es_letra(cadena[indice]) or es_digito(cadena[indice])):
            token += cadena[indice]
            indice += 1
        tipo_token = token.upper() if token.lower() in PALABRAS_RESERVADAS else 'IDENTIFICADOR'
    
    # Números enteros y reales
    elif es_digito(cadena[indice]):
        while indice < longitud and es_digito(cadena[indice]):
            token += cadena[indice]
            indice += 1
        if indice < longitud and cadena[indice] == '.':
            token += cadena[indice]
            indice += 1
            while indice < longitud and es_digito(cadena[indice]):
                token += cadena[indice]
                indice += 1
            tipo_token = 'REAL'
        else:
            tipo_token = 'ENTERO'
    
    # Operadores y otros símbolos
    else:
        if cadena[indice] in '+-':
            tipo_token = 'OPSUMA'
        elif cadena[indice] in '*/':
            tipo_token = 'OPMUL'
        elif cadena[indice] in '()':
            tipo_token = 'PARENTESIS'
        elif cadena[indice] in '{}':
            tipo_token = 'LLAVE'
        elif cadena[indice] == ';':
            tipo_token = 'PUNTOYCOMA'
        elif cadena[indice] in '!&|<>=':
            operadores_dobles = {'&&', '||', '==', '!=', '<=', '>='}
            token = cadena[indice]
            indice += 1
            if indice < longitud and cadena[indice] in '&|=<>' and token+cadena[indice] in operadores_dobles:
                token += cadena[indice]
                indice += 1
            tipo_token = 'OPRELAC' if token in operadores_dobles else 'OPNOT' if token == '!' else 'OPAND' if token == '&&' else 'OPOR'
        else:
            raise ValueError(f"Caracter inesperado: {cadena[indice]}")
        token += cadena[indice]  # Agregar el operador al token.
        indice += 1  # Avanzar el índice después de recoger un operador.

    return TOKEN_MAP[tipo_token], token, indice

def analizar_lexico(cadena):
    tokens = []
    indice = 0
    longitud = len(cadena)
    while indice < longitud:
        if cadena[indice].isspace():  # Ignorar espacios en blanco
            indice += 1
            continue
        token_numero, token, indice = obtener_token(cadena, indice)
        tokens.append((token_numero, token))
    return tokens

# Prueba del analizador léxico
cadena_prueba = "if(a>=10){return a+1;}"
tokens = analizar_lexico(cadena_prueba)
for token_numero, token in tokens:
    print(f"Token Tipo {token_numero}, Valor '{token}'")

# Ejemplo de cadena que debería fallar
cadena_error = "int 3var = 5;"
try:
    tokens_error = analizar_lexico(cadena_error)
except ValueError as e:
    print(e)