import textract
import json
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

def get_content_files():
	txts=[]
	for key,value in files.items():
		if isPdf(value):
			txts.append(key)	
		if isDoc(value):
			txts.append(key)
	return txts		

def convert(filename, pdf, doc):
	sucess=Flase
	try:
		txt=""
		txt=textract.process(filename)
		txt=txt.decode("utf-8")
		sucess=True
	except  Exception as e:
		print(e)
		pass
	if not sucess:
		return None	
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

def get_title(id):
	l=[]
	if id not in files: 
		return []
	o=files[id]
	parent_title=[]
	if 'parents' in o:
		if len(o['parents']) >= 1:
			pid=o['parents'][0]['id']
			parent_title=get_title(pid)
		l= parent_title
	l.append( o['title'])
	return l 
