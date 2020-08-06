import numpy as np

diskColor = {0:"gold", 1: "blue", 2: "red", 3:"green", 4:"pink"}

class Hanoi:
	def __init__(self, n):

		self.size = n

		self.stacks = [[0], [0], [3]]

		for i in xrange(n, 0, -1):
			self.stacks[0].append(i)

	# pops element from stack1 and adds it to stack2
	def move(self, stack1, stack2):
		if len(self.stacks[stack1]) > 1:
			self.stacks[stack2].append(self.stacks[stack1].pop())

	def getStackTop(self, num):
		return self.stacks[num]

	def getStackTopColor(self, num):
		diskNum = self.stacks[num].pop()
		self.stacks[num].append(diskNum)

		return diskColor[diskNum]

	def printState(self):
		for i in xrange(3):
			print self.stacks[i]
