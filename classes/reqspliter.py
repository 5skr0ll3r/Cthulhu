import re

class ReqSpliter:
	def __init__(self, _methods, _fileExt, _imageExt):
		self.methods = _methods
		self.fileExt = _fileExt
		self.imageExt = _imageExt


	def checkReqType(self, request):
		for i in self.methods:
			if i in request:
				return i
			else:
				return False

	def checkReqFilePath(self, request, checkReqType):
		if checkReqType:
			try:
				reqPath = re.search("\/.+?.\s",request).group()
			except AttributeError:
				reqPath = re.search("\/.+?.\s",request)
			return reqPath
		else:
			return False

	def determineFileExtFromReq(self, checkReqFilePath):
		if checkReqFilePath:
			for i in self.fileExt:
				if i in checkReqFilePath:
					return i
				else:
					continue
			for x in self.imageExt:
				if x in checkReqFilePath:
					return x
				else:
					continue
		return False


	def headerContentType(self, determineFileExtFromReq):
		if determineFileExtFromReq in self.fileExt:
			return "text/" + determineFileExtFromReq
		if determineFileExtFromReq in self.imageExt:
			return "image/" + determineFileExtFromReq
		else:
			return "text/plain"


	def requestIsAccepted(self, checkReqType, checkReqFilePath, determineFileExtFromReq):
		if checkReqType and checkReqFilePath and determineFileExtFromReq:
			return True 
		else: 
			return False


