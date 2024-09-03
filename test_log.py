
#python3 test_log.py | grep threads
from src.report import Log
import threading
logger = Log()
threads = list()
data = "testing{}\n"

while True:
	for i in range(30):
		#data = format(data)"testing{i}\n"
		x = threading.Thread(target=logger.report, args=(data.format(i),))
		threads.append(x)
		x.start()
	for index, thread in enumerate(threads):
		#print("waiting for threads to finish")
		thread.join()
		#print("threads finished")
