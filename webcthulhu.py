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

import os,sys,requests,socket,threading,re,codecs

#Checking if values are valid
def Check(args):
    if len(args) != 3:
        sys.exit("Usage: python3 <port> <project_folder>\n\nInside the project_folder the main file should be called\nindex.html or else it wont work for now.")

    if not os.path.isdir(args[2]):
        sys.exit("Dir does not exist")

    else: return True


error_msg = "<html><body><h1>Not Found</h1></body></html>"


#Checking if file exists to responce with 404 or 200 in the hundler function
def stat(folder, name):
    text = (folder + "/" + name)
    if os.path.exists(text):
        with open(text, "r") as ftext:
            html = ftext.read()
            ftext.close()
            return html
    return "False"



def req_spliter(conn):
    #Gets file name from GET request
    link = re.search('/.+\.html', codecs.decode(conn, 'UTF-8'))
    name = link.group()
    file = name.split("/")
    print(file)
    return file[1]


#Handles pretty much everything
def handler(conn,addr, folder):
    print(f"{addr} Connected")
    connected = True
    while connected:
        packet = conn.recv(1024)
        print(packet)
        file = req_spliter(packet)
        print(file)
        if stat(folder, file) != "False":
            conn.send(
                f"HTTP/1.1 200 OK\nConnection: Keep-Alive\nServer: Cthulhu/0.1\nContent-Type: text/html; charset=utf-8\nKeep-Alive: timeout=5, max=1000\n\n{stat(folder,file)}".encode())
            conn.close()
        else:
            conn.send(f"HTTP/1.1 404 Not Found\nServer: Cthulhu/0.1\nContent-Type: text/html; charset=utf-8\n\n{error_msg}".encode())
            conn.close()




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
    print(f"Listening on {HOST}")
    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=handler, args=(conn,addr, folder))
        thread.start()
        print(f"Active connections {threading.activeCount() - 1}")



start()
