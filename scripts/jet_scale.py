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

def main():
    
    parser = argparse.ArgumentParser(description='Plot resolution and response')
    parser.add_argument("-i", "--input"   ,dest="input"   , help="input file name", type=str)
    parser.add_argument("-o", "--output"  ,dest="output"  , help="output folder name", type=str)
    parser.add_argument("-p", "--putype"  ,dest="pu"      , help="define the sample, options are 'flatpu','nopu'",type=str)
    parser.add_argument("-e", "--eta"     ,dest="eta"     , help="define the eta range, options are '0_1p3','1p3_2p1',2p1_2p5','2p5_3p0', '3p0_5p0'",type=str)
    parser.add_argument("-v", "--version" ,dest="version" , help="define the version",type=str)
    parser.add_argument("-r", "--rho"     ,dest="rho"     , help="define the rho range",type=str)
    args = parser.parse_args()    

    print args.pu, args.eta
    f_in = ROOT.TFile(str(args.input),"READ")
    t_in = f_in.Get("events")
    _pt  = [20,50,100,200,500,2000]
    _eta = [float(args.eta.split("_")[0].replace("p",".")), float(args.eta.split("_")[1].replace("p","."))]
    _rho = [float(args.rho.split("_")[0]), float(args.rho.split("_")[1])]

    folder = args.output+"/"+args.version+"/"+args.pu+"/"
    os.system("mkdir -p "+folder)
    os.system("mkdir -p "+folder+"/fit")

    h_mean = ROOT.TH1F("h_mean","h_mean",len(_pt)-1,array('d',_pt))
    h_sigma = ROOT.TH1F("h_sigma","h_sigma",len(_pt)-1,array('d',_pt))
    h_sigma11 = ROOT.TH1F("h_sigma11","h_sigma11",len(_pt)-1,array('d',_pt))

    for i in range(0,len(_pt)-1):
        shape  = ROOT.TH1F("shape","shape",50,0.25,2.5)

        #add here the new and old sum

        chs_sum = "(charged    + neutral    + photon    + muon    + electron    + hhf    + ehf)"        
        rho_cut = " && rhoall>="+str(_rho[0])+" && rhoall<"+str(_rho[1])

        t_in.Draw("("+chs_sum+")/(genjet_pt)>>shape","genjet_pt>"+str(_pt[i])+" && genjet_pt<"+str(_pt[i+1])+" && abs(genjet_eta)>="+str(_eta[0])+" && abs(genjet_eta)<"+str(_eta[1])+rho_cut,"goff")

        mean, mean_error, sigma, sigma_error = ConvFit(shape ,False,"ratio","jet pt/gen jet pt",folder+"/fit","FIT_pf_pt_"+str(_pt[i])+"_eta_"+args.eta+"_rho_"+args.rho)

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

        c = ROOT.TCanvas("mean","mean", 600, 600)
        c.cd()
        c.SetLogx()
        ROOT.gStyle.SetOptStat(False)
        h_mean.SetTitle("")
        h_mean.GetXaxis().SetTitle("Jet p_{T} [GeV]")
        h_mean.GetYaxis().SetTitle("Response")
        h_mean.GetXaxis().SetTitleOffset(1.2)
        h_mean.GetYaxis().SetTitleOffset(1.3)
        h_mean.SetMaximum(1.3)
        h_mean.SetMinimum(0.7)
        h_mean.SetLineWidth(2)
        h_mean.Draw("")
        h_mean.SetMarkerStyle(20)
        h_mean.SetMarkerSize(0.8)
        
        legend = ROOT.TLegend(0.30, 0.65, 0.65, .85);
        legend . AddEntry(h_mean,"pf jet" , "lp")
        legend . AddEntry(h_mean3,"chs jet" , "lp")
        legend . AddEntry(h_mean2,"new jet" , "lp")

        legend.Draw("same")

        latex2 = ROOT.TLatex()
        latex2.SetNDC()
        latex2.SetTextSize(0.4*c.GetTopMargin())
        latex2.SetTextFont(42)
        latex2.SetTextAlign(31) # align right                                                     
        latex2.DrawLatex(0.90, 0.93,str(_eta[0])+" < #eta <"+ str(_eta[1]) + ", "+ str(_rho[0])+" < #rho < " + str(_rho[1]))

        latex2.Draw("same")

        c.SaveAs(folder+"FIT_mean_eta_"+args.eta+"_rho_"+args.rho+".png")
        c.SaveAs(folder+"FIT_mean_eta_"+args.eta+"_rho_"+args.rho+".pdf")

        c1 = ROOT.TCanvas("sigma","sigma", 600, 600)
        c1.cd()
        c1.SetLogx()
        h_sigma.GetXaxis().SetTitle("Jet p_{T} [GeV]")
        h_sigma.GetYaxis().SetTitle("Resolution / Response")
        h_sigma.SetTitle("")
        h_sigma.GetXaxis().SetTitleOffset(1.2)
        h_sigma.GetYaxis().SetTitleOffset(1.3)
        h_sigma.SetLineWidth(2)
        h_sigma.SetMaximum(0.5)
        h_sigma.SetMinimum(0)
        h_sigma.Draw()
        h_sigma.SetMarkerStyle(20)
        h_sigma.SetMarkerSize(0.8)

        latex2 = ROOT.TLatex()
        latex2.SetNDC()
        latex2.SetTextSize(0.4*c1.GetTopMargin())
        latex2.SetTextFont(42)
        latex2.SetTextAlign(31) # align right                                                     
        latex2.DrawLatex(0.90, 0.93,str(_eta[0])+" < #eta <"+ str(_eta[1]) + ", "+ str(_rho[0])+" < #rho < " + str(_rho[1]))

        latex2.Draw("same")

        legend.Draw("same")
        c1.SaveAs(folder+"FIT_sigma_eta_"+args.eta+"_rho_"+args.rho+".png")
        c1.SaveAs(folder+"FIT_sigma_eta_"+args.eta+"_rho_"+args.rho+".pdf")

        c2 = ROOT.TCanvas("sigmaabs","sigmaabs", 600, 600)
        c2.cd()
        c2.SetLogx()
        h_sigma11.GetXaxis().SetTitle("Jet p_{T} [GeV]")        
        h_sigma11.GetYaxis().SetTitle("Resolution")
        h_sigma11.SetTitle("")
        h_sigma11.GetXaxis().SetTitleOffset(1.2)
        h_sigma11.GetYaxis().SetTitleOffset(1.3)
        h_sigma11.SetLineWidth(2)
        h_sigma11.SetMaximum(0.5)
        h_sigma11.SetMinimum(0)
        h_sigma11.SetMarkerStyle(20)
        h_sigma11.SetMarkerSize(0.8)
        h_sigma11.Draw("")

        latex2 = ROOT.TLatex()
        latex2.SetNDC()
        latex2.SetTextSize(0.4*c2.GetTopMargin())
        latex2.SetTextFont(42)
        latex2.SetTextAlign(31) # align right                                                     
        latex2.DrawLatex(0.90, 0.93,str(_eta[0])+" < #eta <"+ str(_eta[1]) + ", "+ str(_rho[0])+" < #rho < " + str(_rho[1]))

        latex2.Draw("same")

        legend.Draw("same")
        c2.SaveAs(folder+"FIT_sigmaabs_eta_"+args.eta+"_rho_"+args.rho+".png")
        c2.SaveAs(folder+"FIT_sigmaabs_eta_"+args.eta+"_rho_"+args.rho+".pdf")

if __name__ == '__main__':
    main()
