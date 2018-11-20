#!/bin/bash
[ "${WORKDIR}" == "" ] && { mkdir -p /tmp/$USER/ ; export WORKDIR=/tmp/${USER}/; }
cd /afs/cern.ch/user/z/zdemirag/lnwork/JetMET/HEM15_16/CMSSW_10_1_7/src/jetmet-pog/analyzer
eval `scramv1 runtime -sh`
cd v1/JetHT_HcalMitig
rm sub_0.fail || true
rm sub_0.done || true
rm sub_0.pend || true
rm sub_0.txt || true
touch sub_0.run
export X509_USER_PROXY=/afs/cern.ch/user/z/zdemirag/lnwork/JetMET/HEM15_16/CMSSW_10_1_7/src/jetmet-pog/analyzer/x509up_u4579
cd $WORKDIR
echo "entering $WORKDIR"
python /afs/cern.ch/user/z/zdemirag/lnwork/JetMET/HEM15_16/CMSSW_10_1_7/src/jetmet-pog/analyzer/v1/JetHT_HcalMitig/jetmet_analyzer_0.py  inputFiles="root://cms-xrd-global.cern.ch///store/relval/CMSSW_10_3_0_pre3/JetHT/MINIAOD/103X_dataRun2_PromptLike_HEfail_v3_RelVal_BadHcalMitig-v2/20000/A3DD06A7-75CC-E14D-8C6B-263C30543CA4.root"  maxEvents=10
EXIT=$?
cd /afs/cern.ch/user/z/zdemirag/lnwork/JetMET/HEM15_16/CMSSW_10_1_7/src/jetmet-pog/analyzer
cd v1/JetHT_HcalMitig
rm sub_0.run
echo "exit status is ${EXIT}"
#[ "${EXIT}" == "0" ] && { /usr/bin/eos  mkdir -p /eos/cms/store/group/phys_jetmet/zdemirag/batch/HEM/  ; cp  ${WORKDIR}/jetmetNtuples_numEvent10.root /eos/cms/store/group/phys_jetmet/zdemirag/batch/HEM//jetmetNtuples_0.root  && touch sub_0.done || echo "cmsStage fail" > sub_0.fail; }
[ "${EXIT}" == "0" ] && { /usr/bin/eos  mkdir -p /eos/cms/store/group/phys_jetmet/zdemirag/batch/HEM/  ; cp  ${WORKDIR}/jetmetNtuples_numEvent10.root ./jetmetNtuples_0.root  && touch sub_0.done || echo "cmsStage fail" > sub_0.fail; }
[ "${EXIT}" == "0" ] || echo ${EXIT} > sub_0.fail

