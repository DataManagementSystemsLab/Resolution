import common as c


f_file = open("files.json", "r")
files = json.load(f_file)

txts=c.get_content_files()

#c.get_contents(txt)