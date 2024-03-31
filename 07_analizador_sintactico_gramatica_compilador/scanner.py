import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHBoxLayout

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
        

tabla_simbolos = {
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

simbolos = ["+", "-", "*", "/", "<", "<=", ">", ">=", "||", "&&", "!", "==", "!=", ";", ",", "(", ")", "{", "}", "="]

class Token:
    def __init__(self, lexema, simbolo, numero):
        self.lexema = lexema
        self.simbolo = simbolo
        self.numero = numero 
    
    def __str__(self):
        return f"( Token: {self.lexema}, {self.simbolo}, {self.numero} )"
    
    def __repr__(self):
        return str(self)

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
                tokens.append(Token(current_token, current_token, tabla_simbolos[current_token][1]))
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
            if i + 1 < longitud and (codigo[i]  in simbolos or codigo[i] + codigo[i + 1] in simbolos):
                current_token += codigo[i + 1]
                i += 1
            i += 1
            if current_token in tabla_simbolos:
                tokens.append(Token(current_token, current_token, tabla_simbolos[current_token][1]))
            else:
                tokens.append(Token(current_token, "error", -1))

    return tokens

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