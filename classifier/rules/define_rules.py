from business_rule_engine import RuleParser
from business_rule_engine.exceptions import MissingArgumentError
import os

with open(os.path.join(os.path.dirname(__file__), "rules.txt")) as f:
    rules = f.readlines()

extensions = {
    "data": ['.txt', '.csv', '.xls', '.xlsx'],
    "model": ['.pkl', '.npy'],
    "conf": ['.conf', '.yml', '.yaml', '.json', '.ini']
}

class Artefact(object):
    def __init__(self, dict_artefact):
        self.name = dict_artefact["artefact_location"]
        self.artefact_type = dict_artefact["artefact_type"]
        self.categories = {}
        self.categorie = None
    
    

def assign(categorie=None, priority=0):
    return [categorie, priority]

def get_categorie_by_name(name, categorie):
    return categorie in name

def get_categorie_by_extension(name, extensions):
    return os.path.splitext(name)[1] in extensions

def set_categories(a):
        params = {
        "name": a.name,
        "extensions": extensions,
        }
        parser = RuleParser()
        parser.register_function(assign)
        parser.register_function(get_categorie_by_name)
        parser.parsestr(rules)
        for rule in parser:
            try:
                rvalue_condition, rvalue_action = rule.execute(params)
                if rule.status:
                    print(rvalue_action[0], rvalue_action[1])
                    break
            except MissingArgumentError:
                pass
