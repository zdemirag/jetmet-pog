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

def deltaPhi(a,b):
    dphi = fabs(a.phi() - b.phi())
    if (dphi <= pi): return dphi
    else: return 2*pi - dphi
        

def deltaR(a,b):
    dphi = deltaPhi(a,b)
    return hypot((a.eta()-b.eta()),dphi)


# create an oput tree.

fout = ROOT.TFile ("jetmet.root","recreate")
t    = ROOT.TTree ("events","events")

maxjet = 10000

njet = n.zeros(1,dtype=int)
npfjet = n.zeros(1,dtype=int)
nnewjet = n.zeros(1,dtype=int)
ncharged = n.zeros(1,dtype=int)
nrun = n.zeros(1,dtype=int)
nlumi = n.zeros(1,dtype=int)
nevent = n.zeros(1,dtype=float)
npv = n.zeros(1,dtype=int)
rhoall = n.zeros(1,dtype=float)
rhocentral = n.zeros(1,dtype=float)
rhoneutral = n.zeros(1,dtype=float)
rhochargedpileup = n.zeros(1,dtype=float)

jet_pt  = n.zeros(maxjet,dtype=float)
pfjet_pt  = n.zeros(maxjet,dtype=float)
newjet_pt  = n.zeros(maxjet,dtype=float)

genjet_pt  = n.zeros(maxjet,dtype=float)
pfgenjet_pt  = n.zeros(maxjet,dtype=float)
newgenjet_pt  = n.zeros(maxjet,dtype=float)

genjet_eta  = n.zeros(maxjet,dtype=float)
pfgenjet_eta  = n.zeros(maxjet,dtype=float)
newgenjet_eta  = n.zeros(maxjet,dtype=float)

jet_eta = n.zeros(maxjet,dtype=float)
pfjet_eta = n.zeros(maxjet,dtype=float)
newjet_eta = n.zeros(maxjet,dtype=float)

genjet_phi  = n.zeros(maxjet,dtype=float)
pfgenjet_phi  = n.zeros(maxjet,dtype=float)
newgenjet_phi  = n.zeros(maxjet,dtype=float)

jet_phi = n.zeros(maxjet,dtype=float)
pfjet_phi = n.zeros(maxjet,dtype=float)
newjet_phi = n.zeros(maxjet,dtype=float)

charged = n.zeros(maxjet,dtype=float)
neutral = n.zeros(maxjet,dtype=float)
photon = n.zeros(maxjet,dtype=float)
muon = n.zeros(maxjet,dtype=float)
electron = n.zeros(maxjet,dtype=float)
hhf = n.zeros(maxjet,dtype=float)
ehf = n.zeros(maxjet,dtype=float)

pfcharged = n.zeros(maxjet,dtype=float)
pfneutral = n.zeros(maxjet,dtype=float)
pfphoton = n.zeros(maxjet,dtype=float)
pfmuon = n.zeros(maxjet,dtype=float)
pfelectron = n.zeros(maxjet,dtype=float)
pfhhf = n.zeros(maxjet,dtype=float)
pfehf = n.zeros(maxjet,dtype=float)

newcharged = n.zeros(maxjet,dtype=float)
newneutral = n.zeros(maxjet,dtype=float)
newphoton = n.zeros(maxjet,dtype=float)
newmuon = n.zeros(maxjet,dtype=float)
newelectron = n.zeros(maxjet,dtype=float)
newhhf = n.zeros(maxjet,dtype=float)
newehf = n.zeros(maxjet,dtype=float)

t.Branch("njet", njet, 'njet/I')
t.Branch("nnewjet", nnewjet, 'nnewjet/I')
t.Branch("npfjet", npfjet, 'npfjet/I')
t.Branch("run", nrun, 'run/I')
t.Branch("lumi", nlumi, 'lumi/I')
t.Branch("event", nevent, 'event/D')
t.Branch("npv", npv, 'npv/I')

