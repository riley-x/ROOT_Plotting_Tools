#!/usr/bin/env python3

'''
Run this file with 

    python3 examples/ratio_plot.py

This script creates a plot with multi-dim formatting and a ratio subplot.
'''

import plot
import histograms

def ratio_plot():
    hists = histograms.hists_mV_unfolding
    hists_shape = (2, 2)

    ### Ratios ###
    ratios = []
    for i in range(0, len(hists), 2):
        r = hists[i + 1].Clone()
        r.Divide(hists[i])
        ratios.append(r)

    ### Format and legend ###
    plot.format(hists, hists_shape)
    legend_hists = plot.reduced_legend_hists(hists_shape)
    legend = [
        (legend_hists[0], 'Diboson', 'L'),
        (legend_hists[1], 'EFT c_{W}^{2}', 'L'),
        (legend_hists[2], 'Fiducial', 'L'),
        (legend_hists[3], 'Fid #cap Reco', 'L'),
    ]

    ### Plot ###
    plot.plot_ratio(hists, ratios,
        filename='ratio_plot',
        ### Text ###
        title='ATLAS Dummy',
        subtitle='#sqrt{s}=13 TeV, 139 fb^{-1}',
        legend=legend,
        ytitle='Events',
        ytitle2='Efficiency',
        xtitle='p_{T}(V) [GeV]',
        ### Style ###
        height1=0.6,
        logy=True,
        opts='HIST',
        markersize=0,
        markersize2=0,
        linecolor2=plot.colors.tableu,
        ### Range ###
        x_range=[0, 2500],
        y_range2=[0, 0.5], 
    )


if __name__ == "__main__":
    plot.save_transparent = False
    ratio_plot()