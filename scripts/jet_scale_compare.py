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

from helper_functions import *

_pt  = [20,50,100,200,500,2000]
#_pt  = [20,30,40,50,100,200,500,2000]
_eta = [0,1.3,2.1,2.5,3.0,5.0]

def prepare(name,input_file, other1, other2, rho0, rho1, folder, pt=True):
    
    f_in = ROOT.TFile(input_file,"READ")
    t_in = f_in.Get("events")

    if pt:
        h_mean    = ROOT.TH1F("h_mean","h_mean",len(_pt)-1,array('d',_pt))
        h_sigma   = ROOT.TH1F("h_sigma","h_sigma",len(_pt)-1,array('d',_pt))
        h_sigma11 = ROOT.TH1F("h_sigma11","h_sigma11",len(_pt)-1,array('d',_pt))
    else:
        h_mean    = ROOT.TH1F("h_mean","h_mean",len(_eta)-1,array('d',_eta))
        h_sigma   = ROOT.TH1F("h_sigma","h_sigma",len(_eta)-1,array('d',_eta))
        h_sigma11 = ROOT.TH1F("h_sigma11","h_sigma11",len(_eta)-1,array('d',_eta))
        
    if pt:
        parameter = _pt
        other    = _eta
        cutparam = "genjet_pt"
        setparam = "abs(genjet_eta)"
    else:
        parameter = _eta
        other    = _pt
        cutparam = "abs(genjet_eta)"
        setparam = "genjet_pt"        

    for i in range(0,len(parameter)-1):

        shape  = ROOT.TH1F("shape","shape",50,0.25,2.5)

        #add here the new and old sum

        chs_sum = "(charged    + neutral    + photon    + muon    + electron    + hhf    + ehf)"        
        rho_cut = " && rhoall>="+str(rho0)+" && rhoall<"+str(rho1)

        t_in.Draw("rawjet_pt/(genjet_pt)>>shape",cutparam+">"+str(parameter[i])+" && "+cutparam+"<"+str(parameter[i+1])+" && "+setparam+">="+str(other1)+" && "+setparam+"<"+str(other2)+rho_cut,"goff")

        mean, mean_error, sigma, sigma_error = ConvFit(shape ,False,"ratio","jet pt/gen jet pt",folder+"/fit","FIT_pf_"+str(parameter[i])+"_"+str(other1))

        h_mean.SetBinContent(i+1,mean)
        h_mean.SetBinError(i+1,mean_error)

        #scale correct the resolution
        if mean>0:
            h_sigma.SetBinContent(i+1,sigma/mean)
        else:
            h_sigma.SetBinContent(i+1,0)

        h_sigma11.SetBinContent(i+1,sigma)
        h_sigma11.SetBinError(i+1,sigma_error)
        h_sigma.SetBinError(i+1,sigma_error)

    h_mean.SetDirectory(0)
    h_sigma.SetDirectory(0)
    h_sigma11.SetDirectory(0)
    return h_mean, h_sigma, h_sigma11


