import socket, asyncio


class Sock:

	def __init__(self, _port):
		self.interface = socket.gethostbyname(socket.gethostname()) #'127.0.0.1'#
		self.port = int(_port)
		self.connection = None
		self.address = None
		self.dataReceived = None
		self.socket = None

	def run(self):
		try:
			self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			self.socket.bind((self.interface,self.port))
			self.socket.listen()
		except OSError:
			print("Something went wrong")
			self.close()

	async def accept(self):
		self.connection, self.address = self.socket.accept()

	async def receive(self):
		self.dataReceived = self.connection.recv(3000).decode('utf-8')
		print(f"\nData received:\n{self.dataReceived}\n\n")
		return self.dataReceived

	async def respond(self, data):
		self.connection.sendall(data)
		#self.connection.close()

	def close(self):
		try: 
			self.socket.shutdown(socket.SHUT_RDWR)
		except (socket.error, OSError, ValueError):
			pass
		self.socket.close()



