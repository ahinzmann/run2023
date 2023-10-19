f=open("sample-list.txt")
for l in f.readlines():
  print("""dasgoclient --query="file dataset="""+l.strip("\n")+"""" > """+l.strip("/\n").replace("/","_")+""".txt""")
