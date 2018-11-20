#!/bin/bash
[ "${WORKDIR}" == "" ] && { mkdir -p /tmp/$USER/ ; export WORKDIR=/tmp/${USER}/; }
cd /afs/cern.ch/user/z/zdemirag/lnwork/JetMET/HEM15_16/CMSSW_10_1_7/src/jetmet-pog/analyzer
eval `scramv1 runtime -sh`
cd v1/JetHT_HEfail
rm sub_3.fail || true
rm sub_3.done || true
rm sub_3.pend || true
rm sub_3.txt || true
touch sub_3.run
export X509_USER_PROXY=/afs/cern.ch/user/z/zdemirag/lnwork/JetMET/HEM15_16/CMSSW_10_1_7/src/jetmet-pog/analyzer/x509up_u4579
cd $WORKDIR
echo "entering $WORKDIR"
python /afs/cern.ch/user/z/zdemirag/lnwork/JetMET/HEM15_16/CMSSW_10_1_7/src/jetmet-pog/analyzer/v1/JetHT_HEfail/jetmet_analyzer_3.py  inputFiles="root://cms-xrd-global.cern.ch///store/relval/CMSSW_10_3_0_pre3/JetHT/MINIAOD/103X_dataRun2_PromptLike_HEfail_v3_RelVal_HEfail-v2/20000/2502E8FB-5C6A-B145-8163-06DF264FB4AA.root"  
EXIT=$?
cd /afs/cern.ch/user/z/zdemirag/lnwork/JetMET/HEM15_16/CMSSW_10_1_7/src/jetmet-pog/analyzer
cd v1/JetHT_HEfail
rm sub_3.run
echo "exit status is ${EXIT}"
[ "${EXIT}" == "0" ] && { /usr/bin/eos  mkdir -p /eos/cms/store/group/phys_jetmet/zdemirag/batch/HEM_HEfail/  ; cp  ${WORKDIR}/jetmetNtuples.root /eos/cms/store/group/phys_jetmet/zdemirag/batch/HEM_HEfail//jetmetNtuples_3.root  && touch sub_3.done || echo "cmsStage fail" > sub_3.fail; }
[ "${EXIT}" == "0" ] || echo ${EXIT} > sub_3.fail

