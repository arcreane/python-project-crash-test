import sys
from PySide6.QtWidgets import QApplication
from OpenMain import InterfaceController

if __name__ == "__main__":
    app = QApplication(sys.argv)

    controller = InterfaceController("radar.ui")  # on crée le contrôleur
    controller.show()  # il contient déjà la fenêtre

    sys.exit(app.exec())
