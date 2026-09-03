from node import Node

class Tree:
    def __init__(self):
        self.root = None

    def getRoot(self):
        return self.root

    def add(self, data):
        if self.root is None:
            self.root = Node(data)
        else:
            self._add(data, self.root)

    def _add(self, data, node):
        if data < node.data:
            if node.left is not None:
                self._add(data, node.left)
            else:
                node.left = Node(data)
        else:
            if node.right is not None:
                self._add(data, node.right)
            else:
                node.right = Node(data)

    def find(self, data):
        if self.root is not None:
            return self._find(data, self.root)
        return None

    def _find(self, data, node):
        if node is None:
            return None
        if data == node.data:
            return node
        elif data < node.data and node.left is not None:
            return self._find(data, node.left)
        elif data > node.data and node.right is not None:
            return self._find(data, node.right)
        return None

    def deleteTree(self):
        self.root = None

    def inorder(self) -> list:
        """Return list of elements from in-order traversal (Left, Root, Right)."""
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node is not None:
            self._inorder(node.left, result)
            result.append(node.data)
            self._inorder(node.right, result)

    def preorder(self) -> list:
        """Return list of elements from pre-order traversal (Root, Left, Right)."""
        result = []
        self._preorder(self.root, result)
        return result

    def _preorder(self, node, result):
        if node is not None:
            result.append(node.data)
            self._preorder(node.left, result)
            self._preorder(node.right, result)

    def postorder(self) -> list:
        """Return list of elements from post-order traversal (Left, Right, Root)."""
        result = []
        self._postorder(self.root, result)
        return result

    def _postorder(self, node, result):
        if node is not None:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.append(node.data)

    def height(self) -> int:
        """Return maximum depth/height of the binary tree."""
        return self._height(self.root)


    def _height(self, node) -> int:
        if node is None:
            return 0
        return 1 + max(self._height(node.left), self._height(node.right))

    def printTree(self):
        """Print tree elements in sorted order."""
        print("Inorder Traversal: ", self.inorder())


