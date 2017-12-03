# Standard importts
import os,sys,socket,argparse
import os
import ROOT
import math
from array import array
from tdrStyle import *
setTDRStyle()
ROOT.gROOT.SetBatch(True)

# RooFit
ROOT.gSystem.Load("libRooFit.so")
ROOT.gSystem.Load("libRooFitCore.so")
ROOT.gROOT.SetStyle("Plain") # Not sure this is needed
ROOT.gSystem.SetIncludePath( "-I$ROOFITSYS/include/" )

def ConvFit( shape, isData, var_name, label, fit_plot_directory, fit_filename = None):

    print "Performing a fit using gaus x landau to get the mean and the width" 
    # declare the observable mean, and import the histogram to a RooDataHist

    tmp_mean = shape.GetMean()
    tmp_sigma = shape.GetRMS()

    asymmetry   = ROOT.RooRealVar(var_name,label,tmp_mean-5*tmp_sigma,tmp_mean+6*tmp_sigma) ;
    dh          = ROOT.RooDataHist("datahistshape","datahistshape",ROOT.RooArgList(asymmetry),ROOT.RooFit.Import(shape)) ;
    
    # plot the data hist with error from sum of weighted events
    frame       = asymmetry.frame(ROOT.RooFit.Title(var_name))
    if isData:
        dh.plotOn(frame,ROOT.RooFit.DataError(ROOT.RooAbsData.Poisson))
    else:
        dh.plotOn(frame,ROOT.RooFit.DataError(ROOT.RooAbsData.SumW2)) ;


    # create a simple gaussian pdf
    gauss_mean  = ROOT.RooRealVar("mean","mean",0)
    gauss_sigma = ROOT.RooRealVar("sigma","sigma gauss",tmp_sigma,0,2.0)
    gauss       = ROOT.RooGaussian("gauss","gauss",asymmetry,gauss_mean,gauss_sigma) 

    landau_mean  = ROOT.RooRealVar("meanl","mean landau",1,0.70,1.5)
    landau_sigma = ROOT.RooRealVar("sigmal","sigma landau",tmp_sigma,0,2.0)
    landau       = ROOT.RooLandau("landau","landau",asymmetry,landau_mean,landau_sigma)

    lxg = ROOT.RooFFTConvPdf("lxg","landau x gauss",asymmetry,landau,gauss)

    # now do the fit and extract the parameters with the correct error
    if isData: 
        gauss.fitTo(dh,ROOT.RooFit.Save(),ROOT.RooFit.Range(dh.mean(asymmetry)-2*dh.sigma(asymmetry),dh.mean(asymmetry)+2*dh.sigma(asymmetry)))
    else:
        #lxg.fitTo(dh,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(True),ROOT.RooFit.Range(dh.mean(asymmetry)-3*dh.sigma(asymmetry),dh.mean(asymmetry)+4*dh.sigma(asymmetry)))
        lxg.fitTo(dh,ROOT.RooFit.Save(),ROOT.RooFit.SumW2Error(True))

    lxg.plotOn(frame)

    argset_fit = ROOT.RooArgSet(gauss_mean,gauss_sigma)
    lxg.paramOn(frame,ROOT.RooFit.Format("NELU",ROOT.RooFit.AutoPrecision(1)),ROOT.RooFit.Layout(0.55)) 
    frame.SetMaximum(frame.GetMaximum()*1.2)

    # add chi2 info
    chi2_text = ROOT.TPaveText(0.3,0.8,0.4,0.9,"BRNDC")
    chi2_text.AddText("#chi^{2} fit = %s" %round(frame.chiSquare(6),2))
    chi2_text.SetTextSize(0.04)
    chi2_text.SetTextColor(2)
    chi2_text.SetShadowColor(0)
    chi2_text.SetFillColor(0)
    chi2_text.SetLineColor(0)
    frame.addObject(chi2_text)

    if fit_filename is not None:
        c = ROOT.TCanvas("cfit","cfit",600,700)
        frame.Draw()
        if not os.path.exists(fit_plot_directory): os.makedirs(fit_plot_directory)
        c.SaveAs(os.path.join( fit_plot_directory, fit_filename+".pdf"))
        c.SaveAs(os.path.join( fit_plot_directory, fit_filename+".png"))
        del c

    mean_asymmetry        = landau_mean.getVal()
    mean_asymmetry_error  = landau_mean.getError()

    rms_asymmetry        = gauss_sigma.getVal()
    rms_asymmetry_error  = gauss_sigma.getError()

    #if the chi2 is going crazy default to the mean and rms of the histogram
    if frame.chiSquare(6)  > 100:
        mean_asymmetry = tmp_mean
        rms_asymmetry  = tmp_sigma

    return mean_asymmetry, mean_asymmetry_error, rms_asymmetry, rms_asymmetry_error

