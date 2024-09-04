# Cthulhu
## Is a webserver

Usage: `python3 cthulhu.py -i <interface> -p <port>`

Example url: `http://<ip>:<port>/index.html`

Clone with git: `git clone https://github.com/5skr0ll3r/Cthulhu`


## Explain 0.9.1:
Current Version can only serve one file so external css, js, images ...etc 
are still not supported.

So let's get started..

# App:

In order to create an app you will have to import the class
from `cthulhu` the main module.

To create the app you simply call the __App()__ class constructor
with the desired interface and port to listen on 

```python
app = App("127.0.0.1", 8080)
```


## Route:

In order to register an endpoint to the app you just use the `route()` wrapper
```python
@app.route("/")
def index(req: Request, res: Response):
	with open("sample_site/index.html", "r") as file:
		print(req)
		return res.send(file.read())
```
The __route()__ takes 2 positional arguments the __path__ for the endpoint
and a list of allowed methods for the api `["GET","POST",....]`

Any method supplied to the wrapper will be provided with the Request and Response objects

### Request:
The Request object contains the following data after the original request is parsed
```
	method: str
	endpoint: str
	ver: str
	headers: dict
	body: any
	tor: str = datetime.now().strftime("%d/%m/%Y %H:%M:%S") #Time of request
```

#### Note:
By default the app wont parse the body of any request so in order to enable parsing
after initiating the app call the `parse_req_body()`

### Response:
The Response object contains only the `client: Client` data which itself
has the folowing data:
```
	address: str
	connection: socket
```

All callbacks will be provided with the __Request__ and __Response__  objects, here is an example
```python
import argparse, sys
from time import sleep
from src.cthulhu import App
from src.datastructs import Request, Response
from src.report import Log


def args():
	ap = argparse.ArgumentParser(description="HTTP/1 Server\n-i interface to listen on\n-p port to listen on\n")
	ap.add_argument("-i", "--interface", required=False, help="Interface to run on")
	ap.add_argument("-p", "--port", required=True, help="Port to run on")
	return vars(ap.parse_args())


argv = args()
app = App(argv['interface'], int(argv['port']))
log = Log()

app.parse_req_body()

@app.route("/")
def before_index(req: Request, res: Response):
	return True

@app.route("/")
def index(req: Request, res: Response):
	with open("sample_site/index.html", "r") as file:
		print(req)
		return res.send(file.read())


@app.route("/test")
def test(req: Request, res: Response):
	return res.send("test")

@app.route("/sec")
def validate(req: Request, res: Response):
	if ("Referer" in req.headers and "127.0.0.1:8000" in req.headers["Referer"]):
		return True
	res.send("Not Allowed sorry")
	log.report(req,res)
	return False

@app.route("/sec")
def sec(req: Request, res: Response):
	return res.send("Secret")

print(app.endpoints)


try:
	app.listen()

except KeyboardInterrupt:
	app.close()
	sleep(2)
	sys.exit("Exited Successfully")

```

## Middlewares: 

In the future you will be able to use the `use()` method of App, which will register middlewares
for now you can achieve this behaviour by implementing a function that will do any check you want
like the example above, the `/sec` endpoint on request will first run the `validate` function which
checks if a specific header is present and if so it returns `True` it then proceeds to call the `sec()`
method that will respond with `Secret`

If the middleware returns `False` for any reason, the app will discontinue the execution of the rest middlewares 
and final repsonse if the dev already provided a response for the case
of `False` an error will apear from the `requesthandler` module `Error sending data: [Errno 9] Bad file descriptor` because it will 
attempt to send by default a 405 response although the connection has already close which i have to fix 

### Note:
Registered functions in the app for a single API will run in a FIFO style (First in First out)
so register all middlewares carefully


## Listen:
The main loop will begin by the time the listen() method is called
```python
app.listen()
```
so add all endpoints above app.listen() or else they 
will not be registered and there for not run


## Close:
To 'safely' close the app you can call the `close()` method
which will attempt to end all active connections if any, 
will wait for the threads to end their tasks and then close



