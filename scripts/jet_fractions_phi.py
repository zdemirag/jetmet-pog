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
    parser.add_argument("-pt","--pt"      ,dest="pt"      , help="define the pt range, options are '20p0_40p0' etc'",type=str)
    parser.add_argument("-t", "--jettype" ,dest="jettype" , help="jettype options are empty, new, pf",type=str)
    args = parser.parse_args()    

    print args.eta, args.jettype

    f_in = TFile(args.input,"READ")
    t_in = f_in.Get("events")

    #_pt  = [20,50,100,200,500,1000,1600]
    _pt = [float(args.pt.split("_")[0].replace("p",".")), float(args.pt.split("_")[1].replace("p","."))]
    _phi = [x*0.30 for x in range(-10, 11)] #[x*0.20 for x in range(-15, 16)]
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
          for k in range(0,len(_phi)-1):

            print "Pt range:", _pt[i], _pt[i+1], "eta range:",  _eta[j], _eta[j+1], "phi range:", _phi[k], _phi[k+1] 

            charged,neutral,photon,muon,electron,hhf,ehf = fraction2(t_in,args.jettype+"charged_e",args.jettype+"neutral_e",args.jettype+"photon_e",args.jettype+"electron_e",args.jettype+"muon_e",args.jettype+"hhf_e",args.jettype+"ehf_e",str(_pt[i]),str(_pt[i+1]),str(_eta[j]),str(_eta[j+1]),str(_phi[k]),str(_phi[k+1]),args.jettype)
            
            mean_ch.append(charged)
            mean_nh.append(neutral)
            mean_ph.append(photon)
            mean_mu.append(muon)
            mean_el.append(electron)
            mean_hhf.append(hhf)
            mean_ehf.append(ehf)
        
    h_ch_mean  = TH1F("hch","hch",len(_phi)-1,array('d',_phi))
    h_nh_mean  = TH1F("hnh","hnh",len(_phi)-1,array('d',_phi))
    h_ph_mean  = TH1F("hph","hph",len(_phi)-1,array('d',_phi))
    h_mu_mean  = TH1F("hmu","hmu",len(_phi)-1,array('d',_phi))
    h_el_mean  = TH1F("hel","hel",len(_phi)-1,array('d',_phi))
    h_hhf_mean = TH1F("hhhf","hhhf",len(_phi)-1,array('d',_phi))
    h_ehf_mean = TH1F("hehf","hehf",len(_phi)-1,array('d',_phi))
        
    for i in range(0,len(_phi)-1):
        
        print i, mean_ph[i]
        h_ch_mean.SetBinContent(i+1, mean_ch[i])
        h_nh_mean.SetBinContent(i+1, mean_nh[i])
        h_ph_mean.SetBinContent(i+1, mean_ph[i])
        h_mu_mean.SetBinContent(i+1, mean_mu[i])
        h_el_mean.SetBinContent(i+1, mean_el[i])
        h_hhf_mean.SetBinContent(i+1, mean_hhf[i])
        h_ehf_mean.SetBinContent(i+1, mean_ehf[i])
        
    ##now make stacks with different choices
    stack_orig = makestack(args.jettype+"_eta_"+args.eta+"_pt_"+ args.pt, h_ch_mean, h_nh_mean,h_ph_mean,h_mu_mean,h_el_mean,h_hhf_mean,h_ehf_mean,args.output,str(_pt[0]),str(_pt[1]),str(_eta[0]),str(_eta[1]))

def makestack(name,h1,h3,h4,h5,h6,h7,h8,output,pt1,pt2,eta1,eta2):
    
    if name.startswith("_"):
        name = "chs"+name
    print name

    stack = THStack(name, name)

    h3.SetLineColor(kBlue-7)
    h3.SetFillColor(kBlue-7)
    stack.Add(h3)

    h4.SetLineColor(kYellow-7)
    h4.SetFillColor(kYellow-7)
    stack.Add(h4)

    h1.SetLineColor(kRed-7)
    h1.SetFillColor(kRed-7)
    stack.Add(h1)

    h5.SetLineColor(kGray+2)
    h5.SetFillColor(kGray+2)
    stack.Add(h5)

    h6.SetLineColor(kGray+2)
    h6.SetFillColor(kGray+2)
    stack.Add(h6)

    h7.SetLineColor(kBlue+2)
    h7.SetFillColor(kBlue+2)
    stack.Add(h7)

    h8.SetLineColor(kBlue-10)
    h8.SetFillColor(kBlue-10)
    stack.Add(h8)

    c = TCanvas(name,name, 600, 600)
    c.cd()
    #c.SetLogx()
    
    stack.Draw("")
    stack.GetXaxis().SetTitle("Gen Jet #phi")
    stack.GetXaxis().SetTitleOffset(1.2)
    stack.GetYaxis().SetTitle("Jet energy fraction")
    stack.GetYaxis().SetTitleOffset(1.15)
    
    f1 = TF1("f1","pol1",0,5000)
    f1.SetParameter(0,1)
    f1.SetLineColor(kGray)
    f1.SetLineStyle(2)
    f1.Draw("same")

    #legend = TLegend(.15,.14,0.40,.35)
    legend = TLegend(.65,.60,0.90,.85)
    legend . AddEntry(h3,"neutral" , "lf")
    legend . AddEntry(h4,"photon" , "lf")
    legend . AddEntry(h1,"charged" , "lf")
    legend . AddEntry(h5,"mu/el" , "lf")
    legend . AddEntry(h7,"hhf" , "lf")
    legend . AddEntry(h8,"ehf" , "lf")
    
    legend.Draw("same")

    latex2 = ROOT.TLatex()
    latex2.SetNDC()
    latex2.SetTextSize(0.5*c.GetTopMargin())
    latex2.SetTextFont(42)
    latex2.SetTextAlign(31) # align right                                                     
    latex2.DrawLatex(0.95, 0.95,str(eta1)+" < #eta_{jet} < "+ str(eta2) + ", "+ str(pt1)+" < pT_{jet} < " + str(pt2))
    


    folder = output+"/"
    os.system("mkdir -p "+folder)
    c.SaveAs(folder+name+".pdf")
    c.SaveAs(folder+name+".png")

    return stack


if __name__ == '__main__':
    main()
