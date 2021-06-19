import argparse
import json
from astroid import parse, Const
from astroid.exceptions import InferenceError
from astroid import MANAGER, nodes, inference_tip
import os
from . import utils


def _looks_like_infer_join(node, node_name="join"):
    if node.__class__.__name__ == "Call":
        name = ""
        if hasattr(node.func, "id"):
            name = node.func.id
        elif hasattr(node.func, "attrname"):
            name = node.func.attrname
        if name == node_name:
            return True
    return False


def infer_join(call_node, context=None):
    new_node = call_node
    # Do some transformation here
    # set the working dir
    success = True
    ags = []
    for arg in call_node.args:
        try:
            val = next(arg.infer())
            if val.__class__.__name__ != "Const":
                success = False
                new_node = InferenceError("Could not infer the value for " + str(call_node.as_string()))
            else:
                ags.append(val.value)
        except InferenceError as e:
            print(e)
            success = False
            break

    if success:
        new_node = Const(value=os.path.join(*ags))
    return iter((new_node,))


MANAGER.register_transform(
    nodes.Call,
    inference_tip(infer_join),
    _looks_like_infer_join,
)


def get_open_node(start_from, names):
    res = []
    nn = None
    for n in start_from.nodes_of_class(nodes.Call):
        if hasattr(n.func, "attrname"):
            nn = n.func.attrname
        elif hasattr(n.func, "name"):
            nn = n.func.name
        if nn is not None and nn in names:
            res.append(n)
    return res


# print(get_open_node(module, "opening")[0].as_string())
def get_v(object):
    v = None
    try:
        v = next(object.infer())
    except Exception as e:
        v = e
    if v.__class__.__name__ == "Const":
        return v.value
    else:
        return "Error::{}::{}".format(v.__class__.__name__, str(v))


def get_keywords(node, index=0):
    keywords = []
    for i, keyword in enumerate(node.keywords):
        index += i
        v = get_v(keyword.value)
        keywords.append({
            "position": index,
            "name": keyword.arg,
            "value": v
        })
    return keywords


def get_args(node, index=0):
    args = []
    for i, arg in enumerate(node.args):
        index = i
        v = get_v(arg)
        args.append({
            "position": index,
            "name": None,
            "value": v
        })
    return args, index + 1

def get_links(args = []):
    links = []
    io_functions = utils.get_io_funcs()

    for arg in args:
        io_method = arg["name"]
        default_type = io_functions[io_method].split(":")[0]
        fparam_position = int(io_functions[io_method].split(":")[1])
        mparam_position = int(io_functions[io_method].split(":")[2])
        artefact_location = None
        artefact_type = None

        if len(arg["args"]) >= fparam_position:
            artefact_location = arg["args"][fparam_position-1]["value"]
        
        if default_type is not None:
            if "r" in default_type:
                artefact_type = "input"
            else:
                artefact_type = "output"
        elif len(arg["args"]) >= mparam_position:
            type = arg["args"][mparam_position-1]
            if "r" in type:
                artefact_type = "input"
            else:
                artefact_type = "output"

        link = {
            "io_method": io_method,
            "lineno": arg["lineno"],
            "artefact_location": artefact_location,
            "artefact_type": artefact_type,
            "weight": 1
        }
        
        links.append(link)
    return links


def get_arguments(ast_node):
    args = []
    for node in get_open_node(ast_node, utils.get_io_funcs().keys()):
        # print(node)
        d = {'name': node.func.name if hasattr(node.func, "name") else node.func.attrname, 'lineno': node.lineno,
            'args': []}
        last = 0
        if node.args is not None:
            d['args'], last = get_args(node)
        if node.keywords is not None:
            d['args'] += get_keywords(node, last)
        #print(json.dumps(d, indent=4))
        args.append(d)
    return args

def identify(name, project, codes):
    res = {}
    result_dir = os.path.join(project, "msr4ml")
    result_file = os.path.join(result_dir, "identifier_results.json")
    #Create msr4ml dir in target project's path if not exists
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)
    
    #Create identifier result json file in target project's path if not exists
    if not os.path.isfile(result_file):
        with open(result_file, 'w') as f:
            f.write('{"default": "Temporary"}')
    
    #Load existing identified artefacts
    with open(result_file, "r") as f:
        res = json.load(f)
        if "default" in res.keys():
            del res["default"]
    
    #Identify artefact for each file in the project
    for fname, ast_node in codes.items():
        links = get_links(get_arguments(ast_node))
        if links:
            res[fname] = links

    # save to result file
    with open(result_file, 'w') as f:
            json.dump(res, f, indent=4, sort_keys=False)

    print("Finished identification.", f'results saved in {result_file}')
    


def main(project, ast_node):
    pass

if __name__ == "__main__":
    main()