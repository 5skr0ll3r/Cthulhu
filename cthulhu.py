import argparse, os, sys, threading
from classes.frapitska import Sock
from classes.frapitska import Headers
from classes.reqspliter import ReqSpliter


#Accepted methods go here
methods = ("GET","POST","HEAD","DELETE","CONNECT","PUT","OPTIONS","TRACE","PATCH")

#Accepted file extensions go here
fileExt = ("html","css","js")
imageExt = ("jpeg","png","jpg","ico")


reqSpliter = ReqSpliter(methods, fileExt, imageExt)



def args():
	ap = argparse.ArgumentParser(description="Local Site Hosting software (Public too if port forward)\n-p is for the port you wish to use to run the site to\n-s is for the psites folder path")
	ap.add_argument("-p", "--port", required=True, help="Port to Run on")
	ap.add_argument("-s", "--site",required=True, help="Path for Project")
	return vars(ap.parse_args())


def readFileContent(sitePath, reqFile, extension, fileExt, imageExt):
	if extension in imageExt:
		path = (sitePath + reqFile).strip()
		if(os.path.exists(path)):
			with open(path, "rb") as opFile:
				return opFile.read()
		else: 
			return False
	else:
		path = (sitePath + reqFile).strip()
		if(os.path.exists(path)):
			with open((sitePath + reqFile).strip(), "r") as opFile:
				return opFile.read()
		else: 
			return False


def handler(sock, sitePath):

	while True:
		req = sock.receive().decode('utf-8')

		reqType = reqSpliter.checkReqType(req)
		reqFilePath = reqSpliter.checkReqFilePath(req, reqType)
		reqFileExt = reqSpliter.determineFileExtFromReq(reqFilePath)
		print("\n\nReqFileExt : " + reqFileExt)
		print("\n\nReqFilePath : " + reqFilePath + "\n\n")
		conType = reqSpliter.headerContentType(reqFileExt)

		data = readFileContent(sitePath,reqFilePath, reqFileExt, reqSpliter.fileExt, reqSpliter.imageExt)

		headers = Headers(conType, data)
		header = headers.header(reqSpliter.requestIsAccepted(reqType, reqFilePath, reqFileExt),data)

		sock.respond(header)


def main():

	argv = args()

	#checking if path exists and if yes storing it in sitePath with the walrus operator
	if(not(os.path.exists(argv["site"]) and (sitePath := argv["site"]))):
		sys.exit("Path is not valid")

	sock = Sock(argv["port"])
	sock.run()



	while True:
		sock.accept()
		thread = threading.Thread(target=handler, args=(sock, sitePath))
		thread.start()



if __name__ == "__main__":
	main()




