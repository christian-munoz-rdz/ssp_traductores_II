from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QPushButton, QWidget
import sys

class AnalizadorLexico:
    def __init__(self, texto=''):
        self.texto = texto
        self.pos = 0

    def es_letra(self, char):
        return char.isalpha()

    def es_digito(self, char):
        return char.isdigit()

    def obtener_siguiente_token(self):
        while self.pos < len(self.texto):
            if self.texto[self.pos].isspace() or self.texto[self.pos] == '\n':
                self.pos += 1
            elif self.es_letra(self.texto[self.pos]):
                inicio = self.pos
                self.pos += 1
                while self.pos < len(self.texto) and (self.es_letra(self.texto[self.pos]) or self.es_digito(self.texto[self.pos])):
                    self.pos += 1
                if self.texto[self.pos].isspace() or self.texto[self.pos] == '\n':
                    token = {'tipo': 'identificador', 'valor': self.texto[inicio:self.pos]}
                    self.pos += 1
                    return token
                else:
                    while self.pos < len(self.texto) and not (self.texto[self.pos].isspace() or self.texto[self.pos] == '\n'):
                        self.pos += 1
                    return {'tipo': 'error', 'valor': self.texto[inicio:self.pos]}              
            elif self.es_digito(self.texto[self.pos]):
                inicio = self.pos
                self.pos += 1
                while self.pos < len(self.texto) and self.es_digito(self.texto[self.pos]):
                    self.pos += 1
                if self.texto[self.pos] == '.':
                    self.pos += 1
                    if self.texto[self.pos].isspace() or self.texto[self.pos] == '\n':
                        self.pos += 1
                        return {'tipo': 'error', 'valor': self.texto[inicio:self.pos]}
                    elif self.es_digito(self.texto[self.pos]):
                        while self.pos < len(self.texto) and self.es_digito(self.texto[self.pos]):
                            self.pos += 1
                        if self.texto[self.pos].isspace() or self.texto[self.pos] == '\n':
                            token = {'tipo': 'real', 'valor': self.texto[inicio:self.pos]}
                            self.pos += 1
                            return token
                        else:
                            while self.pos < len(self.texto) and not (self.texto[self.pos].isspace() or self.texto[self.pos] == '\n'):
                                self.pos += 1
                            return {'tipo': 'error', 'valor': self.texto[inicio:self.pos]}
                    else:
                        while self.pos < len(self.texto) and not (self.texto[self.pos].isspace() or self.texto[self.pos] == '\n'):
                            self.pos += 1
                        return {'tipo': 'error', 'valor': self.texto[inicio:self.pos]}
                elif self.texto[self.pos].isspace() or self.texto[self.pos] == '\n':
                    token = {'tipo': 'entero', 'valor': self.texto[inicio:self.pos]}
                    self.pos += 1
                    return token
                else:
                    while self.pos < len(self.texto) and not (self.texto[self.pos].isspace() or self.texto[self.pos] == '\n'):
                        self.pos += 1
                    return {'tipo': 'error', 'valor': self.texto[inicio:self.pos]}
            else:
                inicio = self.pos
                self.pos += 1
                while self.pos < len(self.texto) and not (self.texto[self.pos].isspace() or self.texto[self.pos] == '\n'):
                    self.pos += 1
                return {'tipo': 'error', 'valor': self.texto[inicio:self.pos]}

    def analizar(self):
        tokens = []
        token = self.obtener_siguiente_token()
        while token:
            tokens.append(token)
            token = self.obtener_siguiente_token()
        return tokens

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
        self.analyzeButton.clicked.connect(self.analyzeText)

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
        text = self.textEdit.toPlainText()
        analizador = AnalizadorLexico(text)
        tokens = analizador.analizar()

        self.tokensTable.setRowCount(len(tokens))

        for i, token in enumerate(tokens):
            self.tokensTable.setItem(i, 0, QTableWidgetItem(token['tipo']))
            self.tokensTable.setItem(i, 1, QTableWidgetItem(token['valor']))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())