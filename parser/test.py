import os
from astroid.exceptions import InferenceError
from astroid import MANAGER, nodes, inference_tip
from astroid import parse, Const


def _looks_like_infer_join(node, node_name="join"):
    if node.__class__.__name__ == "Call":
        name = ""
        if hasattr(node.func, "id"):
            name = node.func.id
        elif hasattr(node.func, "attrname"):
            name = node.func.attrname
        if name == node_name:
            return True
    return True


def infer_join(call_node, context=None):
    print("Inside infer_join")  # Debugging line
    print("Call node:", call_node)  # Debugging line
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

def main():
    code = """
    path = join('dir', 'file.txt')
    """
    tree = parse(code)

    print("Original Code:")
    print(tree.repr_tree())


if __name__ == "__main__":
    main()
