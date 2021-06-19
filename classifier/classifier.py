from .rules.define_rules import Artefact
import json

def classify(artefact:Artefact, categorie=None):
    artefact

def main(links_path):
    result = {}
    with open(links_path) as f:
        links = json.load(f)
        result = links
    for codename, artefacts in links.items():
        i = 0
        for dict_artefact in artefacts:
            a = Artefact(dict_artefact)
            result[codename][i]["possible_categories"] = a.set_categories()
            result[codename][i]["categorie"] = a.set_categorie()

            

if __name__ == '__main__':
    main()