def es_letra(c):
    return c.isalpha()

def es_digito(c):
    return c.isdigit()

def es_identificador(token):
    return es_letra(token[0]) and all(es_letra(c) or es_digito(c) for c in token[1:])

def analizar_lexico(cadena):
    tokens = []
    i = 0

    while i < len(cadena):
        # Ignorar espacios en blanco
        while i < len(cadena) and cadena[i].isspace():
            i += 1
        
        # Si llegamos al final de la cadena
        if i >= len(cadena):
            break

        # Comenzar un nuevo token
        token = cadena[i]
        i += 1

        # Identificar el tipo de token
        if es_letra(token):
            while i < len(cadena) and (es_letra(cadena[i]) or es_digito(cadena[i])):
                token += cadena[i]
                i += 1
            if token in PALABRAS_RESERVADAS:
                tokens.append(('RESERVADA', token))
            else:
                tokens.append(('IDENTIFICADOR', token))
        elif es_digito(token):
            is_real = False
            while i < len(cadena) and (es_digito(cadena[i]) or cadena[i] == '.'):
                if cadena[i] == '.':
                    if is_real:  # No se permiten dos puntos en un número real
                        break
                    is_real = True
                token += cadena[i]
                i += 1
            if is_real:
                tokens.append(('REAL', token))
            else:
                tokens.append(('ENTERO', token))
        else:
            # Para operadores y puntuación, asumiremos que son de un solo caracter
            if token in {'+', '-', '*', '/', '=', '<', '>', '!', '&', '|', '(', ')', '{', '}', ';'}:
                # Para operadores de dos caracteres, verificamos el siguiente caracter
                if i < len(cadena) and cadena[i] in {'=', '&', '|'}:
                    token += cadena[i]
                    i += 1
                tokens.append(('OPERADOR', token))
            else:
                raise ValueError(f"Caracter inesperado: {token}")

    return tokens

# Palabras reservadas
PALABRAS_RESERVADAS = {'if', 'while', 'return', 'else', 'int', 'float'}

# Prueba del analizador léxico
cadena = input("Ingrese una cadena: ")
tokens = analizar_lexico(cadena)
for tipo, valor in tokens:
    print(f"{tipo}: {valor}")