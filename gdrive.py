from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from queue import SimpleQueue
import textract


def isPdf(f):
	if 'mimeType' in f:
		if f['mimeType']=='application/pdf':
			return True
	return False		
def isDoc(f):
	if 'mimeType' in f:
		if f['mimeType']=='application/vnd.openxmlformats-officedocument.wordprocessingml.document':
			return True
	return False		

def isFolder(f):
	if 'mimeType' in f:
		if f['mimeType']=='application/vnd.google-apps.folder':
			return True
	return False

def getList(drive, folderid):
	#folderid='0B0Rlpx3MRZ1SLVFXRFctd0t1cDA'
	value="'%s' in parents and trashed=false" % (folderid )
	obj={'q':value}
	fileList = drive.ListFile(obj).GetList()
	return fileList

def process(drive):
	while not q.empty():
		id=q.get()
		lst=getList(drive,id)
		for x in lst:
			files[x['id']]=x
			if isFolder(x):
				q.put(x['id'])

def get_files(files):
	pdfs=[]
	docs=[]
	for key,value in files.items():
		if isPdf(value):
			pdfs.append(key)	
		if isDoc(value):
			docs.append(key)
	return (pdfs,docs)			

def get_title(id):
	str=""
	if id not in files: 
		return ""
	o=files[id]
	parent_title=""
	if 'parents' in o:
		if len(o['parents']) >= 1:
			pid=o['parents'][0]['id']
			parent_title=get_title(pid)
	str= parent_title + o['title']
	return str 

def get_doc_text(f):
	filename=""
	if isPdf(f):
		filename="a.pdf"
	if isDoc(f):
		filename="a.docx"
	f.GetContentFile(filename)
	txt=textract.process(filename)
	return txt.decode("utf-8")

files={}

q=SimpleQueue()
q.put(folderid);






gauth = GoogleAuth()
gauth.LocalWebserverAuth() # client_secrets.json need to be in the same directory as the script
drive = GoogleDrive(gauth)
fileList = drive.ListFile({'q': "'0B0Rlpx3MRZ1SLVFXRFctd0t1cDA' in parents and trashed=false"}).GetList()
for file in fileList:
	print(file)

 # print('Title: %s, ID: %s' % (file['title'], file['id']))
 MyFiles=["2019-2020 Spring"]

folderid='0B0Rlpx3MRZ1SLVFXRFctd0t1cDA'
value="'%s' in parents" % (folderid )
s={}
 
