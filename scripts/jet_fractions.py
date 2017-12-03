import os,sys,socket,argparse
from ROOT import *
from collections import defaultdict
import math
from array import array

from tdrStyle import *
setTDRStyle()

def main():
    
    parser = argparse.ArgumentParser(description='Plot jet energy fractions as a function of jet pt')
    parser.add_argument("-i", "--input"   ,dest="input"   , help="input file name", type=str)
    parser.add_argument("-o", "--output"  ,dest="output"  , help="output folder name", type=str)
    parser.add_argument("-p", "--putype"  ,dest="pu"   , help="define the sample, options are 'flatpu','nopu'",type=str)
    parser.add_argument("-e", "--eta"     ,dest="eta"  , help="define the eta range, options are '0_1p3','1p3_2p1',2p1_2p5','2p5_3p0', '3p0_5p0'",type=str)
    parser.add_argument("-v", "--version" ,dest="version" , help="define the version",type=str)
    parser.add_argument("-m", "--matched" ,dest="matched" , help="gen matching",type=int)
    parser.add_argument("-t", "--jettype" ,dest="jettype" , help="jettype options are empty, new, pf",type=str)
    args = parser.parse_args()    

    print args.pu, args.eta, args.matched, args.jettype

    f_in = TFile(args.input,"READ")
    t_in = f_in.Get("events")

    _pt  = [20,50,100,200,500,1000,1600]
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

            print _pt[i], _pt[i+1], _eta[j], _eta[j+1]

            charged,neutral,photon,muon,electron,h_hhf,h_ehf = fraction(args.jettype+"charged",args.jettype+"neutral",args.jettype+"photon",args.jettype+"electron",args.jettype+"muon",args.jettype+"hhf",args.jettype+"ehf",str(_pt[i]),str(_pt[i+1]),str(_eta[i]),str(_eta[i+1]),args.jettype)
            
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
        
        print i, mean_ch[i]
        h_ch_mean.SetBinContent(i+1, mean_ch[i])
        h_nh_mean.SetBinContent(i+1, mean_nh[i])
        h_ph_mean.SetBinContent(i+1, mean_ph[i])
        h_mu_mean.SetBinContent(i+1, mean_mu[i])
        h_el_mean.SetBinContent(i+1, mean_el[i])
        h_hhf_mean.SetBinContent(i+1, mean_hhf[i])
        h_ehf_mean.SetBinContent(i+1, mean_ehf[i])
        
    ##now make stacks with different choices
    stack_orig = makestack(args.jettype+"_eta_"+args.eta, h_ch_mean, h_nh_mean,h_ph_mean,h_mu_mean,h_el_mean,h_hhf_mean,h_ehf_mean,args.pu,args.matched)

def makestack(name,h1,h3,h4,h5,h6,h7,h8,pu,matched):
    
    stack = THStack(name, name)

    h1.SetLineColor(kRed-3)
    h1.SetFillColor(kRed-3)
    stack.Add(h1)

    h3.SetLineColor(kBlue+2)
    h3.SetFillColor(kBlue+2)
    stack.Add(h3)

    h4.SetLineColor(kYellow+1)
    h4.SetFillColor(kYellow+1)
    stack.Add(h4)

    h5.SetLineColor(kMagenta+2)
    h5.SetFillColor(kMagenta+2)
    stack.Add(h5)

    h6.SetLineColor(kMagenta+2)
    h6.SetFillColor(kMagenta+2)
    stack.Add(h6)

    h7.SetLineColor(1+7)
    h7.SetFillColor(1+7)
    stack.Add(h7)

    h8.SetLineColor(1+8)
    h8.SetFillColor(1+8)
    stack.Add(h8)

    c = TCanvas(name,name, 600, 700)
    c.cd()

    stack.Draw("")
    stack.GetXaxis().SetTitle("Jet p_{T} [GeV]")
    stack.GetXaxis().SetTitleOffset(1.2)
    stack.GetYaxis().SetTitle("PF energy fraction")
    stack.GetYaxis().SetTitleOffset(1.2)
    
    legend = TLegend(.85,.55,0.99,.93)
    legend . AddEntry(h1,"charged" , "lf")
    legend . AddEntry(h3,"neutral" , "lf")
    legend . AddEntry(h4,"photon" , "lf")
    legend . AddEntry(h5,"mu/el" , "lf")
    legend . AddEntry(h7,"hhf" , "lf")
    legend . AddEntry(h8,"ehf" , "lf")
    
    legend.Draw("same")
    print matched
    if bool(matched):
        folder = args.output+"/"+pu+"/gen_matched/"
    else:
        folder = args.output+"/"+pu+"/"
    os.system("mkdir -p "+folder)
    c.SaveAs(folder+name+".pdf")
    c.SaveAs(folder+name+".png")

    return stack



if __name__ == '__main__':
    main()
