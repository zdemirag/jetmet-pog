import os,sys,socket,argparse
from ROOT import *
from collections import defaultdict
import math
from array import array

from helper_functions import fraction
from tdrStyle import *
setTDRStyle()

def main():
    
    parser = argparse.ArgumentParser(description='Plot jet energy fractions as a function of jet pt')
    parser.add_argument("-i", "--input"   ,dest="input"   , help="input file name", type=str)
    parser.add_argument("-o", "--output"  ,dest="output"   , help="output file name", type=str)
    parser.add_argument("-v", "--var"     ,dest="var"     , help="variable name", type=str)
    parser.add_argument("-bl","--binlow"  ,dest="binlow"  , help="bin low", type=int)
    parser.add_argument("-bh","--binhigh"  ,dest="binhigh"  , help="bin high", type=int)
    parser.add_argument("-b","--bin"  ,dest="bin"  , help="bin", type=int)
    args = parser.parse_args()    

    name=args.var
    
    f_in = TFile(args.input,"READ")
    t_in = f_in.Get("events")

    h1 = TH1F("h1","h1",args.bin,args.binlow,args.binhigh)
    h2 = TH1F("h2","h2",args.bin,args.binlow,args.binhigh)
        
    t_in.Draw(args.var+">>h2","jet_pt[0]>40 && jet_eta[0]<2.5 && jet_eta[0]>1.5 && NHF[0]<0.9","goff")
    t_in.Draw(args.var+">>h1","jet_pt[0]>40 && jet_eta[0]>-2.5 && jet_eta[0]<-1.5 && NHF[0]<0.9","goff")

    #t_in.Draw(args.var+">>h2","jet_pt>40 && jet_eta<2.5 && jet_eta>1.5 && NHF<0.9 && met > 100","goff")
    #t_in.Draw(args.var+">>h1","jet_pt>40 && jet_eta>-2.5 && jet_eta<-1.5 && NHF<0.9 && met > 100","goff")

    if "norm" in args.output:
        h1.Scale(1./h1.Integral())
        h2.Scale(1./h2.Integral())


    h1.SetLineColor(kRed-7)
    h2.SetLineColor(kBlue-7)

    c = TCanvas(name,name, 600, 600)
    c.cd()
    c.SetLogy()

    h1.Draw("")
    h1.GetXaxis().SetTitle(args.var)
    h1.GetXaxis().SetTitleOffset(1.2)
    if "norm" in args.output:
        h1.GetYaxis().SetTitle("a.u.")
    else:
        h1.GetYaxis().SetTitle("Events")
    h1.GetYaxis().SetTitleOffset(1.15)
    h2.Draw("same")
    
    legend = TLegend(.65,.75,0.90,.90)
    legend . AddEntry(h2,"1.5 < #eta_{jet} < 2.5 " , "l")
    legend . AddEntry(h1,"-2.5 < #eta_{jet} < -1.5 " , "l")
    
    legend.Draw("same")

    tex= TLatex(0.12, 0.95,args.output+" pT_{jet} > 40 GeV && NHF <0.9");
    tex.SetTextSize(0.03);
    tex.SetNDC(kTRUE)
    tex.Draw()
   


    folder = "/afs/cern.ch/user/z/zdemirag/www/JetMET/hem15_16/"+args.output+"/"
    os.system("mkdir -p "+folder)
    c.SaveAs(folder+name+".pdf")
    c.SaveAs(folder+name+".png")

    return stack


if __name__ == '__main__':
    main()
