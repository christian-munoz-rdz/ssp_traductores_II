import pandas as pd
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHBoxLayout, QMessageBox
import anytree

# Definición de la gramática
gramatica = """
Gramática:
R1 = programa -> Definiciones 
R2 = Definiciones -> \e 
R3 = Definiciones -> Definicion Definiciones
R4 = Definicion -> DefVar
R5 = Definicion -> DefFunc
R6 = DefVar -> tipo identificador ListaVar ;
R7 = ListaVar -> \e
R8 = ListaVar -> , identificador ListaVar 
R9 = DefFunc -> tipo identificador ( Parametros ) BloqFunc 
R10 = Parametros -> \e
R11 = Parametros -> tipo identificador ListaParam
R12 = ListaParam -> \e
R13 = ListaParam -> , tipo identificador ListaParam
R14 = BloqFunc -> { DefLocales }
R15 = DefLocales -> \e
R16 = DefLocales -> DefLocal DefLocales
R17 = DefLocal -> DefVar
R18 = DefLocal -> Sentencia
R19 = Sentencias -> \e
R20 = Sentencias -> Sentencia Sentencias
R21 = Sentencia -> identificador = Expresion ;
R22 = Sentencia -> if ( Expresion ) SentenciaBloque Otro 
R23 = Sentencia -> while ( Expresion ) Bloque
R24 = Sentencia -> return ValorRegresa ;
R25 = Sentencia -> LlamadaFunc ;
R26 = Otro -> \e
R27 = Otro -> else SentenciaBloque
R28 = Bloque -> { Sentencias }
R29 = ValorRegresa -> \e
R30 = ValorRegresa -> Expresion
R31 = Argumentos -> \e
R32 = Argumentos -> Expresion ListaArgumentos
R33 = ListaArgumentos -> \e
R34 = ListaArgumentos -> , Expresion ListaArgumentos
R35 = Termino -> LlamadaFunc
R36 = Termino -> identificador
R37 = Termino -> entero
R38 = Termino -> real
R39 = Termino -> cadena
R40 = LlamadaFunc -> identificador ( Argumentos )
R41 = SentenciaBloque -> Sentencia
R42 = SentenciaBloque -> Bloque
R43 = Expresion -> ( Expresion )
R44 = Expresion -> opSuma Expresion
R45 = Expresion -> opNot Expresion
R46 = Expresion -> Expresion opMul Expresion
R47 = Expresion -> Expresion opSuma Expresion
R48 = Expresion -> Expresion opRelac Expresion
R49 = Expresion -> Expresion opIgualdad Expresion
R50 = Expresion -> Expresion opAnd Expresion
R51 = Expresion -> Expresion opOr Expresion
R52 = Expresion -> Termino
"""

# Definición de las funciones auxiliares para el análisis léxico
def es_letra(c):
    return c.isalpha()

def es_digito(c):
    return c.isdigit()

def es_espacio(c):
    return c in ' \t\n\r'

def es_entero(cadena):
    try:
        int(cadena)
        return True
    except ValueError:
        return False

def es_numero_real(cadena):
    if '.' in cadena:
        try:
            float(cadena)
            return True
        except ValueError:
            return False
    else:
        return False

