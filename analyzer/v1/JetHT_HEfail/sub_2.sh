#!/bin/bash
[ "${WORKDIR}" == "" ] && { mkdir -p /tmp/$USER/ ; export WORKDIR=/tmp/${USER}/; }
cd /afs/cern.ch/user/z/zdemirag/lnwork/JetMET/HEM15_16/CMSSW_10_1_7/src/jetmet-pog/analyzer
eval `scramv1 runtime -sh`
cd v1/JetHT_HEfail
rm sub_2.fail || true
rm sub_2.done || true
rm sub_2.pend || true
rm sub_2.txt || true
touch sub_2.run
export X509_USER_PROXY=/afs/cern.ch/user/z/zdemirag/lnwork/JetMET/HEM15_16/CMSSW_10_1_7/src/jetmet-pog/analyzer/x509up_u4579
cd $WORKDIR
echo "entering $WORKDIR"
python /afs/cern.ch/user/z/zdemirag/lnwork/JetMET/HEM15_16/CMSSW_10_1_7/src/jetmet-pog/analyzer/v1/JetHT_HEfail/jetmet_analyzer_2.py  inputFiles="root://cms-xrd-global.cern.ch///store/relval/CMSSW_10_3_0_pre3/JetHT/MINIAOD/103X_dataRun2_PromptLike_HEfail_v3_RelVal_HEfail-v2/20000/E314B083-EB9E-1E44-B002-C6CA9D436DAF.root"  
EXIT=$?
cd /afs/cern.ch/user/z/zdemirag/lnwork/JetMET/HEM15_16/CMSSW_10_1_7/src/jetmet-pog/analyzer
cd v1/JetHT_HEfail
rm sub_2.run
echo "exit status is ${EXIT}"
[ "${EXIT}" == "0" ] && { /usr/bin/eos  mkdir -p /eos/cms/store/group/phys_jetmet/zdemirag/batch/HEM_HEfail/  ; cp  ${WORKDIR}/jetmetNtuples.root /eos/cms/store/group/phys_jetmet/zdemirag/batch/HEM_HEfail//jetmetNtuples_2.root  && touch sub_2.done || echo "cmsStage fail" > sub_2.fail; }
[ "${EXIT}" == "0" ] || echo ${EXIT} > sub_2.fail

