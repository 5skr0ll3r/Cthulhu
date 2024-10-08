import socket
from sys import exit
from src.datastructs import Client
from src.report import Log


#TODO: ADD SOCK5 support (later)
#TODO: Has been a long time without changes so something must be wrong
class Sock:

	def __init__(self, _interface: str, _port: int):
		self.interface = _interface if _interface else socket.gethostbyname(socket.gethostname())
		self.port = int(_port)
		self.socket = None

	def run(self):
		try:
			self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			self.socket.bind((self.interface,self.port))
			self.socket.listen()
		except (socket.error, OSError) as e:
			self.socket.close()
		

	def accept(self):
		try:
			connection, address = self.socket.accept()
			return Client(address, connection)
		except (socket.error, OSError) as e:
			print(f"Error while accepting connection: {e}")

####TODO: Handle on shutdown and close "^CError while shuting down the socket: [Errno 57] Socket is not connected" instead of printing
	def close(self):
		try: 
			self.socket.shutdown(socket.SHUT_RDWR)
		except (socket.error, OSError) as e:
			print(f"Error while shuting down the socket: {e}")
		finally:
			try:
				self.socket.close()
			except (socket.error) as e:
				print(f"Error closing the socket: {e}")
