class Empty(Exception):
    """Custom exception for empty stack operations."""
    pass


class LinkedStack:
    """Stack implementation using a singly linked list.

    Examples:
        >>> s = LinkedStack()
        >>> s.push(10)
        >>> s.top()
        10
    """

    class _Node:
        """Lightweight node for singly linked list."""
        __slots__ = ("_element", "_next")

        def __init__(self, element, next):
            self._element = element
            self._next = next

    def __init__(self):
        """Create an empty stack."""
        self._head = None
        self._size = 0

    def __len__(self):
        """Return the number of elements in the stack."""
        return self._size

    def is_empty(self):
        """Return True if the stack is empty."""
        return self._size == 0

    def push(self, e):
        """Push element e onto the top of the stack."""
        self._head = self._Node(e, self._head)
        self._size += 1

    def top(self):
        """Return the top element without removing it."""
        if self.is_empty():
            raise Empty("stack is empty")
        return self._head._element

    def pop(self):
        """Remove and return the top element."""
        if self.is_empty():
            raise Empty("stack is empty")

        answer = self._head._element
        self._head = self._head._next
        self._size -= 1
        return answer

    def clear(self):
        """Remove all elements from the stack."""
        self._head = None
        self._size = 0
