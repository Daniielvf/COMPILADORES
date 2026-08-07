from PySide6.QtCore import Qt
from estilos import ESTILO

from PySide6.QtWidgets import (
    QApplication,
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
    QVBoxLayout,
    QWidget
)


class VentanaPrincipal(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setStyleSheet(ESTILO)
        self.setWindowTitle("Analizador Léxico Ruby")
        self.resize(1000, 700)

        # =========================
        # Ventana principal
        # =========================
        widget = QWidget()
        self.setCentralWidget(widget)

        layout = QVBoxLayout()
        widget.setLayout(layout)

        # =========================
        # Titulo
        # =========================
        titulo = QLabel("ANALIZADOR LÉXICO PARA RUBY")
        titulo.setAlignment(Qt.AlignCenter)

        titulo.setStyleSheet("""
            font-size:30px;
            font-weight:bold;
            color:#1F3A93;
            padding:10px;
        """)

        layout.addWidget(titulo)

        # =========================
        # Selección de archivo
        # =========================
        archivoLayout = QHBoxLayout()

        self.txtArchivo = QLineEdit()
        self.txtArchivo.setPlaceholderText("Seleccione un archivo Ruby (.rb)")

        self.btnExaminar = QPushButton("📂 Examinar")
        self.btnExaminar.setMinimumHeight(40)

        archivoLayout.addWidget(self.txtArchivo)
        archivoLayout.addWidget(self.btnExaminar)

        layout.addLayout(archivoLayout)

        # =========================
        # Accion de Boton Analizar
        # =========================
        self.btnAnalizar = QPushButton("▶ Analizar")
        self.btnAnalizar.setMinimumHeight(45)

        analizarLayout = QHBoxLayout()
        analizarLayout.addStretch()
        analizarLayout.addWidget(self.btnAnalizar)
        analizarLayout.addStretch()

        layout.addLayout(analizarLayout)

        # =========================
        # Estadisticas
        # =========================
        grupo = QGroupBox("Estadísticas")

        grid = QGridLayout()
        grupo.setLayout(grid)

        grid.addWidget(QLabel("Reservadas"), 0, 0)
        self.lblReservadas = QLabel("0")
        grid.addWidget(self.lblReservadas, 0, 1)

        grid.addWidget(QLabel("Identificadores"), 1, 0)
        self.lblIdentificadores = QLabel("0")
        grid.addWidget(self.lblIdentificadores, 1, 1)

        grid.addWidget(QLabel("Enteros"), 2, 0)
        self.lblEnteros = QLabel("0")
        grid.addWidget(self.lblEnteros, 2, 1)

        grid.addWidget(QLabel("Flotantes"), 3, 0)
        self.lblFlotantes = QLabel("0")
        grid.addWidget(self.lblFlotantes, 3, 1)

        grid.addWidget(QLabel("Booleanos"), 4, 0)
        self.lblBooleanos = QLabel("0")
        grid.addWidget(self.lblBooleanos, 4, 1)

        grid.addWidget(QLabel("Cadenas"), 5, 0)
        self.lblCadenas = QLabel("0")
        grid.addWidget(self.lblCadenas, 5, 1)

        grid.addWidget(QLabel("Operadores"), 6, 0)
        self.lblOperadores = QLabel("0")
        grid.addWidget(self.lblOperadores, 6, 1)

        grid.addWidget(QLabel("Lineas"), 7, 0)
        self.lblLineas = QLabel("0")
        grid.addWidget(self.lblLineas, 7, 1)

        grid.addWidget(QLabel("Caracteres"), 8, 0)
        self.lblCaracteres = QLabel("0")
        grid.addWidget(self.lblCaracteres, 8, 1)

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
            "Linea"
        ])

        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.setAlternatingRowColors(True)
        self.tabla.setMinimumHeight(250)

        layout.addWidget(self.tabla)

        # =========================
        # Botones de abajo
        # =========================
        botones = QHBoxLayout()

        self.btnReporte1 = QPushButton("📄 Reporte General")
        self.btnReporte2 = QPushButton("📑 Tabla de Símbolos")
        self.btnMongo = QPushButton("💾 MongoDB")
        self.btnSalir = QPushButton("❌ Salir")

        self.btnReporte1.setMinimumHeight(40)
        self.btnReporte2.setMinimumHeight(40)
        self.btnMongo.setMinimumHeight(40)
        self.btnSalir.setMinimumHeight(40)

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

    def analizar(self):
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