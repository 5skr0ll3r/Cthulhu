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

	def addChild(self,node):
		assert isinstance(node, Tree)		
		self.children.append(node)


	def getIndex(self, name):
		for i in range(len(self.children)):
			if name == str(self.children[i]):
				return i
		return False

	def getValues(self,name):
		li = []
		index = self.getIndex(name)
		for i in range(len(self.children[index].children)):
			li.append(str(self.children[index].children[i]))
		return li


	def printTree(self):
		for i in range(len(self.children)):
			for n in range(len(self.children[i].children)):
				print(str(self.name) + " -> " + str(self.children) + " -> " + str(self.children[i]) + " : " + str(self.children[i].children[n]) + "\n")

#Only Works For the 3Layer structure
	def insertArray(self, fileRequested, array):
		if not self.exists(fileRequested) and not len(array) == 0:
			self.addChild(Tree(fileRequested,[
				Tree(array[0])
					])
				)
			if not len(array) == 1:
				index = self.getIndex(fileRequested)
				for i in range(len(array)):
					self.children[index].addChild(Tree(array[i]))
			return
		else:
			index = self.getIndex(fileRequested)
			for i in range(0,len(array)):
				self.children[index].addChild(Tree(array[i]))


def main():


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



	t.printTree()
	

	print("\n"+"="*12+"\n")

	t.addChild(Tree('register',[
		Tree('reg.css'),
		Tree('reg.js')
		]
	))

	t.printTree()

	t.children[0].addChild(Tree("index.php"))

	t.printTree()

	index = t.getIndex("index")

	values = t.getValues("index")

	print(f"\n\nIndexx: {index}\n\n")
	print(f"\n\nValues: {values}\n\n")




	t.addChild(Tree("register.html"))

	values = t.getValues('register.html')

	print(f"\n\nValues: {values}\n\n")


	t.insertArray("register.html",["reg.css","reg.js"])
	values = t.getValues("register.html")
	print(f"\n\nValues: {values}\n\n")

	t.insertArray("register.html",["skata.css","gamw.js"])
	values = t.getValues("register.html")
	print(f"\n\nValues: {values}\n\n")



if __name__ == '__main__':
	main()