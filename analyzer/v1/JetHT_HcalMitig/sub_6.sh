#!/bin/bash
[ "${WORKDIR}" == "" ] && { mkdir -p /tmp/$USER/ ; export WORKDIR=/tmp/${USER}/; }
cd /afs/cern.ch/user/z/zdemirag/lnwork/JetMET/HEM15_16/CMSSW_10_1_7/src/jetmet-pog/analyzer
eval `scramv1 runtime -sh`
cd v1/JetHT_HcalMitig
rm sub_6.fail || true
rm sub_6.done || true
rm sub_6.pend || true
rm sub_6.txt || true
touch sub_6.run
export X509_USER_PROXY=/afs/cern.ch/user/z/zdemirag/lnwork/JetMET/HEM15_16/CMSSW_10_1_7/src/jetmet-pog/analyzer/x509up_u4579
cd $WORKDIR
echo "entering $WORKDIR"
python /afs/cern.ch/user/z/zdemirag/lnwork/JetMET/HEM15_16/CMSSW_10_1_7/src/jetmet-pog/analyzer/v1/JetHT_HcalMitig/jetmet_analyzer_6.py  inputFiles="root://cms-xrd-global.cern.ch///store/relval/CMSSW_10_3_0_pre3/JetHT/MINIAOD/103X_dataRun2_PromptLike_HEfail_v3_RelVal_BadHcalMitig-v2/20000/9FC93E0E-B303-7F46-A131-9E4B2E472792.root"  
EXIT=$?
cd /afs/cern.ch/user/z/zdemirag/lnwork/JetMET/HEM15_16/CMSSW_10_1_7/src/jetmet-pog/analyzer
cd v1/JetHT_HcalMitig
rm sub_6.run
echo "exit status is ${EXIT}"
[ "${EXIT}" == "0" ] && { /usr/bin/eos  mkdir -p /eos/cms/store/group/phys_jetmet/zdemirag/batch/HEM/  ; cp  ${WORKDIR}/jetmetNtuples.root /eos/cms/store/group/phys_jetmet/zdemirag/batch/HEM//jetmetNtuples_6.root  && touch sub_6.done || echo "cmsStage fail" > sub_6.fail; }
[ "${EXIT}" == "0" ] || echo ${EXIT} > sub_6.fail

