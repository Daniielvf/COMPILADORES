from PySide6.QtWidgets import QApplication
from ventana import Ventana

app = QApplication([])

ventana = Ventana()
ventana.show()

app.exec()