# run2023

python make-file-lists.py > sample-list.txt

voms-proxy-init --voms cms --out /afs/desy.de/user/h/hinzmann/run2023/myproxy.pem

python process-samples.py > submit.sh

source submit.sh

python add-samples.py > add.sh

source add.sh
