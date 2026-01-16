class Node:
    def __init__(self, value: int):
        self.value = value
        self.left = None
        self.right = None


def insert(root: Node, value: int):
    if root is None:
        return Node(value)

    if value < root.value:
        root.left = insert(root.left, value)
    elif value > root.value:
        root.right = insert(root.right, value)

    return root


def inorder(root: Node):
    if root is None:
        return

    inorder(root.left)
    print(root.value)
    inorder(root.right)


def print_tree(node, level=0, prefix="Root: "):
    if node is not None:
        print(" " * (level * 4) + prefix + str(node.value))
        print_tree(node.left, level + 1, "L--- ")
        print_tree(node.right, level + 1, "R--- ")


def search(root, value):
    if root is None:
        return False

    if root.value == value:
        return True
    elif value < root.value:
        return search(root.left, value)
    else:
        return search(root.right, value)
