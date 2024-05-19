import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHBoxLayout, QMessageBox
import subprocess


class TokenizerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Compilador')
        self.setGeometry(100, 100, 1200, 600)
        
        # Layout principal
        layout = QHBoxLayout()
        vlayout_scan = QVBoxLayout()
        vlayout_tree = QVBoxLayout()
        vlayout_tokens = QVBoxLayout()
        
        # Área de texto para entrada de código
        self.code_space = QTextEdit()
        vlayout_scan.addWidget(self.code_space)
        
        # Botón para analizar el texto
        self.btnAnalyze = QPushButton('Analizar')
        self.btnAnalyze.clicked.connect(self.analyzeText)
        vlayout_scan.addWidget(self.btnAnalyze)

        # Mostrar generracion de codigo
        self.showCode = QTextEdit()
        vlayout_scan.addWidget(self.showCode)

        layout.addLayout(vlayout_scan)
        
        # Mostrar tokens en text edit
        self.showTokens = QTextEdit()
        vlayout_tokens.addWidget(self.showTokens)
        layout.addLayout(vlayout_tokens)

        # Espacio para mostrar output del codigo
        self.showResult = QTextEdit()
        vlayout_tokens.addWidget(self.showResult)

        #Espacio para parsing tree
        self.parsing_tree_space = QTextEdit()
        vlayout_tree.addWidget(self.parsing_tree_space)

        layout.addLayout(vlayout_tree)
        
        # Widget contenedor y set layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
    def analyzeText(self):
        codigo = self.code_space.toPlainText()
        with open('./input/main.c', 'w') as file:
            file.write(codigo)
        result = subprocess.run(['python', 'compiler.py', '-r', '-v', '-ef', '-ast', '-ast', '-st', '-t', '.\input\main.c'], capture_output=True, text=True)
        
        # revisa errores
        with open('./errors/lexical_errors.txt', 'r') as file:
            errores_lexicos = file.read()
        QMessageBox.about(self, "Errores", f"Errores lexicos: {errores_lexicos}")
        with open('./errors/syntax_errors.txt', 'r') as file:
            errores_sintacticos = file.read()
        QMessageBox.about(self, "Errores", f"Errores sintacticos: {errores_sintacticos}")
        with open('./errors/semantic_errors.txt', 'r') as file:
            errores_semanticos = file.read()
        QMessageBox.about(self, "Errores", f"Errores semanticos: {errores_semanticos}")
        
        # abre el archivo de tokens
        with open('./output/tokens.txt', 'r') as file:
            tokens = file.read()
            self.showTokens.setText(tokens)
        # abre el archivo de arbol de parsing en utf-8
        with open('./output/parse_tree.txt', 'r', encoding='utf-8') as file:
            arbol = file.read()
            self.parsing_tree_space.setText(arbol)

        # abre el archivo de codigo generado
        with open('./output/output.txt', 'r') as file:
            codigo_generado = file.read()
            self.showCode.setText(codigo_generado)
        
        #muestra el resultado de la compilacion
        self.showResult.setText(result.stdout)
        

        
# Punto de entrada de la aplicación
def main():
    app = QApplication(sys.argv)
    ex = TokenizerWindow()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()