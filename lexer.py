import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QPushButton, QWidget

class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

    def __str__(self):
        return f"{self.tipo}: {self.valor}"

class Identificador(Token):
    def __init__(self, valor):
        super().__init__('IDENTIFICADOR', valor)


class Entero(Token):
    def __init__(self, valor):
        super().__init__('ENTERO', valor)


class Real(Token):
    def __init__(self, valor):
        super().__init__('REAL', valor)

class AnalizadorLexico:
    def __init__(self, texto):
        self.texto = texto
        self.pos = 0

    def es_letra(self, char):
        return char.isalpha()

    def es_digito(self, char):
        return char.isdigit()

    def obtener_siguiente_token(self):
        while self.pos < len(self.texto):
            if self.texto[self.pos].isspace():
                self.pos += 1
                continue

            if self.es_letra(self.texto[self.pos]):
                inicio = self.pos
                while self.pos < len(self.texto) and (self.es_letra(self.texto[self.pos]) or self.es_digito(self.texto[self.pos])):
                    self.pos += 1
                return Identificador(self.texto[inicio:self.pos])

            if self.es_digito(self.texto[self.pos]):
                inicio = self.pos
                while self.pos < len(self.texto) and self.es_digito(self.texto[self.pos]):
                    self.pos += 1
                if self.pos < len(self.texto) and self.texto[self.pos] == '.':
                    self.pos += 1
                    if self.pos < len(self.texto) and self.es_digito(self.texto[self.pos]):
                        while self.pos < len(self.texto) and self.es_digito(self.texto[self.pos]):
                            self.pos += 1
                        return Real(self.texto[inicio:self.pos])
                return Entero(self.texto[inicio:self.pos])

            self.pos += 1

        return None

    def analizar(self):
        tokens = []
        while self.pos < len(self.texto):
            token = self.obtener_siguiente_token()
            if token:
                tokens.append(token)
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
            self.tokensTable.setItem(i, 0, QTableWidgetItem(token.tipo))
            self.tokensTable.setItem(i, 1, QTableWidgetItem(token.valor))

def main():
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
