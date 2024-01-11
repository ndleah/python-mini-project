<!--Please do not remove this part-->

![Star Badge](https://img.shields.io/static/v1?label=%F0%9F%8C%9F&message=If%20Useful&style=style=flat&color=BC4E99)
![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)

## 🛠️ Description

Implementation of a simple Prefix Trie in Python. It allows for insertion, search, and checks if a string in the Trie starts with a prefix.

## ⚙️ Languages or Frameworks Used

The program was created with Python3.

## 🌟 How to run

To use this Trie, import the Trie class by adding:
`from trie import Trie` to the top of your python file.

Then, you can create a Trie using the constructor `trie = Trie()`

**Methods:**\
 _insert(word)_ - Inserts word into Trie\
 _search(word)_ - Returns if word is in Trie\
 _starts_with(prefix)_ - Returns if a word in Trie starts with prefix\

To insert, run `trie.insert("word")`\
To search, run `trie.search("word")`\
To check if the trie contains a prefix, run `trie.starts_with("w")`

## 🤖 Author

[Tim Vuong](https://github.com/Tim-Vuong)

Credits to LeetCode problem:
https://leetcode.com/problems/implement-trie-prefix-tree/description/
