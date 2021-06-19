import argparse
import os
from parser import parser

import astroid
from identifier import identifier

# TODO: For test, delete later
source = '''
import os
from test import Test
f = "hello.png"+"himan"
t = Test(filename="testingoh")
c = os.path.join("root", f)
d = os.path.join(c, "dir2")
open(c, gigi="hi", mode="testing")
t.save_model(model, os.path.join(d, "hello.jo"), oro="r")
'''
module = astroid.parse(source)


def get_python_files(project):
    py_files = []
    for root, dirs, files in os.walk(project):
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.join(root, file))
    return py_files

def call_parser(py_file):
    return parser.to_ast(py_file)

def call_identifier(node):
    identifier.identify(node)

def get_args():
    parser = argparse.ArgumentParser(description="Retrieve which code imports which file in the project")

    parser.add_argument(
        '-p',
        '--project',
        default=None,
        type=str,
        dest='project',
        help="Relative or absolute path of the project to analyse")
    
    parser.add_argument(
        '-n',
        '--name',
        default='',
        type=str,
        dest='name',
        help="Set the name of the project. Defaults to the name of the directory to analyse")
    
    return parser

def main():
    args = get_args().parse_args()
    assert args.project is not None, "The path of the ML project must be specified"
    args.name = args.name if args.name is not None else args.project.split('/')[-1]

    print(args.name, args.project)
    call_identifier(module)



if __name__ == "__main__":
    main()