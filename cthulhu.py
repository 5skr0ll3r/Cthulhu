import socket,threading,re,sys,os
import reqspliter as rs


hel = ("h", "help", "H", "HELP")


#Accepted methods by server
methods = ("GET","POST","HEAD","DELETE","CONNECT","PUT","OPTIONS","TRACE","PATCH")

#Accepted file extensions
file_ext = (".html",".css",".js")
imag_ext = (".ico",".jpeg",".png","jpg")

def requirements_check():
	if len(sys.argv) < 3:
		if len(sys.argv) == 1:
			sys.exit(f"Usage: {sys.argv[0]} <Port> <Project_Path>")
		if sys.argv[1] in hel:
			sys.exit(f"Usage: {sys.argv[0]} <Port> <Project_Path>\n\n<Port>: The port you want the server to communicate through\n<Project_Path>: The path to the directory index file is in\nExample: python3 {sys.argv[0]} 5444 www")
		else:
			sys.exit("Uknown Error Occured")
	else:
		pass


def read_file(Project_Path,req_file_path):
	file_path = Project_Path + req_file_path
	strip_path = file_path.strip()
	print(os.path.exists(strip_path))
	if os.path.exists(strip_path):
		print(f"File {strip_path} found")
		with open(strip_path) as op_file:
			code = op_file.read()
			op_file.close()
			return code
	else:
		print(f"File {strip_path} not found")




def connections_handler(connection,addr,Project_Path):
	print(f"=> {addr} Connected")
	active_connection = True

	while active_connection:
		
		if active_connection == False:
			break

		packet = connection.recv(3000)
		data = packet.decode('utf-8')
		print(f"Data received: \n\n{data}\n\n")

		req_type = rs.check_req_type(data,methods)
		if req_type != "False":
			req_file_path = rs.check_req_file_path(data,req_type)
			if req_file_path != "False":
				file_extension = rs.determine_file_ext_from_req(req_file_path,file_ext)
				if file_extension != "False":
					head_cont_type = rs.header_content_type(file_extension,imag_ext)

					print("Request Accepted")
					code = read_file(Project_Path,req_file_path)

					msg = connection.send(
                f"HTTP/1.1 200 OK\nConnection: Keep-Alive\nServer: Cthulhu/0.1\nContent-Type: {head_cont_type}; charset=utf-8\nKeep-Alive: timeout=5, max=1000\n\n{code}".encode())
					connection.close()
				else:
					connection.send("HTTP/1.1 404 NOT FOUND\nServer: Cthulhu/0.1".encode())
					connection.close()
			else:
				connection.send("HTTP/1.1 404 NOT FOUND\nServer: Cthulhu/0.1".encode())
				connection.close()
		else:
			connection.send("HTTP/1.1 404 NOT FOUND\nServer: Cthulhu/0.1".encode())
			connection.close()






#Main function
def start():

	requirements_check()

	HOST = socket.gethostbyname(socket.gethostname())
	PORT = int(sys.argv[1])
	Project_Path = sys.argv[2]

	#Create socket object bind with given vars and start listening
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.bind((HOST,PORT))
	s.listen()

	print(f"{HOST} Started listening on port: {PORT}")

#Will create a thread for every accepted connection so the server can be non-block
	while True:
		connection, addr = s.accept()
		thread = threading.Thread(target=connections_handler, args=(connection,addr, Project_Path))
		thread.start()
		print(f"=> Active connections {threading.activeCount() - 1}")


start()
