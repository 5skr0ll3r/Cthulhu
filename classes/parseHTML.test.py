import re
from tree import Tree

def main():
	regHref = re.compile('href=[\"|\'].*[\"|\']') 
	regSrc = re.compile('src=[\"|\'].*[\"|\'] ')
	li = re.compile('[\"|\'].*[\"|\']')

	with open('../test/index.html', 'r') as f:
		cont = f.read()
		print(cont)

		#Find HREF-->
		s = regHref.findall(cont)
		print(s)
		d = li.findall(s[0])
		print(d)
		n = d[0].replace('"','')
		print(n)
		#<--
		#Find SRC-->
		s = regSrc.findall(cont)
		print(s)
		d = li.findall(s[0])
		print(d)
		n1 = d[0].replace('"','')
		print(n1)
		#<--
		t = Tree('files',[Tree('index.html',[
				Tree(n),
				Tree(n1)
				]),
				Tree('about.html',[
					Tree(n),
					Tree(n1)
				])
			])


		t.printTree()

if __name__ == '__main__':
	main()