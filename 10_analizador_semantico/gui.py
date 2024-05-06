import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHBoxLayout, QMessageBox
import subprocess

# Clase principal de la ventana de la aplicación
class TokenizerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.acepted = False
        self.arbol = None
        
    def initUI(self):
        self.setWindowTitle('Compilador')
        self.setGeometry(100, 100, 1200, 600)
        
        # Layout principal
        layout = QHBoxLayout()
        vlayout_scan = QVBoxLayout()
        vlayout_tree = QVBoxLayout()
        
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

        #Espacio para parsing tree
        self.textEdit2 = QTextEdit()
        vlayout_tree.addWidget(self.textEdit2)

        layout.addLayout(vlayout_tree)
        
        # Widget contenedor y set layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
    def analyzeText(self):
        codigo = self.textEdit.toPlainText()
        #Guardar el código en un archivo en una ruta específica
        with open('input/main.c', 'w') as f:
            f.write(codigo)
        subprocess.run(['python', 'compiler.py', '-r', '-v', '-ef', '-ast', '-st', '-t', 'input/main.c'])
'''
        codigo += "$"
        tokens = obtener_tokens(codigo)
        self.tableWidget.setRowCount(len(tokens))
        self.acepted, self.arbol = analizar(tokens)
        for i, token in enumerate(tokens):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(token.simbolo))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(token.lexema))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(str(token.numero)))
        
        if self.acepted:
            QMessageBox.about(self, "Resultado", "Sintaxis correcta")
            self.textEdit2.setText(self.arbol)
        else:
            QMessageBox.about(self, "Resultado", "Error de sintaxis")
            self.textEdit2.setText("Error de sintaxis. Arbol no disponible")
        
        with open('errors/semantic_errors.txt', 'r') as f:
            errores = f.read()
        if errores:
            QMessageBox.about(self, "Resultado", "Error semántico")
            self.textEdit2.setText(errores)
            return
'''
        
# Punto de entrada de la aplicación
def main():
    app = QApplication(sys.argv)
    ex = TokenizerWindow()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()