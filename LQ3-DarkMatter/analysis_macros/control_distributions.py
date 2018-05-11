#############################################
#          control_distributions.py
#       Author: Joshuha Thomas-Wilsker
#           IHEP Beijing, CERN
#############################################
from ROOT import TFile, TTree gDirectory, gROOT, TH1, TF1, TProfile
from array import array
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

def main():
    signal_rootfile = TFile('')
    histo_outputFile = open('signal_control_distributions.xml','w+')
