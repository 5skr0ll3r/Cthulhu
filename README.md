# Cthulhu
## Is a webserver (Only For GET Requests)uwu

Modules used: `argparse, os, sys, asyncio, re, socket`

Usage: `python3 cthulhu.py -p <port_to_run_on> -s <project_directory>`

Test: `python3 cthulhu.py -p 8000 -s test`

Example url: `http://<ip>:<port>/index.html`

Clone with git: `git clone https://github.com/5skr0ll3r/Cthulhu`


## Explain 0.6:

In the current version we only get to see
`GET` being poorly implemented
cause of the knowledge i had at that 
time.

The wanted result is something like the nodejs express framework
where the syntax is simple and you can fast enough set everything up
and have a restfull server up and running.

So let's get started..

In order to create an app you will have to import the class
from `cthulhu` the main module .

To create the app object you simply call the __App()__ class constructor
with the desired port to listen on and the path of the sites directory
```python
app = App(8080,"/tmp/site")
```
uppon initiation the app will also create 4 more objects which will be discussed later on.

## Available Methods of App:

`get()`

The __get()__ method takes 3 arguments in which only the 2 are required
Takes a __name__, a __path__ and a __function__ which is by default set to None
```python
async def get(self, name, path, inFunc = None):
```
`name` is the alias for the file you want to be accesed when it is requested
It is also stored and used in the `cache` which is a Tree object
```python
self.cache = Tree()
```

Propably working example having the test folder in the path
```python
import argparse, asyncio
from classes.cthulhu import App


def args():
	ap = argparse.ArgumentParser(description="Local Site Hosting software (Public too if port forward)\n-p is for the port you wish to use to run the site to\n-s is for the psites folder path")
	ap.add_argument("-p", "--port", required=True, help="Port to Run on")
	ap.add_argument("-s", "--site",required=True, help="Path for Project")
	return vars(ap.parse_args())



async def main():

	argv = args()

	app = App(int(argv['port']), argv["site"])

	while True:
		await app.get('index', 'index.html')

		await app.get('about','about.html')

		await app.get('download','download.jpeg')


	app.sock.close()

if __name__ == "__main__":
	asyncio.run(main())
```

In order for the __Sock__ object to accept any incoming requests and recieve data, request
```python
	def __init__(self, _port, _projectFolderPath):
			#checking if port is an intiger
			if(not isinstance(_port,int)):
				sys.exit("Port Must Be an Integer")
			#checking if path exists and if yes storing it in sitePath using the walrus operator
			if(not(os.path.exists(_projectFolderPath))):
				sys.exit("Path is not valid")

			self.sock = Sock(_port)
			self.projectFolderPath = _projectFolderPath
			self.reqSpliter = ReqSpliter()
			self.fileManager = FileManager(self.projectFolderPath)
			self.cache = Tree()
		 -> self.request = None <-
			self.sock.run()
```
has to be `None` or else the `request` stored in it get's processed by the __ReqSpliter (Request Spliter)__
starting with the __dataPrep()__ method
```python
isAccepted, splitedZero, requestType, fileRequested, fileExtension, conType = self.reqSpliter.dataPrep(self.request) 
```
__dataPrep()__ is the sum of all the available functionality of __ReqSpliter__ which is (yeah names == functionallity XD):

* spliter(request)
* checkReqType(requestList)
* checkReqFilePath(requestList)
* determineFileExtFromReq(requestList)
* headerContentType(checkReqFilePath)
* requestIsAccepted(checkReqType, checkReqFilePath, determineFileExtFromReq)
* dataPrep(request)

__spliter()__ Splits the request Headers in every new line and returns a __List of Strings__ so i can parse them easier
__checkReqType()__ Checks the type of the request (GET,POST,PUT,etc..) and returns True if the method is accepted else False
__determineFileExtFromReq()__ Determines the requested File's extension to see if it is allowed and to help determine the correct __Content-Type__ later returns a __String__
__checkReqFilePath()__ Determines the path for the file requested and returns a __String__
__headerContentType()__ Uses the extracted file extension to first see if it is an image or text and then return the correct __Content-Type__
__requestIsAccepted()__ Checks the return of __checkReqType__, __checkReqFilePath__ and __determineFileExtFromReq__ and returns a bool
__dataPrep()__ Returns a everything said above

