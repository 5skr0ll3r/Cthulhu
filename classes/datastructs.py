from dataclasses import dataclass
from socket import socket

@dataclass
class Client:
	"""Client object"""
	address: str
	connection: socket


@dataclass
class Request:
	"""Request object"""
	method: str
	endpoint: str
	ver: str
	headers: dict
	data: str

	@staticmethod
	def parseRequest(request):
		request_list: list = request.split("\r\n")
		head: list = request_list.pop(0).split(" ")
		#A Dictionary in python is a list of tuples so by creating a list 
		#consisting of tuples we can then convert it directly to a dictionary
		#TODO: some check for invalidc header when containing ": " twice in a line 
		#will split and trash the dictionary
		headers_dict : dict = dict([tuple(i.split(": ")) for i in request_list if len(i) != 0])
		data: str = None
		try:
			return Request(head[0], head[1], head[2], headers_dict, data)
		except IndexError:
			return False


@dataclass
class Response:
	"""Response object"""
	status: int
	json: dict
	nextH: str = "\r\n"
	end: str = "\r\n\r\n"
	okay: str = "HTTP/1.1 200 OK"
	notFound: str = "HTTP/1.1 404 NOT FOUND"
	internalError: str = "HTTP/1.1 500 INTERNAL SERVER ERROR"
	server: str = "Server: Cthulhu/0.5"


	@staticmethod
	def response(data=None, accepted=True):
		if(accepted and data):
			return bytes(Response.okay + Response.nextH + f"Content-Type: text/html; charset=utf-8" + Response.nextH + f"Content-Length: {len(data)}" + Response.nextH + Response.server + Response.end + data, 'utf-8')
		elif (accepted and not data):
			return bytes(Response.notFound + Response.nextH + f"Content-Type: text/html; charset=utf-8" + Response.nextH + Response.server + Response.end, 'utf-8')
		else:
			return bytes(Response.internalError + Response.end, 'utf-8')



@dataclass
class Endpoint:
	"""Endpoint Object"""
	method: str
	endpoint: str
	local_path: str
	callback: any



