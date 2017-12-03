import numpy as n

rhoall     = n.zeros(1,dtype=float)
maxjet = 10000
    
    #event information
nrun       = n.zeros(1,dtype=int)
nlumi      = n.zeros(1,dtype=int)
nevent     = n.zeros(1,dtype=float)
npv        = n.zeros(1,dtype=int)
rhoall     = n.zeros(1,dtype=float)
rhocentral = n.zeros(1,dtype=float)
rhoneutral = n.zeros(1,dtype=float)
rhochargedpileup = n.zeros(1,dtype=float)

    #jet information
njet       = n.zeros(1,dtype=int)
jet_pt     = n.zeros(maxjet,dtype=float)
jet_eta    = n.zeros(maxjet,dtype=float)
jet_phi    = n.zeros(maxjet,dtype=float)
genjet_pt  = n.zeros(maxjet,dtype=float)
genjet_eta = n.zeros(maxjet,dtype=float)
genjet_phi = n.zeros(maxjet,dtype=float)
rawjet_pt  = n.zeros(maxjet,dtype=float)
rawjet_eta = n.zeros(maxjet,dtype=float)
rawjet_phi = n.zeros(maxjet,dtype=float)

    #jet fraction information for each jet
charged    = n.zeros(maxjet,dtype=float)
neutral    = n.zeros(maxjet,dtype=float)
photon     = n.zeros(maxjet,dtype=float)
muon       = n.zeros(maxjet,dtype=float)
electron   = n.zeros(maxjet,dtype=float)
hhf        = n.zeros(maxjet,dtype=float)
ehf        = n.zeros(maxjet,dtype=float)

    #met information
met    = n.zeros(1,dtype=float)
genmet = n.zeros(1,dtype=float)
rawmet = n.zeros(1,dtype=float)
#chsmet = n.zeros(1,dtype=float)
#trkmet = n.zeros(1,dtype=float)
#phomet = n.zeros(1,dtype=float)
#neumet = n.zeros(1,dtype=float)
    
def declare_branches(t):

    t.Branch("run", nrun, 'run/I')
    t.Branch("lumi", nlumi, 'lumi/I')
    t.Branch("event", nevent, 'event/D')
    t.Branch("npv", npv, 'npv/I')

    t.Branch("rhoall", rhoall, 'rhoall/D')
    t.Branch("rhocentral", rhocentral, 'rhocentral/D')
    t.Branch("rhoneutral", rhoneutral, 'rhoneutral/D')
    t.Branch("rhochargedpileup", rhochargedpileup, 'rhochargedpileup/D')

    t.Branch("njet", njet, 'njet/I')

    t.Branch("jet_pt",jet_pt,'jet_pt[njet]/D')
    t.Branch("jet_eta",jet_eta,'jet_eta[njet]/D')
    t.Branch("jet_phi",jet_phi,'jet_phi[njet]/D')

    t.Branch("genjet_pt",genjet_pt,'genjet_pt[njet]/D')
    t.Branch("genjet_eta",genjet_eta,'genjet_eta[njet]/D')
    t.Branch("genjet_phi",genjet_phi,'genjet_phi[njet]/D')

    t.Branch("rawjet_pt",rawjet_pt,'rawjet_pt[njet]/D')
    t.Branch("rawjet_eta",rawjet_eta,'rawjet_eta[njet]/D')
    t.Branch("rawjet_phi",rawjet_phi,'rawjet_phi[njet]/D')

    t.Branch("charged", charged, 'charged[njet]/D')
    t.Branch("neutral", neutral, 'neutral[njet]/D')
    t.Branch("photon", photon, 'photon[njet]/D')
    t.Branch("muon", muon, 'muon[njet]/D')
    t.Branch("electron", electron, 'electron[njet]/D')
    t.Branch("hhf", hhf, 'hhf[njet]/D')
    t.Branch("ehf", ehf, 'ehf[njet]/D')

    t.Branch("met", met, 'met/D')
    t.Branch("genmet", genmet, 'genmet/D')
    t.Branch("rawmet", rawmet, 'rawmet/D')
    #t.Branch("chsmet", chsmet, 'chsmet/D')
    #t.Branch("trkmet", trkmet, 'trkmet/D')
    #t.Branch("phomet", phomet, 'phomet/D')
    #t.Branch("neumet", neumet, 'neumet/D')


    print "All branches configured"
