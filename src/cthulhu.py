import os, sys, _thread
from src.serversocket import Sock
from src.requesthandler import RequestHandler
from src.datastructs import Client
from src.datastructs import Endpoint
from time import sleep



class App:

	def __init__(self, _interface: str = None, _port: int = 8000):
		if(not isinstance(_port,int)):
			sys.exit("Port Must Be an Integer")
		self.sock = Sock(_interface, _port)
		self.sock.run()
		self.endpoints = []
		#TODO: parse all registered endpoint static file and
		#add them to the sitemap and serve them all
		self.sitemap = []
		

	####Start Endpoint registration###
	def get(self, endpoint: str, *callbacks):
		for callback in callbacks:
			if(not callable(callback) or not hasattr(callback, '__call__')):
				raise TypeError(f"A callable function is expected as an argument not a {type(callback)}")
		self.endpoints.append(Endpoint("GET", endpoint, callbacks))



	def post(self, endpoint: str, *callbacks):
		print("App->post() not implemented yet")
	####End Endpoint registration###


	###Start Middleware Registration###
	def use(self, endpoint: str, *callbacks):
		print("App->use() not implemented yet")
	###End Middleware Registration###


	def onNewClient(self, client: Client):
		return RequestHandler.requestHandler(client, self.endpoints)

	def listen(self, callback=None):
		while True:
			client = self.sock.accept()
			_thread.start_new_thread(self.onNewClient,(client,))


	def close(self):
		self.sock.close()
		
