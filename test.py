class Token:
    def __init__(self, reglas):
        self.tipo = ''
        self.valor = ''
        self.reglas = reglas
    
    def set_value(self, input):
        if self.reglas(input):
            self.valor = input
        else:
            self.tipo = 'error'
            self.valor = input
    
    def rule_check(self, input):
        return self.reglas(input)
    
    def set_tipo(self, tipo):
        self.tipo = tipo
    
    def return_token(self):
        return {'tipo': self.tipo, 'valor': self.valor}

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
    if input[0].isdigit:
        pos=1
        for char in input[1:]:
            if not (char.isdigit() or char == '.'):
                return False
            elif char == '.':
                if '.' in input[pos+1:]:
                    return False
            pos += 1
        return True
    return False

def obtener_siguiente_token(texto):
    identificador = Token(es_identificador)
    entero = Token(es_entero)
    real = Token(es_real)
    pos = 0
    token_ready = False
    tokens = []
    current_token = ''
    while pos < len(texto):
        if texto[pos].isspace() or texto[pos] == '\n':

            print("Espacio")
            if pos != 0:
                token_ready = True
            variable1 123
        else:
            print("concat")
            texto[pos]
            current_token += texto[pos]
            pos += 1
        
        if token_ready:
            print("Token ready")
            if identificador.rule_check(current_token):
                identificador.set_value(current_token)
                identificador.set_tipo('identificador')
                tokens.append(identificador.return_token())
            elif entero.rule_check(current_token):
                entero.set_value(current_token)
                entero.set_tipo('entero')
                tokens.append(entero.return_token())
            elif real.rule_check(current_token):
                real.set_value(current_token)
                real.set_tipo('real')
                tokens.append(real.return_token())
            else:
                tokens.append({'tipo': 'error', 'valor': current_token})
            current_token = ''


if __name__ == '__main__':
    texto = texto = """variable1 123
    45.67 abc123   1000.000
    _variable
    123variable variable_123 3.14159 numeroGrande1234567890 1.
    .75 casa123calle
    123.456.789 varConNúmero1Y2
    0.001 enteroGrande999999999999999999 realNegativo-3.14 varConEspacio 1
    varConSigno$ varConPuntoYComa;
    0 identificadorConMúltiplesNúmeros1234567890 1E10
    varConGuion-medio varConCaracteresEspeciales!@# 9999. .1234
    enteroConLetras123abc 123,456"""
    tokens = obtener_siguiente_token(texto)
    for token in tokens:
        print(token)

        


        
        
