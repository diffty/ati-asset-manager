import os
import shutil

from asset_resolver import get_file_path


def create_asset_file(asset_category, asset_kind, asset_name, file_extension, file_version=1, file_suffix=None):
    chemin_destination = get_file_path(asset_category, asset_kind, asset_name, file_extension, file_version, file_suffix)
    print(f"Le chemin généré est : {chemin_destination}")

    chemin_destination_dossier = os.path.dirname(chemin_destination)
    print(f"Le dossier parent s'appelle {chemin_destination_dossier}")

    os.makedirs(chemin_destination_dossier, exist_ok=True)

    template_catalogue = {
        "nk": "/home/diffty/Documents/_Projets/Cours/2024_10_CoursPython/m1/code/_templates/compo.nk",
        "blend": "/home/diffty/Documents/_Projets/Cours/2024_10_CoursPython/m1/code/_templates/model.blend",
        "jpg": "/home/diffty/Documents/_Projets/Cours/2024_10_CoursPython/m1/code/_templates/texture.jpg",
        "png": "/home/diffty/Documents/_Projets/Cours/2024_10_CoursPython/m1/code/_templates/texture.png",
        "tga": "/home/diffty/Documents/_Projets/Cours/2024_10_CoursPython/m1/code/_templates/texture.tga",
        "tif": "/home/diffty/Documents/_Projets/Cours/2024_10_CoursPython/m1/code/_templates/texture.tif",
    }

    chemin_template = template_catalogue[file_extension]

    print(f"Copie du template {chemin_template} vers le nouveau fichier source {chemin_destination}...")
    shutil.copyfile(chemin_template, chemin_destination)


if __name__ == "__main__":
    os.chdir("/home/diffty/Bureau/MON_PROJET_DE_FILM")
    create_asset_file("animal", "character", "juno", "blend", 1)
    create_asset_file("animal", "character", "juno", "tif", 1)
    create_asset_file("animal", "character", "juno", "jpg", 1)
