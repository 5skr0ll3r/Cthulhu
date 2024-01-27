import argparse, sys
from time import sleep
from src.cthulhu import App
from src.datastructs import Request, Response


def args():
	ap = argparse.ArgumentParser(description="Site Hosting software\n-i interface to listen on\n-p port to listen on\n")
	ap.add_argument("-i", "--interface", required=False, help="Interface to run on")
	ap.add_argument("-p", "--port", required=True, help="Port to run on")
	return vars(ap.parse_args())


def index(req: Request, res: Response):
	with open("sample_site/index.html") as file:
		return res.send(file.read())

def callbackOne(req: Request, res: Response):
	return True

def callbackTwo(req: Request, res: Response):
	return res.send("test")

def callbackThree(req: Request, res: Response):
	if ("Referer" in req.headers and "http://127.0.0.1:8000/" in req.headers["Referer"]):
		return True
	res.send("Not Allowed sorry")
	return False

def callbackFour(req: Request, res: Response):
	return res.send("Secret")


def main():
	argv = args()
	#App initiation
	app = App(argv['interface'], int(argv['port']))
	try:
		#Registering the api's and listening
		app.get('/', index)
		app.get('/call', callbackOne, callbackTwo)
		app.get('/sec', callbackThree, callbackFour)
		app.listen()

	except KeyboardInterrupt:
		app.close()
		sleep(2)
		sys.exit("Exited Successfully")

if __name__ == "__main__":
	main()
