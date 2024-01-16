# Cthulhu
## Is a webserver (Only For GET Requests)uwu

Modules used: `argparse, os, sys, asyncio, re, socket`

Usage: `python3 cthulhu.py -p <port_to_run_on> -s <project_directory>`

Test: `python3 cthulhu.py -p 8000 -s test`

Example url: `http://<ip>:<port>/index.html`

Clone with git: `git clone https://github.com/5skr0ll3r/Cthulhu`


## Explain 0.9:
In the current version we only get to see
`GET` being implemented for single static
files the version is 0.9 cause this is the 
most complete version until now the following 
updates will continue from 0.9.* and go on
until all methods are covered the ver/1 will
be pushed 

The wanted result is something like the nodejs express framework
where the syntax is simple and you can fast enough set everything up
and have a restfull server up and running.

So let's get started..

In order to create an app you will have to import the class
from `cthulhu` the main module.

To create the app object you simply call the __App()__ class constructor
with the desired port to listen on and the path of the sites directory

```python
app = App(8080,"/local/path/to/site/files")
```

## Available Methods of App:

`get()`

The __get()__ method takes 3 arguments in which only the 2 are required
Takes a __endpoint__, a __local_path__ and a __callback__ which is by default set to None

__Request__ and __Response__ will be provided to the callback if present

So how this works is, the endpoint get's registered to the application
when using any of the methods provided

```python
def get(self, endpoint, local_path, callback=None):
```

Working example having the test folder in the path
```python
import argparse
from sys import exit
from time import sleep
from classes.cthulhu import App


def args():
	ap = argparse.ArgumentParser(description="Local Site Hosting software (Public too if port forward)\n-p is for the port you wish to use to run the site to\n-s is for the psites folder path")
	ap.add_argument("-p", "--port", required=True, help="Port to Run on")
	ap.add_argument("-s", "--site",required=True, help="Path for Project")
	return vars(ap.parse_args())


def main():

	argv = args()

	app = App(int(argv['port']), argv["site"])

	try:
		app.get('/','index.html')
		app.listen()
	except KeyboardInterrupt:
		app.close()
		sleep(2)
		exit("Exited Successfully")

if __name__ == "__main__":
	main()
```

The main loop will begin by the time the listen() method of the app 
is called so add all endpoints above app.listen() or else they 
will not get registered
```python
def listen(self, callback=None):
	while True:
		client = self.sock.accept()
		_thread.start_new_thread(self.on_new_client,(client,))
```

# More coming SoOO0ooOOooooN



