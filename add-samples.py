f=open("sample-list.txt")
for l in f.readlines():
  samplename=l.strip("/\n").replace("/","_")
  print("""haddnano.py /nfs/dust/cms/user/hinzmann/run2023/"""+samplename+""".root /nfs/dust/cms/user/hinzmann/run2023/"""+samplename+"""_tree/*.root""")
