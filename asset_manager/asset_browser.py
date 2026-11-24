from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QWidget, QListWidget
from PySide6.QtWidgets import QHBoxLayout

import project_utils


class AssetBrowserApp:
    def __init__(self, project_path):
        self.project_path = project_path

        self.app = QApplication()

        self.fenetre_principale = QMainWindow()

        self.widget_principal = QWidget()

        self.layout_principal = QHBoxLayout()
        self.widget_principal.setLayout(self.layout_principal)

        self.kind_list_widget = QListWidget()
        self.kind_list_widget.itemSelectionChanged.connect(self.quand_on_selectionne_un_kind)
        self.layout_principal.addWidget(self.kind_list_widget)

        self.category_list_widget = QListWidget()
        self.category_list_widget.itemSelectionChanged.connect(self.quand_on_selectionne_une_categorie)
        self.layout_principal.addWidget(self.category_list_widget)

        self.asset_list_widget = QListWidget()
        self.asset_list_widget.itemSelectionChanged.connect(self.quand_on_selectionne_un_asset)
        self.layout_principal.addWidget(self.asset_list_widget)

        self.files_list_widget = QListWidget()
        self.layout_principal.addWidget(self.files_list_widget)

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

    def quand_on_selectionne_un_kind(self):
        self.asset_list_widget.clear()
        self.files_list_widget.clear()
        self.refresh_categories_list()

    def quand_on_selectionne_une_categorie(self):
        self.files_list_widget.clear()
        self.refresh_assets_list()

    def quand_on_selectionne_un_asset(self):
        self.refresh_files_list()


if __name__ == "__main__":
    asset_browser_app = AssetBrowserApp("/home/diffty/Bureau/asset_manager/_projet_exemple/")
    asset_browser_app.app.exec()

