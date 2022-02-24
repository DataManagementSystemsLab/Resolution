def get_contents(dir,lst):
	contents={}
	i=0
	for id in lst:
		o=g.files[id]
		if g.isPdf(o):
			filename=dir+"/"+id+".pdf"
		if g.isDoc(o):
			filename=dir+"/"+id+".docx"
		txt=convert(filename)
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
		o=g.files[id]
		print(o)
		pdf=False
		doc=False
		if g.isPdf(o):
			filename=dir+"/"+id+".pdf"
			pdf=True
		if g.isDoc(o):
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



		 get_contents("files", txts)