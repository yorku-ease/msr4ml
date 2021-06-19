from astroid import parse
from astroid import  nodes
import os
import json


def get_io_funcs(io_func_file_name="./config/io_functions.json"):
    io_funcs = {}
    libs = []
    functions = {}
    with open(io_func_file_name) as f:
        io_funcs = json.load(f)
    
    #Extract the io functions as dict of values {name: set_value_from_name:fparam_position:mparam_position}
    for k1, v1 in io_funcs.items():
        # libs.append(k1)
        for v1_key, v1_value in v1.items():
            if v1_key not in functions.keys():
                mparam_position = v1_value['mparam_position']
                if mparam_position is None:
                    mparam_position = 1000 #Give huge value in case there is no value to fix index out of range error during spliting
                functions[v1_key] = f"{v1_value['set_mode_from_name']}:{v1_value['fparam_position']}:{mparam_position}"
                if v1_key == "load":
                    print(functions[v1_key])
            else:
                functions[v1_key] = f"{v1_value['set_mode_from_name']}:{v1_value['fparam_position']}:{mparam_position}" if v1_value['set_mode_from_name'] else functions[v1_key]
    return functions

def get_links():
    links = []




