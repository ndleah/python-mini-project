from trie import Trie

def main():
    trie = Trie()

    print("Inserting words: 'apple', 'app', 'application', 'apricot', 'banana'")
    words = ["apple", "app", "application", "apricot", "banana"]
    for w in words:
        trie.insert(w)

    assert len(trie) == 5, f"Trie count should be 5, got {len(trie)}"
    assert trie.search("apple") == True, "search('apple') should be True"
    assert trie.search("app") == True, "search('app') should be True"
    assert trie.search("appl") == False, "search('appl') should be False"
    assert trie.starts_with("app") == True, "starts_with('app') should be True"

    prefix_words = trie.get_words_with_prefix("app")
    print(f"Words starting with 'app': {prefix_words}")

    print("Deleting 'app'...")
    trie.delete("app")
    assert trie.search("app") == False, "search('app') after delete should be False"
    assert trie.search("apple") == True, "search('apple') should remain True"

    print("All Trie tests passed successfully!")

if __name__ == '__main__':
    main()

