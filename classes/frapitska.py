import socket


class Sock:

	def __init__(self, _port):
		self.host = "127.0.0.1"#socket.gethostbyname(socket.gethostname())
		self.port = int(_port)
		self.connection = None
		self.address = None
		self.dataReceived = None
		self.socket = None

	def run(self):
		self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.socket.bind((self.host, self.port))
		self.socket.listen()


	def accept(self):
		self.connection, self.address = self.socket.accept()

	def receive(self):
		self.dataReceived = self.connection.recv(3000)
		return self.dataReceived

	def respond(self, data):
		self.connection.send(data.encode())
		self.connection.close()


	def close(self):
		self.socket = None



class Headers:
	def __init__(self, _contentType, _data):
		self.data = _data
		if(not _data):
			self.data = "No Content"
		self.next = "\r\n"
		self.end = "\r\n\r\n"
		self.okay = "HTTP/1.1 200 OK"
		self.notFound = "HTTP/1.1 404 NOT FOUND"
		self.internalError = "HTTP/1.1 500 INTERNAL SERVER ERROR"
		self.contentType = f"Content-Type: {_contentType}"
		self.length = f"Content-Length: {len(self.data)}"
		self.server = "Server: Cthulhu/0.1"

	def header(self, accepted, exists):
		if(accepted and exists):
			return self.okay + self.next + self.contentType + self.next + self.length + self.next + self.server + self.end + self.data
		elif(accepted and not exists):
			return self.notFound + self.next + self.contentType + self.next + self.length + self.next + self.server + self.end
		else:
			return self.internalError + self.end


