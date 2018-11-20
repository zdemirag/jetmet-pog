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
dphipfmet = n.zeros(1,dtype=float)

    #jet information
njet       = n.zeros(1,dtype=int)
jet_pt     = n.zeros(maxjet,dtype=float)
jet_energy = n.zeros(maxjet,dtype=float)
jet_eta    = n.zeros(maxjet,dtype=float)
jet_phi    = n.zeros(maxjet,dtype=float)
genjet_pt  = n.zeros(maxjet,dtype=float)
genjet_energy = n.zeros(maxjet,dtype=float)
genjet_eta = n.zeros(maxjet,dtype=float)
genjet_phi = n.zeros(maxjet,dtype=float)
rawjet_pt  = n.zeros(maxjet,dtype=float)
rawjet_energy = n.zeros(maxjet,dtype=float)
rawjet_eta = n.zeros(maxjet,dtype=float)
rawjet_phi = n.zeros(maxjet,dtype=float)
jet_loose  = n.zeros(maxjet,dtype=int)


#jet energy fraction
NHF = n.zeros(maxjet,dtype=float)
NEMF = n.zeros(maxjet,dtype=float)
CHF = n.zeros(maxjet,dtype=float)
MUF = n.zeros(maxjet,dtype=float)
CEMF = n.zeros(maxjet,dtype=float)
NumConst = n.zeros(maxjet,dtype=int)
NumNeutralParticle = n.zeros(maxjet,dtype=int)
CHM = n.zeros(maxjet,dtype=int)


    #jet fraction information for each jet
charged    = n.zeros(maxjet,dtype=float)
neutral    = n.zeros(maxjet,dtype=float)
photon     = n.zeros(maxjet,dtype=float)
muon       = n.zeros(maxjet,dtype=float)
electron   = n.zeros(maxjet,dtype=float)
hhf        = n.zeros(maxjet,dtype=float)
ehf        = n.zeros(maxjet,dtype=float)
other      = n.zeros(maxjet,dtype=float)

charged_e  = n.zeros(maxjet,dtype=float)
neutral_e  = n.zeros(maxjet,dtype=float)
photon_e   = n.zeros(maxjet,dtype=float)
muon_e     = n.zeros(maxjet,dtype=float)
electron_e = n.zeros(maxjet,dtype=float)
hhf_e      = n.zeros(maxjet,dtype=float)
ehf_e      = n.zeros(maxjet,dtype=float)
other_e    = n.zeros(maxjet,dtype=float)

charged_n  = n.zeros(maxjet,dtype=int)
neutral_n  = n.zeros(maxjet,dtype=int)
photon_n   = n.zeros(maxjet,dtype=int)
muon_n     = n.zeros(maxjet,dtype=int)
electron_n = n.zeros(maxjet,dtype=int)
hhf_n      = n.zeros(maxjet,dtype=int)
ehf_n      = n.zeros(maxjet,dtype=int)
other_n    = n.zeros(maxjet,dtype=int)

    #met information
met    = n.zeros(1,dtype=float)
mex    = n.zeros(1,dtype=float)
mey    = n.zeros(1,dtype=float)
met_phi= n.zeros(1,dtype=float)
genmet = n.zeros(1,dtype=float)
rawmet = n.zeros(1,dtype=float)
#charged_met = n.zeros(1,dtype=float)
#neutral_met = n.zeros(1,dtype=float)
#photon_met = n.zeros(1,dtype=float)
#muon_met = n.zeros(1,dtype=float)
#electron_met = n.zeros(1,dtype=float)
#hhf_met = n.zeros(1,dtype=float)
#ehf_met = n.zeros(1,dtype=float)
#other_met = n.zeros(1,dtype=float)
#chsmet = n.zeros(1,dtype=float)
#trkmet = n.zeros(1,dtype=float)
#phomet = n.zeros(1,dtype=float)
#neumet = n.zeros(1,dtype=float)
    
