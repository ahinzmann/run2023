f=open("sample-list-2018-data.txt")
for l in f.readlines():
  print("""dasgoclient --query="file dataset="""+l.strip("\n")+"""" > """+l.strip("/\n").replace("/","_")+""".txt""")
  print("""dasgoclient --query="parent dataset="""+l.strip("\n")+'"')
