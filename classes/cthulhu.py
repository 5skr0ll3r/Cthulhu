import os, sys, asyncio
from classes.frapitska import Sock
from classes.frapitska import Headers
from classes.reqspliter import ReqSpliter
from classes.filemanager import FileManager
from classes.tree import Tree


class App:

	def __init__(self, _port, _projectFolderPath):

		if(not isinstance(_port,int)):
			sys.exit("Port Must Be an Integer")

		if(not(os.path.exists(_projectFolderPath))):
			sys.exit("Path is not valid")

		self.sock = Sock(_port)
		self.projectFolderPath = _projectFolderPath
		self.reqSpliter = ReqSpliter()
		self.fileManager = FileManager(self.projectFolderPath)
		self.cache = Tree()
		#self.request = None
		self.sock.run()




	#Get Request implimentation
	async def get(self, alias, path, inFunc = None):

		while True:
			
			await self.sock.accept()
			request = await self.sock.receive()
			

			headers = Headers()
			#request = await self.sock.receive()
			#self.request = request
			
			isAccepted, requestDict, requestType, fileRequested, fileExtension, conType = self.reqSpliter.dataPrep(request) 

			print(f"\n\npath: {path}\nisAccepted: {isAccepted}\nsplitedZero: {requestDict}\nrequestType:{requestType}\nfileRequested: {fileRequested}\nfileExtension: {fileExtension}\nConType: {conType}\n\n")

			if requestType == "GET" and isAccepted and (alias == fileRequested):
				if not inFunc == None: return inFunc(request)
				

				data = self.fileManager.readFileContent(path, conType)
				parsedHS = self.fileManager.parserHTML(data, conType)
				print("="*30+f"\n{parsedHS}\n\n")

				##This should start on initialization
				## Appends The tree for each file
				self.cache.insertArray(fileRequested, parsedHS)
				self.cache.printTree()

				#headers = Headers(conType, data)
				header = headers.header(isAccepted,data,data,conType)
				#print("="*30+f"\n\n{data}\n\n")
				await self.sock.respond(header)
				#request = None
				data = None
				parsedHS = None

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
									


				continue
			else: 
				#self.request = None
				continue



	async def post(self, apiPath, inFunc = None):
		pass