from doubly_linked_list import _DoublyLinkedList

class Empty(Exception):
    pass

class LinkedDeque(_DoublyLinkedList):

    def first(self):
        if self.is_empty():
            raise Empty("Dequeu is empty") 
        return self._header._next._element
    
    def last(self):
        if self.is_empty():
            raise Empty("Dequeu is empty")
        return self._trailer._previous._element
    
    def insert_first(self, element):
        self._insert_between(element, self._header, self._trailer)

    def insert_last(self, element):
        self._insert_between(element, self._trailer._previous, self._trailer)

    def delete_first(self):
        if self.is_empty():
            raise Empty("Deque is empty")
        return self._delete_node(self._header._next)
    
    def delete_last(self):
        if self.is_empty():
            raise Empty("Deque is empty")
        
        return self._delete_node(self._trailer._previous)
    
