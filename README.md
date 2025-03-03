# Install environment for sample production

cmsrel CMSSW_14_0_18
cp CMSSW_10_6_30/src/PhysicsTools/NanoAODTools/python/postprocessing/modules/jme/jetRecalib.py CMSSW_14_0_18/src/PhysicsTools/NanoAODTools/python/postprocessing/modules/jme/
cp CMSSW_10_6_30/src/PhysicsTools/NanoAODTools/data/jme/puppiCorr.root CMSSW_14_0_18/src/PhysicsTools/NanoAODTools/data/jme/
wget https://raw.githubusercontent.com/cms-nanoAOD/nanoAOD-tools/refs/heads/master/python/postprocessing/modules/jme/JetReCalibrator.py
wget https://raw.githubusercontent.com/cms-nanoAOD/nanoAOD-tools/refs/heads/master/python/postprocessing/tools.py
scram b -j5

# Environment for sample production

ssh naf-cms.desy.de

source /cvmfs/grid.desy.de/etc/profile.d/grid-ui-env.sh

source /cvmfs/cms.cern.ch/cmsset_default.sh

export SCRAM_ARCH=slc7_amd64_gcc9

#cd ~/run2023/CMSSW_10_6_30/src/
cd ~/run2023/CMSSW_14_0_18/src/

cmsenv

cd ~/run2023/

# Sample production

python make-file-lists.py > make_file_lists.sh

source make_file_lists.sh

voms-proxy-init --voms cms --out /afs/desy.de/user/h/hinzmann/run2023/myproxy.pem

python process-samples.py > submit.sh

source submit.sh

python add-samples.py > add.sh

source add.sh

# Get event counts of samples

python make-event-counts.py > make-event-counts.sh

source make-event-counts.sh

python make-event-counts-step2.py > event-counts.txt

# Cross section calculation for QCD_PT samples

ssh lxplus8.cern.ch

export SCRAM_ARCH=el8_amd64_gcc11

cd ~/run2023/CMSSW_13_0_13/src/

cmsenv

cd ~/run2023/

cmsRun QCD_PT_cfg.py