def fraction(charged,neutral,photon,electron,muon,hhf,ehf,pt1,pt2,eta1,eta2,jet):
    
    h_charged  = TH1F("hch" ,"hch",100,0,1)
    h_neutral  = TH1F("hnh" ,"hnh",100,0,1)
    h_photon   = TH1F("hph" ,"hph",100,0,1)
    h_muon     = TH1F("hmu" ,"hmu",100,0,1)
    h_electron = TH1F("hel" ,"hel",100,0,1)
    h_hhf      = TH1F("hhhf","hhhf",100,0,1)
    h_ehf      = TH1F("hehf","hehf",100,0,1)

    sum_jet = charged + neutral + photon + electron + muon + hhf + ehf

    cut_gen = "("+jet+"genjet_pt>0)"

    t_in.Draw(charged+"/"+sum_jet+">>hch",
              sum_jet+">"+str(pt1)+" && "+sum_jet+"<"+str(pt2)+" && "+cut_gen+" && abs("+jet+"jet_eta)>="+str(eta1)+" && abs("+jet+"jet_eta)<"+str(eta2),"goff")

    t_in.Draw(neutral+"/"+sum_jet+">>hnh",
              sum_jet+">"+str(pt1)+" && "+sum_jet+"<"+str(pt2)+" && "+cut_gen+" && abs("+jet+"jet_eta)>="+str(eta1)+" && abs("+jet+"jet_eta)<"+str(eta2),"goff")

    t_in.Draw(photon+"/"+sum_jet+">>hph",
              sum_jet+">"+str(pt1)+" && "+sum_jet+"<"+str(pt2)+" && "+cut_gen+" && abs("+jet+"jet_eta)>="+str(eta1)+" && abs("+jet+"jet_eta)<"+str(eta2),"goff")

    t_in.Draw(muon+"/"+sum_jet+">>hmu",
              sum_jet+">"+str(pt1)+" && "+sum_jet+"<"+str(pt2)+" && "+cut_gen+" && abs("+jet+"jet_eta)>="+str(eta1)+" && abs("+jet+"jet_eta)<"+str(eta2),"goff")

    t_in.Draw(electron+"/"+sum_jet+">>hel",
              sum_jet+">"+str(pt1)+" && "+sum_jet+"<"+str(pt2)+" && "+cut_gen+" && abs("+jet+"jet_eta)>="+str(eta1)+" && abs("+jet+"jet_eta)<"+str(eta2),"goff")

    t_in.Draw(hhf+"/"+sum_jet+">>hhf",
              sum_jet+">"+str(pt1)+" && "+sum_jet+"<"+str(pt2)+" && "+cut_gen+" && abs("+jet+"jet_eta)>="+str(eta1)+" && abs("+jet+"jet_eta)<"+str(eta2),"goff")

    t_in.Draw(hef+"/"+sum_jet+">>hef",
              sum_jet+">"+str(pt1)+" && "+sum_jet+"<"+str(pt2)+" && "+cut_gen+" && abs("+jet+"jet_eta)>="+str(eta1)+" && abs("+jet+"jet_eta)<"+str(eta2),"goff")


    return h_charged.GetMean(), h_neutral.GetMean(), h_photon.GetMean(), h_muon.GetMean(), h_electron.GetMean(), h_hhf.GetMean(), h_ehf.GetMean()
    
