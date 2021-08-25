import re


#Checks if method is valid/accepted
def check_req_type(request, methods):
	for i in methods:
		if i in request:
			print(f"Request Method: {i} is valid")
			return i
		else:
		 	return "False"


#Returns the requested path
def check_req_file_path(request, check_req_type):
	if check_req_type != "False":
		try:
			req_path = re.search("\/.+?.\s",request).group()
		except AttributeError:
			req_path = re.search("\/.+?.\s",request)
		print(f"Requested Path: {req_path}")
		return req_path
	else:
		return "False"


#Detects if requested file extension is accepted and returns it if accepted
def determine_file_ext_from_req(check_req_file_path, file_ext):
	if check_req_file_path != "False":
		for i in file_ext:
			if i in check_req_file_path:
				print(f"Extension {i} accepted")
				return i
	return "False"


def request_is_accepted(check_req_type, check_req_file_path, determine_file_ext_from_req):
	if check_req_type and check_req_file_path and determine_file_ext_from_req:
		return True 
	else: 
		return False


def header_content_type(file_ext):
	if file_ext == ".html":
		return "text/html"
	if file_ext == ".css":
		return "text/css"
	if file_ext == ".js":
		return "text/js"
	else:
		return "text/plain"
