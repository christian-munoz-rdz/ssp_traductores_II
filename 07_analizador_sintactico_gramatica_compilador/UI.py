import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHBoxLayout
import scanner

# Clase principal de la ventana de la aplicación
class TokenizerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Compilador')
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
        self.tableWidget.setHorizontalHeaderLabels(['Token', 'Lexema', 'Número'])
        layout.addWidget(self.tableWidget)

        #Añadir text edit vacío a la derecha
        self.textEdit2 = QTextEdit()
        layout.addWidget(self.textEdit2)
        
        # Widget contenedor y set layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
    def analyzeText(self):
        codigo = self.textEdit.toPlainText() + "$"
        tokens = scanner.obtener_tokens(codigo)
        self.tableWidget.setRowCount(len(tokens))
        
        for i, token in enumerate(tokens):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(token.simbolo))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(token.lexema))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(str(token.numero)))
        
# Punto de entrada de la aplicación
def main():
    app = QApplication(sys.argv)
    ex = TokenizerWindow()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()