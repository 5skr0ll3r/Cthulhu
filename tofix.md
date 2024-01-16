
make a daemon that will list all incoming connections and then serve them
in a fifo order 


on final from each lib only import used methods for optimization

Cthulhu: get: move almost everything into a controller for cleaner code

checkReqType() in reqspliter.py should not return a boolean if reqType not found


The Sock object should accept and recieve without having to be awaited in every method 
cause the server wont be able to serve the client any other than the first 
specified request by the developer, create a deamon thread that will handle each request 
and send it to the right handler

create a request error handler and a logger

add a timeout if the client does not request the rest of the files that are cached

create a renderer that shall read the files and if they extra constructs them and then serve them to the client

have to somehow close connections
recursive get and render href's to client


when requested file is from local cache search and compare by name to remove it

with asyncio a task should be created for every request made to actually be asyncronous The task should contain{
	sock,filemanager,reqspliter 
}and be implimented in the controller and then invoked in the cthulhu.py

move Headers from frapitska and create a stand alone module for header construction

XD damn asynchronous functionality... or so i thought have to rewrite
For each hardcoded awaited request create a thread instead to wait for it
in order to achieve a non block experience

===================================
# Fixed:

Chtulhu.py: When pasing to header function accesable from Header object i pass data first to varible self.data and then to the function to see if data exists so the request can procced
fix:pass directly to the header() method so i don't have to create every time an instance of the Header object (make static)

reqSpliter: prep2: remake regex

make most objects static so i dont have to handle so much instances every time

change determineFileExtFromReq(), headerContentType() in reqSpliter should not check the file requested, cause from now they 
will be alliased and instead read the files name when specified by the dev, so move them instead to the fileManager

Tree: insertArray: check if item already exists in tree

Convert request headers to dictionary for easy access

ReqSpliter: method: dataPrep() the splitedList online returns the first element of the actuall list
Fix: change name

create client object with connection, address, request

right now dev wont be able to have a secondary file path with any "/" have to fix it later

ReqSpliter: when reterning path i regex out the "/" so i manually put it for the file manager to work
else the user input on command should have the / to be saved in projectFolderPath 
fix: automate the process with a simple check


# Snippets i want to remember
```
if(not(os.path.exists(_projectFolderPath) and (self.projectFolderPath := _projectFolderPath))):
			sys.exit("Path is not valid")
```
```
if(not(self.request and (self.request := request))):
			sys.exit("Path is not valid")
```
