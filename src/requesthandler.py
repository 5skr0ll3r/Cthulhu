from src.datastructs import Response, Request, Req, Endpoint, Client

#TODO: Revisit since i have a long time to do changes
class RequestHandler:
	@staticmethod
	def requestHandler(client: Client, endpoints: list[Endpoint], parse_body: bool = False):
		data = client.connection.recv(1024).decode('utf-8') #check if it auto handles chunks as i remember in c it wont so probably neither python
		if parse_body:
			request = Req.parse(data)
		else: 
			request = Request.parse(data)
			
		response = Response(client, {})
		if (request):
			try:
				endpointMatch = [i for i in endpoints if i.endpoint == request.endpoint][0]
				for func in endpointMatch.funcs:
					if func(request, response):
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
