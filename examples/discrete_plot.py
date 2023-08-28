#!/usr/bin/env python3

'''
Run this file with 

    python3 examples/discrete_plot.py

This script showcases both plot.plot_discrete_bins(), which plots histograms discretized
in equal-width bins, and plot.plot_ratio3(), which adds two subplots beneath the main 
plot.
'''

import plot
import histograms
import ROOT

def discrete_plot():
    hists = histograms.hists_mVV_vjetsfit
    args = {
        'filename':     'discrete_plot',
        'title':        'ATLAS Dummy',
        'subtitle':     [
            '#sqrt{s}=13 TeV, 139 fb^{-1}',
            'W+jets Fits',
        ],
        'legend':       ['MC', 'GPR MLE Fit', 'GPR p(f | X,y)'],
        'xtitle':       'm(VV) [GeV]',
    }

    ### Main pad ###
    for i,h in enumerate(hists): # Do styles before cloning for the ratio plots
        h.SetLineWidth(2)
        h.SetLineColor(plot.colors.tableu(i))
        h.SetFillColorAlpha(plot.colors.tableu(i), 0.2)
        h.SetMarkerColor(plot.colors.tableu(i))
        h.SetMarkerStyle(ROOT.kFullCircle + i)
    args.setdefault('ytitle', 'Events / GeV')
    args.setdefault('opts', 'P2+')
    args.setdefault('legend_opts', 'PE')
    args.setdefault('x_range', None)
    args.setdefault('y_range', [0, None])

    ### Ratio plot ###
    hists2 = _ratios(hists)
    args.setdefault('opts2', 'P2+')
    args.setdefault('ytitle2', '#frac{Fit}{MC}')
    args.setdefault('ignore_outliers_y2', 0)
    args.setdefault('hline2', 1)

    ### Fractional uncertainty ###
    hists3 = _fractional_uncertainties(hists)
    args.setdefault('opts3', 'P2+')
    args.setdefault('ytitle3', '% Error')
    args.setdefault('ignore_outliers_y3', 0)
    args.setdefault('y_range3', [0, None])

    ### Remove bottom ticks ###
    def frame_callback(frame):
        frame.GetYaxis().ChangeLabel(1, -1, 0)
    args['frame_callback'] = frame_callback
    args['frame_callback2'] = frame_callback

    ### Plot ###
    plot.plot_discrete_bins(hists, hists2, hists3, plotter=plot.plot_ratio3, **args)


def _ratios(hists):
    hists2 = []
    for h in hists[1:]:
        r = h.Clone()
        r.Divide(hists[0])
        hists2.append(r)
    return hists2


def _fractional_uncertainties(hists):
    hists3 = []
    for h in hists:
        h = h.Clone()
        for i in range(h.GetNbinsX() + 2):
            v = h.GetBinContent(i)
            if v > 0:
                h.SetBinContent(i, 100 * h.GetBinError(i) / v)
            else:
                h.SetBinContent(i, 0)
            h.SetBinError(i, 0)
        hists3.append(h)
    return hists3



if __name__ == "__main__":
    plot.save_transparent = False
    discrete_plot()