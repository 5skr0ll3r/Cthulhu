#Probably wont need to parse the href tags cause the server doesnt need to send anything external and 
#this might lead to some issues, LFI(LocalFileInclusion) ..etc
#(The href get's handled by the client) 



import os,re

class FileManager:

	#global projectFolderPath
	fileExt = ("html","css","js")
	imageExt = ("jpeg","png","jpg","ico")
	srcFind = re.compile('src=[\"|\'].*[\"|\'] ')
	hrefFind = re.compile('href=[\"|\'].*[\"|\']')
	li = re.compile('[\"|\'].*[\"|\']')
	spliter = re.compile('[\"|\']')
	FileName = re.compile('[a-zA-Z]+\.[a-zA-Z]+')

	def readFileContent(path):
		print(f"\nFileManager.projectFolderPath + path : {FileManager.projectFolderPath + path}\n")
		if(os.path.isfile(FileManager.projectFolderPath + path) and "image" not in FileManager.headerContentType(path)):
			with open(FileManager.projectFolderPath + path, "r") as opFile:
				return opFile.read()
		elif(os.path.isfile(FileManager.projectFolderPath + path)):
			with open(FileManager.projectFolderPath + path, "rb") as opFile:
				return opFile.read()
		else: 
			print("file does not exist")
			return False


	def parserHTML(data, path):
		if not "image" in FileManager.headerContentType(path) and data:
			src = FileManager.srcFind.findall(data)
			href = FileManager.hrefFind.findall(data)
			if len(src) != 0:
				for i in range(len(src)):
					src[i] = FileManager.li.findall(src[i])[0]
					src[i] = re.sub('[\"|\']', '', str(src[i]))

					href[i] = FileManager.li.findall(href[i])[0]
					href[i] = re.sub('[\"|\']', '', str(href[i]))
					if not FileManager.FileName.match(href[i]):
						href.pop(i)
				parsedHS = src + href
				return parsedHS
		return False


	def headerContentType(fileName):
		print(f"\n\nFileName in filemanager: {fileName}\n\n")
		extension = fileName.split(".")[1]
		if extension in FileManager.fileExt:
			return "text/" + extension
		if extension in FileManager.imageExt:
			return "image/" + extension
		else:
			return "text/plain"



