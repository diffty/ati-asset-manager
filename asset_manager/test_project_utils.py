import project_utils

kind_list = project_utils.get_kinds("/Users/diffty/Documents/_Projets/Cours/2024_10_CoursPython/m1/code/_dummy_project")
print(kind_list)

categories_list = project_utils.get_categories("/Users/diffty/Documents/_Projets/Cours/2024_10_CoursPython/m1/code/_dummy_project", "character")
print(categories_list)

assets_list = project_utils.get_assets("/Users/diffty/Documents/_Projets/Cours/2024_10_CoursPython/m1/code/_dummy_project", "character", "animal")
print(assets_list)

files_list = project_utils.get_files("/Users/diffty/Documents/_Projets/Cours/2024_10_CoursPython/m1/code/_dummy_project", "character", "human", "freddy")
print(files_list)
