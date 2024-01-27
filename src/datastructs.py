from dataclasses import dataclass
from socket import socket
import logging

@dataclass
class Client:
	"""Client object"""
	address: str
	connection: socket

@dataclass
class Endpoint:
	"""Endpoint Object"""
	method: str
	endpoint: str
	callbacks: any


@dataclass
class StaticHeaders:
	nextH: str = "\r\n"
	end: str = "\r\n\r\n"
	okay: str = "HTTP/1.1 200 OK"
	notFound: str = "HTTP/1.1 404 NOT FOUND"
	notAccepted: str = "HTTP/1.1 405 METHOD NOT ALLOWED"
	internalError: str = "HTTP/1.1 500 INTERNAL SERVER ERROR"
	server: str = "Server: Cthulhu/0.9"


@dataclass
class Request:
	"""Request object"""
	method: str
	endpoint: str
	ver: str
	headers: dict
	body: str

	def __enter__(self):
		return self
	def __exit__(self, exc_type, exc_value, exc_traceback):
		return 


	@staticmethod
	def parseRequest(request: str):
		try:
			requestList = request.split("\r\n")
			startLine = requestList.pop(0).split()
			headersEndIndex = requestList.index("")
			headersList = requestList[:headersEndIndex]
			headersDict = dict([tuple(i.split(": ")) for i in headersList if len(i) != 0])
			body = "".join(requestList[len(requestList[:headersEndIndex])::])
			print(body)
			#TODO: add parse body on Content-Type
			return Request(startLine[0], startLine[1], startLine[2], headersDict, body)
		except (IndexError, TypeError, ValueError):
			return False


@dataclass
class Response:
	"""Response object"""
	client: Client

	def send(self, data: str = None, accepted: bool = True):
		try:
			with self.client.connection as conn:
				conn.sendall(self.response(data, accepted))
		except OSError as e:
				logging.info(f"Error sending data: {e}")
		except Exception as e:
				logging.info(f"Unexpected error: {e}")


	@staticmethod
	def response(data: str = None, accepted: bool = True):
		if(not accepted):
			return bytes(StaticHeaders.notAccepted + StaticHeaders.end, 'utf-8')
		if(data is None):
			content = "Content-Type: text/html; charset=utf-8"
			return bytes(f"{StaticHeaders.notFound}{StaticHeaders.nextH}{content}{StaticHeaders.nextH}{StaticHeaders.server}{StaticHeaders.end}", 'utf-8')
		
		content = f"Content-Type: text/html; charset=utf-8{StaticHeaders.nextH}Content-Length: {len(data)}"
		return bytes(f"{StaticHeaders.okay}{StaticHeaders.nextH}{content}{StaticHeaders.nextH}{StaticHeaders.server}{StaticHeaders.end}{data}", 'utf-8')



