import socket
from sys import exit
from classes.datastructs import Client

class Sock:

	def __init__(self, _port):
		self.interface = socket.gethostbyname(socket.gethostname()) #'127.0.0.1'#
		self.port = int(_port)
		self.socket = None

	def run(self):
		try:
			self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			self.socket.bind((self.interface,self.port))
			self.socket.listen()
		except OSError:
			exit("Something went wrong got OSError on Sock.run()")
			self.close()

	def accept(self):
		connection, address = self.socket.accept()
		return Client(address, connection)

	def close(self):
		try: 
			self.socket.shutdown(socket.SHUT_RDWR)
		except (socket.error, OSError, ValueError):
			pass
		self.socket.close()



