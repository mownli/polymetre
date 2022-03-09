class LinkedList:

	class Node:

		def __init__(self, data):
			self.data = data
			self.next = None

	def __init__(self):
		self.head = None
		self.tail = None
		self.size = 0
		self.dict = {}

	def append(self, data):
		if self.head is None:
			self.head = self.Node(data)
			self.tail = self.head
		else:
			self.tail.next = self.Node(data)
			self.tail = self.tail.next
		if self.tail not in self.dict:
			self.dict[self.tail] = self.size
		self.size += 1

	def __iter__(self):
		node = self.head
		while node is not None:
			yield node
			node = node.next

	def __len__(self):
		return self.size

	def index(self, node):
		return self.dict[node]
