import os

class FileManager:

	global projectFolderPath

	def readFileContent(path: str):
		if(os.path.isfile(path)):#FileManager.projectFolderPath +
			with open(path, "r") as opFile:
				return opFile.read()
		else: 
			print("file does not exist")
			return False


