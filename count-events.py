f=open("sample-list.txt")
for l in f.readlines():
  samplename=l.strip("/\n").replace("/","_")
  print("""echo """+samplename+"""; root -l -b -q 'EventsPrint.C("/nfs/dust/cms/user/hinzmann/run2023/"""+samplename+""".root")' | grep events""")
