from typing import Dict, List, Any
from Data_Manipulation.tree import Tree, Node

if __name__ == "__main__":
    root = Node(5)
    node1 = Node(2)
    node1.value = { "test": "test1" }
    node2 = Node(12)
    node3 = Node(10)
    node4 = Node(1)
    node5 = Node(7)

    tree = Tree(root)
    tree.insertOrdered(node1)
    tree.insertOrdered(node2)
    tree.insertOrdered(node3)
    tree.insertOrdered(node4)
    tree.insertOrdered(node5)

    print(tree.getDepth())
    tree.print()
    print("\n")
    print(tree.getValue(tree.root, 122))
