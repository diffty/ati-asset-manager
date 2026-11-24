import sys
import subprocess

from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QWidget, QListWidget, QPushButton
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout

import copykitten

import project_utils


class AssetBrowserApp:
    def __init__(self, project_path):
        self.project_path = project_path.rstrip("/")

        self.app = QApplication()

        self.fenetre_principale = QMainWindow()

        # Définition du widget principal
        self.widget_principal = QWidget()
    
        self.layout_principal = QVBoxLayout()
        self.widget_principal.setLayout(self.layout_principal)

        # Définition du navigateur
        self.widget_browser = QWidget()

        self.layout_browser = QHBoxLayout()
        self.widget_browser.setLayout(self.layout_browser)

        self.kind_list_widget = QListWidget()
        self.kind_list_widget.itemSelectionChanged.connect(self.quand_on_selectionne_un_kind)
        self.layout_browser.addWidget(self.kind_list_widget)

        self.category_list_widget = QListWidget()
        self.category_list_widget.itemSelectionChanged.connect(self.quand_on_selectionne_une_categorie)
        self.layout_browser.addWidget(self.category_list_widget)

        self.asset_list_widget = QListWidget()
        self.asset_list_widget.itemSelectionChanged.connect(self.quand_on_selectionne_un_asset)
        self.layout_browser.addWidget(self.asset_list_widget)

        self.files_list_widget = QListWidget()
        self.layout_browser.addWidget(self.files_list_widget)

        # Définition de la barre d'outils
        self.open_button = QPushButton("Open")
        self.open_button.clicked.connect(self.quand_on_appuie_sur_open)
        self.copy_path_button = QPushButton("Copy Path")
        self.copy_path_button.clicked.connect(self.quand_on_appuie_sur_copy_path)

        # Remplissage du widget principal
        self.layout_principal.addWidget(self.widget_browser)
        self.layout_principal.addWidget(self.open_button)
        self.layout_principal.addWidget(self.copy_path_button)

        self.fenetre_principale.setCentralWidget(self.widget_principal)

        self.afficher_fenetre()

        self.refresh_kinds_list()

    def afficher_fenetre(self):
        self.fenetre_principale.show()

    def refresh_kinds_list(self):
        self.kind_list_widget.clear()
        kinds_list = project_utils.get_kinds(self.project_path)
        self.kind_list_widget.addItems(kinds_list)

    def refresh_categories_list(self):
        self.category_list_widget.clear()
        selected_kinds_items = self.kind_list_widget.selectedItems()
        if selected_kinds_items:
            selected_kind = selected_kinds_items[0].text()
            categories_list = project_utils.get_categories(self.project_path, selected_kind)
            self.category_list_widget.addItems(categories_list)

    def refresh_assets_list(self):
        self.asset_list_widget.clear()
        selected_kinds_items = self.kind_list_widget.selectedItems()
        selected_category_items = self.category_list_widget.selectedItems()

        if selected_kinds_items and selected_category_items:
            selected_kind = selected_kinds_items[0].text()
            selected_category = selected_category_items[0].text()

            assets_list = project_utils.get_assets(self.project_path, selected_kind, selected_category)
            self.asset_list_widget.addItems(assets_list)

    def refresh_files_list(self):
        self.files_list_widget.clear()
        selected_kinds_items = self.kind_list_widget.selectedItems()
        selected_category_items = self.category_list_widget.selectedItems()
        selected_asset_items = self.asset_list_widget.selectedItems()

        if selected_kinds_items and selected_category_items and selected_asset_items:
            selected_kind = selected_kinds_items[0].text()
            selected_category = selected_category_items[0].text()
            selected_asset = selected_asset_items[0].text()

            files_list = project_utils.get_files(self.project_path, selected_kind, selected_category, selected_asset)
            self.files_list_widget.addItems(files_list)

    def get_selected_path(self):
        path = ""
        
        selected_kinds_items = self.kind_list_widget.selectedItems()
        if selected_kinds_items:
            selected_kind_name = selected_kinds_items[0].text()
            path = selected_kind_name

            selected_category_items = self.category_list_widget.selectedItems()
            if selected_category_items:
                selected_category_name = selected_category_items[0].text()
                path = path + "/" + selected_category_name

                selected_asset_items = self.asset_list_widget.selectedItems()

                if selected_asset_items:
                    selected_asset_name = selected_asset_items[0].text()

                    path = path + "/" + selected_asset_name

                    selected_file_items = self.files_list_widget.selectedItems()
                    if selected_file_items:
                        selected_file_name = selected_file_items[0].text()
                        path = path + "/" + selected_file_name

        return path

    def quand_on_selectionne_un_kind(self):
        self.asset_list_widget.clear()
        self.files_list_widget.clear()
        self.refresh_categories_list()

    def quand_on_selectionne_une_categorie(self):
        self.files_list_widget.clear()
        self.refresh_assets_list()

    def quand_on_selectionne_un_asset(self):
        self.refresh_files_list()

    def quand_on_appuie_sur_copy_path(self):
        path = self.get_selected_path()

        if path:
            full_path = self.project_path + "/" + path
            copykitten.copy(full_path)

    def quand_on_appuie_sur_open(self):
        path = self.get_selected_path()
        
        if path:
            full_path = self.project_path + "/" + path

            if sys.platform == 'win32':
                subprocess.Popen(['start', full_path], shell=True)
            elif sys.platform == 'darwin':
                subprocess.Popen(['open', full_path])
            else:
                try:
                    subprocess.Popen(['xdg-open', full_path])
                except OSError:
                    # er, think of something else to try
                    # xdg-open *should* be supported by recent Gnome, KDE, Xfce
                    print("I can't open the selected path bro....")


if __name__ == "__main__":
    asset_browser_app = AssetBrowserApp("/home/diffty/Bureau/asset_manager/_projet_exemple/")
    asset_browser_app.app.exec()
