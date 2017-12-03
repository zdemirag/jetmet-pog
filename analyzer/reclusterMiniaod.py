import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing

process = cms.Process("USER")

process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag (process.GlobalTag, 'auto:run2_mc')

## Events to process
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

## Input files
process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
        "file:/eos/cms/store/mc/RunIISummer17MiniAOD/QCD_Pt-15to7000_TuneCUETP8M1_Flat_13TeV_pythia8/MINIAODSIM/FlatPU0to70_magnetOn_92X_upgrade2017_realistic_v10-v1/70000/F8A5A68B-8D9A-E711-AD5F-0242AC130002.root",
        )
                            )

## Output file
from PhysicsTools.PatAlgos.patEventContent_cff import patEventContent

process.options = cms.untracked.PSet(
        wantSummary = cms.untracked.bool(False), 
        allowUnscheduled = cms.untracked.bool(True)
)

from PhysicsTools.PatAlgos.tools.helpers import getPatAlgosToolsTask, addToProcessAndTask

task = getPatAlgosToolsTask(process)

#################################################
## Remake jets
#################################################

## Filter out neutrinos from packed GenParticles
process.packedGenParticlesForJetsNoNu = cms.EDFilter("CandPtrSelector", src = cms.InputTag("packedGenParticles"), cut = cms.string("abs(pdgId) != 12 && abs(pdgId) != 14 && abs(pdgId) != 16"))

task.add(process.packedGenParticlesForJetsNoNu)

## Define GenJets
from RecoJets.JetProducers.ak4GenJets_cfi import ak4GenJets
process.ak4GenJetsNoNu = ak4GenJets.clone(src = 'packedGenParticlesForJetsNoNu')

task.add(process.ak4GenJetsNoNu)

## Select charged hadron subtracted packed PF candidates
#new cut to test:
process.pfCHS = cms.EDFilter("CandPtrSelector", src = cms.InputTag("packedPFCandidates"), 
                             cut = cms.string("fromPV")
                             )

process.pfnewCHS = cms.EDFilter("CandPtrSelector", src = cms.InputTag("packedPFCandidates"), 
                             cut = cms.string("((fromPV && abs(eta) < 2.4) || (abs(eta) >= 2.4 && ((pvAssociationQuality()<5 && vertexRef().key()!=0) || (vertexRef().key()==0) ) ))"))

task.add(process.pfCHS)
task.add(process.pfnewCHS)

from RecoJets.JetProducers.ak4PFJets_cfi import ak4PFJets

## Define PFJetsCHS
process.ak4PFJetsCHS    = ak4PFJets.clone(src = 'pfCHS', doAreaFastjet = True)
process.ak4PFJetsnewCHS = ak4PFJets.clone(src = 'pfnewCHS', doAreaFastjet = True)
process.ak4PFJets       = ak4PFJets.clone(src = 'packedPFCandidates', doAreaFastjet = True)

task.add(process.ak4PFJetsCHS)
task.add(process.ak4PFJetsnewCHS)
task.add(process.ak4PFJets)

#################################################
## Remake PAT jets
#################################################

## b-tag discriminators
bTagDiscriminators = [
    'pfCombinedInclusiveSecondaryVertexV2BJetTags'
]

from PhysicsTools.PatAlgos.tools.jetTools import *

## Add PAT jet collection based on the above-defined ak4PFJetsCHS
addJetCollection(
    process,
    labelName = 'AK4PFCHS',
    jetSource = cms.InputTag('ak4PFJetsCHS'),
    pvSource = cms.InputTag('offlineSlimmedPrimaryVertices'),
    pfCandidates = cms.InputTag('packedPFCandidates'),
    svSource = cms.InputTag('slimmedSecondaryVertices'),
    btagDiscriminators = bTagDiscriminators,
    jetCorrections = ('AK4PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute'], 'None'),
    genJetCollection = cms.InputTag('ak4GenJetsNoNu'),
    genParticles = cms.InputTag('prunedGenParticles'),
    algo = 'AK',
    rParam = 0.4
)

getattr(process,'selectedPatJetsAK4PFCHS').cut = cms.string('pt > 10')

addJetCollection(
    process,
    labelName = 'AK4PFnewCHS',
    jetSource = cms.InputTag('ak4PFJetsnewCHS'),
    pvSource = cms.InputTag('offlineSlimmedPrimaryVertices'),
    pfCandidates = cms.InputTag('packedPFCandidates'),
    svSource = cms.InputTag('slimmedSecondaryVertices'),
    btagDiscriminators = bTagDiscriminators,
    jetCorrections = ('AK4PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute'], 'None'),
    genJetCollection = cms.InputTag('ak4GenJetsNoNu'),
    genParticles = cms.InputTag('prunedGenParticles'),
    algo = 'AK',
    rParam = 0.4
)

getattr(process,'selectedPatJetsAK4PFnewCHS').cut = cms.string('pt > 10')

addJetCollection(
    process,
    labelName = 'AK4PF',
    jetSource = cms.InputTag('ak4PFJets'),
    pvSource = cms.InputTag('offlineSlimmedPrimaryVertices'),
    pfCandidates = cms.InputTag('packedPFCandidates'),
    svSource = cms.InputTag('slimmedSecondaryVertices'),
    btagDiscriminators = bTagDiscriminators,
    jetCorrections = ('AK4PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute'], 'None'),
    genJetCollection = cms.InputTag('ak4GenJetsNoNu'),
    genParticles = cms.InputTag('prunedGenParticles'),
    algo = 'AK',
    rParam = 0.4
)

getattr(process,'selectedPatJetsAK4PF').cut = cms.string('pt > 10')

from PhysicsTools.PatAlgos.tools.pfTools import *
## Adapt primary vertex collection
adaptPVs(process, pvCollection=cms.InputTag('offlineSlimmedPrimaryVertices'))

process.OUT = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('rerunminiaod.root'),
    #outputCommands = cms.untracked.vstring(['drop *'
    #                                        ,'keep *_packedPFCandidates_*_*'
    #                                        ,'keep *_*Rho*_*_*'
    #                                        ,'keep *_offlineSlimmedPrimaryVertices_*_*'
    #                                        ,'keep *_selectedPatJets*_*_*'])
)

process.endpath= cms.EndPath(process.OUT,process.patAlgosToolsTask)
