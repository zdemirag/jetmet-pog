# import ROOT in batch mode
import sys
oldargv = sys.argv[:]
sys.argv = [ '-b-' ]
import ROOT
ROOT.gROOT.SetBatch(True)
sys.argv = oldargv

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing('python')

#default options
options.inputFiles="/eos/cms/store/relval/CMSSW_9_4_0_pre3/RelValTTbar_13/MINIAODSIM/PU25ns_94X_mc2017_realistic_PixFailScenario_Run305081_FIXED_HS_AVE50-v1/10000/02B605A1-86C2-E711-A445-4C79BA28012B.root"
options.outputFile="jetmetNtuples.root"
options.maxEvents=-1

#overwrite if given any command line arguments
options.parseArguments()

# define deltaR
from math import hypot, pi, sqrt, fabs
import numpy as n

from jetmet_tree import *
from functions import *

# create an oput tree.

#fout = ROOT.TFile ("jetmet.root","recreate")
fout = ROOT.TFile (options.outputFile,"recreate")
t    = ROOT.TTree ("events","events")

declare_branches(t)

# load FWLite C++ libraries
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.FWLiteEnabler.enable()

# load FWlite python libraries
from DataFormats.FWLite import Handle, Events

pfs, pfLabel        = Handle("std::vector<pat::PackedCandidate>"), "packedPFCandidates"
jets, jetLabel      = Handle("std::vector<pat::Jet>"), "slimmedJets"
mets, metLabel      = Handle("std::vector<pat::MET>"), "slimmedMETs"
vertex, vertexLabel = Handle("std::vector<reco::Vertex>"),"offlineSlimmedPrimaryVertices"

rhoall_, rhoallLabel         = Handle("double"), "fixedGridRhoFastjetAll"
rhocentral_, rhocentralLabel = Handle("double"), "fixedGridRhoFastjetCentral"
rhoneutral_, rhoneutralLabel = Handle("double"), "fixedGridRhoFastjetCentralNeutral"
rhochargedpileup_, rhochargedpileupLabel = Handle("double"), "fixedGridRhoFastjetCentralChargedPileUp"

# open file (you can use 'edmFileUtil -d /store/whatever.root' to get the physical file name)
#events = Events("file:/eos/cms/store/relval/CMSSW_9_4_0_pre3/RelValTTbar_13/MINIAODSIM/PU25ns_94X_mc2017_realistic_PixFailScenario_Run305081_FIXED_HS_AVE50-v1/10000/02B605A1-86C2-E711-A445-4C79BA28012B.root")
events = Events(options)

for ievent,event in enumerate(events):

    if options.maxEvents is not -1:
        if ievent > options.maxEvents: continue
    
    event.getByLabel(pfLabel, pfs)
    event.getByLabel(jetLabel, jets)
    event.getByLabel(metLabel, mets)
    event.getByLabel(vertexLabel, vertex)

    event.getByLabel(rhoallLabel,rhoall_)
    event.getByLabel(rhocentralLabel,rhocentral_)
    event.getByLabel(rhoneutralLabel,rhoneutral_)
    event.getByLabel(rhochargedpileupLabel,rhochargedpileup_)

    rhoall[0]     = rhoall_.product()[0]
    rhocentral[0] = rhocentral_.product()[0]
    rhoneutral[0] = rhoneutral_.product()[0]
    rhochargedpileup[0] = rhochargedpileup_.product()[0]

    #print "\nEvent %d: run %6d, lumi %4d, event %12d" % (ievent,event.eventAuxiliary().run(), event.eventAuxiliary().luminosityBlock(),event.eventAuxiliary().event())

    nrun[0]   = event.eventAuxiliary().run()
    nlumi[0]  = event.eventAuxiliary().luminosityBlock()
    nevent[0] = event.eventAuxiliary().event()
    npv[0]    = vertex.product().size()

    njet[0]   = jets.product().size()

    dphipfmet[0] = 999.
    ###CHS JETS
    for i,j in enumerate(jets.product()):

        if i>=maxjet: break

        jet_pt[i]  = j.pt()
        jet_eta[i] = j.eta()
        jet_phi[i] = j.phi()
        jet_energy[i]  = j.energy()

        rawjet_pt[i]  = j.pt()*j.jecFactor("Uncorrected")
        rawjet_eta[i] = j.eta()*j.jecFactor("Uncorrected")
        rawjet_phi[i] = j.phi()*j.jecFactor("Uncorrected")
        rawjet_energy[i] = j.energy()*j.jecFactor("Uncorrected")

        NHF[i]                 = j.neutralHadronEnergyFraction()
        NEMF[i]                = j.neutralEmEnergyFraction();
        CHF[i]                 = j.chargedHadronEnergyFraction();
        MUF[i]                 = j.muonEnergyFraction();
        CEMF[i]                = j.chargedEmEnergyFraction();
        NumConst[i]            = j.chargedMultiplicity()+j.neutralMultiplicity();
        NumNeutralParticle[i]  = j.neutralMultiplicity();
        CHM[i]                 = j.chargedMultiplicity();
        eta                    = j.eta();
        
        jet_loose[i] = (NHF[i]<0.99 and NEMF[i]<0.99 and NumConst[i]>1) and ((abs(eta)<=2.4 and CHF[i]>0 and CHM[i]>0 and CEMF[i]<0.99) or abs(eta)>2.4) and abs(eta)<=2.7
        jet_loose[i] = jet_loose[i] or (NHF[i]<0.98 and NEMF[i]>0.01 and NumNeutralParticle[i]>2 and abs(eta)>2.7 and abs(eta)<=3.0 )
        jet_loose[i] = jet_loose[i] or (NEMF[i]<0.90 and NumNeutralParticle[i]>10 and abs(eta)>3.0)

        if j.pt()>30.:
            dphipfmet[0] = min(abs(deltaPhi(j.phi(),mets.product().front().phi())),dphipfmet[0])
            #print i, j.pt(),  j.phi(), mets.product().front().phi(), dphipfmet
            
            #print "Final", dphipfmet[0]
    #MET Information
    metprod   = mets.product().front()
    met[0]    = metprod.pt()                
    met_phi[0]= metprod.phi()                
    mex[0]    = metprod.px()                
    mey[0]    = metprod.py()                
    #genmet[0] = metprod.genMET().pt()                
    rawmet[0] = metprod.uncorPt()

    
    for ipf,pf in enumerate(pfs.product()):            
        if ( abs(pf.pdgId()) == 211 ):
            charged_met[0]   += pf.pt();
            #charged_n_met[0] += 1;
                    
        elif abs(pf.pdgId()) == 130:
            neutral_met[0] += pf.pt();
            #neutral_n_met[0] += 1;

        elif abs(pf.pdgId()) == 22:
            photon_met[0] += pf.pt();
            #photon_n_met[0] += 1;

        elif abs(pf.pdgId()) == 13:
            muon_met[0] += pf.pt();
            #muon_n_met[0] += 1;
            
        elif abs(pf.pdgId()) == 11:
            electron_met[0] += pf.pt();
            #electron_n_met[0] += 1;

        elif abs(pf.pdgId()) == 1:
            hhf_met[0] += pf.pt();            
            #hhf_n_met[0] += 1;
            
        elif abs(pf.pdgId()) == 2:
            ehf_met[0] += pf.pt();
            #ehf_n_met[0] += 1;
            
        else:
            other_met[0] += pf.pt();
            #other_n_met[0] += 1;
       
    t.Fill()


fout.Write()
fout.Close()
