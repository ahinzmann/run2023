f=open("sample-list.txt")
for l in f.readlines():
  print("""dasgoclient --query="dataset="""+l.strip("\n")+"""" -json > """+l.strip("/\n").replace("/","_")+""".json""")

f=open("sample-list.txt")
for l in f.readlines():
  print(l.strip("/\n").replace("/","_"))
  f=open(l.strip("/\n").replace("/","_")+""".json""")
  for l in f.readlines():
    for s in l.split(","):
      if "nevents" in s: print(s)
