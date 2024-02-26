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
        ";": ("Punto y coma", ";", 12), ",": ("Coma", ",", 13), "(": ("ParéntesisI", "(", 14), ")": ("ParéntesisD", ")", 15), 
        "{": ("LlaveI", "{", 16), "}": ("LlaveD", "}", 17), "=": ("Asignación", "=", 18),
        "if": ("Palabra Reservada", "if", 19), "while": ("Palabra Reservada", "while", 20), 
        "return": ("Palabra Reservada", "return", 21), "else": ("Palabra Reservada", "else", 22), 
        "+": ("Operador Suma", "+", 5), "-": ("Operador Suma", "-", 5),
        "||": ("Operador Or", "||", 8), "&&": ("Operador And", "&&", 9), "!": ("Operador Not", "!", 10),
        "*": ("Operador Multiplicacion", "*", 6), "/": ("Operador Multiplicacion", "/", 6), 
        "==": ("Operador Igualdad", "==", 11), "!=": ("Operador Igualdad", "!=", 11), "<": ("Operador Relacional", "<", 7), 
        "<=": ("Operador Relacional", "<=", 7), ">": ("Operador Relacional", ">", 7), ">=": ("Operador Relacional", ">=", 7),  
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
        
        if es_letra(codigo[i]):  # Inicio de identificador o palabra reservada
            while i < longitud and (es_letra(codigo[i]) or es_digito(codigo[i])):
                temp += codigo[i]
                i += 1
            
            if temp in tipos_de_dato:
                tokens_identificados.append(("Tipo de Dato", temp, 4))
            elif temp in tokens:
                tokens_identificados.append(tokens[temp])
            else:
                tokens_identificados.append(("Identificador", temp, 0))
        
        elif es_digito(codigo[i]) or (codigo[i] == '.' and i + 1 < longitud and es_digito(codigo[i + 1])):  # Inicio de constante numérica
            while i < longitud and (es_digito(codigo[i]) or codigo[i] == '.'):
                temp += codigo[i]
                i += 1
            if es_entero(temp):
                tokens_identificados.append(("Entero", temp, 1))
            elif es_real(temp):
                tokens_identificados.append(("Real", temp, 2))
        
        else:  # Otros caracteres (operadores, delimitadores)
            temp += codigo[i]
            if i + 1 < longitud:
                temp_doble = temp + codigo[i + 1]
                if temp_doble in tokens:  # Verificar operadores de dos caracteres
                    tokens_identificados.append(tokens[temp_doble])
                    i += 2
                    continue
            if temp in tokens:
                tokens_identificados.append(tokens[temp])
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

        #Añadir text edit vacío a la derecha
        self.textEdit2 = QTextEdit()
        layout.addWidget(self.textEdit2)
        
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