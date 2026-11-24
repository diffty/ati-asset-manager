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
        # Nettoyage des éventuels slashs à la fin
        self.project_path = project_path.rstrip("/\\")

        self.app = QApplication()

        self.fenetre_principale = QMainWindow()

        # Création du widget principal de la fenetre
        self.widget_principal = QWidget()

        # Création du layout au widget principal
        # Il empilera ses enfants à la verticale (layout de type QVBoxLayout)
        self.layout_principal = QVBoxLayout()

        # Affectation de ce layout au widget principal
        self.widget_principal.setLayout(self.layout_principal)

        # Création du widget qui contiendra le navigateur
        self.widget_browser = QWidget()

        # Création du layout qui contiendra les widgets qui composeront le navigateur
        # Ses enfants seront disposés à l'horizontal de gauche à droite
        self.layout_browser = QHBoxLayout()

        # On rattache ce layout au widget global du navigateur
        self.widget_browser.setLayout(self.layout_browser)

        # Création des différents widgets de liste composant les colonnes du navigateur
        # Définition des fonctions qui réagiront aux évènements de sélection d'item des colonnes
        # Ajout de chaque widget liste dans le layout du navigateur
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

        # Remplissage du widget principal qui empilera :
        # * le widget du navigateur (et ses enfants, les widget de listes)
        # * Le bouton Open
        # * Le bouton Copy Path
        self.layout_principal.addWidget(self.widget_browser)
        self.layout_principal.addWidget(self.open_button)
        self.layout_principal.addWidget(self.copy_path_button)

        # Définition du widget_principal comme Widget rattaché à la fenêtre.
        self.fenetre_principale.setCentralWidget(self.widget_principal)

        self.fenetre_principale.show()

        # Premier chargement de données : récupération de la liste des kinds du projet depuis
        # le disque dur et mise à jour de la première colonne de l'interface.
        self.refresh_kinds_list()

    def refresh_kinds_list(self):
        # Purge de la liste de kinds
        self.kind_list_widget.clear()
        kinds_list = project_utils.get_kinds(self.project_path)
        self.kind_list_widget.addItems(kinds_list)

    def refresh_categories_list(self):
        # Purge de la liste de categories
        self.category_list_widget.clear()

        # Check des éléments sélectionnés dans les autres colonnes,
        # permettant de reconstituer un chemin
        selected_kinds_items = self.kind_list_widget.selectedItems()
        if selected_kinds_items:
            # selectedItems renvoie des listes car il est possible d'activer la multi-sélection sur les listes.
            # Lorsqu'elle n'est pas permise (comme ici), une liste sera tout de même renvoyée,
            # mais n'aura qu'une unique valeur
            selected_kind = selected_kinds_items[0].text()

            # Récupération des données depuis le projet, en fonction de
            # la sélection de l'utilisateurice et remplissage du widget de liste
            categories_list = project_utils.get_categories(self.project_path, selected_kind)
            self.category_list_widget.addItems(categories_list)

    def refresh_assets_list(self):
        # Purge de la liste de assets
        self.asset_list_widget.clear()

        # Check des éléments sélectionnés dans les autres colonnes,
        # permettant de reconstituer un chemin
        selected_kinds_items = self.kind_list_widget.selectedItems()
        selected_category_items = self.category_list_widget.selectedItems()

        if selected_kinds_items and selected_category_items:
            # selectedItems renvoie des listes car il est possible d'activer la multi-sélection sur les listes.
            # Lorsqu'elle n'est pas permise (comme ici), une liste sera tout de même renvoyée,
            # mais n'aura qu'une unique valeur
            selected_kind = selected_kinds_items[0].text()
            selected_category = selected_category_items[0].text()

            # Récupération des données depuis le projet, en fonction de
            # la sélection de l'utilisateurice et remplissage du widget de liste
            assets_list = project_utils.get_assets(self.project_path, selected_kind, selected_category)
            self.asset_list_widget.addItems(assets_list)

    def refresh_files_list(self):
        # Purge de la liste de files
        self.files_list_widget.clear()

        # Check des éléments sélectionnés dans les autres colonnes,
        # permettant de reconstituer un chemin
        selected_kinds_items = self.kind_list_widget.selectedItems()
        selected_category_items = self.category_list_widget.selectedItems()
        selected_asset_items = self.asset_list_widget.selectedItems()

        if selected_kinds_items and selected_category_items and selected_asset_items:
            # selectedItems renvoie des listes car il est possible d'activer la multi-sélection sur les listes.
            # Lorsqu'elle n'est pas permise (comme ici), une liste sera tout de même renvoyée,
            # mais n'aura qu'une unique valeur
            selected_kind = selected_kinds_items[0].text()
            selected_category = selected_category_items[0].text()
            selected_asset = selected_asset_items[0].text()

            # Récupération des données depuis le projet, en fonction de
            # la sélection de l'utilisateurice et remplissage du widget de liste
            files_list = project_utils.get_files(self.project_path, selected_kind, selected_category, selected_asset)
            self.files_list_widget.addItems(files_list)

    def get_selected_path(self):
        # Fonction qui va assembler un chemin en fonction des différents éléments
        # sélectionnés dans l'interface, de gauche à droite.
        # NOTE: La construction s'arrête dès qu'une liste n'a aucun élément sélectionné.
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
        # Lorsqu'un kind est sélectionné, on efface la liste d'asset et la liste de fichiers
        # et recharge/rafraichis la liste de catégories
        self.asset_list_widget.clear()
        self.files_list_widget.clear()
        self.refresh_categories_list()

    def quand_on_selectionne_une_categorie(self):
        # Lorsqu'une catégorie est sélectionnée, on efface la liste de fichiers
        # et recharge/rafraichis la liste d'assets
        self.files_list_widget.clear()
        self.refresh_assets_list()

    def quand_on_selectionne_un_asset(self):
        # Lorsqu'une catégorie est sélectionnée, on rafrachis la liste de fichiers
        self.refresh_files_list()

    def quand_on_appuie_sur_copy_path(self):
        path = self.get_selected_path()

        if path:
            # Le chemin renvoyé par get_selected_path est un chemin relatif à la racine du projet.
            # On recompose donc un chemin complet en lui concaténant le chemin complet du projet.
            full_path = self.project_path + "/" + path
            copykitten.copy(full_path)

    def quand_on_appuie_sur_open(self):
        path = self.get_selected_path()
        
        if path:
            # Le chemin renvoyé par get_selected_path est un chemin relatif à la racine du projet.
            # On recompose donc un chemin complet en lui concaténant le chemin complet du projet.
            full_path = self.project_path + "/" + path

            # Ouverture du fichier en fonction du système d'exploitation
            # Code volé de https://stackoverflow.com/a/1795849
            if sys.platform == 'win32':
                # Windows
                subprocess.Popen(['start', full_path], shell=True)

            elif sys.platform == 'darwin':
                # macOS
                subprocess.Popen(['open', full_path])

            else:
                # Le reste (probablement Linux)
                try:
                    subprocess.Popen(['xdg-open', full_path])
                except OSError:
                    # er, think of something else to try
                    # xdg-open *should* be supported by recent Gnome, KDE, Xfce
                    print("I can't open the selected path bro....")


if __name__ == "__main__":
    asset_browser_app = AssetBrowserApp("/home/diffty/Bureau/asset_manager/_projet_exemple/")
    asset_browser_app.app.exec()
