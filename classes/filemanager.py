import os

class FileManager:

	global projectFolderPath

	def readFileContent(path):
		if(os.path.isfile(FileManager.projectFolderPath + path)):
			with open(FileManager.projectFolderPath + path, "r") as opFile:
				return opFile.read()
		else: 
			print("file does not exist")
			return False





