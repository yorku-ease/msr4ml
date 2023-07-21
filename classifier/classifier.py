import os
import sys
from .rules.rules import Artefact
import json
import logging

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def classify(identifier_result_file):
    result_file = os.path.join(
        os.path.dirname(identifier_result_file), "classifier_results.json"
    )
    with open(identifier_result_file) as f:
        links = json.load(f)

    for fname, artefacts in links.items():
        for artefact in artefacts:
            a = Artefact(artefact)
            a.set_categories()
            artefact["possible_categories"] = a.categories
            artefact["categorie"] = a.categorie

    # save to result file
    with open(result_file, "w") as f:
        json.dump(links, f, indent=4, sort_keys=False)
    print("Finished classification.", f"results saved in {result_file}")
    return result_file


def main(links):
    pass


if __name__ == "__main__":
    main()
