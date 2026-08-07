from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout
)

class Ventana(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Analizador Lexico Ruby")
        self.resize(900,600)

        titulo = QLabel("ANALIZADOR LEXICO PARA RUBY")

        boton = QPushButton("Abrir archivo")

        layout = QVBoxLayout()

        layout.addWidget(titulo)
        layout.addWidget(boton)

        self.setLayout(layout)