class SymbolTable:
    def __init__(self):
        self.table = {}
        self.current_scope = [{}]  # Lista de diccionarios, uno por cada nivel de anidamiento

    def enter_scope(self):
        self.current_scope.append({})

    def exit_scope(self):
        self.current_scope.pop()

    def declare(self, name, symbol_info):
        if name in self.current_scope[-1]:
            raise Exception(f"Error: Variable '{name}' ya declarada en este ámbito.")
        self.current_scope[-1][name] = symbol_info

    def declare_function(self, name, return_type, parameters):
        if name in self.current_scope[-1]:
            raise Exception(f"Error: Función '{name}' ya declarada en este ámbito.")
        self.current_scope[-1][name] = {'type': 'function', 'return_type': return_type, 'parameters': parameters}

    def lookup(self, name):
        for scope in reversed(self.current_scope):
            if name in scope:
                return scope[name]
        raise Exception(f"Error: Variable o función '{name}' no declarada.")

    def check_function_call(self, name, args):
        func_info = self.lookup(name)
        if func_info['type'] != 'function':
            raise Exception(f"Error: '{name}' no es una función.")
        if len(args) != len(func_info['parameters']):
            raise Exception(f"Error: Número incorrecto de argumentos para la función '{name}'. Se esperaban {len(func_info['parameters'])}, se recibieron {len(args)}.")
        for arg, param in zip(args, func_info['parameters']):
            if arg['type'] != param['type']:
                raise Exception(f"Error: Tipo de argumento incorrecto para la función '{name}'. Se esperaba '{param['type']}', se recibió '{arg['type']}'.")

    def check_assignment(self, name, value_type):
        var_info = self.lookup(name)
        if var_info['type'] != value_type:
            raise Exception(f"Error: Tipo de asignación incorrecto para la variable '{name}'. Se esperaba '{var_info['type']}', se recibió '{value_type}'.")

# Diccionarios para los lexemas y palabras reservadas
lexemas = {
    "int": ("tipo", 4), "float": ("tipo", 4), "void": ("tipo", 4), 
    "+": ("opSuma", 5), "-": ("opSuma", 5), 
    "*": ("opMul", 6), "/": ("opMul", 6),
    "<": ("opRelac", 7), "<=": ("opRelac", 7), ">": ("opRelac", 7), ">=": ("opRelac", 7), 
    "||": ("opOr", 8), 
    "&&": ("opAnd", 9),
    "!": ("opNot", 10),
    "==": ("opIgualdad", 11), "!=": ("opIgualdad", 11),
    ";": (";", 12), 
    ",": (",", 13),
    "(": ("(", 14), 
    ")": (")", 15),
    "{": ("{", 16),
    "}": ("}", 17),
    "=": ("=", 18),
    "if": ("if", 19), 
    "while": ("while", 20),
    "return": ("return", 21),
    "else": ("else", 22),
    "$": ("$", 23)
}

palabras_reservadas = ["int", "float", "void", "if", "while", "return", "else"]
simbolos = ["+", "-", "*", "/", "<", "<=", ">", ">=", "||", "&&", "!", "==", "!=", ";", ",", "(", ")", "{", "}", "=", "$", "&", "|"]

# Clase para representar un token
class Token:
    def __init__(self, lexema, simbolo, numero):
        self.lexema = lexema
        self.simbolo = simbolo
        self.numero = numero 
    
    def __str__(self):
        return f"[{self.simbolo} -> {self.lexema}]"
    
    def __repr__(self):
        return str(self)

# Función para obtener los tokens de una cadena de código
def obtener_tokens(codigo):
    i = 0
    longitud = len(codigo)
    tokens = []

    while i < longitud:
        if es_espacio(codigo[i]):
            i += 1
            continue
        
        current_token = ""
        
        if es_letra(codigo[i]):
            while i < longitud and (es_letra(codigo[i]) or es_digito(codigo[i])):
                current_token += codigo[i]
                i += 1

            if current_token in palabras_reservadas:
                tokens.append(Token(current_token, lexemas[current_token][0], lexemas[current_token][1]))
            else:
                tokens.append(Token(current_token, "identificador", 0))
        elif es_digito(codigo[i]):
            cuenta_puntos = 0
            while i < longitud and (es_digito(codigo[i]) or (codigo[i] == '.' and cuenta_puntos < 1)):
                if codigo[i] == '.':
                    cuenta_puntos += 1

                current_token += codigo[i]
                if cuenta_puntos > 1:
                    break
                i += 1
            
            if cuenta_puntos == 0:
                tokens.append(Token(current_token, "entero", 0))
            elif cuenta_puntos == 1:
                tokens.append(Token(current_token, "real", 0))
            else:
                tokens.append(Token(current_token, "error", -1))
        else:
            current_token = codigo[i]
            if current_token not in simbolos:
                tokens.append(Token(current_token, "error", -1))
                i += 1
            else:
                if (i + 1) < longitud and (current_token + codigo[i + 1]) in simbolos:
                    i += 1
                    current_token += codigo[i]
                    tokens.append(Token(current_token, lexemas[current_token][0], lexemas[current_token][1]))
                    i += 1
                else:
                    tokens.append(Token(current_token, lexemas[current_token][0], lexemas[current_token][1]))
                    i += 1
    return tokens

