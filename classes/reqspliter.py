import re

class ReqSpliter:
	def __init__(self):
		self.methods = ("GET","POST","HEAD","DELETE","CONNECT","PUT","OPTIONS","TRACE","PATCH")
		self.fileExt = ("html","css","js")
		self.imageExt = ("jpeg","png","jpg","ico")
		self.regSplit = re.compile(".+.\n")
		self.regMethod = re.compile("[A-Z]+\S")
		self.regFileName = re.compile('[a-zA-Z]+\.[a-zA-Z]+')

		#Splites the request headers and stores them in a dictionary for easier access/ first line stored as request
	def spliter(self,request):
	    reqDict = {}
	    iterZero = True
	    for i in re.finditer(self.regSplit, request):
	        if iterZero:
	            reqDict["request"] = i.group()
	            iterZero = False
	            continue
	        reqDict[i.group().split(":")[0]] = i.group().split(":")[1].strip()
	    return reqDict

#Checks the type of the request 
	def checkReqType(self, requestDict):
		#Returning the first cause if any other method is mentioned in the request this might create a bug 
		requestType = self.regMethod.findall(requestDict["request"])[0]
		print(f"Regex -> requestType: {requestType}")
		for i in self.methods:
			if i == requestType:
				return i
			else:
				continue
		return False


#Determines the path for the file requested
	def checkReqFilePath(self, requestDict):
		#Returning the first element (index 0) cause if any other method is mentioned in the request this might create a bug 
		print(f"Regex -> checkRegFilePath: {self.regFileName.findall(requestDict['request'])[0]}")
		return self.regFileName.findall(requestDict["request"])[0]

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


	def dataPrep(self, request):
		requestDict = self.spliter(request)
		requestType = self.checkReqType(requestDict)
		prep1 = self.checkReqFilePath(requestDict)
		fileRequested = self.regFileName.findall(prep1)[0]
		fileExtension = self.determineFileExtFromReq(fileRequested)
		conType = self.headerContentType(fileExtension)
		isAccepted = self.requestIsAccepted(requestType, fileRequested, fileExtension)
		return isAccepted, requestDict, requestType, fileRequested, fileExtension, conType
