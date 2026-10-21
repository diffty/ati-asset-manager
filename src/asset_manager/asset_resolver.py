def get_file_path(asset_category, asset_kind, asset_name, file_extension, file_version=1, file_suffix=None):
    file_version_padded = str(file_version).zfill(3)

    if file_suffix != None:
        chemin = f"{asset_kind}/{asset_category}/{asset_name}/{asset_category}__{asset_name}__{file_version_padded}__{file_suffix}.{file_extension}"
    else:
        chemin = f"{asset_kind}/{asset_category}/{asset_name}/{asset_category}__{asset_name}__{file_version_padded}.{file_extension}"

    return chemin


if __name__ == "__main__":
    asset_name = "juno"
    asset_kind = "character"
    asset_category = "animal"
    file_extension = "ma"
    file_version = 1

    chemin_fichier = get_file_path(
        "animal",
        asset_name="juno",
        asset_kind="character",
        file_extension="ma",
    )

    print(f"Le chemin de mon fichier est : {chemin_fichier}")

    nouveau_fichier = get_file_path(
        asset_kind, asset_category, asset_name, file_extension, 12)

    print(f"Le chemin de mon autre fichier est : {nouveau_fichier}")

    ma_texture = get_file_path(asset_kind, asset_category,
                               asset_name, "png", 12, "diffuse")
    print(f"Le chemin de ma texture est : {ma_texture}")
