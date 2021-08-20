import re,codecs

#Returns file name that GET's requested by client
def req_get_spliter(connection):
    print("module req_spliter re_get_spliter(connection) conn type is: ", type(connection))
    try:
        print("Try: ", connection)
        code = str(re.search('GET', connection).group())#codecs.decode(connection, 'UTF-8'))
        print("code is type: ", type(code))
    except AttributeError:
        print("AttributeError ", connection)
        code = str(re.search('GET', connection))
        print("code is type: ", type(code))
    if "GET" in code.split():
        print("Is GET request")
        try:
            link = str(re.search('/.+.\.html|/.+.\.css|/.+.\.js', connection).group())#codecs.decode(connection, 'UTF-8'))
        except AttributeError:
            link = str(re.search('/.+.\.html|/.+.\.css|/.+.\.js', connection))
        file = link.split("/")
        print("File is: ", file)
        for i in file:
            if ".css" in i or ".js" in i or "html" in i:
                return i
    return False





