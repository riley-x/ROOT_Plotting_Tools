#!/usr/bin/env python3

'''
Run this file with 

    python3 examples/tiered_plot.py

This script showcases plot.plot_tiered(), which plots multiple histograms in several
top-to-bottom tiers. This plot style is useful for comparing multiple distribution 
shapes without crowding the plot, at the cost of obscuring the normalizations.
'''

import plot
import histograms
import ROOT

def tiered_plot():
    hists = histograms.hists_ptV_tiered_mVV_SMvEFT
    hists = [[hists[i], hists[i+1]] for i in range(0, len(hists), 2)]
    args = {
        'filename':     'tiered_plot',
        'title':        'ATLAS Dummy',
        'subtitle':     '#sqrt{s}=13 TeV, 139 fb^{-1}',
        'legend':       ['SM Diboson', 'EFT c_{W}^{2}'],
        'xtitle':       'p_{T}(V) [GeV]',
        'ytitle':       'Normalized Events',
        'tier_title':   'm(VV) [GeV]',
        'tier_labels':  make_bins([0, 200, 500, 800, 1200, 2000, 3000]),
        'linecolor':    plot.colors.tableu,
        'x_range':      [0, 2000],
        'xdivs':        506,
    }
    plot.plot_tiered(hists, **args)


def make_bins(vals):
    out = []
    for i in range(len(vals) - 1):
        out.append('{},{}'.format(vals[i], vals[i+1]))
    return out



if __name__ == "__main__":
    plot.save_transparent = False
    tiered_plot()