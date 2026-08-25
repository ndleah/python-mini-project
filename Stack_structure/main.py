class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Stack:
    def __init__(self):
        self.top = None
        self._size = 0

    def push(self, data):
        print(f"Adding {data} to the top of the stack")
        new_node = Node(data)
        new_node.next = self.top
        self.top = new_node
        self._size += 1

    def pop(self):
        if self.top is None:
            print("There is no item on the stack to unstack")
            return None

        popped_data = self.top.data
        print(f"Unstack {popped_data}")
        self.top = self.top.next
        self._size -= 1
        return popped_data

    def peek(self):
        if self.top is None:
            return None
        return self.top.data

    def is_empty(self) -> bool:
        return self.top is None

    def size(self) -> int:
        return self._size

    def __len__(self) -> int:
        return self._size

    def printData(self):
        print("Printing stack: ", end="")
        tmp_node = self.top
        while tmp_node is not None:
            print(f"[{tmp_node.data}]", end="")
            tmp_node = tmp_node.next
        print("")

def main():
    stack = Stack()
    stack.push('a')
    stack.push('b')
    stack.push('c')
    stack.push('d')
    stack.printData()
    print("Popped:", stack.pop())
    stack.push("Hello")
    stack.printData()
    print("Popped:", stack.pop())
    print("Popped:", stack.pop())

if __name__ == '__main__':
    main()

