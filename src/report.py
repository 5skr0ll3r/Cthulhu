from os import getcwd, mkdir, stat, listdir
from os.path import exists, isfile
from re import compile as rcompile, match
from threading import Lock
from src.utils import NIY, CSI, DNHE, NT, CNFF
import zipfile
from datetime import datetime
from src.datastructs import Request, Response
from json import loads, dumps

#TODO: Make Accessable from the App class (app.report())

#TODO: report navigation interface either host a web service and have a nodejs app running for the interface or have an offline tkinter interface or both
#TODO: add support for sqlite storage
#######TODO: ZIPS FULL PATH  Users/username/Desktop/Cthulhu/Cthulhu_ver_09.1/logs/log.log   Must Fix
#######TODO: ADD ERROR TYPES AND LEVELS(error on request, error on connection and report the raw data)
#TODO: add multiple file writing (one for errors, one for security reports, one for connections (all customizable, default will be one file for all) .etc....)
#############TODO: store in a var(boolean) if the logs folder existed, store a listdir() in an array if the folder exists and convert the array to only the indexes in the file_names sort it and do indexing based on that, do on __init__
#############TODO: add layers for def files and folders of report
################TODO: PROBABLY WILL BE REQUIREDTO BE GIVEN TO EVERY THREAD IN ORDER TO HANDLE ALL THE ERRORS WHICH WILL BE DONE IN THE cthulhu.py file
######TODO: Test with script if it logs correctly while sending many parallel requests using the `xargs` command with the flag `-P` and providing it with `curl`
class Log:
	def __init__(self, _name = None, _extension = None):
		#TODO: should propably use path (lib) for directory and file handling 
		print("MUSTDO FIX FOR: ZIPS FULL PATH  Users/username/Desktop/Cthulhu/Cthulhu_ver_09.1/logs/log.log")
		self.folder = "/logs/"

		if not _name : self.name = "log"
		else: self.name = _name
		if not _extension : self.extension = "log"
		else: self.extension = _extension

		self.file = self.name + "0." + self.extension
		self.max_size = 200 * 1024 * 1024 #size in bytes #Default 200mb
		self.cwd = getcwd()
		self.re = rcompile(r'log(\d+)\.log')
		self.zip_str = "log{}.zip"


		if(not exists(self.cwd + self.folder + "/")):
			mkdir(self.folder.strip("/"))

		self.log_folder_path = self.cwd + self.folder 
		self.current_full_path = self.log_folder_path + self.file
		self.log_files = listdir(self.log_folder_path)
		#If the folder is empty this will just return an empty list and if empty, the possible index_error that could occure gets handled in the get_next_index method which is also the only function reading data from this variable. If this changes and you read this please inform me 
		self.log_file_indexes = sorted(int(results.group(1)) for file in self.log_files if (results := self.re.match(file)))


		if len(self.log_files) == 0:
			with open(self.current_full_path, "w") as f:
				f.write("")

		#This is not a duplicate of the above cause check_last_file is then calling the check_size which calls new_name and this will generate a new file path that will be stored in the self.current_full_path by reset_file_name()
		if self.check_last_file():
			with open(self.current_full_path, "w") as f:
				f.write("")

		self.lock = Lock()

	#True, means it will use old file
	def check_last_file(self):
		try: #If the folder is empty it wil INDEX_ERROR when attempting to retrive the last value of the list bellow so this is my highway to hell of fixing it because i dont want to have another if statement
			#TODO: Check by size if a not empty file is actualy reused or not and then zipped
			tmp_last_file = self.log_folder_path + self.log_files[-1] 
			if not check_size(tmp_last_file):
				return True
			return False
		except:
			return False


	#TODO try/except for JSON dumps this will be only used in testing if else please inform me
	#self is not currently used but in order to later add log templates i imagine i will want to store the template inside the Log object and therefor constructor will require self
	#also if i dont add self it will not be in the Log `self` group and other methods in it, will not be able to access it  
	def contructor(self, request: Request = Request("","","",{},""), response: Response = Response("",{})):
		CSI()
		DNHE()
		now =  datetime.now()
		date_time = now.strftime("%d/%m/%Y %H:%M:%S")
		req, res = dumps(request.__dict__()), dumps(response.__dict__())
		#c_template for common template will be customizable by the dev or fully provided by them (some time in the future).
		c_template = {
			"report_time": f"{date_time}",
			"report_data": {
				"request": req,
				"response": res
			}
		}
		return dumps(c_template)

#If True then overweight, generate new name and file
	def check_size(self, file_path: str = None):
		DNHE()
		#TODO: Check if file_path is valid
		if file_path:
			file_size = stat(file_path).st_size
			if int(file_size) >= self.max_size:
				self.zip_file()
				self.new_name()
				return True
			return False	

		file_size = stat(self.current_full_path).st_size
		if int(file_size) >= int(self.max_size):
			self.zip_file()
			self.new_name()
			return True
		return False

	def get_next_index(self): #Happy to see that i already checked for index error here
		try:
			return self.log_file_indexes[-1] + 1
		except IndexError:
			return 1

	def new_name(self, index: int = None):
		if index:
			return f"{self.name}{index}.{self.extension}"
		next_index = self.get_next_index()
		self.log_file_indexes.append(next_index)
		self.file = f"{self.name}{next_index}.{self.extension}"
		return self.reset_file_name()

	def reset_file_name(self):
		self.current_full_path = self.log_folder_path + self.file
		return

	def zip_file(self):
		#TODO: Check if file already zipped
		#TODO: Before Zip sort by date the reports
		try:
			zip_name = f"{self.log_folder_path}{self.file.split(".")[0]}.zip"
			with zipfile.ZipFile(zip_name, mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zd:
				zd.write(self.current_full_path)
		except FileNotFoundError:
			CNFF(self.current_full_path)
		return

	def report(self, req: Request, res: Response):
		DNHE()
		NT()
		with self.lock:
			self.check_size()
			with open(self.current_full_path, "a") as f:
					f.write(self.contructor(req,res) + "\n")
			return





#seq 10 | xargs -n 1 -P 50 -I {} curl http://127.0.0.1:8000/
