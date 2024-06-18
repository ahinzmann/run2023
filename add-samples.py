#print("""rm /nfs/dust/cms/user/hinzmann/run2023/QCD_PT-50to80_TuneCP5_13p6TeV_pythia8_Run3Summer23NanoAODv12-130X_mcRun3_2023_realistic_v14-v2_NANOAODSIM_tree/ed043711-3973-4cb5-880b-adef42f76d53_Skim.root""")

f=open("sample-list-2023.txt")
for l in f.readlines():
  samplename=l.strip("/\n").replace("/","_")
  print("""haddnano.py /nfs/dust/cms/user/hinzmann/run2023/"""+samplename+"""-28May2024.root /nfs/dust/cms/user/hinzmann/run2023/"""+samplename+"""_tree/*.root""")

f=open("sample-list-2023.txt")
for l in f.readlines():
  samplename=l.strip("/\n").replace("/","_")
  print("""rm -r /nfs/dust/cms/user/hinzmann/run2023/"""+samplename+"""_tree""")