# Cargar la tabla de parsing
parsing_table = pd.read_csv('compilador.csv', index_col=0)
parsing_table.fillna("error", inplace=True)

# Diccionario de reducciones
reducciones = {
    1: ('programa', 1),
    2: ('Definiciones', 0),
    3: ('Definiciones', 2),
    4: ('Definicion', 1),
    5: ('Definicion', 1),
    6: ('DefVar', 4),
    7: ('ListaVar', 0),
    8: ('ListaVar', 3),
    9: ('DefFunc', 6),
    10: ('Parametros', 0),
    11: ('Parametros', 3),
    12: ('ListaParam', 0),
    13: ('ListaParam', 4),
    14: ('BloqFunc', 3),
    15: ('DefLocales', 0),
    16: ('DefLocales', 2),
    17: ('DefLocal', 1),
    18: ('DefLocal', 1),
    19: ('Sentencias', 0),
    20: ('Sentencias', 2),
    21: ('Sentencia', 4),
    22: ('Sentencia', 6),
    23: ('Sentencia', 5),
    24: ('Sentencia', 3),
    25: ('Sentencia', 2),
    26: ('Otro', 0),
    27: ('Otro', 2),
    28: ('Bloque', 3),
    29: ('ValorRegresa', 0),
    30: ('ValorRegresa', 1),
    31: ('Argumentos', 0),
    32: ('Argumentos', 2),
    33: ('ListaArgumentos', 0),
    34: ('ListaArgumentos', 3),
    35: ('Termino', 1),
    36: ('Termino', 1),
    37: ('Termino', 1),
    38: ('Termino', 1),
    39: ('Termino', 1),
    40: ('LlamadaFunc', 4),
    41: ('SentenciaBloque', 1),
    42: ('SentenciaBloque', 1),
    43: ('Expresion', 3),
    44: ('Expresion', 2),
    45: ('Expresion', 2),
    46: ('Expresion', 3),
    47: ('Expresion', 3),
    48: ('Expresion', 3),
    49: ('Expresion', 3),
    50: ('Expresion', 3),
    51: ('Expresion', 3),
    52: ('Expresion', 1)
}

non_terminals = ['programa', 'Definiciones', 'Definicion', 'DefVar', 'ListaVar', 'DefFunc', 'Parametros', 'ListaParam', 'BloqFunc', 'DefLocales', 
                 'DefLocal', 'Sentencias', 'Sentencia', 'Otro', 'Bloque', 'ValorRegresa', 'Argumentos', 'ListaArgumentos', 'Termino', 'LlamadaFunc', 
                 'SentenciaBloque', 'Expresion']

# Clase para la pila
class Pila:
    def __init__(self):
        self.pila = []
    
    def push(self, elemento):
        self.pila.append(elemento)
    
    def pop(self):
        return self.pila.pop()
    
    def top(self):
        return self.pila[-1]
    
# Clase para la generación de código
class CodeGenerator:
    def __init__(self):
        self.code = []
        self.temp_count = 0

    def new_temp(self):
        temp_name = f"t{self.temp_count}"
        self.temp_count += 1
        return temp_name

    def generate(self, instruction):
        self.code.append(instruction)

    def get_code(self):
        return "\n".join(self.code)

