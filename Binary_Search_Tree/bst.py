class BST:

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def addHelper(self, root, data):
        if data < root.val:
            if root.left is None:
                root.left = BST(data)
                return "insertion completed"
            else:
                return self.addHelper(root.left, data)
        elif data > root.val:
            if root.right is None:
                root.right = BST(data)
                return "insertion completed"
            else:
                return self.addHelper(root.right, data)
        else:
            return "insertion failed: duplicate value"

    def add(self, data, root=None):
        if root is None:
            root = self
        return self.addHelper(root, data)

    def _get_min(self, root):
        current = root
        while current.left is not None:
            current = current.left
        return current.val

    def removeHelper(self, root, data):
        if root is None:
            return root, False

        deleted = False
        if data < root.val:
            root.left, deleted = self.removeHelper(root.left, data)
        elif data > root.val:
            root.right, deleted = self.removeHelper(root.right, data)
        else:
            deleted = True
            # Case 1: Leaf node
            if root.left is None and root.right is None:
                return None, True
            # Case 2: One child
            if root.left is None:
                return root.right, True
            if root.right is None:
                return root.left, True
            # Case 3: Two children - replace with in-order successor
            min_val = self._get_min(root.right)
            root.val = min_val
            root.right, _ = self.removeHelper(root.right, min_val)

        return root, deleted

    def remove(self, data, root=None):
        if root is None:
            root = self

        if root == self and self.val == data and self.left is None and self.right is None:
            return "deletion failed: deleting from an empty tree"

        _, deleted = self.removeHelper(root, data)
        if deleted:
            return "deletion completed"
        return "deletion failed: could not find value"

    def search(self, data):
        if data == self.val:
            return True
        elif data < self.val and self.left:
            return self.left.search(data)
        elif data > self.val and self.right:
            return self.right.search(data)
        return False

    def inorder(self):
        result = []
        if self.left:
            result.extend(self.left.inorder())
        result.append(self.val)
        if self.right:
            result.extend(self.right.inorder())
        return result

            
        
    
    