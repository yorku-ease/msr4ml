import os

extensions = {
    "data": [".txt", ".csv", ".xls", ".xlsx"],
    "model": [".pkl", ".npy"],
    "conf": [".conf", ".yml", ".yaml", ".json", ".ini"],
}


class Artefact(object):
    def __init__(self, dict_artefact):
        self.name = dict_artefact["artefact_location"]
        self.artefact_type = dict_artefact["artefact_type"]
        self.categories = {}
        self.categorie = None

    def set_categories(self):
        self.categories = get_by_name(self.name)
        ext_cat = get_by_extension(self.name)
        for cat in ["data", "model", "conf"]:
            if (cat in ext_cat.keys()) and (cat in self.categories.keys()):
                self.categories[cat] = max(self.categories[cat], ext_cat[cat])
            elif cat in ext_cat.keys():
                self.categories[cat] = ext_cat[cat]

        # Set the highest priority as categorie
        if self.categories:
            self.categorie = max(self.categories, key=self.categories.get)


def get_by_name(name, cat=["data", "model", "conf"]):
    categories = {}
    # check if name is not NoneType
    if name is None:
        return categories

    for categorie in cat:
        if categorie in name:
            categories[categorie] = 1
    return categories


def get_by_extension(name, exs=extensions):
    categories = {}
    # check if name is not NoneType
    if name is None:
        return categories

    for categorie, values in exs.items():
        if os.path.splitext(name)[1] in values:
            categories[categorie] = 2
    return categories
