#Probably wont need to parse the href tags cause the server doesnt need to send anything external and 
#this might lead to some issues, LFI(LocalFileInclusion) ..etc
#(The href get's handled by the client) 



import os,re

class FileManager:

	def __init__(self,_projectFolderPath):
		self.projectFolderPath = _projectFolderPath
		self.srcFind = re.compile('src=[\"|\'].*[\"|\'] ')
		self.hrefFind = re.compile('href=[\"|\'].*[\"|\']')
		self.li = re.compile('[\"|\'].*[\"|\']')
		#self.spliter = re.compile('[\"|\']')
		self.FileName = re.compile('[a-zA-Z]+\.[a-zA-Z]+')

	def readFileContent(self, path, tp=None):
		print(f"\nself.projectFolderPath + path : {self.projectFolderPath + path}\n")
		if(os.path.isfile(self.projectFolderPath + path) and "image" not in tp):
			with open(self.projectFolderPath + path, "r") as opFile:
				return opFile.read()
		elif(os.path.isfile(self.projectFolderPath + path)):
			with open(self.projectFolderPath + path, "rb") as opFile:
				return opFile.read()
		else: 
			print("file does not exist")
			return False


	def parserHTML(self, fileContent, tp=None):
		if not "image" in tp and fileContent:
			src = self.srcFind.findall(fileContent)
			href = self.hrefFind.findall(fileContent)
			if len(src) != 0:
				for i in range(len(src)):
					src[i] = self.li.findall(src[i])[0]
					src[i] = re.sub('[\"|\']', '', str(src[i]))

					href[i] = self.li.findall(href[i])[0]
					href[i] = re.sub('[\"|\']', '', str(href[i]))
					if not self.FileName.match(href[i]):
						href.pop(i)
				parsedHS = src + href
				return parsedHS
		return False