def declare_branches(t):

    t.Branch("run", nrun, 'run/I')
    t.Branch("lumi", nlumi, 'lumi/I')
    t.Branch("event", nevent, 'event/D')
    t.Branch("npv", npv, 'npv/I')

    t.Branch("dphipfmet", dphipfmet, 'dphipfmet/D')

    t.Branch("rhoall", rhoall, 'rhoall/D')
    t.Branch("rhocentral", rhocentral, 'rhocentral/D')
    t.Branch("rhoneutral", rhoneutral, 'rhoneutral/D')
    t.Branch("rhochargedpileup", rhochargedpileup, 'rhochargedpileup/D')

    t.Branch("njet", njet, 'njet/I')

    t.Branch("jet_pt",jet_pt,'jet_pt[njet]/D')
    t.Branch("jet_energy",jet_energy,'jet_energy[njet]/D')
    t.Branch("jet_eta",jet_eta,'jet_eta[njet]/D')
    t.Branch("jet_phi",jet_phi,'jet_phi[njet]/D')

    t.Branch("genjet_pt",genjet_pt,'genjet_pt[njet]/D')
    t.Branch("genjet_energy",genjet_energy,'genjet_energy[njet]/D')
    t.Branch("genjet_eta",genjet_eta,'genjet_eta[njet]/D')
    t.Branch("genjet_phi",genjet_phi,'genjet_phi[njet]/D')

    t.Branch("rawjet_pt",rawjet_pt,'rawjet_pt[njet]/D')
    t.Branch("rawjet_energy",rawjet_energy,'rawjet_energy[njet]/D')
    t.Branch("rawjet_eta",rawjet_eta,'rawjet_eta[njet]/D')
    t.Branch("rawjet_phi",rawjet_phi,'rawjet_phi[njet]/D')

    t.Branch("NHF",NHF,'NHF[njet]/D')
    t.Branch("NEMF",NEMF,'NEMF[njet]/D')
    t.Branch("CHF",CHF,'CHF[njet]/D')
    t.Branch("MUF",MUF,'MUF[njet]/D')
    t.Branch("CEMF",CEMF,'CEMF[njet]/D')
    t.Branch("NumConst",NumConst,'NumConst[njet]/I')
    t.Branch("NumNeutralParticle",NumNeutralParticle,'NumNeutralParticle[njet]/I')
    t.Branch("CHM",CHM,'CHM[njet]/I')

    t.Branch("jet_loose",jet_loose,'jet_loose[njet]/I')

    t.Branch("charged", charged, 'charged[njet]/D')
    t.Branch("neutral", neutral, 'neutral[njet]/D')
    t.Branch("photon", photon, 'photon[njet]/D')
    t.Branch("muon", muon, 'muon[njet]/D')
    t.Branch("electron", electron, 'electron[njet]/D')
    t.Branch("hhf", hhf, 'hhf[njet]/D')
    t.Branch("ehf", ehf, 'ehf[njet]/D')
    t.Branch("other", other, 'other[njet]/D')

    t.Branch("charged_e", charged_e, 'charged_e[njet]/D')
    t.Branch("neutral_e", neutral_e, 'neutral_e[njet]/D')
    t.Branch("photon_e", photon_e, 'photon_e[njet]/D')
    t.Branch("muon_e", muon_e, 'muon_e[njet]/D')
    t.Branch("electron_e", electron_e, 'electron_e[njet]/D')
    t.Branch("hhf_e", hhf_e, 'hhf_e[njet]/D')
    t.Branch("ehf_e", ehf_e, 'ehf_e[njet]/D')
    t.Branch("other_e", other_e, 'other_e[njet]/D')

    t.Branch("charged_n", charged_n, 'charged_n[njet]/I')
    t.Branch("neutral_n", neutral_n, 'neutral_n[njet]/I')
    t.Branch("photon_n", photon_n, 'photon_n[njet]/I')
    t.Branch("muon_n", muon_n, 'muon_n[njet]/I')
    t.Branch("electron_n", electron_n, 'electron_n[njet]/I')
    t.Branch("hhf_n", hhf_n, 'hhf_n[njet]/I')
    t.Branch("ehf_n", ehf_n, 'ehf_n[njet]/I')
    t.Branch("other_n", other_n, 'other_n[njet]/I')

    t.Branch("met", met, 'met/D')
    t.Branch("mex", mex, 'mex/D')
    t.Branch("mey", mey, 'mey/D')
    t.Branch("met_phi", met_phi, 'met_phi/D')
    t.Branch("genmet", genmet, 'genmet/D')
    t.Branch("rawmet", rawmet, 'rawmet/D')
    #t.Branch("charged_met", charged_met, 'charged_met/D')
    #t.Branch("neutral_met", neutral_met, 'neutral_met/D')
    #t.Branch("photon_met", photon_met, 'photon_met/D')
    #t.Branch("muon_met", muon_met, 'muon_met/D')
    #t.Branch("electron_met", electron_met, 'electron_met/D')
    #t.Branch("hhf_met", hhf_met, 'hhf_met/D')
    #t.Branch("ehf_met", ehf_met, 'ehf_met/D')
    #t.Branch("other_met", other_met, 'other_met/D')


    print "All branches configured"
