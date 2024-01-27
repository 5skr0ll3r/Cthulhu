from src.datastructs import Response, Request, Endpoint, Client


class RequestHandler:

	@staticmethod
	def requestHandler(client: Client, endpoints: list[Endpoint]):
		data = client.connection.recv(1024).decode('utf-8')
		request = Request.parseRequest(data)
		response = Response(client)
		print(data)
		if (request and request.method == "GET"):
			try:
				endpointMatch = [i for i in endpoints if i.method == "GET" and i.endpoint == request.endpoint][0]
				for callback in endpointMatch.callbacks:
					if callback(request, response):
						continue
					else:
						response.send()
						break
				return
			except (IndexError, OSError):
				response.send(accepted = False)
				return
		else:
			response.send(accepted = False)
			return
