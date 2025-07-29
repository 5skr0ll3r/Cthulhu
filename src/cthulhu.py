import os, sys, _thread
from src.serversocket import Sock
from src.requesthandler import RequestHandler
from src.datastructs import Client, Endpoint, Methods
from src.utils import validateFuncs, index
from time import sleep
from src.utils import NIY
from src.report import Log


class App:

	def __init__(self, _interface: str = None, _port: int = 8000):
		if(not isinstance(_port,int)):
			sys.exit("Port Must Be an Integer")

		self.sock = Sock(_interface, _port)
		self.sock.run()
		self.endpoints: list[Endpoint] = []
		self.parse_body: bool = False
	
	def __str__(self):
		sock_name = self.sock.getsockname()
		return f"App-Settings:\nInterface: {sock_name[0]}\nPort: {sock_name[1]}"

	def route(self, endpoint: str, methods: list[str] = ["GET"]):
		meths = [s.strip() for s in methods]
		for i in meths:
			if(i not in Methods.methods):
				raise ValueError(f"Method {i} is not included in Methods.methods") #TODO: Add a traceback tool in utils
		def wrapper(func):
			i = index(endpoint, self.endpoints)
			if(i != None):
				self.endpoints[i].addFunc(func)
				return func
			validateFuncs(func)
			self.endpoints.append(Endpoint(meths, endpoint, [func]))
			return func
		return wrapper


	def parse_req_body(self):
		self.parse_body = True
		return 

	#Middleware registration
	def use(self, endpoint: str, *funcs):
		return NIY()
		

	def on_new_client(self, client: Client):
		return RequestHandler.requestHandler(client, self.endpoints, self.parse_body)

	def listen(self, func=None):
		while True:
			client = self.sock.accept()
			_thread.start_new_thread(self.on_new_client,(client,))


	def close(self):
		self.sock.close()
		
