import re

class ReqSpliter:
	def __init__(self):
		self.methods = ("GET","POST","HEAD","DELETE","CONNECT","PUT","OPTIONS","TRACE","PATCH")
		self.fileExt = ("html","css","js")
		self.imageExt = ("jpeg","png","jpg","ico")
		self.regSplit = re.compile(".+.\n")
		self.regMethod = re.compile("[A-Z]+\S")
		self.regFileName = re.compile('[a-zA-Z]+\.[a-zA-Z]+')


#Splits the request Headers in every new line and returns a list so i can parse them easier
	def spliter(self,request):
		reqList = []
		for l in re.finditer(self.regSplit, request):
			try:
				reqList.append(l.group())
			except AttributeError:
				reqList.append(l)
		print("\n\n" + reqList[0] + "\n\n")
		return reqList


#Checks the type of the request
	def checkReqType(self, requestList):
		#Returning the first element (index 0) cause if any other method is mentioned in the request this might create a bug 
		requestType = self.regMethod.findall(requestList)[0]
		print(f"Regex -> requestType: {requestType}")
		for i in self.methods:
			if i == requestType:
				return i
			else:
				continue
		return False


#Determines the path for the file requested
	def checkReqFilePath(self, requestList):
		#Returning the first element (index 0) cause if any other method is mentioned in the request this might create a bug 
		print(f"Regex -> checkRegFilePath: {self.regFileName.findall(requestList)[0]}")
		return self.regFileName.findall(requestList)[0]

#Determines the requested File's extension
	def determineFileExtFromReq(self, checkReqFilePath):
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


	def dataPrep(self, request):
		splitedZero = self.spliter(request)[0]
		requestType = self.checkReqType(splitedZero)
		prep1 = self.checkReqFilePath(splitedZero)
		fileRequested = self.regFileName.findall(prep1)[0]
		fileExtension = self.determineFileExtFromReq(fileRequested)
		conType = self.headerContentType(fileExtension)
		isAccepted = self.requestIsAccepted(requestType, fileRequested, fileExtension)
		return isAccepted, splitedZero, requestType, fileRequested, fileExtension, conType

	def final(self):
		pass

