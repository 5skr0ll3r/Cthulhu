from classes.frapitska import Sock
from classes.frapitska import Headers
from classes.reqspliter import ReqSpliter


#Accepted methods go here
methods = ("GET","POST","HEAD","DELETE","CONNECT","PUT","OPTIONS","TRACE","PATCH")

#Accepted file extensions go here
fileExt = ("html","css","js")
imageExt = ("jpeg","png","jpg","ico")

data = "<html>\n<head>\n<title>Test</title>\n</head>\n<body>\n<h1>Testing</h1>\n</body>\n</html>"

reqSpliter = ReqSpliter(methods, fileExt, imageExt)


sock = Sock(8000)
sock.run()

while True:
	sock.accept()
	req = sock.receive().decode('utf-8')

	reqType = reqSpliter.checkReqType(req)
	reqFilePath = reqSpliter.checkReqFilePath(req, reqType)
	reqFileExt = reqSpliter.determineFileExtFromReq(reqFilePath)
	conType = reqSpliter.headerContentType(reqFileExt)


	headers = Headers(conType, data)
	header = headers.header(True,True)

	sock.respond(header)
	#sock.close()