import asset_resolver


asset_name = "juno"
asset_kind = "character"
asset_category = "animal"
file_extension = "ma"
file_version = 1

chemin_fichier = asset_resolver.get_file_path(asset_kind, asset_category, asset_name, file_extension, file_version)
print(chemin_fichier)
