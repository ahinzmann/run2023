f=open("sample-list-2018.txt")
for l in f.readlines():
  if not "NANO" in l: continue
  print(l.strip("/\n").replace("/","_"))
  f=open(l.strip("/\n").replace("/","_")+""".json""")
  for l in f.readlines():
    for s in l.split(","):
      if "nevents" in s: print(s)
