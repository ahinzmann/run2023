print("""rm /nfs/dust/cms/user/hinzmann/run2023/JetMET0_Run2023B-PromptNanoAODv11p9_v1-v1_NANOAOD_tree/4b709855-2ca3-44e0-9921-c866bc3b8ace_Skim.root""")

f=open("sample-list.txt")
for l in f.readlines():
  samplename=l.strip("/\n").replace("/","_")
  print("""haddnano.py /nfs/dust/cms/user/hinzmann/run2023/"""+samplename+""".root /nfs/dust/cms/user/hinzmann/run2023/"""+samplename+"""_tree/*.root""")

f=open("sample-list.txt")
for l in f.readlines():
  samplename=l.strip("/\n").replace("/","_")
  print("""rm -r /nfs/dust/cms/user/hinzmann/run2023/"""+samplename+"""_tree""")