t.Branch("rhoall", rhoall, 'rhoall/D')
t.Branch("rhocentral", rhocentral, 'rhocentral/D')
t.Branch("rhoneutral", rhoneutral, 'rhoneutral/D')
t.Branch("rhochargedpileup", rhochargedpileup, 'rhochargedpileup/D')

t.Branch("genjet_pt",genjet_pt,'genjet_pt[njet]/D')
t.Branch("pfgenjet_pt",pfgenjet_pt,'pfgenjet_pt[npfjet]/D')
t.Branch("newgenjet_pt",newgenjet_pt,'newgenjet_pt[nnewjet]/D')
t.Branch("pfjet_pt",pfjet_pt,'pfjet_pt[npfjet]/D')
t.Branch("newjet_pt",newjet_pt,'newjet_pt[nnewjet]/D')
t.Branch("jet_pt",jet_pt,'jet_pt[njet]/D')

t.Branch("genjet_eta",genjet_eta,'genjet_eta[njet]/D')
t.Branch("pfgenjet_eta",pfgenjet_eta,'pfgenjet_eta[npfjet]/D')
t.Branch("newgenjet_eta",newgenjet_eta,'newgenjet_eta[nnewjet]/D')

t.Branch("jet_eta",jet_eta,'jet_eta[njet]/D')
t.Branch("pfjet_eta",pfjet_eta,'pfjet_eta[npfjet]/D')
t.Branch("newjet_eta",newjet_eta,'newjet_eta[nnewjet]/D')

t.Branch("genjet_phi",genjet_phi,'genjet_phi[njet]/D')
t.Branch("pfgenjet_phi",pfgenjet_phi,'pfgenjet_phi[npfjet]/D')
t.Branch("newgenjet_phi",newgenjet_phi,'newgenjet_phi[nnewjet]/D')

t.Branch("jet_phi",jet_phi,'jet_phi[njet]/D')
t.Branch("pfjet_phi",pfjet_phi,'pfjet_phi[npfjet]/D')
t.Branch("newjet_phi",newjet_phi,'newjet_phi[nnewjet]/D')

t.Branch("ncharged",ncharged,'ncharged/I')

t.Branch("charged", charged, 'charged[njet]/D')
t.Branch("neutral", neutral, 'neutral[njet]/D')
t.Branch("photon", photon, 'photon[njet]/D')
t.Branch("muon", muon, 'muon[njet]/D')
t.Branch("electron", electron, 'electron[njet]/D')
t.Branch("hhf", hhf, 'hhf[njet]/D')
t.Branch("ehf", ehf, 'ehf[njet]/D')

t.Branch("pfcharged", pfcharged, 'pfcharged[npfjet]/D')
t.Branch("pfneutral", pfneutral, 'pfneutral[npfjet]/D')
t.Branch("pfphoton", pfphoton, 'pfphoton[npfjet]/D')
t.Branch("pfmuon", pfmuon, 'pfmuon[npfjet]/D')
t.Branch("pfelectron", pfelectron, 'pfelectron[npfjet]/D')
t.Branch("pfhhf", pfhhf, 'pfhhf[npfjet]/D')
t.Branch("pfehf", pfehf, 'pfehf[npfjet]/D')

t.Branch("newcharged", newcharged, 'newcharged[nnewjet]/D')
t.Branch("newneutral", newneutral, 'newneutral[nnewjet]/D')
t.Branch("newphoton", newphoton, 'newphoton[nnewjet]/D')
t.Branch("newmuon", newmuon, 'newmuon[nnewjet]/D')
t.Branch("newelectron", newelectron, 'newelectron[nnewjet]/D')
t.Branch("newhhf", newhhf, 'newhhf[nnewjet]/D')
t.Branch("newehf", newehf, 'newehf[nnewjet]/D')

# load FWLite C++ libraries
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.FWLiteEnabler.enable()

# load FWlite python libraries
from DataFormats.FWLite import Handle, Events

pfs, pfLabel = Handle("std::vector<pat::PackedCandidate>"), "packedPFCandidates"
jets, jetLabel = Handle("std::vector<pat::Jet>"), "selectedPatJetsAK4PFCHS"
vertex, vertexLabel = Handle("std::vector<reco::Vertex>"),"offlineSlimmedPrimaryVertices"

