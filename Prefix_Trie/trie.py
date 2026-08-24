from typing import List

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
        self._count = 0

    def insert(self, word: str) -> None:
        """Inserts the string word into the trie."""
        if not word:
            return
        curr = self.root
        for c in word:
            if c not in curr.children:
                curr.children[c] = TrieNode()
            curr = curr.children[c]
        if not curr.is_end:
            curr.is_end = True
            self._count += 1

    def search(self, word: str) -> bool:
        """Returns true if the string word is in the trie."""
        if not word:
            return False
        curr = self.root
        for c in word:
            if c not in curr.children:
                return False
            curr = curr.children[c]
        return curr.is_end

    def starts_with(self, prefix: str) -> bool:
        """Returns true if there is a previously inserted string word that has the prefix prefix."""
        curr = self.root
        for c in prefix:
            if c not in curr.children:
                return False
            curr = curr.children[c]
        return True

    def delete(self, word: str) -> bool:
        """Deletes a word from the trie if present. Returns True if deleted."""
        def _delete_helper(node, word, depth):
            if depth == len(word):
                if not node.is_end:
                    return False
                node.is_end = False
                self._count -= 1
                return len(node.children) == 0

            char = word[depth]
            if char not in node.children:
                return False

            should_delete_child = _delete_helper(node.children[char], word, depth + 1)
            if should_delete_child:
                del node.children[char]
                return len(node.children) == 0 and not node.is_end

            return False

        return _delete_helper(self.root, word, 0)

    def get_words_with_prefix(self, prefix: str) -> List[str]:
        """Returns all words stored in the Trie matching the given prefix."""
        curr = self.root
        for c in prefix:
            if c not in curr.children:
                return []
            curr = curr.children[c]

        results = []

        def _dfs(node, path):
            if node.is_end:
                results.append(path)
            for c, child in node.children.items():
                _dfs(child, path + c)

        _dfs(curr, prefix)
        return results

    def is_empty(self) -> bool:
        return self._count == 0

    def __len__(self) -> int:
        return self._count

