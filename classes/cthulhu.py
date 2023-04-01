import os, sys, asyncio
from classes.frapitska import Sock
from classes.headconsrtuctor import Headers
from classes.reqspliter import ReqSpliter
from classes.filemanager import FileManager
from classes.tree import Tree
from time import sleep


class App:

	def __init__(self, _port, _projectFolderPath):

		if(not isinstance(_port,int)):
			sys.exit("Port Must Be an Integer")

		if(not(os.path.exists(_projectFolderPath))):
			sys.exit("Path is not valid")

		self.sock = Sock(_port)
		self.projectFolderPath = _projectFolderPath
		FileManager.projectFolderPath = _projectFolderPath
		self.cache = Tree()
		self.sock.run()




	#Get Request implimentation
	async def get(self, alias, path, inFunc = None):
		data = FileManager.readFileContent(path)
		parsedHS = FileManager.parserHTML(data, path)
		print(f"\n\nparsed:\n{parsedHS}\n\n")
		self.cache.insertArray(alias, parsedHS)
		self.cache.printTree()
		print(f"\n\nCached:\n{self.cache.getValues(alias)}\n\n")
		while True:
			
			await self.sock.accept()
			request = await self.sock.receive()
			
			isAccepted, requestDict, requestType, pathRequested = ReqSpliter.dataPrep(request) 
			contentType = FileManager.headerContentType(path)

			print(f"\n\npath: {path}\nisAccepted: {isAccepted}\nsplitedZero: {requestDict}\nrequestType:{requestType}\npathRequested: {pathRequested}\n\nConType: {contentType}\n\n")

			if requestType == "GET" and isAccepted and (alias == pathRequested):
				if inFunc != None: return inFunc(request)

				header = Headers.header(isAccepted, data, contentType)

				await self.sock.respond(header)

				cached = self.cache.getValues(alias)
				i = 0

				while i <= len(cached) - 1:
					print(f"\n\ni:{i}\n\n")
					nextRequest = await self.sock.receive()

					isAccepted, requestDict, requestType, newPathRequested = ReqSpliter.dataPrep(nextRequest)
					print(f"\n\npath: {path}\nisAccepted: {isAccepted}\nsplitedZero: {requestDict}\nrequestType:{requestType}\npathRequested: {pathRequested}\n\nConType: {contentType}\n\n")

					if newPathRequested.startswith("/"): cachedPath = newPathRequested[1:]
					else: cachedPath = newPathRequested
					newData = FileManager.readFileContent(cachedPath)
					if not cachedPath: continue
					newContentType = FileManager.headerContentType(cachedPath)

					header = Headers.header(isAccepted, newData, newContentType)

					await self.sock.respond(header)
					i += 1
					

				#self.sock.close()
				sleep(.1)
				continue
			else: 

				continue



	async def post(self, apiPath, inFunc = None):
		pass