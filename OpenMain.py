from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

class InterfaceController:
    def __init__(self, ui_path):
        # Charge l'interface .ui
        loader = QUiLoader()
        ui_file = QFile(ui_path)
        ui_file.open(QFile.ReadOnly)
        self.window = loader.load(ui_file)
        ui_file.close()

        self.vitesse = 0

        # Connecte les boutons ici
        self.connect_signals()

    def connect_signals(self):
        """
        Connecte les signaux (clics de boutons) aux méthodes correspondantes.
        """
        try:
            self.window.AltSup.clicked.connect(self.Alt1)
            self.window.AltInf.clicked.connect(self.Alt2)

            self.window.sliderspeed.valueChanged.connect(self.slider_changeSpeed)
            self.window.slideralt.valueChanged.connect(self.slider_changeAlt)

        except AttributeError:
            pass

    # Fonctions appelées par les boutons
    def Alt1(self):
        pass

    def Alt2(self):
        pass

    def slider_changeSpeed(self, valeur):
        self.vitesse = valeur
        self.window.labelspeed.setText(f"Valeur : {valeur}")
    def slider_changeAlt(self, valeur):
        self.vitesse = valeur
        self.window.labelalt.setText(f"Valeur : {valeur}")

    def show(self):
        self.window.show()
