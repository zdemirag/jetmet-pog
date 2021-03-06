import os,sys,socket,argparse
from ROOT import *
from collections import defaultdict
import math
from array import array

from helper_functions import fraction, fraction2
from tdrStyle import *
setTDRStyle()

def main():
    
    parser = argparse.ArgumentParser(description='Plot jet energy fractions as a function of jet pt')
    parser.add_argument("-i", "--input"   ,dest="input"   , help="input file name", type=str)
    parser.add_argument("-o", "--output"  ,dest="output"  , help="output folder name", type=str)
    parser.add_argument("-e", "--eta"     ,dest="eta"     , help="define the eta range, options are '0_1p3','1p3_2p1',2p1_2p5','2p5_3p0', '3p0_5p0'",type=str)
    parser.add_argument("-t", "--jettype" ,dest="jettype" , help="jettype options are empty, new, pf",type=str)
    args = parser.parse_args()    

    print args.eta, args.jettype

    f_in = TFile(args.input,"READ")
    t_in = f_in.Get("events")

    _pt  = [10,30,50,100,200,500,1000,1600]
    _eta = [float(args.eta.split("_")[0].replace("p",".")), float(args.eta.split("_")[1].replace("p","."))]

    mean_ch = list()
    mean_nh = list()
    mean_ph = list()
    mean_mu = list()
    mean_el = list()
    mean_hhf = list()
    mean_ehf = list()
    
    for i in range(0,len(_pt)-1):
        for j in range(0,len(_eta)-1):

            print "Pt range:", _pt[i], _pt[i+1], "eta range:",  _eta[j], _eta[j+1]

            charged,neutral,photon,muon,electron,hhf,ehf = fraction2(t_in,args.jettype+"charged_e",args.jettype+"neutral_e",args.jettype+"photon_e",args.jettype+"electron_e",args.jettype+"muon_e",args.jettype+"hhf_e",args.jettype+"ehf_e",str(_pt[i]),str(_pt[i+1]),str(_eta[j]),str(_eta[j+1]),str(-4),str(4),args.jettype)
            
            mean_ch.append(charged)
            mean_nh.append(neutral)
            mean_ph.append(photon)
            mean_mu.append(muon)
            mean_el.append(electron)
            mean_hhf.append(hhf)
            mean_ehf.append(ehf)
        
    h_ch_mean  = TH1F("hch","hch",len(_pt)-1,array('d',_pt))
    h_nh_mean  = TH1F("hnh","hnh",len(_pt)-1,array('d',_pt))
    h_ph_mean  = TH1F("hph","hph",len(_pt)-1,array('d',_pt))
    h_mu_mean  = TH1F("hmu","hmu",len(_pt)-1,array('d',_pt))
    h_el_mean  = TH1F("hel","hel",len(_pt)-1,array('d',_pt))
    h_hhf_mean = TH1F("hhhf","hhhf",len(_pt)-1,array('d',_pt))
    h_ehf_mean = TH1F("hehf","hehf",len(_pt)-1,array('d',_pt))
        
    for i in range(0,len(_pt)-1):
        
        print i, mean_ph[i]
        h_ch_mean.SetBinContent(i+1, mean_ch[i])
        h_nh_mean.SetBinContent(i+1, mean_nh[i])
        h_ph_mean.SetBinContent(i+1, mean_ph[i])
        h_mu_mean.SetBinContent(i+1, mean_mu[i])
        h_el_mean.SetBinContent(i+1, mean_el[i])
        h_hhf_mean.SetBinContent(i+1, mean_hhf[i])
        h_ehf_mean.SetBinContent(i+1, mean_ehf[i])
        
    ##now make stacks with different choices
    stack_orig = makestack(args.jettype+"_eta_"+args.eta, h_ch_mean, h_nh_mean,h_ph_mean,h_mu_mean,h_el_mean,h_hhf_mean,h_ehf_mean,args.output)

def makestack(name,h1,h3,h4,h5,h6,h7,h8,output):
    
    if name.startswith("_"):
        name = "chs"+name
    print name

    stack = THStack(name, name)

    h1.SetLineColor(kRed-7)
    h1.SetFillColor(kRed-7)
    stack.Add(h1)

    h3.SetLineColor(kBlue-7)
    h3.SetFillColor(kBlue-7)
    stack.Add(h3)

    h4.SetLineColor(kYellow-7)
    h4.SetFillColor(kYellow-7)
    stack.Add(h4)

    h5.SetLineColor(kMagenta-8)
    h5.SetFillColor(kMagenta-8)
    stack.Add(h5)

    h6.SetLineColor(kMagenta-8)
    h6.SetFillColor(kMagenta-8)
    stack.Add(h6)

    h7.SetLineColor(kCyan-8)
    h7.SetFillColor(kCyan-8)
    stack.Add(h7)

    h8.SetLineColor(kCyan-7)
    h8.SetFillColor(kCyan-7)
    stack.Add(h8)

    c = TCanvas(name,name, 600, 700)
    c.cd()
    c.SetLogx()

    stack.Draw("")
    stack.GetXaxis().SetTitle("Gen Jet p_{T} [GeV]")
    stack.GetXaxis().SetTitleOffset(1.2)
    stack.GetYaxis().SetTitle("PF p_{T} fraction")
    stack.GetYaxis().SetTitleOffset(1.15)
    
    f1 = TF1("f1","pol1",0,5000)
    f1.SetParameter(0,1)
    f1.SetLineColor(kGray)
    f1.SetLineStyle(2)
    f1.Draw("same")

    legend = TLegend(.85,.55,0.99,.93)
    legend . AddEntry(h1,"charged" , "lf")
    legend . AddEntry(h3,"neutral" , "lf")
    legend . AddEntry(h4,"photon" , "lf")
    legend . AddEntry(h5,"mu/el" , "lf")
    legend . AddEntry(h7,"hhf" , "lf")
    legend . AddEntry(h8,"ehf" , "lf")
    
    legend.Draw("same")

    folder = output+"/"
    os.system("mkdir -p "+folder)
    c.SaveAs(folder+name+".pdf")
    c.SaveAs(folder+name+".png")

    return stack


if __name__ == '__main__':
    main()
