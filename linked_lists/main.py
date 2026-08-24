from doubly_linked_list import _DoublyLinkedList
from linked_deque import LinkedDeque
from linked_queue import LinkedQueue
from linked_stack import LinkedStack

def main():
    print("--- Testing LinkedStack ---")
    stack = LinkedStack()
    stack.push(10)
    stack.push(20)
    print("Stack top:", stack.top())
    print("Stack pop:", stack.pop())
    print("Stack len:", len(stack))

    print("\n--- Testing LinkedQueue ---")
    queue = LinkedQueue()
    queue.enqueue("A")
    queue.enqueue("B")
    print("Queue first:", queue.first())
    print("Queue dequeue:", queue.dequeue())
    print("Queue len:", len(queue))

    print("\n--- Testing LinkedDeque ---")
    deque = LinkedDeque()
    deque.insert_first(1)
    deque.insert_last(2)
    deque.insert_first(0)
    print("Deque first:", deque.first())
    print("Deque last:", deque.last())
    print("Deque delete_first:", deque.delete_first())
    print("Deque delete_last:", deque.delete_last())
    print("Deque len:", len(deque))

if __name__ == "__main__":
    main()


