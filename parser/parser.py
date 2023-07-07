# from astroid import parse
# import astroid
# from test import infer_join, _looks_like_infer_join

# module = astroid.parse('''
# "my name is {}".format(name)
# ''')

# print(module);

# def to_ast(py_file):
#     return parse(py_file)

# def main():
#     pass

# if __name__ == "__main__":
#     main()
import astroid
from astroid import MANAGER, nodes
import test


def main():
    code = """
    path = join('dir', 'file.txt')
    """
    tree = astroid.parse(code)

    print("Original Code:")
    print(tree.repr_tree())


if __name__ == "__main__":
    main()
