#Trre Has only 3 Layers cause the files passed in the tree will only be
#1 Root Name when Initialized
#2 Main HTML file path
#3 Content's. Meaning src,img,videos (Note no href) paths
#
#

class Tree:
	def __init__(self, name="root", children=None):
		self.name = name
		self.children = []
		if children is not None:
			for child in children:
				self.addChild(child)

	def __repr__(self):
		return self.name

	def exists(self, name):
		for i in range(len(self.children)):
			if name == self.children[i]:
				return True
		return False

	def isEmpty(self):
		if not len(self.children) == 0:
			return False
		return True

	def addChild(self,node):
		assert isinstance(node, Tree)		
		self.children.append(node)


	def getIndex(self, name):
		for i in range(len(self.children)):
			if name == str(self.children[i]):
				return i
		return False

	def getValues(self,name):
		if self.exists(name):
			li = []
			index = self.getIndex(name)
			for i in range(len(self.children[index].children)):
				li.append(str(self.children[index].children[i]))
			return li
		return False


	def printTree(self):
		for i in range(len(self.children)):
			for n in range(len(self.children[i].children)):
				print("\n\n" + str(self.name) + " -> " + str(self.children) + " -> " + str(self.children[i]) + " : " + str(self.children[i].children[n]) + "\n\n")

#Only Works For the 3Layer structure
	def insertArray(self, fileRequested, array):
		if not self.exists(fileRequested) and not array == False:
			self.addChild(Tree(fileRequested,[
				Tree(array[0])
					])
				)
			if not len(array) == 1:
				index = self.getIndex(fileRequested)
				for i in range(1,len(array)):
					self.children[index].addChild(Tree(array[i]))
			return True
		if(not array == False):
			index = self.getIndex(fileRequested)
			for i in range(0,len(array)):
				self.children[index].addChild(Tree(array[i]))
			return True
		return False




#def main():
#

	t = Tree('files', [
			Tree('index',[
				Tree('index.js'),
                Tree('index.css')
				]),
            Tree('about',[
            	Tree('about.js'),
                Tree('about.css')
                ]),
            Tree('login', [
            	Tree('log.js'),
                Tree('log.css')
                ])
            ])
#
#

#	printTree(t)
#	

#	print("\n"+"="*12+"\n")

#	t.add_child(Tree('register',[
#		Tree('reg.css'),
#		Tree('reg.js')
#		]
#	))

#	printTree(t)

#if __name__ == '__main__':
#	main()