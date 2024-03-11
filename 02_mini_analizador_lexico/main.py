from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QPushButton, QWidget
import sys

#Definimos las reglas de los tokens
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

#Definimos la clase Token
class Token:
    def __init__(self, tipo, reglas=None):
        self.tipo = tipo
        self.valor = ''
        self.reglas = reglas
    
    def set_valor(self, input):
            self.valor = input
    
    def rule_check(self, input):
        return self.reglas(input)
    
    def return_token(self):
        return (self.tipo,self.valor)

#Utilizamos herencia para definir los diferentes tipos de tokens
class Identificador(Token):
    def __init__(self):
        super().__init__('identificador', es_identificador)

class Entero(Token):
    def __init__(self):
        super().__init__('entero', es_entero)

class Real(Token):
    def __init__(self):
        super().__init__('real', es_real)

class Error(Token):
    def __init__(self):
        super().__init__('error')

#Definimos el analizador lexico
class AnalizadorLexico:
    def __init__(self, texto=''):
        self.texto = texto

    def obtener_tokens(self):
            """
            Esta función analiza el texto y devuelve una lista de tokens encontrados.
            
            Returns:
                list: Lista de tokens encontrados en el texto.
            """
            identificador = Identificador()
            entero = Entero()
            real = Real()
            error = Error()
            pos = 0
            tokens = []
            current_token = ''
            while pos < len(self.texto):
                char = self.texto[pos]
                if (char in ['\n', '\t', ' ']) or (pos == len(self.texto) - 1):
                    if current_token:

                        if pos == len(self.texto) - 1:
                            current_token += char

                        if identificador.rule_check(current_token):
                            identificador.set_valor(current_token)
                            tokens.append(identificador.return_token())
                        elif entero.rule_check(current_token):
                            entero.set_valor(current_token)
                            tokens.append(entero.return_token())
                        elif real.rule_check(current_token):
                            real.set_valor(current_token)
                            tokens.append(real.return_token())
                        else:
                            error.set_valor(current_token)
                            tokens.append(error.return_token())
                        current_token = ''
                else:
                    current_token += char
                pos += 1
            return tokens

#Definimos la interfaz grafica   
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Analizador Léxico")
        self.setGeometry(100, 100, 800, 600)

        # Layouts
        layout = QHBoxLayout()
        leftLayout = QVBoxLayout()
        rightLayout = QVBoxLayout()

        # Componentes
        self.textEdit = QTextEdit()
        self.analyzeButton = QPushButton("Analizar")
        self.analyzeButton.clicked.connect(self.analyzeText) # Conectar el evento click del botón con el método analyzeText

        self.tokensTable = QTableWidget()
        self.tokensTable.setColumnCount(2)
        self.tokensTable.setHorizontalHeaderLabels(["Tipo", "Valor"])

        # Añadir componentes a los layouts
        leftLayout.addWidget(self.textEdit)
        leftLayout.addWidget(self.analyzeButton)

        rightLayout.addWidget(self.tokensTable)

        layout.addLayout(leftLayout)
        layout.addLayout(rightLayout)

        # Contenedor central
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def analyzeText(self):
        """
        Analiza el texto ingresado en el widget de texto y muestra los tokens en una tabla.
        """
        text = self.textEdit.toPlainText() # Obtenemos el texto del widget de texto
        analizador = AnalizadorLexico(text) # Creamos una instancia del analizador léxico con el texto ingresado
        tokens = analizador.obtener_tokens() # Obtenemos los tokens del analizador léxico

        self.tokensTable.setRowCount(len(tokens))

        # Mostramos los tokens en la tabla
        for i, token in enumerate(tokens):
            tipo = QTableWidgetItem(token[0])
            valor = QTableWidgetItem(token[1])

            self.tokensTable.setItem(i, 0, tipo)
            self.tokensTable.setItem(i, 1, valor)

#Ejecutamos la interfaz grafica
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())