import argparse, asyncio,sys
from time import sleep
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
		try:
			await app.get('/','index.html')

		except KeyboardInterrupt:
			app.sock.close()
			sleep(2)
			sys.exit("Exited Successfully")

if __name__ == "__main__":
	asyncio.run(main())




