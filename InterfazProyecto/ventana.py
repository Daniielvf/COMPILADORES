from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from estilos import ESTILO

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

        self.tabla.setColumnCount(5)

        self.tabla.setHorizontalHeaderLabels([
            "No.",
            "Token",
            "Lexema",
            "Tipo",
            "Línea"
        ])

        # La columna No. será pequeña
        self.tabla.horizontalHeader().setSectionResizeMode(
            0,
            QHeaderView.Fixed
        )
        self.tabla.setColumnWidth(0, 55)

        # Las demás columnas ocupan el espacio disponible
        self.tabla.horizontalHeader().setSectionResizeMode(
            1,
            QHeaderView.Stretch
        )

        self.tabla.horizontalHeader().setSectionResizeMode(
            2,
            QHeaderView.Stretch
        )

        self.tabla.horizontalHeader().setSectionResizeMode(
            3,
            QHeaderView.Stretch
        )

        # Línea también será un poco más pequeña
        self.tabla.horizontalHeader().setSectionResizeMode(
            4,
            QHeaderView.Fixed
        )
        self.tabla.setColumnWidth(4, 80)

        self.tabla.setAlternatingRowColors(True)
        self.tabla.setMinimumHeight(250)

        layout.addWidget(self.tabla)

        # =========================
        # Estado
        # =========================
        estadoLayout = QHBoxLayout()

        self.lblEstado = QLabel("●  Estado:  Listo para analizar")
        self.lblEstado.setObjectName("estado")

        self.lblTokens = QLabel("Tokens encontrados:  0")
        self.lblTokens.setObjectName("tokensEncontrados")

        estadoLayout.addWidget(self.lblEstado)
        estadoLayout.addStretch()
        estadoLayout.addWidget(self.lblTokens)

        layout.addLayout(estadoLayout)

        # =========================
        # Botones de abajo
        # =========================
        botones = QHBoxLayout()
        botones.setSpacing(12)

        self.btnReporte1 = QPushButton("▣  Reporte General")
        self.btnReporte2 = QPushButton("▦  Tabla de Símbolos")
        self.btnMongo = QPushButton("◉  MongoDB")
        self.btnSalir = QPushButton("✕  Salir")

        self.btnReporte1.setObjectName("btnInferior")
        self.btnReporte2.setObjectName("btnInferior")
        self.btnMongo.setObjectName("btnInferior")
        self.btnSalir.setObjectName("btnSalir")

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
        self.btnSalir.clicked.connect(self.close)
        self.btnAnalizar.clicked.connect(self.analizar)
        self.btnExaminar.clicked.connect(self.abrirArchivo)

    # ======================================
    # Los metodos
    # ======================================

    def crearTarjeta(self, grid, fila, columna, icono, texto):

        tarjeta = QFrame()
        tarjeta.setObjectName("tarjeta")

        layoutTarjeta = QHBoxLayout()
        layoutTarjeta.setContentsMargins(15, 12, 15, 12)

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

        grid.addWidget(tarjeta, fila, columna)

        return lblNumero

    def analizar(self):

        if not self.txtArchivo.text():
            QMessageBox.warning(
                self,
                "Advertencia",
                "Primero debe seleccionar un archivo Ruby."
            )
            return

        self.lblEstado.setText("●  Estado:  Analizando...")

        QMessageBox.information(
            self,
            "Analizador",
            "Aquí ejecutaremos el analizador léxico."
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