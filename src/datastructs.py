from dataclasses import dataclass
from socket import socket
from src.utils import validateFuncs, parse_body, NIY
from datetime import datetime
#from src.report import Log

@dataclass
class Methods:
	methods = ["GET", "HEAD", "POST", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"]


@dataclass
class Client:
	"""Client object"""
	address: str
	connection: socket

	def __dict__(self):
		return {"address": self.address}


@dataclass
class Endpoint:
	"""Endpoint Object"""
	methods: list[str]
	endpoint: str
	funcs: list
	sitemap: list[str] = None

	def addFunc(self, func):
		validateFuncs(func)
		self.funcs.append(func)
		return

	def parseFile(path: str): #will only be used if dev uses my long to come renderer or io api (will also §cache static files)
		NIY()
		return


@dataclass
class StaticHeaders:
	#TODO: To begin with dont do this XD
	nextH: str = "\r\n"
	end: str = "\r\n\r\n"
	ver11: str = "HTTP/1.1"
	okay: str = "HTTP/1.1 200 OK"
	notFound: str = "HTTP/1.1 404 NOT FOUND"
	notAccepted: str = "HTTP/1.1 405 METHOD NOT ALLOWED"
	internalError: str = "HTTP/1.1 500 INTERNAL SERVER ERROR"
	server: str = "Server: Cthulhu/0.9.1"

#TODO: add ip and mac address, or address those in the tcp layer (serversocket.py) and report them somewhere (propably just store Client in Request as a client: Client)
#####: already exists in the Response but if an error occures in parsing or a warning the report will not contain the users ip and MAC 
@dataclass
class Request:
	"""Request object"""
	method: str
	endpoint: str
	ver: str
	headers: dict
	body: any
	tor: str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
	parse_body_bool: bool = False

	def __str__(self):
		return f"method: {self.method}, \nendpoint: {self.endpoint}, \nversion: {self.ver}, \nheaders: {self.headers}, \nbody: {self.body}, \ntime_of_request: {self.tor}"
	def __dict__(self):
		return { "method": self.method, "endpoint": self.endpoint, "version": self.ver, "headers": self.headers, "body": self.body, "time_of_request": self.tor}


	#TODO: Check (if i must check (if a header from a request is valid and if invalid may cause a vuln or bug i don't remember if i have it handled))
	#@staticmethod
	@classmethod
	def parse(self, request: str):
		try:
			requestList = request.replace('\r\n', '\n').split('\n')
			startLine = requestList.pop(0).split()
			headersEndIndex = requestList.index("")
			headersList = requestList[:headersEndIndex]
			headersDict = dict([tuple(i.split(": ")) for i in headersList if len(i) != 0])
			body = "".join(requestList[len(requestList[:headersEndIndex])::])
			
			#TODO: This is probably not required ill handle 0 length bodies in parser and parse on every type(or not(will see))
			if startLine[0] == "POST" and self.parse_body_bool:
				body = parse_body(headersDict, body)

			return Request(startLine[0], startLine[1], startLine[2], headersDict, body)
		except (IndexError, TypeError, ValueError):
			return False

#TODO: OverWriting the variable instead of upplying it as an argument everytime this makes the Request exist 2 times tho (will fix later) 
@dataclass
class Req(Request):
	parse_body_bool: bool = True



#TODO: Change all of it do not leave anything 
@dataclass
class Response:
	"""Response object"""
	client: Client
	headers: dict

	def __str__(self):
		return f"client_address: {self.client.address}\nheaders: {self.headers}"
	def __dict__(self):
		return { "client_address": self.client.address, "headers": self.headers}

	def send(self, data: str = None, accepted: bool = True):
		try:
			with self.client.connection as conn:
				conn.sendall(self.response(data, accepted))
		except OSError as e:
				print(f"Error sending data: {e}")
		except Exception as e:
				print(f"Unexpected error: {e}")


	def finalize_headers(self):
		NIY()
		return

	@staticmethod
	def response(data: str = None, accepted: bool = True):
		if(not accepted):
			return bytes(StaticHeaders.notAccepted + StaticHeaders.end, 'utf-8')
		if(data is None):
			content = "Content-Type: text/html; charset=utf-8"
			return bytes(f"{StaticHeaders.notFound}{StaticHeaders.nextH}{content}{StaticHeaders.nextH}{StaticHeaders.server}{StaticHeaders.end}", 'utf-8')
		
		content = f"Content-Type: text/html; charset=utf-8{StaticHeaders.nextH}Content-Length: {len(data)}"
		return bytes(f"{StaticHeaders.okay}{StaticHeaders.nextH}{content}{StaticHeaders.nextH}{StaticHeaders.server}{StaticHeaders.end}{data}", 'utf-8')



