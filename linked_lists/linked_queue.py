
class Empty(Exception):
    pass

class LinkedQueue:

    class _Node:
        __slots__ = ("_element", "_next")

        def __init__(self, element, next_):
            self._element = element
            self._next = next_
    
    def __init__(self):
        self._head = None
        self._size = 0
        self._tail = None
    
    def is_empty(self):
        return self._size == 0
    

    def enqueue(self, element):
        new_tail = self._Node(element, None)
        if self.is_empty():
            self._head = new_tail
        else:
            self._tail._next = new_tail
        self._tail = new_tail
        self._size += 1
    
    def dequeue(self):
        if self.is_empty():
            raise Empty("Queue is empty")
        target = self._head._element
        self._head = self._head._next
        self._size -= 1

        return target
