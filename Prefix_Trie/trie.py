class TrieNode:
    def __init__(self):
        """
        children is a dict from char -> TrieNode
        is_end represents whether the Node is the end of a word
        """
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    """
    Inserts the string word into the trie.
    """
    def insert(self, word: str) -> None:
        curr = self.root
        for c in word:
            if c not in curr.children:
                curr.children[c] = TrieNode()
            curr = curr.children[c]
        curr.is_end = True

    """
    Returns true if the string word is in the trie (i.e., was inserted before).
    Otherwise, returns false.
    """
    def search(self, word: str) -> bool:
        curr = self.root
        for c in word:
            if c not in curr.children:
                return False
            curr = curr.children[c]
        return curr.is_end

    """
    Returns true if there is a previously inserted string word that has the prefix prefix.
    Otherwise, returns false.
    """
    def starts_with(self, prefix: str) -> bool:
        curr = self.root
        for c in prefix:
            if c not in curr.children:
                return False
            curr = curr.children[c]
        return True
