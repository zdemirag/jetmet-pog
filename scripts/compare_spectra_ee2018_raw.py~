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
    h3 = TH1F("h3","h3",args.bin,args.binlow,args.binhigh)
    h4 = TH1F("h4","h4",args.bin,args.binlow,args.binhigh)
        

    # plots to make raw jet eta, corrected jet eta => at different pT thresholds 
    # energy fraction plots for jets in this problematic regions - at different pT thresholds 
    t_in.Draw(args.var+">>h4","jet_pt>40","goff")
    t_in.Draw(args.var+">>h3","jet_pt>30","goff")
    t_in.Draw(args.var+">>h2","jet_pt>20","goff")
    t_in.Draw(args.var+">>h1","jet_pt>10","goff")

    if "norm" in args.output:
        h1.Scale(1./h1.Integral())
        h2.Scale(1./h2.Integral())
        h3.Scale(1./h3.Integral())
        h4.Scale(1./h4.Integral())


    h1.SetLineColor(kRed-7)
    h2.SetLineColor(kBlue-7)
    h3.SetLineColor(kGreen-7)
    h4.SetLineColor(kBlack)

    c = TCanvas(name,name, 600, 600)
    c.cd()
    #c.SetLogy()

    h1.Draw("hist")
    h1.GetXaxis().SetTitle(args.var)
    h1.GetXaxis().SetTitleOffset(1.2)
    h1.SetMaximum(h1.GetMaximum()*2.10)

    if "norm" in args.output:
        h1.GetYaxis().SetTitle("a.u.")
    else:
        h1.GetYaxis().SetTitle("Events")
    h1.GetYaxis().SetTitleOffset(1.15)
    h2.Draw("samehist")
    h3.Draw("samehist")
    h4.Draw("samehist")
    
    legend = TLegend(.65,.75,0.90,.90)
    legend . AddEntry(h1,"pT_{jet} > 10 GeV" , "l")
    legend . AddEntry(h2,"pT_{jet} > 20 GeV" , "l")
    legend . AddEntry(h3,"pT_{jet} > 30 GeV" , "l")
    legend . AddEntry(h4,"pT_{jet} > 40 GeV" , "l")
    legend . SetBorderSize(0)
    legend.Draw("same")

    tex= TLatex(0.12, 0.95,args.output);
    tex.SetTextSize(0.03);
    tex.SetNDC(kTRUE)
    tex.Draw()
   
    folder = "/afs/cern.ch/user/z/zdemirag/www/JetMET/ee2018/"+args.output+"/"
    os.system("mkdir -p "+folder)
    c.SaveAs(folder+name+".pdf")
    c.SaveAs(folder+name+".png")

    return stack


if __name__ == '__main__':
    main()