pfjets, pfjetLabel = Handle("std::vector<pat::Jet>"), "selectedPatJetsAK4PF"
newjets, newjetLabel = Handle("std::vector<pat::Jet>"), "selectedPatJetsAK4PFnewCHS"


rhoall_, rhoallLabel = Handle("double"), "fixedGridRhoFastjetAll"
rhocentral_, rhocentralLabel = Handle("double"), "fixedGridRhoFastjetCentral"
rhoneutral_, rhoneutralLabel = Handle("double"), "fixedGridRhoFastjetCentralNeutral"
rhochargedpileup_, rhochargedpileupLabel = Handle("double"), "fixedGridRhoFastjetCentralChargedPileUp"

# open file (you can use 'edmFileUtil -d /store/whatever.root' to get the physical file name)
events = Events(
    "file:test.root")
    # flat,pu0-70
    #"file:/eos/cms/store/mc/RunIISummer17MiniAOD/QCD_Pt-15to7000_TuneCUETP8M1_Flat_13TeV_pythia8/MINIAODSIM/FlatPU0to70_magnetOn_92X_upgrade2017_realistic_v10-v1/70000/BE3567C8-589A-E711-9B72-0CC47A13D16E.root")
    # no pu sample
    #"file:/eos/cms/store/mc/RunIISummer17MiniAOD/QCD_Pt-15to7000_TuneCUETP8M1_Flat_13TeV_pythia8/MINIAODSIM/NoPU_magnetOn_92X_upgrade2017_realistic_v10-v1/10000/7CE31FF1-3E9E-E711-BCF2-0CC47A00941C.root")

associate = {
    0: 'NotReconstructedPrimary',
    1: 'OtherDeltaZ',
    4: 'CompatibilityBTag',
    5: 'CompatibilityDz',
    6: 'UsedInFitLoose',
    7: 'UsedInFitTight'
}