def analizar(tokens):
    pila = Pila()
    pila.push(0)
    i = 0
    longitud = len(tokens)
    acepted = False

    # Crea la raíz del árbol de análisis
    root = anytree.Node("programa")
    current_node = root # rastrea el nodo actual para agregar hijos
    node_stack = []  # Pila para almacenar los nodos del árbol

    symbol_table = SymbolTable()
    code_generator = CodeGenerator()

    while i < longitud:
        print(pila.pila)
        print(symbol_table.current_scope)
        
        token = tokens[i]
        estado = pila.top()
        accion = parsing_table.loc[estado, token.simbolo]
        if accion == 'r0':
            acepted = True
            root.children = node_stack
            break    
        elif accion[0] == 'd':
            pila.push(token)
            pila.push(int(accion[1:]))

            # Crea un nuevo nodo terminal y lo agrega al stack
            new_terminal = anytree.Node(token.lexema, parent=current_node)
            node_stack.append(new_terminal)

            if token.simbolo == '$':
                continue
            else:
                i += 1
        elif accion[0] == 'r':
            regla = int(accion[1:])
            regla = reducciones[regla]
            no_terminal = regla[0]

            new_non_terminal = anytree.Node(no_terminal, parent=None)
            for _ in range(regla[1]):
                current_node = node_stack.pop()
                current_node.parent = new_non_terminal
            
            node_stack.append(new_non_terminal)
            
            for _ in range(regla[1]*2):
                pila.pop()
            estado = pila.top()
            pila.push(no_terminal)
            pila.push(int(parsing_table.loc[estado, no_terminal]))
            print(f"Reducir: {no_terminal}")

            # Reglas para la generación de código
            if no_terminal == 'DefVar':
                tipo = tokens[i-3].lexema
                nombre = tokens[i-2].lexema
                try:
                    symbol_table.declare(nombre, {'tipo': tipo})
                except Exception as e:
                    print(e)
                    return (False, None)
            elif no_terminal == 'DefFunc':
                tipo = tokens[i-4].lexema
                nombre = tokens[i-3].lexema
                # Obtener los parámetros de la función
                parametros = []  # Extrae los parámetros del token correspondiente
                try:
                    symbol_table.declare_function(nombre, tipo, parametros)
                except Exception as e:
                    print(e)
                    return (False, None)
                symbol_table.enter_scope()
            elif no_terminal == 'BloqFunc':
                symbol_table.exit_scope()
            elif no_terminal == 'DefLocal':
                tipo = tokens[i-3].lexema
                nombre = tokens[i-2].lexema
                try:
                    symbol_table.declare(nombre, {'tipo': tipo})
                except Exception as e:
                    print(e)
                    return (False, None)
            elif no_terminal == 'Sentencia':
                if tokens[i-1].lexema == '=':
                    nombre = tokens[i-2].lexema
                    tipo_asignacion = "int"  # Determinar el tipo de la expresión a la derecha
                    try:
                        symbol_table.check_assignment(nombre, tipo_asignacion)
                    except Exception as e:
                        print(e)
                        return (False, None)
                    # Generar código para la asignación
                    temp_var = code_generator.new_temp()
                    code_generator.generate(f"{temp_var} = {tokens[i-1].lexema}")
                    code_generator.generate(f"{nombre} = {temp_var}")
            elif no_terminal == 'LlamadaFunc':
                nombre = tokens[i-4].lexema
                # Obtener los argumentos de la llamada a función
                argumentos = []  # Extrae los argumentos del token correspondiente
                try:
                    symbol_table.check_function_call(nombre, argumentos)
                except Exception as e:
                    print(e)
                    return (False, None)
            elif no_terminal == 'ValorRegresa':
                if tokens[i-1].lexema != ';':
                    nombre = tokens[i-2].lexema
                    try:
                        symbol_table.lookup(nombre)
                    except Exception as e:
                        print(e)
                        return (False, None)
            elif no_terminal == 'Termino':
                if tokens[i-1].simbolo == 'identificador':
                    nombre = tokens[i-1].lexema
                    try:
                        symbol_table.lookup(nombre)
                    except Exception as e:
                        print(e)
                        return (False, None)
            elif no_terminal == 'Expresion':
                if tokens[i-2].simbolo == 'identificador':
                    nombre = tokens[i-2].lexema
                    try:
                        symbol_table.lookup(nombre)
                    except Exception as e:
                        print(e)
                        return (False, None)
                if tokens[i-2].simbolo == '(':
                    if tokens[i-3].simbolo == 'identificador':
                        nombre = tokens[i-3].lexema
                        try:
                            symbol_table.lookup(nombre)
                        except Exception as e:
                            print(e)
                            return (False, None)
            elif no_terminal == 'DefLocales':
                pass
            elif no_terminal == 'Parametros':
                pass
            elif no_terminal == 'ListaParam':
                pass
            elif no_terminal == 'ListaVar':
                pass
            elif no_terminal == 'ListaArgumentos':
                pass
            elif no_terminal == 'Argumentos':
                pass
            elif no_terminal == 'Sentencias':
                pass
            elif no_terminal == 'SentenciaBloque':
                pass
            elif no_terminal == 'Otro':
                pass
            elif no_terminal == 'Bloque':
                pass
            elif no_terminal == 'programa':
                pass

        else:
            break
    
    if acepted:
        # recorrer el árbol para eliminar todas las hojas sin hijos que sean no terminales
        for pre, _, node in anytree.RenderTree(root):
            if node.children == ():
                if node.name in non_terminals:
                    node.parent = None

        arbol = anytree.RenderTree(root).by_attr()

        # Retornar la bandera de aceptación, el árbol y el código generado
        return (acepted, arbol, code_generator.get_code())
    else:
        return (acepted, None, None)

