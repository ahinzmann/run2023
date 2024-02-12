f=open("sample-list.txt")
for l in f.readlines():
  if not "NANO" in l: continue
  print("""dasgoclient --query="dataset="""+l.strip("\n")+"""" -json > """+l.strip("/\n").replace("/","_")+""".json""")