#for ievent,event in enumerate(events):
for ievent,event in enumerate(events):
    
    if ievent >1000000 : continue

    event.getByLabel(jetLabel, jets)
    event.getByLabel(newjetLabel, newjets)
    event.getByLabel(pfjetLabel, pfjets)
    event.getByLabel(pfLabel, pfs)
    event.getByLabel(vertexLabel, vertex)

    event.getByLabel(rhoallLabel,rhoall_)
    event.getByLabel(rhocentralLabel,rhocentral_)
    event.getByLabel(rhoneutralLabel,rhoneutral_)
    event.getByLabel(rhochargedpileupLabel,rhochargedpileup_)

    rhoall[0] = rhoall_.product()[0]
    rhocentral[0] = rhocentral_.product()[0]
    rhoneutral[0] = rhoneutral_.product()[0]
    rhochargedpileup[0] = rhochargedpileup_.product()[0]


    #print "\nEvent %d: run %6d, lumi %4d, event %12d" % (ievent,event.eventAuxiliary().run(), event.eventAuxiliary().luminosityBlock(),event.eventAuxiliary().event())

    nrun[0]   = event.eventAuxiliary().run()
    nlumi[0]  = event.eventAuxiliary().luminosityBlock()
    nevent[0] = event.eventAuxiliary().event()
    npv[0]    = vertex.product().size()

    njet[0]    = jets.product().size()
    npfjet[0]  = pfjets.product().size()
    nnewjet[0] = newjets.product().size()



    ##PF Jets

    for i,j in enumerate(pfjets.product()):
        if i>=maxjet: break

        pfjet_pt[i] = j.pt()*j.jecFactor("Uncorrected")
        pfjet_eta[i] = j.eta()
        pfjet_phi[i] = j.phi()

        if not (j.genJet() == None):
            pfgenjet_pt[i] = j.genJet().pt()
            pfgenjet_eta[i] = j.genJet().eta()
            pfgenjet_phi[i] = j.genJet().phi()

        else:
            pfgenjet_pt[i] = -999.

        pfsourceCandidate = set()
        # now get a list of the PF candidates used to build this jet
        for isource in xrange(j.numberOfSourceCandidatePtrs()):
            pfsourceCandidate.add(j.sourceCandidatePtr(isource).key()) # the key is the index in the pf collection


        pfneutral[i], pfcharged[i], pfphoton[i], pfmuon[i], pfelectron[i], pfhhf[i], pfehf[i], pileup = 0, 0, 0, 0, 0, 0, 0, 0

        for ipf,pf in enumerate(pfs.product()):

            # if pf candidate is part of the jet, lets categorize
            if ipf in pfsourceCandidate:

                if ( abs(pf.pdgId()) == 211 ):
                    pfcharged[i] += pf.pt();
                    
                elif abs(pf.pdgId()) == 130:
                    pfneutral[i] += pf.pt();

                elif abs(pf.pdgId()) == 22:
                    pfphoton[i] += pf.pt();

                elif abs(pf.pdgId()) == 13:
                    pfmuon[i] += pf.pt();

                elif abs(pf.pdgId()) == 11:
                    pfelectron[i] += pf.pt();

                elif abs(pf.pdgId()) == 1:
                    pfhhf[i] += pf.pt();

                elif abs(pf.pdgId()) == 2:
                    pfehf[i] += pf.pt();
                
                else:
                    pileup += pf.pt()


    ##### NEW CHS JETS

    for i,j in enumerate(newjets.product()):
        if i>=maxjet: break

        newjet_pt[i] = j.pt()*j.jecFactor("Uncorrected")
        newjet_eta[i] = j.eta()
        newjet_phi[i] = j.phi()

        if not (j.genJet() == None):
            newgenjet_pt[i] = j.genJet().pt()
            newgenjet_eta[i] = j.genJet().eta()
            newgenjet_phi[i] = j.genJet().phi()

        else:
            newgenjet_pt[i] = -999.

        newsourceCandidate = set()

        # now get a list of the PF candidates used to build this jet
        for isource in xrange(j.numberOfSourceCandidatePtrs()):
            newsourceCandidate.add(j.sourceCandidatePtr(isource).key()) # the key is the index in the pf collection


        newneutral[i], newcharged[i], newphoton[i], newmuon[i], newelectron[i], newhhf[i], newehf[i], pileup = 0, 0, 0, 0, 0, 0, 0, 0

        for ipf,pf in enumerate(pfs.product()):

            # if pf candidate is part of the jet, lets categorize
            if ipf in newsourceCandidate:

                if ( abs(pf.pdgId()) == 211 ):
                    newcharged[i] += pf.pt();
                    
                elif abs(pf.pdgId()) == 130:
                    newneutral[i] += pf.pt();

                elif abs(pf.pdgId()) == 22:
                    newphoton[i] += pf.pt();

                elif abs(pf.pdgId()) == 13:
                    newmuon[i] += pf.pt();

                elif abs(pf.pdgId()) == 11:
                    newelectron[i] += pf.pt();

                elif abs(pf.pdgId()) == 1:
                    newhhf[i] += pf.pt();

                elif abs(pf.pdgId()) == 2:
                    newehf[i] += pf.pt();
                
                else:
                    pileup += pf.pt()



    ###CHS JETS

    for i,j in enumerate(jets.product()):

        if i>=maxjet: break

        jet_pt[i] = j.pt()*j.jecFactor("Uncorrected")
        jet_eta[i] = j.eta()
        jet_phi[i] = j.phi()

        if not (j.genJet() == None):
            genjet_pt[i] = j.genJet().pt()
            genjet_eta[i] = j.genJet().eta()
            genjet_phi[i] = j.genJet().phi()

        else:
            genjet_pt[i] = -999.


        sourceCandidate = set()

        # now get a list of the PF candidates used to build this jet
        for isource in xrange(j.numberOfSourceCandidatePtrs()):
            sourceCandidate.add(j.sourceCandidatePtr(isource).key()) # the key is the index in the pf collection

        #debug
        #print sourceCandidate

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


    t.Fill()


fout.Write()
fout.Close()
