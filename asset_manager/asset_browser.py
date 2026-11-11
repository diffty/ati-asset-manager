from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QWidget, QListWidget
from PySide6.QtWidgets import QHBoxLayout


class AssetBrowserApp:
    def __init__(self):
        self.app = QApplication()

        self.fenetre_principale = QMainWindow()

        self.widget_principal = QWidget()

        self.layout_principal = QHBoxLayout()
        self.widget_principal.setLayout(self.layout_principal)

        self.kind_list_widget = QListWidget()
        self.layout_principal.addWidget(self.kind_list_widget)

        self.category_list_widget = QListWidget()
        self.layout_principal.addWidget(self.category_list_widget)

        self.asset_list_widget = QListWidget()
        self.layout_principal.addWidget(self.asset_list_widget)

        self.files_list_widget = QListWidget()
        self.layout_principal.addWidget(self.files_list_widget)

        self.fenetre_principale.setCentralWidget(self.widget_principal)

        self.afficher_fenetre()

    def afficher_fenetre(self):
        self.fenetre_principale.show()


asset_browser_app = AssetBrowserApp()
asset_browser_app.app.exec()

