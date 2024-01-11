![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)

# Binary Search Tree
- Differ from a regular Binary Tree because of one key property: Nodes must be arranged in order
  - the node's left subtree must have values less than the node
  - the node's right subtree must have values greater than the node
  - this is going based on that every value in the BST must be unique

# Functions Implemented
- Init
  - tree = BST(1,None,None) _creates a tree with one node_
  - A basic constructor that creates a BST with three parameters
  - BST(value,left_subtree,right_subtree)
- Add
  - tree.add(4) _adds 4 to our previous tree created, giving a right child_
  - Maintains BST properties by adding to either subtree depending on the value
  - returns a string telling if insertion was or wasn't successful
- Remove
  - tree.remove(1) _removes 1 from our current tree, resulting 4 to be the sole node_
  - Maintains BST properties by restructuring the tree when we remove the value
  - returns a string telling if deletion was or wasn't successful
# Author
[Tomas Urdinola](https://github.com/tomurdi)
