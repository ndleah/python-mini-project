class StringManipulator:
    def __init__(self, string: str):
        self.string = str(string)

    def concatenate(self, other_string: str) -> str:
        return self.string + str(other_string)

    def length(self) -> int:
        return len(self.string)

    def slice(self, start: int = 0, end: int = None) -> str:
        return self.string[start:end]

    def repeat(self, times: int) -> str:
        return self.string * max(0, times)

    def uppercase(self) -> str:
        return self.string.upper()

    def lowercase(self) -> str:
        return self.string.lower()

    def strip(self) -> str:
        return self.string.strip()

    def split(self, separator: str = None):
        return self.string.split(separator)

    def format(self, *args) -> str:
        return self.string.format(*args)

    def interpolate(self, **kwargs) -> str:
        return self.string.format(**kwargs)

    def reverse(self) -> str:
        return self.string[::-1]

    def is_palindrome(self) -> bool:
        cleaned = ''.join(c.lower() for c in self.string if c.isalnum())
        return cleaned == cleaned[::-1]


    def replace(self, old: str, new: str) -> str:
        return self.string.replace(old, new)

    def count(self, sub: str) -> int:
        return self.string.count(sub)

    def contains(self, sub: str) -> bool:
        return sub in self.string

