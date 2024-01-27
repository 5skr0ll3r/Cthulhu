# Cthulhu
## Is a webserver (Only For GET Requests)uwu

Usage: `python3 file.py -i <interface> -p <port_to_run_on> `

Test: `python3 server.py -i 127.0.0.1 -p 8000`

Example url: `http://<ip>:<port>/`

Clone with git: `git clone https://github.com/5skr0ll3r/Cthulhu`


## Explain 0.9.1:
In the current version we only get to see
`GET` being implemented for stand alone static
files, the version is 0.9 cause this is the 
most complete version until now the following 
updates will continue from 0.9.* and go on
until all methods are covered then version 1 will
be pushed 

The wanted result is something like the nodejs express framework
where the syntax is simple and you can fast enough set everything up
and have a restfull server up and running.

So let's get started..

## App:

In order to create an app you will have to import the class
from `cthulhu` the main module.

To create the app you simply call the __App()__ class constructor
with the desired interface and port to listen on 

```python
app = App("127.0.0.1", 8080)
```

## Available Methods of App:

`get()`

The __get()__ method takes as many arguments as you want, the first argument is the __endpoint__, and the rest are __callbacks__ 
in which you can add tests for the specific endpoint, or just serve a page when a request on that endpoint is made
```python
def get(self, endpoint, *callbacks):
```

All callbacks will be provided with the __Request__ and __Response__  objects, here is an example
```python
import argparse, sys
from time import sleep
from src.cthulhu import App
from src.filemanager import FileManager
from src.datastructs import Request, Response


def args():
	ap = argparse.ArgumentParser(description="Site Hosting software\n-i interface to listen on\n-p port to listen on\n")
	ap.add_argument("-i", "--interface", required=False, help="Interface to run on")
	ap.add_argument("-p", "--port", required=True, help="Port to run on")
	return vars(ap.parse_args())

def index(req: Request, res: Response):
	with open("sample_site/index.html", "r") as file:
		return res.send(file.read())


def callbackThree(req: Request, res: Response):
	if ("Referer" in req.headers and "http://127.0.0.1:8000/" in req.headers["Referer"]):
		return True
	res.send("Not Allowed sorry")
	return False

def callbackTwo(req: Request, res: Response):
	return res.send("Secret")

def main():
	argv = args()
	app = App(argv['interface'], int(argv['port']))
	try:

		app.get('/', index)
		app.get('/sec', callbackOne, callbackTwo)
		app.listen()

	except KeyboardInterrupt:
		app.close()
		sleep(2)
		sys.exit("Exited Successfully")

if __name__ == "__main__":
	main()
```

In the above example we have two endpoints registered, when someone requests the path "/"
the index page will show up. On the "/sec" path the request has to contain a specific header
in order to proceed and if the criteria is not met then it will respond with a not found

__Note: the callbacks will run in a FIFO (Firtst in First Out) style, so if let's say the callbackOne() in the above example 
was to respond to the request by `res.send()` then callbackTwo would not run__

So how this works is, the endpoint get's registered to the application
when using any of the methods provided by the __App__ Class

The main loop will begin by the time the listen()
```python
def listen(self):
```
 method of the app 
is called, so add all endpoints above app.listen() or else they 
will not be registered and there for not run


# More coming SoOO0ooOOooooN



