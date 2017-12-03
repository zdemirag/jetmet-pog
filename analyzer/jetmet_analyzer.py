# import ROOT in batch mode
import sys
oldargv = sys.argv[:]
sys.argv = [ '-b-' ]
import ROOT
ROOT.gROOT.SetBatch(True)
sys.argv = oldargv

# define deltaR
from math import hypot, pi, sqrt, fabs
import numpy as n

from jetmet_tree import *
from functions import *

# create an oput tree.

fout = ROOT.TFile ("jetmet.root","recreate")
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
events = Events("file:/eos/cms/store/relval/CMSSW_9_4_0_pre3/RelValTTbar_13/MINIAODSIM/PU25ns_94X_mc2017_realistic_PixFailScenario_Run305081_FIXED_HS_AVE50-v1/10000/02B605A1-86C2-E711-A445-4C79BA28012B.root")

for ievent,event in enumerate(events):
    if ievent > 10: continue
    
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

    ###CHS JETS
    for i,j in enumerate(jets.product()):

        if i>=maxjet: break

        jet_pt[i]  = j.pt()
        jet_eta[i] = j.eta()
        jet_phi[i] = j.phi()

        rawjet_pt[i]  = j.pt()*j.jecFactor("Uncorrected")
        rawjet_eta[i] = j.eta()*j.jecFactor("Uncorrected")
        rawjet_phi[i] = j.phi()*j.jecFactor("Uncorrected")

        if not (j.genJet() == None):
            genjet_pt[i]  = j.genJet().pt()
            genjet_eta[i] = j.genJet().eta()
            genjet_phi[i] = j.genJet().phi()

        else:
            genjet_pt[i] = -999.


        sourceCandidate = set()

        # now get a list of the PF candidates used to build this jet
        for isource in xrange(j.numberOfSourceCandidatePtrs()):
            sourceCandidate.add(j.sourceCandidatePtr(isource).key()) # the key is the index in the pf collection

        neutral[i], charged[i], photon[i], muon[i], electron[i], hhf[i], ehf[i], pileup = 0, 0, 0, 0, 0, 0, 0, 0

        for ipf,pf in enumerate(pfs.product()):            

            # if pf candidate is part of the jet, lets categorize
            if ipf in sourceCandidate:

                if ( abs(pf.pdgId()) == 211 ):
                    charged[i] += pf.pt();
                    
                elif abs(pf.pdgId()) == 130:
                    neutral[i] += pf.pt();

                elif abs(pf.pdgId()) == 22:
                    photon[i] += pf.pt();

                elif abs(pf.pdgId()) == 13:
                    muon[i] += pf.pt();

                elif abs(pf.pdgId()) == 11:
                    electron[i] += pf.pt();

                elif abs(pf.pdgId()) == 1:
                    hhf[i] += pf.pt();

                elif abs(pf.pdgId()) == 2:
                    ehf[i] += pf.pt();
                
                else:
                    pileup += pf.pt()


    #MET Information
    metprod   = mets.product().front()
    met[0]    = metprod.pt()                
    genmet[0] = metprod.genMET().pt()                
    rawmet[0] = metprod.uncorPt()
    
    t.Fill()


fout.Write()
fout.Close()
