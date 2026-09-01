from tree import Tree
from node import Node

def main():
    print("=== Binary Search Tree Demo ===")
    tree = Tree()
    nodes_to_add = [3, 4, 0, 8, 2]
    print(f"Adding nodes: {nodes_to_add}")

    for val in nodes_to_add:
        tree.add(val)

    print(f"Tree Height: {tree.height()}")
    print(f"Inorder Traversal:   {tree.inorder()}")
    print(f"Preorder Traversal:  {tree.preorder()}")
    print(f"Postorder Traversal: {tree.postorder()}")

    found_node = tree.find(8)
    print(f"Find Node (8): {'Found' if found_node else 'Not Found'}")
    missing_node = tree.find(99)
    print(f"Find Node (99): {'Found' if missing_node else 'Not Found'}")

if __name__ == '__main__':
    main()

