class Node:
	def __init__(self, data):
		self.data = data
		self.next = None
	
class Stack:
	def __init__(self):
	    self.top = None
	    
	def push(self, data):
		print(f"Adding {data} to the top of the stack")

		# If there is no data, we add the value in the top element and return
		if self.top == None:
			self.top = Node(data)
			return
		new_node = Node(data)
		new_node.next = self.top
		self.top = new_node

	def pop(self):
		# If there is no data in the top node, we return
		if self.top == None:
			print ("There is no item on the stack to unstack")
			return

		print(f"Unstack {self.top.data}")
		self.top = self.top.next

	def printData(self):
		print("Printing stack: ")

		# Step through the stack and print values
		tmp_node = self.top

		while tmp_node != None:
			print (f"[{tmp_node.data}]", end = "")
			tmp_node = tmp_node.next

		print("")

stack = Stack()
stack.push('a')
stack.push('b')
stack.push('c')
stack.push('d')
stack.printData()
stack.pop()
stack.push("Hello")
stack.printData()
stack.pop()
stack.pop()
