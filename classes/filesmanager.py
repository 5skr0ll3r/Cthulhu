import os

class File:
	def __init__(self, _fileExtensions, _imageExtenxions):
		self.fileExtensions = _fileExtensions
		self.imageExtenxions = _imageExtenxions


	def isImage(self,fileExt):
		if(fileExt in self.imageExtenxions):
			return True
		else:
			return False


	def read(self, sitePath, filePath, isImage):
		path = (sitePath + filePath).strip()
		if(os.path.isfile(path)):
			if(isImage):
				with open(path,"rb") as opFile:
					return str(opFile.read())
			else:
				with open(path) as opFile:
					return opFile.read()
		else:
			return False
