from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from queue import SimpleQueue
import textract
import json
import os
import subprocess

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

def bfs(drive):
	while not q.empty():
		id=q.get()
		lst=getList(drive,id)
		for x in lst:
			files[x['id']]=x
			if isFolder(x):
				q.put(x['id'])

def get_files():
	pdfs=[]
	docs=[]
	for key,value in files.items():
		if isPdf(value):
			pdfs.append(key)	
		if isDoc(value):
			docs.append(key)
	return (pdfs,docs)

def get_content_files():
	txts=[]
	for key,value in files.items():
		if isPdf(value):
			txts.append(key)	
		if isDoc(value):
			txts.append(key)
	return txts			

def get_title(id):
	l=[]
	if id not in files: 
		return ""
	o=files[id]
	parent_title=[]
	if 'parents' in o:
		if len(o['parents']) >= 1:
			pid=o['parents'][0]['id']
			parent_title=get_title(pid)
	l= parent_title
	l.append( o['title'])
	return l 

def download_doc(f,dir):
	filename=""
	id=f['id']
	if isPdf(f):
		filename=dir+"/"+id+".pdf"
	if isDoc(f):
		filename=dir+"/"+id+".docx"
	f.GetContentFile(filename)

def download(lst, start=0, len=100):
	for id in lst[start: start+len]:
		path="tmp/"+str((int)(start/100))
		isExist = os.path.exists(path)
		if not isExist:
			os.mkdir(path)
		o=files[id]
		download_doc(o,path)


def convert(filename, pdf, doc):
	try:
		txt=""
		if doc:
			txt=textract.process(filename)
			#os.remove(filename)
			txt=txt.decode("utf-8")
		if pdf:
			cmd="python3 /Users/user/homebrew/bin/pdf2txt.py "+filename +" --outfile "+ filename+".txt"
			os.system(cmd)
			file=open(filename+".txt",mode='r')
			txt=file.read();
			file.close()
			#os.remove(filename)
			os.remove(filename+".txt")
	except  Exception as e:
		print(e)
		pass
	return txt

def get_contents(dir,lst):
	contents={}
	i=0
	for id in lst:
		o=files[id]
		print(o)
		pdf=False
		doc=False
		if isPdf(o):
			filename=dir+"/"+id+".pdf"
			pdf=True
		if isDoc(o):
			filename=dir+"/"+id+".docx"
			doc=True
		txt=convert(filename, pdf, doc)
		contents[id]=txt
		i=i+1
		if i%100==0:
			f=str((int)(i/100))
			contents_file = open("contents_"+f+".json", "w")
			json.dump(contents, contents_file)
			contents_file.close()
			contents={}
	if len(contents)>0:
		f=str((int)(i/100))
		contents_file = open("contents_"+f+".json", "w")
		json.dump(contents, contents_file)
		contents_file.close()

