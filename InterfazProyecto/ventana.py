from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from estilos import ESTILO
import subprocess
import os

from reportes.generador_pdf import generar_reporte_1, generar_reporte_2
from database.mongo import guardar_tabla_simbolos

from PySide6.QtWidgets import (
    QFileDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QFrame
)


class VentanaPrincipal(QMainWindow):

    def __init__(self):
        super().__init__()

        # =========================
        # Datos del analisis
        # =========================
        self.tokens = []
        self.estadisticas = {}
        self.simbolos = []

        self.setStyleSheet(ESTILO)
        self.setWindowTitle("Analizador Léxico Ruby")
        self.resize(1150, 850)

        # =========================
        # Ventana principal
        # =========================
        widget = QWidget()
        self.setCentralWidget(widget)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(15)

        widget.setLayout(layout)

        # =========================
        # Titulo
        # =========================
        encabezado = QHBoxLayout()

        self.logo = QLabel()
        self.logo.setFixedSize(65, 65)

        pixmap = QPixmap("recursos/ruby.png")

        if not pixmap.isNull():
            pixmap = pixmap.scaled(
                60,
                60,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

            self.logo.setPixmap(pixmap)

        textos = QVBoxLayout()

        titulo = QLabel("ANALIZADOR LÉXICO PARA RUBY")
        titulo.setObjectName("tituloPrincipal")

        subtitulo = QLabel(
            "Analiza archivos .rb e identifica sus tokens léxicos"
        )

        subtitulo.setObjectName("subtitulo")

        textos.addWidget(titulo)
        textos.addWidget(subtitulo)

        encabezado.addWidget(self.logo)
        encabezado.addLayout(textos)
        encabezado.addStretch()

        layout.addLayout(encabezado)

        # =========================
        # Selección de archivo
        # =========================
        panelArchivo = QFrame()
        panelArchivo.setObjectName("panelArchivo")

        archivoLayout = QHBoxLayout()
        archivoLayout.setContentsMargins(20, 15, 20, 15)

        lblArchivo = QLabel("Archivo Ruby:")
        lblArchivo.setObjectName("labelArchivo")

        self.txtArchivo = QLineEdit()
        self.txtArchivo.setPlaceholderText(
            "Seleccione un archivo Ruby (.rb)"
        )

        self.txtArchivo.setReadOnly(True)

        self.btnExaminar = QPushButton("📂  Examinar")
        self.btnExaminar.setObjectName("btnSecundario")
        self.btnExaminar.setMinimumWidth(150)
        self.btnExaminar.setMinimumHeight(45)

        self.btnAnalizar = QPushButton("▷  Analizar")
        self.btnAnalizar.setObjectName("btnPrincipal")
        self.btnAnalizar.setMinimumWidth(150)
        self.btnAnalizar.setMinimumHeight(45)

        archivoLayout.addWidget(lblArchivo)
        archivoLayout.addWidget(self.txtArchivo, 1)
        archivoLayout.addWidget(self.btnExaminar)
        archivoLayout.addWidget(self.btnAnalizar)

        panelArchivo.setLayout(archivoLayout)

        layout.addWidget(panelArchivo)

        # =========================
        # Estadisticas
        # =========================
        grupo = QGroupBox("ESTADÍSTICAS")
        grupo.setObjectName("grupoEstadisticas")

        grid = QGridLayout()
        grid.setSpacing(12)

        grupo.setLayout(grid)

        self.lblReservadas = self.crearTarjeta(
            grid, 0, 0, "🔖", "Reservadas"
        )

        self.lblIdentificadores = self.crearTarjeta(
            grid, 0, 1, "ID", "Identificadores"
        )

        self.lblEnteros = self.crearTarjeta(
            grid, 0, 2, "123", "Enteros"
        )

        self.lblFlotantes = self.crearTarjeta(
            grid, 1, 0, "1.23", "Flotantes"
        )

        self.lblBooleanos = self.crearTarjeta(
            grid, 1, 1, "true", "Booleanos"
        )

        self.lblCadenas = self.crearTarjeta(
            grid, 1, 2, "❝", "Cadenas"
        )

        self.lblOperadores = self.crearTarjeta(
            grid, 2, 0, "+−*/", "Operadores"
        )

        self.lblLineas = self.crearTarjeta(
            grid, 2, 1, "☷", "Líneas"
        )

        self.lblCaracteres = self.crearTarjeta(
            grid, 2, 2, "A", "Caracteres"
        )

        layout.addWidget(grupo)

        # =========================
        # Tabla de Tokens
        # =========================
        self.tabla = QTableWidget()

        self.tabla.setColumnCount(4)

        self.tabla.setHorizontalHeaderLabels([
            "Token",
            "Lexema",
            "Tipo",
            "Línea"
        ])

        # Las columnas ocupan el espacio disponible
        self.tabla.horizontalHeader().setSectionResizeMode(
            0,
            QHeaderView.Stretch
        )

        self.tabla.horizontalHeader().setSectionResizeMode(
            1,
            QHeaderView.Stretch
        )

        self.tabla.horizontalHeader().setSectionResizeMode(
            2,
            QHeaderView.Stretch
        )

        # Línea será un poco más pequeña
        self.tabla.horizontalHeader().setSectionResizeMode(
            3,
            QHeaderView.Fixed
        )

        self.tabla.setColumnWidth(3, 80)

        self.tabla.setAlternatingRowColors(True)
        self.tabla.setMinimumHeight(250)

        layout.addWidget(self.tabla)

        # =========================
        # Estado
        # =========================
        estadoLayout = QHBoxLayout()

        self.lblEstado = QLabel(
            "●  Estado:  Listo para analizar"
        )

        self.lblEstado.setObjectName("estado")

        self.lblTokens = QLabel(
            "Tokens encontrados:  0"
        )

        self.lblTokens.setObjectName(
            "tokensEncontrados"
        )

        estadoLayout.addWidget(self.lblEstado)
        estadoLayout.addStretch()
        estadoLayout.addWidget(self.lblTokens)

        layout.addLayout(estadoLayout)

        # =========================
        # Botones de abajo
        # =========================
        botones = QHBoxLayout()
        botones.setSpacing(12)

        self.btnReporte1 = QPushButton(
            "▣  Reporte General"
        )

        self.btnReporte2 = QPushButton(
            "▦  Tabla de Símbolos"
        )

        self.btnMongo = QPushButton(
            "◉  MongoDB"
        )

        self.btnSalir = QPushButton(
            "✕  Salir"
        )

        self.btnReporte1.setObjectName(
            "btnInferior"
        )

        self.btnReporte2.setObjectName(
            "btnInferior"
        )

        self.btnMongo.setObjectName(
            "btnInferior"
        )

        self.btnSalir.setObjectName(
            "btnSalir"
        )

        self.btnReporte1.setMinimumHeight(45)
        self.btnReporte2.setMinimumHeight(45)
        self.btnMongo.setMinimumHeight(45)
        self.btnSalir.setMinimumHeight(45)

        botones.addWidget(self.btnReporte1)
        botones.addWidget(self.btnReporte2)
        botones.addWidget(self.btnMongo)
        botones.addWidget(self.btnSalir)

        layout.addLayout(botones)

        # =========================
        # Conectar botones
        # =========================
        self.btnReporte1.clicked.connect(
            self.crearReporte1
        )

        self.btnReporte2.clicked.connect(
            self.crearReporte2
        )

        self.btnMongo.clicked.connect(
            self.guardarMongoDB
        )

        self.btnSalir.clicked.connect(
            self.close
        )

        self.btnAnalizar.clicked.connect(
            self.analizar
        )

        self.btnExaminar.clicked.connect(
            self.abrirArchivo
        )

    # ======================================
    # Los metodos
    # ======================================

    def crearTarjeta(
        self,
        grid,
        fila,
        columna,
        icono,
        texto
    ):

        tarjeta = QFrame()
        tarjeta.setObjectName("tarjeta")

        layoutTarjeta = QHBoxLayout()

        layoutTarjeta.setContentsMargins(
            15,
            12,
            15,
            12
        )

        lblIcono = QLabel(icono)
        lblIcono.setObjectName("iconoTarjeta")
        lblIcono.setFixedWidth(55)

        datos = QVBoxLayout()

        lblTexto = QLabel(texto)
        lblTexto.setObjectName("textoTarjeta")

        lblNumero = QLabel("0")
        lblNumero.setObjectName("numeroTarjeta")

        datos.addWidget(lblTexto)
        datos.addWidget(lblNumero)

        layoutTarjeta.addWidget(lblIcono)
        layoutTarjeta.addLayout(datos)

        tarjeta.setLayout(layoutTarjeta)

        grid.addWidget(
            tarjeta,
            fila,
            columna
        )

        return lblNumero

    def analizar(self):

        archivo = self.txtArchivo.text()

        if archivo == "":

            QMessageBox.warning(
                self,
                "Error",
                "Seleccione un archivo Ruby."
            )

            return

        try:

            self.lblEstado.setText(
                "●  Estado:  Analizando..."
            )

            # =========================
            # Leer archivo Ruby
            # =========================
            with open(
                archivo,
                "r",
                encoding="utf-8"
            ) as archivo_ruby:

                contenido = archivo_ruby.readlines()

            cantidad_lineas = len(contenido)

            cantidad_caracteres = 0

            for linea_archivo in contenido:
                cantidad_caracteres += len(
                    linea_archivo
                )

            # =========================
            # Ruta del analizador Flex
            # =========================
            ruta_analizador = os.path.join(
                os.path.dirname(__file__),
                "..",
                "Analizador",
                "Analizador"
            )

            # =========================
            # Ejecutar analizador Flex
            # =========================
            with open(
                archivo,
                "r",
                encoding="utf-8"
            ) as entrada:

                resultado = subprocess.run(
                    [ruta_analizador],
                    stdin=entrada,
                    capture_output=True,
                    text=True
                )

            if resultado.returncode != 0:

                raise Exception(
                    resultado.stderr
                )

            lineas_resultado = (
                resultado.stdout.splitlines()
            )

            # =========================
            # Limpiar datos anteriores
            # =========================
            self.tabla.setRowCount(0)

            self.tokens = []
            self.simbolos = []
            self.estadisticas = {}

            conta_reservadas = 0
            conta_identificadores = 0
            conta_enteros = 0
            conta_flotantes = 0
            conta_booleanos = 0
            conta_cadenas = 0
            conta_operadores = 0

            conteo_reservadas = {}

            # =========================
            # Tokens de operadores
            # =========================
            tokens_operadores = {
                "=": "TK_ASIGNACION",
                "+": "TK_SUMA",
                "-": "TK_RESTA",
                "*": "TK_MULTIPLICACION",
                "/": "TK_DIVISION",
                "%": "TK_MODULO",
                "==": "TK_IGUALDAD",
                "!=": "TK_DIFERENTE",
                ">": "TK_MAYOR",
                "<": "TK_MENOR",
                ">=": "TK_MAYOR_IGUAL",
                "<=": "TK_MENOR_IGUAL",
                "&&": "TK_AND",
                "||": "TK_OR",
                "!": "TK_NOT"
            }

            # =========================
            # Procesar salida de Flex
            # =========================
            for resultado_linea in lineas_resultado:

                partes = resultado_linea.split(
                    " -> ",
                    1
                )

                if len(partes) != 2:
                    continue

                izquierda = partes[0]
                lexema = partes[1]

                datos = izquierda.split(
                    ": ",
                    1
                )

                if len(datos) != 2:
                    continue

                numero_linea = (
                    datos[0]
                    .replace("Linea ", "")
                )

                tipo = datos[1]

                # =========================
                # Contadores
                # =========================
                if tipo == "Palabra reservada":

                    conta_reservadas += 1

                    if lexema in conteo_reservadas:

                        conteo_reservadas[
                            lexema
                        ] += 1

                    else:

                        conteo_reservadas[
                            lexema
                        ] = 1

                elif tipo == "Identificador":

                    conta_identificadores += 1

                elif tipo == "Entero":

                    conta_enteros += 1

                elif tipo == "Flotante":

                    conta_flotantes += 1

                elif tipo == "Booleano":

                    conta_booleanos += 1

                elif tipo == "Cadena":

                    conta_cadenas += 1

                elif tipo == "Operador":

                    conta_operadores += 1

                # =========================
                # Asignar token
                # =========================
                if tipo == "Palabra reservada":

                    token = (
                        "TK_" +
                        lexema.upper()
                    )

                elif tipo == "Identificador":

                    token = "TK_IDENTIFICADOR"

                elif tipo == "Entero":

                    token = "TK_ENTERO"

                elif tipo == "Flotante":

                    token = "TK_FLOTANTE"

                elif tipo == "Booleano":

                    if lexema == "true":

                        token = "TK_TRUE"

                    else:

                        token = "TK_FALSE"

                elif tipo == "Cadena":

                    token = "TK_CADENA"

                elif tipo == "Operador":

                    token = tokens_operadores.get(
                        lexema,
                        "TK_OPERADOR"
                    )

                else:

                    token = "TK_DESCONOCIDO"

                # =========================
                # Guardar token
                # =========================
                self.tokens.append({
                    "token": token,
                    "lexema": lexema,
                    "tipo": tipo,
                    "linea": int(numero_linea)
                })

                # =========================
                # Tabla de simbolos
                # =========================
                if tipo == "Identificador":

                    self.simbolos.append({
                        "token": token,
                        "lexema": lexema,
                        "tipo": tipo,
                        "linea": int(numero_linea)
                    })

                # =========================
                # Mostrar en tabla
                # =========================
                fila = self.tabla.rowCount()

                self.tabla.insertRow(fila)

                self.tabla.setItem(
                    fila,
                    0,
                    QTableWidgetItem(token)
                )

                self.tabla.setItem(
                    fila,
                    1,
                    QTableWidgetItem(lexema)
                )

                self.tabla.setItem(
                    fila,
                    2,
                    QTableWidgetItem(tipo)
                )

                self.tabla.setItem(
                    fila,
                    3,
                    QTableWidgetItem(
                        numero_linea
                    )
                )

            # =========================
            # Guardar estadisticas
            # =========================
            self.estadisticas = {
                "lineas": cantidad_lineas,
                "caracteres": cantidad_caracteres,
                "enteros": conta_enteros,
                "flotantes": conta_flotantes,
                "identificadores":
                    conta_identificadores,
                "booleanos": conta_booleanos,
                "cadenas": conta_cadenas,
                "operadores": conta_operadores,
                "reservadas":
                    conteo_reservadas
            }

            # =========================
            # Mostrar estadisticas
            # =========================
            self.lblReservadas.setText(
                str(conta_reservadas)
            )

            self.lblIdentificadores.setText(
                str(conta_identificadores)
            )

            self.lblEnteros.setText(
                str(conta_enteros)
            )

            self.lblFlotantes.setText(
                str(conta_flotantes)
            )

            self.lblBooleanos.setText(
                str(conta_booleanos)
            )

            self.lblCadenas.setText(
                str(conta_cadenas)
            )

            self.lblOperadores.setText(
                str(conta_operadores)
            )

            self.lblLineas.setText(
                str(cantidad_lineas)
            )

            self.lblCaracteres.setText(
                str(cantidad_caracteres)
            )

            total_tokens = len(
                self.tokens
            )

            self.lblTokens.setText(
                "Tokens encontrados: " +
                str(total_tokens)
            )

            self.lblEstado.setText(
                "●  Estado:  Análisis completado"
            )

            QMessageBox.information(
                self,
                "Análisis completado",
                "El archivo Ruby fue analizado correctamente."
            )

        except Exception as error:

            self.lblEstado.setText(
                "●  Estado:  Error durante el análisis"
            )

            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo ejecutar el analizador:\n{error}"
            )

    def abrirArchivo(self):

        archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo Ruby",
            "",
            "Archivos Ruby (*.rb)"
        )

        if archivo:

            self.txtArchivo.setText(archivo)

            self.lblEstado.setText(
                "●  Estado:  Archivo cargado correctamente"
            )

    def crearReporte1(self):

        # =========================
        # Validar analisis
        # =========================
        if not self.estadisticas:

            QMessageBox.warning(
                self,
                "Reporte General",
                "Primero debe analizar un archivo Ruby."
            )

            return

        archivo, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar Reporte General",
            "Reporte_General.pdf",
            "Archivos PDF (*.pdf)"
        )

        if not archivo:
            return

        if not archivo.endswith(".pdf"):
            archivo += ".pdf"

        try:

            generar_reporte_1(
                archivo,
                self.estadisticas
            )

            QMessageBox.information(
                self,
                "Reporte generado",
                "El Reporte General se generó correctamente."
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo generar el reporte:\n{error}"
            )

    def crearReporte2(self):

        # =========================
        # Validar analisis
        # =========================
        if not self.tokens:

            QMessageBox.warning(
                self,
                "Reporte de Símbolos",
                "Primero debe analizar un archivo Ruby."
            )

            return

        archivo, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar Reporte de Símbolos",
            "Reporte_Simbolos.pdf",
            "Archivos PDF (*.pdf)"
        )

        if not archivo:
            return

        if not archivo.endswith(".pdf"):
            archivo += ".pdf"

        try:

            generar_reporte_2(
                archivo,
                self.tokens,
                self.simbolos
            )

            QMessageBox.information(
                self,
                "Reporte generado",
                "El Reporte de Símbolos se generó correctamente."
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo generar el reporte:\n{error}"
            )

    def guardarMongoDB(self):

        # =========================
        # Validar tabla de simbolos
        # =========================
        if not self.simbolos:

            QMessageBox.warning(
                self,
                "MongoDB",
                "Primero debe analizar un archivo Ruby."
            )

            return

        try:

            cantidad = guardar_tabla_simbolos(
                self.simbolos
            )

            QMessageBox.information(
                self,
                "MongoDB",
                f"Tabla de símbolos guardada correctamente.\n\n"
                f"Registros guardados: {cantidad}"
            )

            self.lblEstado.setText(
                "●  Estado:  Tabla de símbolos guardada en MongoDB"
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Error MongoDB",
                str(error)
            )