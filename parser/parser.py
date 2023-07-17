from astroid import parse

def to_ast(py_file):
    return parse(py_file)

def main():
    pass

if __name__ == "__main__":
    main()