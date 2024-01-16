from classes.datastructs import Response
from classes.datastructs import Request
from classes.filemanager import FileManager

class RequestHandler:

	@staticmethod
	def requestHandler(client, endpoints):
		data = client.connection.recv(3000).decode('utf-8')
		request = Request.parseRequest(data)

		if (request and request.method == "GET"):
			endpoints_match = [i for i in endpoints if i.method == "GET" and i.endpoint == request.endpoint]
			try:
				file_contents = FileManager.readFileContent(endpoints_match[0].local_path)
				response = Response.response(file_contents)
				client.connection.sendall(response)
				client.connection.close()
				return 
			except IndexError:
				response = Response.response()
				client.connection.sendall(response)
				client.connection.close()
				return
				
		else:
			response = Response.response("Method not supported")
			client.connection.sendall(response)
			client.connection.close()
			return
