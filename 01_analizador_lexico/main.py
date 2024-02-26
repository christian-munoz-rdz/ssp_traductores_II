import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHBoxLayout

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
        
        if codigo[i] == '"':  # Inicio de cadena
            inicio_cadena = i
            i += 1
            while i < longitud and codigo[i] != '"':
                temp += codigo[i]
                i += 1
            if i < longitud and codigo[i] == '"':  # Cerrar cadena correctamente
                temp = codigo[inicio_cadena:i+1]
                tokens_identificados.append(("cadena", temp, 3))
                i += 1
            else:
                # Error: cadena no cerrada
                temp = codigo[inicio_cadena:i+1]
                tokens_identificados.append(("Error: Cadena no cerrada", temp, -1))
        
        elif es_letra(codigo[i]):  # Inicio de identificador o palabra reservada
            inicio_token = i
            while i < longitud and (es_letra(codigo[i]) or es_digito(codigo[i])):
                temp += codigo[i]
                i += 1
            
            if not es_identificador(temp):  # Si el identificador no es válido
                tokens_identificados.append(("Error: Identificador no válido", codigo[inicio_token:i], -1))
            elif temp in tipos_de_dato:
                tokens_identificados.append(("tipo", temp, 4))
            elif temp in tokens:
                tokens_identificados.append(tokens[temp])
            else:
                tokens_identificados.append(("identificador", temp, 0))
        
        elif es_digito(codigo[i]):  # Inicio de constante numérica
            inicio_numero = i
            while i < longitud and (es_digito(codigo[i]) or codigo[i] == '.'):
                temp += codigo[i]
                i += 1
            
            if not es_entero(temp) and not es_real(temp):  # Si el número no es válido
                tokens_identificados.append(("Error: Número no válido", codigo[inicio_numero:i], -1))
            elif es_entero(temp):
                tokens_identificados.append(("entero", temp, 1))
            elif es_real(temp):
                tokens_identificados.append(("real", temp, 2))
        
        else:  # Otros caracteres (operadores, delimitadores) o errores
            temp += codigo[i]
            if i + 1 < longitud:
                temp_doble = temp + codigo[i + 1]
                if temp_doble in tokens:  # Verificar operadores de dos caracteres
                    tokens_identificados.append(tokens[temp_doble])
                    i += 2
                    continue
            if temp in tokens:
                tokens_identificados.append(tokens[temp])
            else:
                # Error: caracter no reconocido
                tokens_identificados.append(("Error: Caracter no reconocido", temp, -1))
            i += 1

    return tokens_identificados

# Clase principal de la ventana de la aplicación
class TokenizerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Analizador de Tokens')
        self.setGeometry(100, 100, 1200, 600)
        
        # Layout principal
        layout = QHBoxLayout()
        
        # Área de texto para entrada de código
        self.textEdit = QTextEdit()
        layout.addWidget(self.textEdit)
        
        # Botón para analizar el texto
        self.btnAnalyze = QPushButton('Analizar')
        self.btnAnalyze.clicked.connect(self.analyzeText)
        layout.addWidget(self.btnAnalyze)
        
        # Tabla para mostrar los tokens
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(['Tipo de Token', 'Token', 'Número Asociado'])
        layout.addWidget(self.tableWidget)
        
        # Widget contenedor y set layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
    def analyzeText(self):
        codigo = self.textEdit.toPlainText()
        tokens = obtener_tokens(codigo)
        self.tableWidget.setRowCount(len(tokens))
        
        for i, token in enumerate(tokens):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(token[0]))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(token[1]))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(str(token[2])))
        
# Punto de entrada de la aplicación
def main():
    app = QApplication(sys.argv)
    ex = TokenizerWindow()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()