f=open("sample-list-2024.txt")
for l in f.readlines():
  samplename=l.strip("/\n").replace("/","_")
  if samplename.startswith("Jet"):
    branches_out="dijetangular_branches_data.txt"
    branches_in="dijetangular_branches_input_data.txt"
    if "Run2022" in samplename:
      json_option=" --json /afs/desy.de/user/h/hinzmann/run2023/Cert_Collisions2022_355100_362760_Golden.json" # from /eos/user/c/cmsdqm/www/CAF/certification/Collisions22/Cert_Collisions2022_355100_362760_Golden.json
    elif "Run2023" in samplename:
      json_option=" --json /afs/desy.de/user/h/hinzmann/run2023/Cert_Collisions2023_366442_370790_Golden.json" # from /eos/user/c/cmsdqm/www/CAF/certification/Collisions23/Cert_Collisions2023_366442_370790_Golden.json
    elif "Run2024" in samplename:
      json_option=" --json /afs/desy.de/user/h/hinzmann/run2023/Cert_Collisions2024_378981_386951_Golden.json" # from https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions24/Cert_Collisions2024_378981_386951_Golden.json
    elif "Run2018" in samplename:
      json_option=" --json /afs/desy.de/user/h/hinzmann/run2023/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt" # from /eos/user/c/cmsdqm/www/CAF/certification/Collisions23/Cert_Collisions2023_366442_370790_Golden.json
    elif "Run2017" in samplename:
      json_option=" --json /afs/desy.de/user/h/hinzmann/run2023/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt" # from /eos/user/c/cmsdqm/www/CAF/certification/Collisions23/Cert_Collisions2023_366442_370790_Golden.json
    elif "Run2016" in samplename:
      json_option=" --json /afs/desy.de/user/h/hinzmann/run2023/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt" # from /eos/user/c/cmsdqm/www/CAF/certification/Collisions23/Cert_Collisions2023_366442_370790_Golden.json
    else:
      unknownjson
  else:
    branches_out="dijetangular_branches_mc.txt"
    branches_in="dijetangular_branches_input_mc.txt"
    json_option=""
  f2=open(samplename+".txt")
  count=0
  with open("submit/"+samplename+".sh",'w+') as wrapper_script:
            wrapper_script.write("""#!/bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
#cd /afs/desy.de/user/h/hinzmann/run2023/CMSSW_10_6_30/src
cd /afs/desy.de/user/h/hinzmann/run2023/CMSSW_14_0_18/src
cmsenv
cd /afs/desy.de/user/h/hinzmann/run2023
export X509_USER_PROXY=/afs/desy.de/user/h/hinzmann/run2023/myproxy.pem
python3 dijetangular_postproc.py $1 $2 --bi """+branches_in+""" --bo """+branches_out+json_option+""" -P  -c "Jet_pt>200"
""")
  for l2 in f2.readlines():
    name=str(count)
    with open("submit/"+samplename+"""_"""+name+".submit",'w+') as htc_config:
            htc_config.write("""
#HTC Submission File for GEN sample production
#requirements      =  OpSysAndVer == "SL7"
universe          = vanilla
notification      = Error
notify_user       = andreas.hinzmann@desy.de
initialdir        = /afs/desy.de/user/h/hinzmann/run2023/
#output            = submit/"""+samplename+"""_"""+name+""".o
#error             = submit/"""+samplename+"""_"""+name+""".e
#log               = submit/"""+samplename+"""_"""+name+""".log
#Requesting CPU and DISK Memory - default +RequestRuntime of 3h stays unaltered
+RequestRuntime   = 50000
RequestMemory     = 32G
JobBatchName      = """+samplename+"""
#RequestDisk       = 10G
getenv            = True
executable        = /usr/bin/sh
arguments         = " submit/"""+samplename+""".sh /data/dust/user/hinzmann/run2023/"""+samplename+"""_tree/ root://cms-xrd-global.cern.ch/"""+l2.strip("\n")+""""
queue 1
""")
    print("condor_submit submit/"+samplename+"""_"""+name+".submit")
    count+=1

#NanoAOD content
# https://cms-nanoaod-integration.web.cern.ch/autoDoc/NanoAODv12/2022/2023/doc_EGamma_Run2022F-22Sep2023-v1.html

print("voms-proxy-init --voms cms --out /afs/desy.de/user/h/hinzmann/run2023/myproxy.pem")
