Chtulhu.py: When pasing to header function accesable from Header object i pass data first to varible self.data and then to the function to see if data exists so the request can procced
fix:pass directly to the header() method so i don't have to create every time an instance of the Header object 


ReqSpliter: when reterning path i regex out the "/" so i manually put it for the file manager to work
else the user input on command should have the / to be saved in projectFolderPath 
fix: automate the process with a simple check

Cthulhu: get: move almost everything into a controller for cleaner code


Tree: insertArray: check if item already exists in existant tree


Every sock request from each client should be stored in an array
cause the asyncio interferes with the processing of each
sock should also not be async


with asyncio a task should be created for every request made to actually be asyncronous The task should contain{
	sock,filemanager,reqspliter 
}and be implimented in the controller and then invoked in the cthulhu.py


XD damn asynchronous functionality... or so i thought have to rewrite
For each hardcoded awaited request create a thread instead to wait for it
in order to achieve a non block experience

===================================
# Fixed:

reqSpliter: prep2: remake regex


ReqSpliter: method: dataPrep() the splitedList online returns the first element of the actuall list
Fix: change name



# Snippets i want to remember
```
if(not(os.path.exists(_projectFolderPath) and (self.projectFolderPath := _projectFolderPath))):
			sys.exit("Path is not valid")
```
```
if(not(self.request and (self.request := request))):
			sys.exit("Path is not valid")
```
