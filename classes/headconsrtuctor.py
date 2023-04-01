class Headers:
	nextH = "\r\n"
	end = "\r\n\r\n"
	okay = "HTTP/1.1 200 OK"
	notFound = "HTTP/1.1 404 NOT FOUND"
	internalError = "HTTP/1.1 500 INTERNAL SERVER ERROR"
	server = "Server: Cthulhu/0.5"

	def header(accepted, data, contentType):
		if(accepted and data and "image" in contentType):
			return bytes(Headers.okay + Headers.nextH + f"Content-Type: {contentType}" + Headers.nextH + f"Content-Length: {len(data)}" + Headers.nextH + Headers.server + Headers.end,'utf-8') + data
		elif(accepted and data):
			return bytes(Headers.okay + Headers.nextH + f"Content-Type: {contentType}" + Headers.nextH + f"Content-Length: {len(data)}" + Headers.nextH + Headers.server + Headers.end + data, 'utf-8')
		elif (accepted and not data):
			return bytes(Headers.notFound + Headers.nextH + f"Content-Type: {contentType}" + Headers.nextH + Headers.server + Headers.end, 'utf-8')
		else:
			return bytes(Headers.internalError + Headers.end, 'utf-8')