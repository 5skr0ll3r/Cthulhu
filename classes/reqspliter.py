import re

class ReqSpliter:
	methods = ("GET","POST","HEAD","DELETE","CONNECT","PUT","OPTIONS","TRACE","PATCH")
	regSplit = re.compile(".+.\n")
	regMethod = re.compile("[A-Z]+\S")
	regFileName = re.compile('[a-zA-Z]+\.[a-zA-Z]+')

		#Splites the request headers and stores them in a dictionary for easier access/ first line stored as request
	def spliter(request):
	    reqDict = {}
	    iterZero = True
	    for i in re.finditer(ReqSpliter.regSplit, request):
	        if iterZero:
	            reqDict["request"] = i.group()
	            iterZero = False
	            continue
	        reqDict[i.group().split(":")[0]] = i.group().split(":")[1].strip()
	    return reqDict

#Checks the type of the request 
	def checkReqType(requestDict):
		#Returning the first cause if any other method is mentioned in the request this might create a bug 
		requestType = ReqSpliter.regMethod.findall(requestDict["request"])[0]
		print(f"Regex -> requestType: {requestType}")
		for i in ReqSpliter.methods:
			if i == requestType:
				return i
			else:
				continue
		return False


#Determines the path for the file requested
	def checkReqFilePath(requestDict):
		return requestDict["request"].split(" ")[1]



	def requestIsAccepted(checkReqType):
		if checkReqType and checkReqType in ReqSpliter.methods:
			return True 
		else: 
			return False


	def dataPrep(request):
		requestDict = ReqSpliter.spliter(request)
		requestType = ReqSpliter.checkReqType(requestDict)
		pathRequested = ReqSpliter.checkReqFilePath(requestDict) #prep1
		isAccepted = ReqSpliter.requestIsAccepted(requestType)
		return isAccepted, requestDict, requestType, pathRequested
