import os, sys, _thread
from classes.serversocket import Sock
from classes.filemanager import FileManager
from classes.tree import Tree
from classes.requesthandler import RequestHandler
from classes.datastructs import Client
from classes.datastructs import Endpoint
from time import sleep



class App:

	def __init__(self, _port, _projectFolderPath):

		#self.daemon = Daemon(_port,_projectFolderPath)
		if(not isinstance(_port,int)):
			sys.exit("Port Must Be an Integer")
		if(not _projectFolderPath[-1] == "/"):
			_projectFolderPath += "/"
		if(not(os.path.exists(_projectFolderPath))):
			sys.exit("Path is not valid")

		self.sock = Sock(_port)
		self.projectFolderPath = _projectFolderPath
		FileManager.projectFolderPath = _projectFolderPath
		#self.cache = Tree()
		self.sock.run()
		self.endpoints = []
		#TODO: parse all registered endpoint static file and
		#add them to the sitemap and serve them all
		self.sitemap = []
		

	####Start Endpoint registration###
	def get(self, endpoint, local_path, callback=None):
		self.endpoints.append(Endpoint("GET", endpoint, local_path, callback))



	def post(self, endpoint, callback=None):
		pass
	####End Endpoint registration###


	###Start Middleware Registration###
	def use(self, endpoint, callback=None):
		pass
	###End Middleware Registration###


	def on_new_client(self, client):
		RequestHandler.requestHandler(client, self.endpoints)

	def listen(self, callback=None):
		while True:
			client = self.sock.accept()
			_thread.start_new_thread(self.on_new_client,(client,))


	def close(self):
		self.sock.close()
		

#def main():
#	app = App(8000)
#	app.get("/", "index.html")
#	app.listen()
#if __name__ == "__main__":
#	main()

#python3 cthulhu.py > res.tmp
#seq 10000 | xargs -n 1 -P 200 -I {} curl http://192.168.1.126:8000/
#cat res.tmp | uniq -c