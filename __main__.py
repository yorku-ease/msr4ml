import argparse
import os
from parser import parser
from pathlib import PurePath

import astroid
from identifier import identifier
from classifier import classifier


def get_python_files(project):
    py_files = []
    for root, dirs, files in os.walk(project):
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.join(root, file))
    return py_files


def call_parser(py_file):
    return parser.to_ast(py_file)


def call_identifier(name, project, codes):
    return identifier.identify(name, project, codes)


def call_classifier(identifier_result_file):
    print("+++ Starting classification...")
    classifier.classify(identifier_result_file)


def get_args():
    parser = argparse.ArgumentParser(
        description="Retrieve which code imports which file in the project"
    )

    parser.add_argument(
        "-p",
        "--project",
        default=None,
        type=str,
        dest="project",
        help="Relative or absolute path of the project to analyse",
    )

    parser.add_argument(
        "-n",
        "--name",
        default="",
        type=str,
        dest="name",
        help="Set the name of the project. Defaults to the name of the directory to analyse",
    )

    return parser


def main():
    args = get_args().parse_args()
    assert args.project is not None, "The path of the ML project must be specified"
    name = (
        args.name
        if args.name != ""
        else os.path.basename(os.path.normpath(args.project))
    )

    filenames = []
    codes = {}
    filenames = get_python_files(args.project)
    # for root, _, files in os.walk(args.project):
    #     for file in files:
    #         if file.endswith(".py"):
    #             filenames.append(os.path.join(root, file))
    for file in filenames:
        with open(file, encoding="utf8") as f:
            # codes[file] = astroid.parse(f.read())
            codes[file] = call_parser(f.read())

    print("+++ Starting identification...")
    identifier_result_file = call_identifier(name, os.path.abspath(args.project), codes)
    if identifier_result_file:
        call_classifier(identifier_result_file)


if __name__ == "__main__":
    main()
