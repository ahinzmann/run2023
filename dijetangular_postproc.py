#!/usr/bin/env python
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from importlib import import_module
import os
import sys
import ROOT
import math
import copy
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetRecalib import jetRecalib

class EventInfo(Module):
    def __init__(
        self,
        storeVariables = []
    ):
        self.storeVariables = storeVariables
        
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        for variable in self.storeVariables:
            variable[0](self.out)
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
        
    def analyze(self, event):
        for variable in self.storeVariables:
            variable[1](self.out,event)
        return True

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] outputDir inputFiles")
    parser.add_option("-s", "--postfix", dest="postfix", type="string", default=None,
                      help="Postfix which will be appended to the file name (default: _Friend for friends, _Skim for skims)")
    parser.add_option("-J", "--json", dest="json", type="string",
                      default=None, help="Select events using this JSON file")
    parser.add_option("-c", "--cut", dest="cut", type="string",
                      default=None, help="Cut string")
    parser.add_option("-b", "--branch-selection", dest="branchsel",
                      type="string", default=None, help="Branch selection")
    parser.add_option("--bi", "--branch-selection-input", dest="branchsel_in",
                      type="string", default=None, help="Branch selection input")
    parser.add_option("--bo", "--branch-selection-output", dest="branchsel_out",
                      type="string", default=None, help="Branch selection output")
    parser.add_option("--friend", dest="friend", action="store_true", default=False,
                      help="Produce friend trees in output (current default is to produce full trees)")
    parser.add_option("--full", dest="friend", action="store_false", default=False,
                      help="Produce full trees in output (this is the current default)")
    parser.add_option("--noout", dest="noOut", action="store_true",
                      default=False, help="Do not produce output, just run modules")
    parser.add_option("-P", "--prefetch", dest="prefetch", action="store_true", default=False,
                      help="Prefetch input files locally instead of accessing them via xrootd")
    parser.add_option("--long-term-cache", dest="longTermCache", action="store_true", default=False,
                      help="Keep prefetched files across runs instead of deleting them at the end")
    parser.add_option("-N", "--max-entries", dest="maxEntries", type="long", default=None,
                      help="Maximum number of entries to process from any single given input tree")
    parser.add_option("--first-entry", dest="firstEntry", type="long", default=0,
                      help="First entry to process in the three (to be used together with --max-entries)")
    parser.add_option("--justcount", dest="justcount", default=False,
                      action="store_true", help="Just report the number of selected events")
    parser.add_option("-I", "--import", dest="imports", type="string", default=[], action="append",
                      nargs=2, help="Import modules (python package, comma-separated list of ")
    parser.add_option("-z", "--compression", dest="compression", type="string",
                      default=("LZMA:9"), help="Compression: none, or (algo):(level) ")

    (options, args) = parser.parse_args()

    if options.friend:
        if options.cut or options.json:
            raise RuntimeError(
                "Can't apply JSON or cut selection when producing friends")

    if len(args) < 2:
        parser.print_help()
        sys.exit(1)
    outdir = args[0]
    args = args[1:]

    modules = []
    for mod, names in options.imports:
        import_module(mod)
        obj = sys.modules[mod]
        selnames = names.split(",")
        mods = dir(obj)
        for name in selnames:
            if name in mods:
                print("Loading %s from %s " % (name, mod))
                if type(getattr(obj, name)) == list:
                    for mod in getattr(obj, name):
                        modules.append(mod())
                else:
                    modules.append(getattr(obj, name)())
    if options.noOut:
        if len(modules) == 0:
            raise RuntimeError(
                "Running with --noout and no modules does nothing!")
    if options.branchsel != None:
        options.branchsel_in = options.branchsel
        options.branchsel_out = options.branchsel
    
    # 2023
    if "Run2023C" in outdir and ("22Sep2023_v1" in outdir or "22Sep2023_v2" in outdir or "22Sep2023_v3" in outdir):
      modules.append(jetRecalib("Summer23Prompt23_RunCv123_V1_DATA", "Summer23Prompt23_RunCv123_V1_DATA", jetType="AK4PFPuppi", redoJEC=True)) # from https://github.com/cms-jet/JECDatabase/blob/master/tarballs/Summer23Prompt23_RunCv123_V1_DATA.tar.gz
    elif "Run2023C" in outdir and "22Sep2023_v4" in outdir:
      modules.append(jetRecalib("Summer23Prompt23_RunCv4_V1_DATA", "Summer23Prompt23_RunCv4_V1_DATA", jetType="AK4PFPuppi", redoJEC=True)) # https://github.com/cms-jet/JECDatabase/blob/master/tarballs/Summer23Prompt23_RunCv4_V1_DATA.tar.gz
    elif "Run2023D" in outdir:
      modules.append(jetRecalib("Summer23BPixPrompt23_RunD_V1_DATA", "Summer23BPixPrompt23_RunD_V1_DATA", jetType="AK4PFPuppi", redoJEC=True)) # from https://github.com/cms-jet/JECDatabase/blob/master/tarballs/Summer23BPixPrompt23_RunD_V1_DATA.tar.gz
    elif "Run3Summer23NanoAODv12" in outdir:
      modules.append(jetRecalib("Summer23Prompt23_V1_MC", "Summer23Prompt23_V1_MC", jetType="AK4PFPuppi", redoJEC=True)) # from https://github.com/cms-jet/JECDatabase/blob/master/tarballs/Summer23Prompt23_V1_MC.tar.gz
    elif "Run3Summer23BPixNanoAODv12" in outdir:
      modules.append(jetRecalib("Summer23BPixPrompt23_V1_MC", "Summer23BPixPrompt23_V1_MC", jetType="AK4PFPuppi", redoJEC=True)) # from https://github.com/cms-jet/JECDatabase/blob/master/tarballs/Summer23BPixPrompt23_V1_MC.tar.gz
    # 2024
    if "Run2024C" in outdir or "Run2024D" in outdir:
      modules.append(jetRecalib("Winter24Prompt24_RunBCD_V2_DATA", "Winter24Prompt24_RunBCD_V2_DATA", jetType="AK4PFPuppi", redoJEC=True)) # from https://github.com/cms-jet/JECDatabase/blob/master/tarballs/Winter24Prompt24_RunBCD_V2_DATA.tar.gz
    elif "Run2024E" in outdir:
      modules.append(jetRecalib("Winter24Prompt24_RunE_V2_DATA", "Winter24Prompt24_RunE_V2_DATA", jetType="AK4PFPuppi", redoJEC=True)) # https://github.com/cms-jet/JECDatabase/blob/master/tarballs/Winter24Prompt24_RunE_V2_DATA.tar.gz
    elif "Run2024F" in outdir:
      modules.append(jetRecalib("Winter24Prompt24_RunF_V2_DATA", "Winter24Prompt24_RunF_V2_DATA", jetType="AK4PFPuppi", redoJEC=True)) # https://github.com/cms-jet/JECDatabase/blob/master/tarballs/Winter24Prompt24_RunF_V2_DATA.tar.gz
    elif "Run2024G" in outdir:
      modules.append(jetRecalib("Winter24Prompt24_RunG_V2_DATA", "Winter24Prompt24_RunG_V2_DATA", jetType="AK4PFPuppi", redoJEC=True)) # https://github.com/cms-jet/JECDatabase/blob/master/tarballs/Winter24Prompt24_RunG_V2_DATA.tar.gz
    elif "Run2024H" in outdir:
      modules.append(jetRecalib("Winter24Prompt24_RunH_V2_DATA", "Winter24Prompt24_RunH_V2_DATA", jetType="AK4PFPuppi", redoJEC=True)) # https://github.com/cms-jet/JECDatabase/blob/master/tarballs/Winter24Prompt24_RunH_V2_DATA.tar.gz
    elif "Run2024I" in outdir:
      modules.append(jetRecalib("Winter24Prompt24_RunI_V2_DATA", "Winter24Prompt24_RunI_V2_DATA", jetType="AK4PFPuppi", redoJEC=True)) # https://github.com/cms-jet/JECDatabase/blob/master/tarballs/Winter24Prompt24_RunI_V2_DATA.tar.gz
    elif "RunIII2024Summer24NanoAOD" in outdir:
      modules.append(jetRecalib("Winter24Prompt24_V2_MC", "Winter24Prompt24_V2_MC", jetType="AK4PFPuppi", redoJEC=True)) # from https://github.com/cms-jet/JECDatabase/blob/master/tarballs/Winter24Prompt24_V2_MC.tar.gz
    # 2022
    elif "Run2022C" in outdir or "Run2022D" in outdir:
      modules.append(jetRecalib("Summer22_22Sep2023_RunCD_V2_DATA", "Summer22_22Sep2023_RunCD_V2_DATA", jetType="AK4PFPuppi", redoJEC=True)) # from https://github.com/cms-jet/JECDatabase/raw/master/tarballs/Summer22_22Sep2023_RunCD_V2_DATA.tar.gz
    elif "Run2022E" in outdir:
      modules.append(jetRecalib("Summer22EE_22Sep2023_RunE_V2_DATA", "Summer22EE_22Sep2023_RunE_V2_DATA", jetType="AK4PFPuppi", redoJEC=True)) # from https://github.com/cms-jet/JECDatabase/raw/master/tarballs/Summer22EE_22Sep2023_RunE_V2_DATA.tar.gz
    elif "Run2022F" in outdir:
      modules.append(jetRecalib("Summer22EE_22Sep2023_RunF_V2_DATA", "Summer22EE_22Sep2023_RunF_V2_DATA", jetType="AK4PFPuppi", redoJEC=True)) # from https://github.com/cms-jet/JECDatabase/raw/master/tarballs/Summer22EE_22Sep2023_RunF_V2_DATA.tar.gz
    elif "Run2022G" in outdir:
      modules.append(jetRecalib("Summer22EE_22Sep2023_RunG_V2_DATA", "Summer22EE_22Sep2023_RunG_V2_DATA", jetType="AK4PFPuppi", redoJEC=True)) # from https://github.com/cms-jet/JECDatabase/raw/master/tarballs/Summer22EE_22Sep2023_RunG_V2_DATA.tar.gz
    elif "Run3Summer22NanoAODv12" in outdir:
      modules.append(jetRecalib("Summer22_22Sep2023_V2_MC", "Summer22_22Sep2023_V2_MC", jetType="AK4PFPuppi", redoJEC=True)) # from https://github.com/cms-jet/JECDatabase/blob/master/tarballs/Summer22_22Sep2023_V2_MC.tar.gz
    elif "Run3Summer22EENanoAODv12" in outdir:
      modules.append(jetRecalib("Summer22EE_22Sep2023_V2_MC", "Summer22EE_22Sep2023_V2_MC", jetType="AK4PFPuppi", redoJEC=True)) # from https://github.com/cms-jet/JECDatabase/blob/master/tarballs/Summer22EE_22Sep2023_V2_MC.tar.gz
    # 2018
    elif "RunIISummer20UL18" in outdir:
      modules.append(jetRecalib("Summer19UL18_V5_MC", "Summer19UL18_V5_MC", jetType="AK4PFchs", redoJEC=True)) # from https://github.com/cms-jet/JECDatabase/blob/master/tarballs/Summer19UL18_V5_MC.tar.gz
    elif "Run2018A" in outdir:
      modules.append(jetRecalib("Summer19UL18_RunA_V5_DATA", "Summer19UL18_RunA_V5_DATA", jetType="AK4PFchs", redoJEC=True)) # from https://github.com/cms-jet/JECDatabase/blob/master/tarballs/Summer19UL18_RunA_V5_DATA.tar.gz?raw=true
    elif "Run2018B" in outdir:
      modules.append(jetRecalib("Summer19UL18_RunB_V5_DATA", "Summer19UL18_RunB_V5_DATA", jetType="AK4PFchs", redoJEC=True)) # from https://github.com/cms-jet/JECDatabase/blob/master/tarballs/Summer19UL18_RunB_V5_DATA.tar.gz?raw=true
    elif "Run2018C" in outdir:
      modules.append(jetRecalib("Summer19UL18_RunC_V5_DATA", "Summer19UL18_RunC_V5_DATA", jetType="AK4PFchs", redoJEC=True)) # from https://github.com/cms-jet/JECDatabase/blob/master/tarballs/Summer19UL18_RunC_V5_DATA.tar.gz?raw=true
    elif "Run2018D" in outdir:
      modules.append(jetRecalib("Summer19UL18_RunD_V5_DATA", "Summer19UL18_RunD_V5_DATA", jetType="AK4PFchs", redoJEC=True)) # from https://github.com/cms-jet/JECDatabase/blob/master/tarballs/Summer19UL18_RunD_V5_DATA.tar.gz?raw=true
    elif "Run2017B" in outdir:
      modules.append(jetRecalib("Summer19UL17_RunB_V5_DATA", "Summer19UL17_RunB_V5_DATA", jetType="AK4PFchs", redoJEC=True)) # from https://github.com/cms-jet/JECDatabase/blob/master/tarballs/Summer19UL17_RunB_V5_DATA.tar.gz?raw=true
    elif "Run2017C" in outdir:
      modules.append(jetRecalib("Summer19UL17_RunC_V5_DATA", "Summer19UL17_RunC_V5_DATA", jetType="AK4PFchs", redoJEC=True)) # from https://github.com/cms-jet/JECDatabase/blob/master/tarballs/Summer19UL17_RunC_V5_DATA.tar.gz?raw=true
    elif "Run2017D" in outdir:
      modules.append(jetRecalib("Summer19UL17_RunD_V5_DATA", "Summer19UL17_RunD_V5_DATA", jetType="AK4PFchs", redoJEC=True)) # from https://github.com/cms-jet/JECDatabase/blob/master/tarballs/Summer19UL17_RunD_V5_DATA.tar.gz?raw=true
    elif "Run2017E" in outdir:
      modules.append(jetRecalib("Summer19UL17_RunE_V5_DATA", "Summer19UL17_RunE_V5_DATA", jetType="AK4PFchs", redoJEC=True)) # from https://github.com/cms-jet/JECDatabase/blob/master/tarballs/Summer19UL17_RunE_V5_DATA.tar.gz?raw=true
    elif "Run2017F" in outdir:
      modules.append(jetRecalib("Summer19UL17_RunF_V5_DATA", "Summer19UL17_RunF_V5_DATA", jetType="AK4PFchs", redoJEC=True)) # from https://github.com/cms-jet/JECDatabase/blob/master/tarballs/Summer19UL17_RunF_V5_DATA.tar.gz?raw=true
    elif "Run2016B" in outdir or "Run2016C" in outdir or "Run2016D" in outdir:
      modules.append(jetRecalib("Summer19UL16APV_RunBCD_V7_DATA", "Summer19UL16APV_RunBCD_V7_DATA", jetType="AK4PFchs", redoJEC=True)) # from https://github.com/cms-jet/JECDatabase/blob/master/tarballs/Summer19UL16_V7_all.tar.gz?raw=true
    elif "Run2016E" in outdir or  "Run2016F-HIPM" in outdir:
      modules.append(jetRecalib("Summer19UL16APV_RunEF_V7_DATA", "Summer19UL16APV_RunEF_V7_DATA", jetType="AK4PFchs", redoJEC=True)) # from https://github.com/cms-jet/JECDatabase/blob/master/tarballs/Summer19UL16_V7_all.tar.gz?raw=true
    elif "Run2016F-UL" in outdir or  "Run2016G" in outdir or  "Run2016H" in outdir:
      modules.append(jetRecalib("Summer19UL16_RunFGH_V7_DATA", "Summer19UL16_RunFGH_V7_DATA", jetType="AK4PFchs", redoJEC=True)) # from https://github.com/cms-jet/JECDatabase/blob/master/tarballs/Summer19UL16_V7_all.tar.gz?raw=true
    else:
      noJECs
    
    storeVariables=[]
    storeVariables += [
        [lambda tree: tree.branch("jetAK4_pt1", "F"), lambda tree, event: tree.fillBranch("jetAK4_pt1", event.Jet_pt[0] if event.nJet>0 else -999.)],
        [lambda tree: tree.branch("jetAK4_pt1_raw", "F"), lambda tree, event: tree.fillBranch("jetAK4_pt1_raw", event.Jet_pt_raw[0] if event.nJet>0 else -999.)],
        [lambda tree: tree.branch("jetAK4_pt1_nom", "F"), lambda tree, event: tree.fillBranch("jetAK4_pt1_nom", event.Jet_pt_nom[0] if event.nJet>0 else -999.)],
        [lambda tree: tree.branch("jetAK4_eta1", "F"), lambda tree, event: tree.fillBranch("jetAK4_eta1", event.Jet_eta[0] if event.nJet>0 else -999.)],
        [lambda tree: tree.branch("jetAK4_y1", "F"), lambda tree, event: tree.fillBranch("jetAK4_y1", max(min(ROOT.Math.PtEtaPhiMVector(event.Jet_pt[0],event.Jet_eta[0],event.Jet_phi[0],event.Jet_mass[0]).Rapidity(),999.),-999.) if event.nJet>0 else -999.)],
        [lambda tree: tree.branch("jetAK4_phi1", "F"), lambda tree, event: tree.fillBranch("jetAK4_phi1", event.Jet_phi[0] if event.nJet>0 else -999.)],
        [lambda tree: tree.branch("jetAK4_mass1", "F"), lambda tree, event: tree.fillBranch("jetAK4_mass1", event.Jet_mass[0] if event.nJet>0 else -999.)],
        [lambda tree: tree.branch("jetAK4_jec1", "F"), lambda tree, event: tree.fillBranch("jetAK4_jec1", (1.-event.Jet_rawFactor[0]) if event.nJet>0 else -999.)],
        [lambda tree: tree.branch("jetAK4_muf1", "F"), lambda tree, event: tree.fillBranch("jetAK4_muf1", event.Jet_muEF[0] if event.nJet>0 else -999.)],
        [lambda tree: tree.branch("jetAK4_nhf1", "F"), lambda tree, event: tree.fillBranch("jetAK4_nhf1", event.Jet_neHEF[0] if event.nJet>0 else -999.)],
        [lambda tree: tree.branch("jetAK4_chf1", "F"), lambda tree, event: tree.fillBranch("jetAK4_chf1", event.Jet_chHEF[0] if event.nJet>0 else -999.)],
        [lambda tree: tree.branch("jetAK4_area1", "F"), lambda tree, event: tree.fillBranch("jetAK4_area1", event.Jet_area[0] if event.nJet>0 else -999.)],
        [lambda tree: tree.branch("jetAK4_nemf1", "F"), lambda tree, event: tree.fillBranch("jetAK4_nemf1", event.Jet_neEmEF[0] if event.nJet>0 else -999.)],
        [lambda tree: tree.branch("jetAK4_cemf1", "F"), lambda tree, event: tree.fillBranch("jetAK4_cemf1", event.Jet_chEmEF[0] if event.nJet>0 else -999.)],
        [lambda tree: tree.branch("jetAK4_btagDeepFlavB1", "F"), lambda tree, event: tree.fillBranch("jetAK4_btagDeepFlavB1", event.Jet_btagDeepFlavB[0] if event.nJet>0 else -999.)],
        [lambda tree: tree.branch("jetAK4_TightID1", "i"), lambda tree, event: tree.fillBranch("jetAK4_TightID1", ((event.Jet_jetId[0] if isinstance(event.Jet_jetId[0],int) else ord(event.Jet_jetId[0]))>=6) if event.nJet>0 else 0)],
        [lambda tree: tree.branch("jetAK4_nConstituents1", "i"), lambda tree, event: tree.fillBranch("jetAK4_nConstituents1", ord(event.Jet_nConstituents[0]) if event.nJet>0 else 0)],
    ]
    storeVariables += [
        [lambda tree: tree.branch("jetAK4_pt2", "F"), lambda tree, event: tree.fillBranch("jetAK4_pt2", event.Jet_pt[1] if event.nJet>1 else -999.)],
        [lambda tree: tree.branch("jetAK4_pt2_raw", "F"), lambda tree, event: tree.fillBranch("jetAK4_pt2_raw", event.Jet_pt_raw[1] if event.nJet>1 else -999.)],
        [lambda tree: tree.branch("jetAK4_pt2_nom", "F"), lambda tree, event: tree.fillBranch("jetAK4_pt2_nom", event.Jet_pt_nom[1] if event.nJet>1 else -999.)],
        [lambda tree: tree.branch("jetAK4_eta2", "F"), lambda tree, event: tree.fillBranch("jetAK4_eta2", event.Jet_eta[1] if event.nJet>1 else -999.)],
        [lambda tree: tree.branch("jetAK4_y2", "F"), lambda tree, event: tree.fillBranch("jetAK4_y2", max(min(ROOT.Math.PtEtaPhiMVector(event.Jet_pt[1],event.Jet_eta[1],event.Jet_phi[1],event.Jet_mass[1]).Rapidity(),999.),-999.) if event.nJet>1 else -999.)],
        [lambda tree: tree.branch("jetAK4_phi2", "F"), lambda tree, event: tree.fillBranch("jetAK4_phi2", event.Jet_phi[1] if event.nJet>1 else -999.)],
        [lambda tree: tree.branch("jetAK4_mass2", "F"), lambda tree, event: tree.fillBranch("jetAK4_mass2", event.Jet_mass[1] if event.nJet>1 else -999.)],
        [lambda tree: tree.branch("jetAK4_jec2", "F"), lambda tree, event: tree.fillBranch("jetAK4_jec2", (1.-event.Jet_rawFactor[1]) if event.nJet>1 else -999.)],
        [lambda tree: tree.branch("jetAK4_muf2", "F"), lambda tree, event: tree.fillBranch("jetAK4_muf2", event.Jet_muEF[1] if event.nJet>1 else -999.)],
        [lambda tree: tree.branch("jetAK4_nhf2", "F"), lambda tree, event: tree.fillBranch("jetAK4_nhf2", event.Jet_neHEF[1] if event.nJet>1 else -999.)],
        [lambda tree: tree.branch("jetAK4_chf2", "F"), lambda tree, event: tree.fillBranch("jetAK4_chf2", event.Jet_chHEF[1] if event.nJet>1 else -999.)],
        [lambda tree: tree.branch("jetAK4_area2", "F"), lambda tree, event: tree.fillBranch("jetAK4_area2", event.Jet_area[1] if event.nJet>1 else -999.)],
        [lambda tree: tree.branch("jetAK4_nemf2", "F"), lambda tree, event: tree.fillBranch("jetAK4_nemf2", event.Jet_neEmEF[1] if event.nJet>1 else -999.)],
        [lambda tree: tree.branch("jetAK4_cemf2", "F"), lambda tree, event: tree.fillBranch("jetAK4_cemf2", event.Jet_chEmEF[1] if event.nJet>1 else -999.)],
        [lambda tree: tree.branch("jetAK4_btagDeepFlavB2", "F"), lambda tree, event: tree.fillBranch("jetAK4_btagDeepFlavB2", event.Jet_btagDeepFlavB[1] if event.nJet>1 else -999.)],
        [lambda tree: tree.branch("jetAK4_TightID2", "i"), lambda tree, event: tree.fillBranch("jetAK4_TightID2", ((event.Jet_jetId[1] if isinstance(event.Jet_jetId[1],int) else ord(event.Jet_jetId[1]))>=6) if event.nJet>1 else 0)],
        [lambda tree: tree.branch("jetAK4_nConstituents2", "i"), lambda tree, event: tree.fillBranch("jetAK4_nConstituents2", ord(event.Jet_nConstituents[1]) if event.nJet>1 else 0)],
    ]
    storeVariables += [
        [lambda tree: tree.branch("jetAK4_pt3", "F"), lambda tree, event: tree.fillBranch("jetAK4_pt3", event.Jet_pt[2] if event.nJet>2 else -999.)],
        [lambda tree: tree.branch("jetAK4_pt3_raw", "F"), lambda tree, event: tree.fillBranch("jetAK4_pt3_raw", event.Jet_pt_raw[2] if event.nJet>2 else -999.)],
        [lambda tree: tree.branch("jetAK4_pt3_nom", "F"), lambda tree, event: tree.fillBranch("jetAK4_pt3_nom", event.Jet_pt_nom[2] if event.nJet>2 else -999.)],
        [lambda tree: tree.branch("jetAK4_eta3", "F"), lambda tree, event: tree.fillBranch("jetAK4_eta3", event.Jet_eta[2] if event.nJet>2 else -999.)],
        [lambda tree: tree.branch("jetAK4_y3", "F"), lambda tree, event: tree.fillBranch("jetAK4_y3", max(min(ROOT.Math.PtEtaPhiMVector(event.Jet_pt[2],event.Jet_eta[2],event.Jet_phi[2],event.Jet_mass[2]).Rapidity(),999.),-999.) if event.nJet>2 else -999.)],
        [lambda tree: tree.branch("jetAK4_phi3", "F"), lambda tree, event: tree.fillBranch("jetAK4_phi3", event.Jet_phi[2] if event.nJet>2 else -999.)],
        [lambda tree: tree.branch("jetAK4_mass3", "F"), lambda tree, event: tree.fillBranch("jetAK4_mass3", event.Jet_mass[2] if event.nJet>2 else -999.)],
        [lambda tree: tree.branch("jetAK4_jec3", "F"), lambda tree, event: tree.fillBranch("jetAK4_jec3", (1.-event.Jet_rawFactor[2]) if event.nJet>2 else -999.)],
        [lambda tree: tree.branch("jetAK4_muf3", "F"), lambda tree, event: tree.fillBranch("jetAK4_muf3", event.Jet_muEF[2] if event.nJet>2 else -999.)],
        [lambda tree: tree.branch("jetAK4_nhf3", "F"), lambda tree, event: tree.fillBranch("jetAK4_nhf3", event.Jet_neHEF[2] if event.nJet>2 else -999.)],
        [lambda tree: tree.branch("jetAK4_chf3", "F"), lambda tree, event: tree.fillBranch("jetAK4_chf3", event.Jet_chHEF[2] if event.nJet>2 else -999.)],
        [lambda tree: tree.branch("jetAK4_area3", "F"), lambda tree, event: tree.fillBranch("jetAK4_area3", event.Jet_area[2] if event.nJet>2 else -999.)],
        [lambda tree: tree.branch("jetAK4_nemf3", "F"), lambda tree, event: tree.fillBranch("jetAK4_nemf3", event.Jet_neEmEF[2] if event.nJet>2 else -999.)],
        [lambda tree: tree.branch("jetAK4_cemf3", "F"), lambda tree, event: tree.fillBranch("jetAK4_cemf3", event.Jet_chEmEF[2] if event.nJet>2 else -999.)],
        [lambda tree: tree.branch("jetAK4_btagDeepFlavB3", "F"), lambda tree, event: tree.fillBranch("jetAK4_btagDeepFlavB3", event.Jet_btagDeepFlavB[2] if event.nJet>2 else -999.)],
        [lambda tree: tree.branch("jetAK4_TightID3", "i"), lambda tree, event: tree.fillBranch("jetAK4_TightID3", ((event.Jet_jetId[2] if isinstance(event.Jet_jetId[2],int) else ord(event.Jet_jetId[2]))>=6) if event.nJet>2 else 0)],
        [lambda tree: tree.branch("jetAK4_nConstituents3", "i"), lambda tree, event: tree.fillBranch("jetAK4_nConstituents3", ord(event.Jet_nConstituents[2]) if event.nJet>2 else 0)],
    ]
    storeVariables += [
        [lambda tree: tree.branch("mjj", "F"), lambda tree, event: tree.fillBranch("mjj", (ROOT.Math.PtEtaPhiMVector(event.Jet_pt[0],event.Jet_eta[0],event.Jet_phi[0],event.Jet_mass[0])+ROOT.Math.PtEtaPhiMVector(event.Jet_pt[1],event.Jet_eta[1],event.Jet_phi[1],event.Jet_mass[1])).M() if event.nJet>1 else -999.)],
        [lambda tree: tree.branch("mjj_raw", "F"), lambda tree, event: tree.fillBranch("mjj_raw", (ROOT.Math.PtEtaPhiMVector(event.Jet_pt_raw[0],event.Jet_eta[0],event.Jet_phi[0],event.Jet_mass_raw[0])+ROOT.Math.PtEtaPhiMVector(event.Jet_pt_raw[1],event.Jet_eta[1],event.Jet_phi[1],event.Jet_mass_raw[1])).M() if event.nJet>1 else -999.)],
        [lambda tree: tree.branch("mjj_nom", "F"), lambda tree, event: tree.fillBranch("mjj_nom", (ROOT.Math.PtEtaPhiMVector(event.Jet_pt_nom[0],event.Jet_eta[0],event.Jet_phi[0],event.Jet_mass_nom[0])+ROOT.Math.PtEtaPhiMVector(event.Jet_pt_nom[1],event.Jet_eta[1],event.Jet_phi[1],event.Jet_mass_nom[1])).M() if event.nJet>1 else -999.)],
        [lambda tree: tree.branch("chi", "F"), lambda tree, event: tree.fillBranch("chi", math.exp(abs(ROOT.Math.PtEtaPhiMVector(event.Jet_pt[0],event.Jet_eta[0],event.Jet_phi[0],event.Jet_mass[0]).Rapidity()-ROOT.Math.PtEtaPhiMVector(event.Jet_pt[1],event.Jet_eta[1],event.Jet_phi[1],event.Jet_mass[1]).Rapidity())) if event.nJet>1 else 999.)],
        [lambda tree: tree.branch("yboost", "F"), lambda tree, event: tree.fillBranch("yboost", abs(ROOT.Math.PtEtaPhiMVector(event.Jet_pt[0],event.Jet_eta[0],event.Jet_phi[0],event.Jet_mass[0]).Rapidity()+ROOT.Math.PtEtaPhiMVector(event.Jet_pt[1],event.Jet_eta[1],event.Jet_phi[1],event.Jet_mass[1]).Rapidity())/2. if event.nJet>1 else 999.)],
    ]
    if "mc" in options.branchsel_out:
      storeVariables += [
        [lambda tree: tree.branch("jetAK4_partonFlavour1", "I"), lambda tree, event: tree.fillBranch("jetAK4_partonFlavour1", event.Jet_partonFlavour[0] if event.nJet>0 else -999)],
        [lambda tree: tree.branch("jetAK4_partonFlavour2", "I"), lambda tree, event: tree.fillBranch("jetAK4_partonFlavour2", event.Jet_partonFlavour[1] if event.nJet>1 else -999)],
        [lambda tree: tree.branch("jetAK4_partonFlavour3", "I"), lambda tree, event: tree.fillBranch("jetAK4_partonFlavour3", event.Jet_partonFlavour[2] if event.nJet>2 else -999)],
      ]
      storeVariables += [
        [lambda tree: tree.branch("genJetAK4_pt1", "F"), lambda tree, event: tree.fillBranch("genJetAK4_pt1", event.GenJet_pt[0] if event.nGenJet>0 else -999.)],
        [lambda tree: tree.branch("genJetAK4_eta1", "F"), lambda tree, event: tree.fillBranch("genJetAK4_eta1", event.GenJet_eta[0] if event.nGenJet>0 else -999.)],
        [lambda tree: tree.branch("genJetAK4_y1", "F"), lambda tree, event: tree.fillBranch("genJetAK4_y1", max(min(ROOT.Math.PtEtaPhiMVector(event.GenJet_pt[0],event.GenJet_eta[0],event.GenJet_phi[0],event.GenJet_mass[0]).Rapidity(),999.),-999.) if event.nGenJet>0 else -999.)],
        [lambda tree: tree.branch("genJetAK4_phi1", "F"), lambda tree, event: tree.fillBranch("genJetAK4_phi1", event.GenJet_phi[0] if event.nGenJet>0 else -999.)],
        [lambda tree: tree.branch("genJetAK4_mass1", "F"), lambda tree, event: tree.fillBranch("genJetAK4_mass1", event.GenJet_mass[0] if event.nGenJet>0 else -999.)],
      ]
      storeVariables += [
        [lambda tree: tree.branch("genJetAK4_pt2", "F"), lambda tree, event: tree.fillBranch("genJetAK4_pt2", event.GenJet_pt[1] if event.nGenJet>1 else -999.)],
        [lambda tree: tree.branch("genJetAK4_eta2", "F"), lambda tree, event: tree.fillBranch("genJetAK4_eta2", event.GenJet_eta[1] if event.nGenJet>1 else -999.)],
        [lambda tree: tree.branch("genJetAK4_y2", "F"), lambda tree, event: tree.fillBranch("genJetAK4_y2", max(min(ROOT.Math.PtEtaPhiMVector(event.GenJet_pt[1],event.GenJet_eta[1],event.GenJet_phi[1],event.GenJet_mass[1]).Rapidity(),999.),-999.) if event.nGenJet>1 else -999.)],
        [lambda tree: tree.branch("genJetAK4_phi2", "F"), lambda tree, event: tree.fillBranch("genJetAK4_phi2", event.GenJet_phi[1] if event.nGenJet>1 else -999.)],
        [lambda tree: tree.branch("genJetAK4_mass2", "F"), lambda tree, event: tree.fillBranch("genJetAK4_mass2", event.GenJet_mass[1] if event.nGenJet>1 else -999.)],
      ]
      storeVariables += [
        [lambda tree: tree.branch("genJetAK4_pt3", "F"), lambda tree, event: tree.fillBranch("genJetAK4_pt3", event.GenJet_pt[2] if event.nGenJet>2 else -999.)],
        [lambda tree: tree.branch("genJetAK4_eta3", "F"), lambda tree, event: tree.fillBranch("genJetAK4_eta3", event.GenJet_eta[2] if event.nGenJet>2 else -999.)],
        [lambda tree: tree.branch("genJetAK4_y3", "F"), lambda tree, event: tree.fillBranch("genJetAK4_y3", max(min(ROOT.Math.PtEtaPhiMVector(event.GenJet_pt[2],event.GenJet_eta[2],event.GenJet_phi[2],event.GenJet_mass[2]).Rapidity(),999.),-999.) if event.nGenJet>2 else -999.)],
        [lambda tree: tree.branch("genJetAK4_phi3", "F"), lambda tree, event: tree.fillBranch("genJetAK4_phi3", event.GenJet_phi[2] if event.nGenJet>2 else -999.)],
        [lambda tree: tree.branch("genJetAK4_mass3", "F"), lambda tree, event: tree.fillBranch("genJetAK4_mass3", event.GenJet_mass[2] if event.nGenJet>2 else -999.)],
      ]
      storeVariables += [
        [lambda tree: tree.branch("genmjj", "F"), lambda tree, event: tree.fillBranch("genmjj", (ROOT.Math.PtEtaPhiMVector(event.GenJet_pt[0],event.GenJet_eta[0],event.GenJet_phi[0],event.GenJet_mass[0])+ROOT.Math.PtEtaPhiMVector(event.GenJet_pt[1],event.GenJet_eta[1],event.GenJet_phi[1],event.GenJet_mass[1])).M() if event.nGenJet>1 else -999.)],
        [lambda tree: tree.branch("genchi", "F"), lambda tree, event: tree.fillBranch("genchi", math.exp(abs(ROOT.Math.PtEtaPhiMVector(event.GenJet_pt[0],event.GenJet_eta[0],event.GenJet_phi[0],event.GenJet_mass[0]).Rapidity()-ROOT.Math.PtEtaPhiMVector(event.GenJet_pt[1],event.GenJet_eta[1],event.GenJet_phi[1],event.GenJet_mass[1]).Rapidity())) if event.nGenJet>1 else 999.)],
        [lambda tree: tree.branch("genyboost", "F"), lambda tree, event: tree.fillBranch("genyboost", abs(ROOT.Math.PtEtaPhiMVector(event.GenJet_pt[0],event.GenJet_eta[0],event.GenJet_phi[0],event.GenJet_mass[0]).Rapidity()+ROOT.Math.PtEtaPhiMVector(event.GenJet_pt[1],event.GenJet_eta[1],event.GenJet_phi[1],event.GenJet_mass[1]).Rapidity())/2. if event.nGenJet>1 else 999.)],
      ]
    
    modules.append(EventInfo(storeVariables=storeVariables))
    
    p = PostProcessor(outdir, args,
                      cut=options.cut,
                      branchsel=options.branchsel_in,
                      modules=modules,
                      compression=options.compression,
                      friend=options.friend,
                      postfix=options.postfix,
                      jsonInput=options.json,
                      noOut=options.noOut,
                      justcount=options.justcount,
                      prefetch=options.prefetch,
                      longTermCache=options.longTermCache,
                      maxEntries=options.maxEntries,
                      firstEntry=options.firstEntry,
                      outputbranchsel=options.branchsel_out)
    p.run()