Some regex is also compiled in the initialization in order to parse the requests faster.
```python
	def __init__(self):
		self.methods = ("GET","POST","HEAD","DELETE","CONNECT","PUT","OPTIONS","TRACE","PATCH")
		self.fileExt = ("html","css","js")
		self.imageExt = ("jpeg","png","jpg","ico")
		self.regSplit = re.compile(".+.\n")
		self.regMethod = re.compile("[A-Z]+\S")
		self.regFileName = re.compile('[a-zA-Z]+\.[a-zA-Z]+')
```

After the __request__ get's parsed the method type is checked and then if the third argument in the __get()__ method is still __None__
if it isn't the the request get's passed to it and you do you, from this point you are alone XD.

If __None__, __FileManager__ is used to read and parse the file requested

* readFileContent()
* parserHTML()

__readFileContent(path)__ Reads the file depending of the type (image/txt) either reads as bytes or just a simple read and returns the content
__parserHTML(fileContent)__ Reads the content and using the precompiled regex shown bellow retrieves the contents of src and href attributes and returns a list  

```python
	def __init__(self,_projectFolderPath):
		self.projectFolderPath = _projectFolderPath
		self.srcFind = re.compile('src=[\"|\'].*[\"|\'] ')
		self.hrefFind = re.compile('href=[\"|\'].*[\"|\']')
		self.li = re.compile('[\"|\'].*[\"|\']')
		#self.spliter = re.compile('[\"|\']')
		self.FileName = re.compile('[a-zA-Z]+\.[a-zA-Z]+')
```

Later on the __get()__ method after the files have been parsed i insert in the cache the file structure discovered by this request
using the __Tree__ object

This is usefull cause this way you wont have to reparse the files
cause when index.html is requested the paths have already being verified
and stored in the 'cache' saving time 

__Tree()__ is a 3 layer tree where the structure lookes like this
```
						__ /css/master.css
					   |
		 __ index.html-
		 |			   |__ /js/master.js
		 |
	root--- about.html -- /css/master2.css
		 |
		 |
		 -- some.html

```
on initialization we set the name of the tree default is __root__

* exists(name)
* isEmpty()
* addChild(node)
* getIndex(name)
* getValues(name)
* printTree()
* insertArray(fileRequested, array)

__exists()__ Checks if file is already register and returns a bool
__isEmpty()__ Checks if the Tree is empty and returns a bool
__addChild()__ First checks if the node you try to append to the tree has a Tree like structure and either appends or returns False
__getIndex()__ Finds the index of the main/node (html) file by name and returns an int else False
__getValues()__ Returns a list of the files under the main/node (html) file
__printTree()__ Prints the whole tree for debugging
__insertArray()__ Either Adds a whole Node to the Tree or if the main file already exists just appends the subfiles and returns bool

Tree creation sample
```python
	t = Tree('files', [
			Tree('index',[
				Tree('index.js'),
                Tree('index.css')
				]),
            Tree('about',[
            	Tree('about.js'),
                Tree('about.css')
                ]),
            Tree('login', [
            	Tree('log.js'),
                Tree('log.css')
                ])
            ])
```

Now we get to the frapitska module which holds the __Headers__ and __Sock__

__Sock__ is for handling the connections

* run()
* accept()
* receive()
* respond(data)
* close()

__run()__ Sets up the socket.socket object binds the host and the port and starts listening
__accept()__ Accepts incoming connections
__receive()__ Receives and returns the data as a String
__respond()__ Sends the data 
__close()__ Emptys the self.socket object

The __Headers__ is used to format the data that will be sent to the client containing only
one method currently 

* header(accepted,exists)

__header()__ checks if the request is accepted and if the file exists to determine the status code and what to send





