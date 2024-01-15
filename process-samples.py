f=open("sample-list.txt")
for l in f.readlines():
  samplename=l.strip("/\n").replace("/","_")
  if samplename.startswith("JetMET"):
    branches_out="dijetangular_branches_data.txt"
    branches_in="dijetangular_branches_input_data.txt"
    if "Run2023" in samplename:
      json_option=" --json /afs/desy.de/user/h/hinzmann/run2023/Cert_Collisions2023_366442_370790_Golden.json" # from /eos/user/c/cmsdqm/www/CAF/certification/Collisions23/Cert_Collisions2023_366442_370790_Golden.json
    else:
      unknownjson
  else:
    branches_out="dijetangular_branches_mc.txt"
    branches_in="dijetangular_branches_input_mc.txt"
    json_option=""
  f2=open(samplename+".txt")
  count=0
  for l2 in f2.readlines():
    name=str(count)
    with open(samplename+"""_"""+name+".sh",'w+') as wrapper_script:
            wrapper_script.write("""#!/bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /afs/desy.de/user/h/hinzmann/run2023/CMSSW_10_6_30/src
cmsenv
cd /afs/desy.de/user/h/hinzmann/run2023
export X509_USER_PROXY=/afs/desy.de/user/h/hinzmann/run2023/myproxy.pem
python dijetangular_postproc.py /nfs/dust/cms/user/hinzmann/run2023/"""+samplename+"""_tree/ root://cms-xrd-global.cern.ch/"""+l2.strip("\n")+""" --bi """+branches_in+""" --bo """+branches_out+json_option+""" -P  -c "Jet_pt>200"
""")
    with open(samplename+"""_"""+name+".submit",'w+') as htc_config:
            htc_config.write("""
#HTC Submission File for GEN sample production
#requirements      =  OpSysAndVer == "SL7"
universe          = vanilla
notification      = Error
notify_user       = andreas.hinzmann@desy.de
initialdir        = /afs/desy.de/user/h/hinzmann/run2023/
#output            = """+samplename+"""_"""+name+""".o
error             = """+samplename+"""_"""+name+""".e
#log               = """+samplename+"""_"""+name+""".log
#Requesting CPU and DISK Memory - default +RequestRuntime of 3h stays unaltered
#+RequestRuntime   = 170000
RequestMemory     = 8G
JobBatchName      = """+samplename+"""
#RequestDisk       = 10G
getenv            = True
executable        = /usr/bin/sh
arguments         = " """+samplename+"""_"""+name+""".sh"
queue 1
""")
    print("condor_submit "+samplename+"""_"""+name+".submit")
    count+=1

#NanoAOD content
# https://cms-nanoaod-integration.web.cern.ch/autoDoc/NanoAODv12/2022/2023/doc_EGamma_Run2022F-22Sep2023-v1.html

print("voms-proxy-init --voms cms --out /afs/desy.de/user/h/hinzmann/run2023/myproxy.pem")
