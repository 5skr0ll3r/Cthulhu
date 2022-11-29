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




