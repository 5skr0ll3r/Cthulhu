import re,codecs

#Returns file name that GET's requested by client
def req_get_spliter(connection):
    print("module req_spliter re_get_spliter(connection) conn type is: ", type(connection))
    code = re.search('GET', codecs.decode(connection, 'UTF-8'))
    req = code.group()
    if "GET" in req:
        print("Is GET request")
        link = re.search('/.+.\.html|/.+.\.css|/.+.\.js', connection)#codecs.decode(connection, 'UTF-8'))
        name = link.group()
        file = name.split("/")
        print("File is: ", file)
        for i in file:
            if ".css" in i or ".js" in i or "html" in i:
                return i
    return False