# Clase principal de la ventana de la aplicación
class TokenizerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.acepted = False
        self.arbol = None
        self.codigo = None
        
    def initUI(self):
        self.setWindowTitle('Compilador')
        self.setGeometry(100, 100, 1200, 600)
        
        # Layout principal
        layout = QHBoxLayout()
        vlayout_scan = QVBoxLayout()
        vlayout_tree = QVBoxLayout()
        vlayout_code = QVBoxLayout()
        
        # Área de texto para entrada de código
        self.textEdit = QTextEdit()
        vlayout_scan.addWidget(self.textEdit)
        
        # Botón para analizar el texto
        self.btnAnalyze = QPushButton('Analizar')
        self.btnAnalyze.clicked.connect(self.analyzeText)
        vlayout_scan.addWidget(self.btnAnalyze)

        layout.addLayout(vlayout_scan)
        
        # Tabla para mostrar los tokens
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(['Token', 'Lexema', 'Número'])
        layout.addWidget(self.tableWidget)

        # Espacio para parsing tree
        self.textEdit2 = QTextEdit()
        vlayout_tree.addWidget(self.textEdit2)

        # Espacio para el código generado
        self.textEdit3 = QTextEdit()
        vlayout_code.addWidget(self.textEdit3)

        layout.addLayout(vlayout_tree)
        layout.addLayout(vlayout_code)
        
        # Widget contenedor y set layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
    def analyzeText(self):
        codigo = self.textEdit.toPlainText() + "$"
        tokens = obtener_tokens(codigo)
        self.tableWidget.setRowCount(len(tokens))
        try:
            self.acepted, self.arbol, self.codigo = analizar(tokens)
        except Exception as e:
            QMessageBox.about(self, "Resultado", str(e))
            self.textEdit2.setText("Error de análisis semántico. Árbol no disponible")
            return
        
        for i, token in enumerate(tokens):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(token.simbolo))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(token.lexema))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(str(token.numero)))
        
        if self.acepted:
            QMessageBox.about(self, "Resultado", "Sintaxis y semántica correctas")
            self.textEdit2.setText(self.arbol)
            self.textEdit3.setText(self.codigo)
        else:
            QMessageBox.about(self, "Resultado", "Error de sintaxis")
            self.textEdit2.setText("Error de sintaxis. Árbol no disponible")
            self.textEdit3.setText("")

# Punto de entrada de la aplicación
def main():
    app = QApplication(sys.argv)
    ex = TokenizerWindow()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
