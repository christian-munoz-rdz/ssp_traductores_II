import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHBoxLayout, QMessageBox, QLabel

class Tokenizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Analizador Sintactico')
        self.setGeometry(100, 100, 1200, 600)

        # Layout principal
        h_layout = QHBoxLayout()
        v_layout = QVBoxLayout()

        # Área de texto para entrada de código
        self.textEdit = QTextEdit()
        v_layout.addWidget(self.textEdit)

        # Botón para analizar el texto
        self.btnAnalyze = QPushButton('Analizar')
        self.btnAnalyze.clicked.connect(self.analyzeText)
        v_layout.addWidget(self.btnAnalyze)

        # Tabla para mostrar los tokens
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(['Token', 'Lexema', 'Identificador'])
        h_layout.addLayout(v_layout)
        h_layout.addWidget(self.tableWidget)

        # Widget contenedor y set layout
        container = QWidget()
        container.setLayout(h_layout)
        self.setCentralWidget(container)

    def analyzeText(self):
        elementos = []
        pila = [0]
        tokens = []
        reglas = []
        tabla_slr = []
        estado = 0
        indice = 0
        cadena = self.textEdit.toPlainText() + '$'
        identificador = []
        while (indice <= (len(cadena) - 1) and estado == 0):
            lexema = ''
            token = 'error'
            while (indice <= (len(cadena) - 1) and estado != 20):
                if estado == 0:
                    if (cadena[indice].isspace()):
                        estado = 0
                    elif cadena[indice].isalpha() or cadena[indice] == '_':
                        estado = 4
                        lexema += cadena[indice]
                        token = 'id'
                        identificador = 1
                    elif cadena[indice].isnumeric():
                        estado = 20
                        lexema += cadena[indice]
                        token = 'constante'
                        identificador = 13
                    elif cadena[indice] == '$':
                        estado = 20
                        lexema += cadena[indice]
                        token = 'pesos'
                        identificador = 18
                    elif cadena[indice] == '=':
                        lexema += cadena[indice]
                        token = 'asignación'
                        estado = 5
                        identificador = 8
                    elif cadena[indice] == '>':

                        lexema += cadena[indice]
                        token = 'opRelacional'
                        estado = 5
                        identificador = 15
                    elif cadena[indice] == '<':

                        lexema += cadena[indice]
                        token = 'opRelacional'
                        estado = 5
                        identificador = 15
                    elif cadena[indice] == '!':

                        lexema += cadena[indice]
                        estado = 5
                    elif cadena[indice] == ';':

                        lexema += cadena[indice]
                        token = ';'
                        estado = 20
                        identificador = 2
                    elif cadena[indice] == '+':

                        lexema += cadena[indice]
                        token = 'opSuma'
                        estado = 20
                        identificador = 14
                    elif cadena[indice] == '-':

                        lexema += cadena[indice]
                        token = 'opSuma'
                        estado = 20
                        identificador = 14
                    elif cadena[indice] == '*':

                        lexema += cadena[indice]
                        token = 'opMultiplicacion'
                        estado = 20
                        identificador = 16
                    elif cadena[indice] == ',':

                        lexema += cadena[indice]
                        token = 'coma'
                        estado = 20
                        identificador = 3
                    elif cadena[indice] == '(':

                        lexema += cadena[indice]
                        token = '('
                        estado = 20
                        identificador = 4
                    elif cadena[indice] == ')':

                        lexema += cadena[indice]
                        token = ')'
                        estado = 20
                        identificador = 5
                    elif cadena[indice] == '{':

                        lexema += cadena[indice]
                        token = '{'
                        estado = 20
                        identificador = 6
                    elif cadena[indice] == '}':

                        lexema += cadena[indice]
                        token = '}'
                        estado = 20
                        identificador = 7
                    elif cadena[indice] == '|':

                        lexema += cadena[indice]
                        estado = 15
                    elif cadena[indice] == '&':

                        lexema += cadena[indice]
                        estado = 16
                    else:
                        estado = 20
                        token = 'error'
                        lexema = cadena[indice]
                        identificador = 18
                    indice += 1

                elif estado == 4:
                    if cadena[indice].isdigit() or cadena[indice].isalpha() or cadena[indice] == '_':
                        estado = 4
                        lexema += cadena[indice]
                        token = 'id'
                        indice += 1
                    else:
                        estado = 20

                elif estado == 5:
                    if cadena[indice] != '=':
                        estado = 20
                    else:
                        estado = 20
                        lexema += cadena[indice]
                        token = 'opRelacional'
                        identificador = 17
                    indice += 1
                elif estado == 15:
                    if cadena[indice] != '|':
                        estado = 20
                    else:
                        estado = 20
                        lexema += cadena[indice]
                        token = 'opLogico'
                        identificador = 15
                        indice += 1
                elif estado == 16:
                    if cadena[indice] != '&':
                        token = 'error'
                        estado = 20
                    else:
                        estado = 20
                        lexema += cadena[indice]
                        token = 'opLogico'
                        identificador = 15
                        indice += 1

            estado = 0
            elementos.append({'token': token, 'lexema': lexema,
                              'identificador': identificador})

        for elemento in elementos:
            if elemento['lexema'] == "if":
                elemento['token'] = "condicional SI"
                elemento['identificador'] = 9
            if elemento['lexema'] == "else":
                elemento['token'] = "else"
                elemento['identificador'] = 12
            if elemento['lexema'] == "while":
                elemento['token'] = "while"
                elemento['identificador'] = 10
            if elemento['lexema'] == "return":
                elemento['token'] = "return"
                elemento['identificador'] = 11
            if elemento['lexema'] == "int":
                elemento['token'] = "tipo de dato"
                elemento['identificador'] = 0
            if elemento['lexema'] == "float":
                elemento['token'] = "tipo de dato"
                elemento['identificador'] = 0
            if elemento['lexema'] == "char":
                elemento['token'] = "tipo de dato"
                elemento['identificador'] = 0
            if elemento['lexema'] == "void":
                elemento['token'] = "tipo de dato"
                elemento['identificador'] = 0

        # Limpiar la tabla anterior
        self.tableWidget.setRowCount(0)

        # Mostrar los resultados en la tabla
        for elemento in elementos:
            rowCount = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowCount)
            self.tableWidget.setItem(rowCount, 0, QTableWidgetItem(elemento['token']))
            self.tableWidget.setItem(rowCount, 1, QTableWidgetItem(elemento['lexema']))
            self.tableWidget.setItem(rowCount, 2, QTableWidgetItem(str(elemento['identificador'])))
            tokens.append(elemento['identificador'])

        with open('GR2slrRulesId.txt', 'r') as archivo_reglas:
            for fila in archivo_reglas:
                arreglo_fila = fila.strip().split('\t')
                arreglo_fila = [int(numero) for numero in arreglo_fila]
                reglas.append(arreglo_fila)

        with open('GR2slrTable.txt', 'r') as archivo_tabla:
            for fila in archivo_tabla:
                arreglo_fila = fila.strip().split('\t')
                arreglo_fila = [int(numero) for numero in arreglo_fila]
                del (arreglo_fila[0])
                tabla_slr.append(arreglo_fila)

        continuar_analisis = True

        while tokens and continuar_analisis:
            accion = tabla_slr[pila[-1]][tokens[0]]
            if accion == -1:
                # Significa que la cadena es valida, muestralo en interfaz
                QMessageBox.about(self, "Resultado", "Cadena Válida")
                continuar_analisis = False
            # Si es mayor a 0 en la tabla, significa que es un desplazamiento (lo que vendria siendo dX) haciendola a mano, X es el que te da la tabla
            elif accion > 0:
                pila.append(tokens[0])
                pila.append(accion)
                del (tokens[0])
            # Si es menor que 0, significa que es una reduccion (lo que vendria siendo rX) haciendola a mano, nomas que en la tabla el -1 es r0, el -2 es r1 y asi, por eso lo ajustamos
            elif accion < 0:
                accion = abs(accion + 1)
                regla = reglas[accion]
                for i in range(regla[1] * 2):
                    pila.pop()
                pila.append(regla[0])
                pila.append(tabla_slr[pila[-2]][pila[-1]])
            else:
                # Significa que la cadena es invalida, muestralo en interfaz
                QMessageBox.about(self, "Resultado", "Cadena Inválida")

                continuar_analisis = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Tokenizer()
    window.show()
    sys.exit(app.exec_())