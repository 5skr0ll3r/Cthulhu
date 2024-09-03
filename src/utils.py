from json import loads
import inspect

def validateFuncs(*funcs):
	for func in funcs:
		if(not callable(func) or not hasattr(func, '__call__')):
			raise TypeError (f"A callable function is expected as an argument not {func} a {type(func)}")


def index(endpoint: str ,endpoints: list):
	for index, ep in enumerate(endpoints):
		if ep.endpoint == endpoint:#Typo(3): endpoints
			return index
	return None


#https://stackoverflow.com/questions/23714383/what-are-all-the-possible-values-for-http-content-type-header
#https://www.iana.org/assignments/media-types/media-types.xhtml
def parse_body(headers: dict, body: str):
	DNHE()
	#TODO do more types and handle errors
	match headers["Content-Type"]:
		case "text/plain":
			return body
		case"application/json":
			return loads(body) #converts to dict
		case _:
			return body




#######TODO: Do these in a class and have a state variable to be or not to be enabled cause it get's on my nerves
#######Also: have a layer number and custom text  
#NotImplementedYet
def NIY():
	caller_frame = inspect.currentframe().f_back
	caller_name = caller_frame.f_code.co_name
	caller_info = inspect.getframeinfo(caller_frame)
	print(f"Function: {caller_name} is not implemented yet")
	print(f"Called from {caller_info.filename}, line {caller_info.lineno}")

#ContainsSecurityIssues
def CSI():
	caller_frame = inspect.currentframe().f_back
	caller_name = caller_frame.f_code.co_name
	caller_info = inspect.getframeinfo(caller_frame)
	print(f"Function: {caller_name} is not secure yet, be conscious while using it")
	print(f"Called from {caller_info.filename}, line {caller_info.lineno}")


#DoesNotHandleErrors
def DNHE():
	caller_frame = inspect.currentframe().f_back
	caller_name = caller_frame.f_code.co_name
	caller_info = inspect.getframeinfo(caller_frame)
	print(f"Any Errors caused by: {caller_name} are not yet either handled correctly or not at all")
	print(f"Called from {caller_info.filename}, line {caller_info.lineno}")


#NotTested
def NT():
	caller_frame = inspect.currentframe().f_back
	caller_name = caller_frame.f_code.co_name
	caller_info = inspect.getframeinfo(caller_frame)
	print(f"Function: {caller_name} has not been tested")
	print(f"Called from {caller_info.filename}, line {caller_info.lineno}")


#Could Not Find File
def CNFF(file_name: str):
	caller_frame = inspect.currentframe().f_back
	caller_info = inspect.getframeinfo(caller_frame)
	print(f"Could not find file: {file_name}")
	print(f"Called from {caller_info.filename}, line {caller_info.lineno}")