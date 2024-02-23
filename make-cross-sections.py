f=open("sample-list-MINI.txt")
for l in f.readlines():
  if not "MINI" in l: continue
  g=open(l.strip("/\n").replace("/","_")+".txt")
  for m in g.readlines():
    print('cmsRun genXsec_cfg.py inputFiles="'+m.strip("\n")+'" maxEvents=1')
    break
