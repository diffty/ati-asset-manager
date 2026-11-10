import os


def get_kinds(project_path):
    kinds_list = os.listdir(project_path)

    kinds_list_filtered = []

    for kind in kinds_list:
        if os.path.isdir(f"{project_path}/{kind}") and kind.startswith(".") == False:
            kinds_list_filtered.append(kind)

    return kinds_list_filtered


def get_categories(project_path, kind):
    categories_list = os.listdir(f"{project_path}/{kind}")

    categories_list_filtered = []

    for category in categories_list:
        if os.path.isdir(f"{project_path}/{kind}/{category}") and category.startswith(".") == False:
            categories_list_filtered.append(category)

    return categories_list_filtered


def get_assets(project_path, kind, category):
    assets_list = os.listdir(f"{project_path}/{kind}/{category}")

    assets_list_filtered = []

    for asset in assets_list:
        if os.path.isdir(f"{project_path}/{kind}/{category}/{asset}") and asset.startswith(".") == False:
            assets_list_filtered.append(asset)

    return assets_list_filtered


def get_files(project_path, kind, category, asset):
    files_list = os.listdir(f"{project_path}/{kind}/{category}/{asset}")

    files_list_filtered = []

    for filename in files_list:
        if os.path.isfile(f"{project_path}/{kind}/{category}/{asset}/{filename}") and filename.startswith(".") == False:
            files_list_filtered.append(filename)

    return files_list_filtered


if __name__ == "__main__":
    kind_list = get_kinds("/Users/diffty/Documents/_Projets/Cours/2024_10_CoursPython/m1/code/_dummy_project")
    print(kind_list)

    categories_list = get_categories("/Users/diffty/Documents/_Projets/Cours/2024_10_CoursPython/m1/code/_dummy_project", "character")
    print(categories_list)

    assets_list = get_assets("/Users/diffty/Documents/_Projets/Cours/2024_10_CoursPython/m1/code/_dummy_project", "character", "animal")
    print(assets_list)

    files_list = get_files("/Users/diffty/Documents/_Projets/Cours/2024_10_CoursPython/m1/code/_dummy_project", "character", "human", "freddy")
    print(files_list)
