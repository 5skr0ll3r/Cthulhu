'''
MIT License
Copyright (c) 2021 5skr0ll3r
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import os,sys,requests,socket,threading,re,codecs,mimetypes
import req_spliter as rs

#Checking if values are valid
def Check(args):
    if len(args) != 3:
        sys.exit("Usage: python3 <port> <project_folder>\n\nInside the project_folder the main file should be called\nindex.html or else it wont work for now.")

    if not os.path.isdir(args[2]):
        sys.exit("Dir does not exist")

    else: return True


error_msg = "<html><body><h1>Not Found</h1></body></html>"



def headcr():
    if os.path.exists("conf/head.txt"):
        pass


#checks for file extension from get request
def extcheck(connection):
    print("=> Connection in extcheck equals: ", connection)
    if rs.req_get_spliter(connection) != "False":
        print("=> extcheck runned :" ,rs.req_get_spliter(connection))
        return str(rs.req_get_spliter(connection))

    return "False"



#Checking if file exists to responce with 404 or 200 in the hundler function
def stat(folder, file_name):
    text = (str(folder) + "/" + str(file_name))
    print("=> Final path: ",file_name)
    if os.path.exists(text):
        with open(text) as ftext:
            html = ftext.read()
            ftext.close()
            return html
    print("=> def stat outs False")
    return "False"



#Handles pretty much everything
def handler(connection,addr, folder):
    print(f"=> {addr} Connected")
    active = True
    while active:
        if connection == False:
            break
        packet = connection.recv(1024)
        deccon = packet.decode('utf-8')
        print("=> DECCON =========> ", deccon, "\n\n\n deccon is type: ", type(deccon), "\n\n\n")

        file_name = extcheck(deccon)
        print("=> file_name = extcheck(deccon) file_name is type: ",type(file_name))
        
        print("=> Output of rs.req_get_spliter(deccon): ", rs.req_get_spliter(deccon))
        exten_f_req = rs.extdetect(rs.req_get_spliter(deccon))

        #mimetype, _ = mimetypes.guess_type(file_name)
        print("=> Header for file is: ", exten_f_req)

        if stat(folder, file_name) != "False":# and extcheck(file_name) != "False":
            print("=> 200 Ok")
            connection.send(
                f"HTTP/1.1 200 OK\nConnection: Keep-Alive\nServer: Cthulhu/0.1\nContent-Type: {exten_f_req}; charset=utf-8\nKeep-Alive: timeout=5, max=1000\n\n{stat(folder,file_name)}".encode())
            connection.close()
        else:
            print("=> 404 Not Found")
            print("\n\n\n\n\nstat: ",stat(folder, file_name), "\n\nextcheck: ",extcheck(file_name) )
            connection.send(f"HTTP/1.1 404 Not Found\nServer: Cthulhu/0.1\nContent-Type: text/html; charset=utf-8\n\n{error_msg}".encode())
            connection.close()




def start():

    Check(sys.argv)

    HOST = "127.0.0.1"
    PORT = int(sys.argv[1])
    folder = (sys.argv[2])

    print(HOST)
    print(PORT)
    print(folder)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))

    s.listen()
    print(f"=> Listening on {HOST}")
    while True:
        connection, addr = s.accept()
        thread = threading.Thread(target=handler, args=(connection,addr, folder))
        thread.start()
        print(f"=> Active connections {threading.activeCount() - 1}")



start()
