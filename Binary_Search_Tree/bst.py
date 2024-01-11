class BST:

    def __init__(self,val,left,right):
        self.val = val
        self.left = left
        self.right = right

    def addHelper(self,root,data):
        
        # case for reaching current leafs, base cases
        if root.val < data and root.right == None:
            root.right = BST(data,None,None)
            return "insertion completed"
        elif root.val > data and root.left == None:
            root.left = BST(data,None,None)
            return "insertion completed"
        
        # else we continue tracing downwards
        if root.val < data:
            return self.add(root.right,data)
        elif root.val > data:
            return self.add(root.left,data)
        else:
            return "insertion failed: duplicate value"
        
    def add(self,root,data):
        if root == None:
            return "insertion failed: empty root"
        return self.addHelper(root,data)
    
    def restructdata(self,root):
        # base case: we reach a leaf
        if root == None or (root.left == None and root.right == None):
            root = None
            return "restructure finished"
        
        # need dummy nodes to compare target value to children value
        v1 = float('-inf')
        v2 = float('inf')
        if root.left != None:
            v1 = root.left.val
        if root.right != None:
            v2 = root.right.val
        
        temp = root.val
        if v1 > v2 or v2 == float('inf'):
            root.val = root.left.val
            root.left.val = temp
            return self.restructdata(root.left)
        else:
            root.val = root.right.val
            root.right.val = temp
            return self.restructdata(root.right)
    
    
    def removeHelper(self,root,data):
        if root == None:
            return "deletion failed: could not find value"
        
        # adhering to typical bst properties
        if root.val < data:
            return self.removeHelper(root.right,data)
        elif root.val > data:
            return self.removeHelper(root.left,data)
        else:
            temp = root.val
            v1 = float('-inf')
            v2 = float('inf')
            if root.left != None:
                v1 = root.left.val
            elif root.right != None:
                v2 = root.right.val
            
            if v1 > v2 or v2 == float('inf'):
                root.val = root.left.val
                root.left.val = temp
                return self.restructdata(root.left)
            else:
                root.val = root.right.val
                root.right.val = temp
                return self.restructdata(root.right)
            
    def remove(self,root,data):
        if root == None:
            return "deletion failed: deleting from an empty tree"
        return self.removeHelper(root,data)
            
        
    
    