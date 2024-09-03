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


