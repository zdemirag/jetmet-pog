
## jetmet_analyzer.py

This is a very simple ntuplizer that saves the raw, corrected and gen pts of jets and met objects. To run on subset of events you can do:
   * python jetmet_analyzer.py inputFiles=input.root outputFile=output.root maxEvents=10

## rerunMiniaod.py

It has the capability to recluster jets and re-correct jets on the fly.

## submitBatch.py
With this script you can submit jobs for a given PD, by default it will submit jobs for the analyzer jetmet_analyzer.py
   * python submitBatch.py -e "/RelValTTbar_13/CMSSW_9_4_0_pre3-94X_mc2017_design_IdealBS_v4-v1/MINIAODSIM" --query -n 1