def main():
    
    parser = argparse.ArgumentParser(description='Plot resolution and response')
    parser.add_argument("-o", "--output"  ,dest="output"  , help="output folder name", type=str)
    parser.add_argument("-p", "--putype"  ,dest="pu"      , help="define the sample, options are 'flatpu','nopu'",type=str)
    parser.add_argument("-e", "--eta"     ,dest="eta"     , help="define the eta range, options are '0_1p3','1p3_2p1',2p1_2p5','2p5_3p0', '3p0_5p0'",type=str)
    parser.add_argument("-r", "--rho"     ,dest="rho"     , help="define the rho range",type=str)
    args = parser.parse_args()    

    _rho = [float(args.rho.split("_")[0]), float(args.rho.split("_")[1])]
    _other = [float(args.eta.split("_")[0].replace("p",".")), float(args.eta.split("_")[1].replace("p","."))]

    folder = args.output+"/"+args.pu+"/"
    os.system("mkdir -p "+folder)
    os.system("mkdir -p "+folder+"/fit")

    h_mean, h_sigma, h_sigma11   = prepare("test1","../output/QCD_FlatPt_v2_SRtest1_numEvent5000.root",_other[0],_other[1],_rho[0],_rho[1], folder,pt=True)
    h_mean2, h_sigma2, h_sigma21 = prepare("../output/QCD_FlatPt_v2_SRtest2_numEvent5000.root",_other[0],_other[1],_rho[0],_rho[1], folder,pt=True)
    h_mean3, h_sigma3, h_sigma31 = prepare("../output/QCD_FlatPt_v2_SRtest3_numEvent5000.root",_other[0],_other[1],_rho[0],_rho[1], folder,pt=True)
    h_mean4, h_sigma4, h_sigma41 = prepare("../output/QCD_FlatPt_v2_SRtest4_numEvent10000.root",_other[0],_other[1],_rho[0],_rho[1], folder,pt=True)
    #h_mean5, h_sigma5, h_sigma51 = prepare("../output/QCD_FlatPt_v2_SRtest5_numEvent10000.root",_other[0],_other[1],_rho[0],_rho[1], folder,pt=True)
    #h_mean6, h_sigma6, h_sigma61 = prepare("../output/QCD_FlatPt_v2_SRoff_numEvent10000.root",_other[0],_other[1],_rho[0],_rho[1], folder,pt=True)
    h_mean5, h_sigma5, h_sigma51 = prepare("../output/QCD_FlatPt_v2_SRtest6_numEvent10000.root",_other[0],_other[1],_rho[0],_rho[1], folder,pt=True)
    h_mean6, h_sigma6, h_sigma61 = prepare("../output/QCD_FlatPt_v2_SRtest7_numEvent10000.root",_other[0],_other[1],_rho[0],_rho[1], folder,pt=True)
    h_mean7, h_sigma7, h_sigma71 = prepare("../output/QCD_FlatPt_v2_SRon_numEvent10000.root",_other[0],_other[1],_rho[0],_rho[1], folder,pt=True)


    print h_mean.GetTitle()

    c = ROOT.TCanvas("mean","mean", 600, 600)
    c.cd()
    c.SetLogx()
    ROOT.gStyle.SetOptStat(False)
    h_mean.SetTitle("")
    h_mean.GetXaxis().SetTitle("Gen jet p_{T} [GeV]")
    h_mean.GetYaxis().SetTitle("Response")
    h_mean.GetXaxis().SetTitleOffset(1.2)
    h_mean.GetYaxis().SetTitleOffset(1.3)
    h_mean.SetMaximum(1.2)
    h_mean.SetMinimum(0.65)
    h_mean.SetLineWidth(2)

    h_mean.SetLineColor(ROOT.kGreen+2)
    h_mean.Draw("l")
    h_mean2.SetLineColor(ROOT.kOrange+2)
    h_mean2.Draw("lsame")
    h_mean3.SetLineColor(ROOT.kCyan+3)
    #h_mean3.Draw("lsame")
    h_mean4.SetLineColor(ROOT.kMagenta+2)
    h_mean4.Draw("lsame")

    h_mean5.SetLineColor(ROOT.kGray+2)
    h_mean5.Draw("lsame")
    h_mean6.SetLineColor(ROOT.kCyan+3)
    h_mean6.Draw("lsame")

    h_mean7.SetLineColor(1)
    h_mean7.Draw("lsame")

    legend = ROOT.TLegend(0.30, 0.65, 0.65, .85);
    legend . AddEntry(h_mean, "test 1" , "l")
    legend . AddEntry(h_mean2,"test 2" , "l")
    #legend . AddEntry(h_mean3,"test 3" , "l")
    legend . AddEntry(h_mean4,"test 4" , "l")
    legend . AddEntry(h_mean5,"test 6" , "l")
    legend . AddEntry(h_mean6,"test 7" , "l")
    legend . AddEntry(h_mean7,"test 0" , "l")

    legend.Draw("same")

    latex2 = ROOT.TLatex()
    latex2.SetNDC()
    latex2.SetTextSize(0.4*c.GetTopMargin())
    latex2.SetTextFont(42)
    latex2.SetTextAlign(31) # align right                                                     
    latex2.DrawLatex(0.90, 0.93,str(_other[0])+" < #eta <"+ str(_other[1]) + ", "+ str(_rho[0])+" < #rho < " + str(_rho[1]))
    
    latex2.Draw("same")
        
    c.SaveAs(folder+"FIT_mean_eta_"+args.eta+"_rho_"+args.rho+".png")
    c.SaveAs(folder+"FIT_mean_eta_"+args.eta+"_rho_"+args.rho+".pdf")
    
    c1 = ROOT.TCanvas("sigma","sigma", 600, 600)
    c1.cd()
    c1.SetLogx()
    h_sigma.GetXaxis().SetTitle("Gen jet p_{T} [GeV]")
    h_sigma.GetYaxis().SetTitle("Resolution / Response")
    h_sigma.SetTitle("")
    h_sigma.GetXaxis().SetTitleOffset(1.2)
    h_sigma.GetYaxis().SetTitleOffset(1.3)
    h_sigma.SetLineWidth(2)
    h_sigma.SetMaximum(0.4)
    h_sigma.SetMinimum(0)

    h_sigma.SetLineColor(ROOT.kGreen+2)
    h_sigma.Draw()
    h_sigma2.SetLineColor(ROOT.kOrange+2)
    h_sigma2.Draw("lsame")
    h_sigma3.SetLineColor(ROOT.kCyan+3)
    #h_sigma3.Draw("lsame")
    h_sigma4.SetLineColor(ROOT.kMagenta+2)
    h_sigma4.Draw("lsame")
    h_sigma5.SetLineColor(ROOT.kGray+2)
    h_sigma5.Draw("lsame")
    
    h_sigma6.SetLineColor(ROOT.kCyan+3)
    h_sigma6.Draw("lsame")
    h_sigma7.SetLineColor(1)
    h_sigma7.Draw("lsame")

    latex2 = ROOT.TLatex()
    latex2.SetNDC()
    latex2.SetTextSize(0.4*c1.GetTopMargin())
    latex2.SetTextFont(42)
    latex2.SetTextAlign(31) # align right                                                     
    latex2.DrawLatex(0.90, 0.93,str(_other[0])+" < #eta <"+ str(_other[1]) + ", "+ str(_rho[0])+" < #rho < " + str(_rho[1]))
    
    latex2.Draw("same")
    
    legend.Draw("same")
    c1.SaveAs(folder+"FIT_sigma_eta_"+args.eta+"_rho_"+args.rho+".png")
    c1.SaveAs(folder+"FIT_sigma_eta_"+args.eta+"_rho_"+args.rho+".pdf")
    
    c2 = ROOT.TCanvas("sigmaabs","sigmaabs", 600, 600)
    c2.cd()
    c2.SetLogx()
    h_sigma11.GetXaxis().SetTitle("Gen jet p_{T} [GeV]")        
    h_sigma11.GetYaxis().SetTitle("Resolution")
    h_sigma11.SetTitle("")
    h_sigma11.GetXaxis().SetTitleOffset(1.2)
    h_sigma11.GetYaxis().SetTitleOffset(1.3)
    h_sigma11.SetLineWidth(2)
    h_sigma11.SetMaximum(0.5)
    h_sigma11.SetMinimum(0)
    h_sigma11.SetLineColor(ROOT.kGreen+2)
    h_sigma11.Draw("l")
    
    h_sigma21.SetLineColor(ROOT.kOrange+2)
    h_sigma21.Draw("lsame")
    h_sigma31.SetLineColor(ROOT.kCyan+3)
    #h_sigma31.Draw("lsame")
    h_sigma41.SetLineColor(ROOT.kMagenta+2)
    h_sigma41.Draw("lsame")
    h_sigma51.SetLineColor(ROOT.kGray+2)
    h_sigma51.Draw("lsame")

    h_sigma61.SetLineColor(ROOT.kCyan+3)
    h_sigma61.Draw("lsame")
    h_sigma71.SetLineColor(1)
    h_sigma71.Draw("lsame")

    latex2 = ROOT.TLatex()
    latex2.SetNDC()
    latex2.SetTextSize(0.4*c2.GetTopMargin())
    latex2.SetTextFont(42)
    latex2.SetTextAlign(31) # align right                                                     
    latex2.DrawLatex(0.90, 0.93,str(_other[0])+" < #eta <"+ str(_other[1]) + ", "+ str(_rho[0])+" < #rho < " + str(_rho[1]))
    
    latex2.Draw("same")

    legend.Draw("same")
    c2.SaveAs(folder+"FIT_sigmaabs_eta_"+args.eta+"_rho_"+args.rho+".png")
    c2.SaveAs(folder+"FIT_sigmaabs_eta_"+args.eta+"_rho_"+args.rho+".pdf")
    
if __name__ == '__main__':
    main()
