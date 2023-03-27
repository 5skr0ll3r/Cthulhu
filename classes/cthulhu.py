import argparse, os, sys, asyncio
from classes.frapitska import Sock
from classes.frapitska import Headers
from classes.reqspliter import ReqSpliter
from classes.filemanager import FileManager
from classes.tree import Tree


class App:

	def __init__(self, _port, _projectFolderPath):
		#checking if port is an intiger
		if(not isinstance(_port,int)):
			sys.exit("Port Must Be an Integer")
		#checking if path exists and if yes storing it in sitePath using the walrus operator
		if(not(os.path.exists(_projectFolderPath))):
			sys.exit("Path is not valid")

		self.sock = Sock(_port)
		self.projectFolderPath = _projectFolderPath
		self.reqSpliter = ReqSpliter()
		self.fileManager = FileManager(self.projectFolderPath)
		self.cache = Tree()
		self.request = None
		self.sock.run()


	#Get Request implimentation
	async def get(self, path, inFunc = None):

		while True:
			if(self.request == None):
				await self.sock.accept()
				self.request = await self.sock.receive()
			

			headers = Headers()
			#request = await self.sock.receive()
			#self.request = request
			
			isAccepted, requestDict, requestType, fileRequested, fileExtension, conType = self.reqSpliter.dataPrep(self.request) 

			print(f"\n\npath: {path}\nisAccepted: {isAccepted}\nsplitedZero: {requestDict}\nrequestType:{requestType}\nfileRequested: {fileRequested}\nfileExtension: {fileExtension}\nConType: {conType}\n\n")

			if requestType == "GET" and isAccepted:
				if not inFunc == None: return inFunc(self.request)
				

				data = self.fileManager.readFileContent(path, conType)
				parsedHS = self.fileManager.parserHTML(data, conType)
				print("="*30+f"\n{parsedHS}\n\n")

				##This should start on initialization
				## Appends The tree for each file
				self.cache.insertArray(fileRequested, parsedHS)
				self.cache.printTree()

				#headers = Headers(conType, data)
				header = headers.header(isAccepted,data,data,conType)
				print("="*30+f"\n\n{data}\n\n")
				await self.sock.respond(header)
				self.request = None

#				if not self.cache.isEmpty():
#					rest = self.cache.getValues(fileRequested)
#					await self.sock.accept()
#					self.request = await self.sock.receive()#

#					isAccepted, splitedZero, requestType, fileRequested, fileExtension, conType = self.reqSpliter.dataPrep(self.request)#

#					while True:
#						if rest and fileRequested in rest:
#							data = self.fileManager.readFileContent(path, conType)
#							headers = Headers(conType, data)
#							header = headers.header(isAccepted,data)
#							print("="*30+f"\n\n{data}\n\n")
#							await self.sock.respond(header)
#						else: break
									


				break
			else: 
				#self.request = None
				break



	async def post(self, apiPath, inFunc = None):
		pass