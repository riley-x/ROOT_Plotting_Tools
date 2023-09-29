#!/usr/bin/env python3

'''
Run this file with 

    python3 examples/stack_plot.py

This script plots MC backgrounds in a stack, then overlays total error as a hash
band and data points as points.

This showcases both the 'stack' option and how to use the low-level plotter class 
to do some advanced formatting.  
'''

import ROOT
import plot
import histograms

def stack_plot():
    h_bkgs, h_sum, h_data, h_ratio = get_hists()

    ### Create canvas and pads ###
    c = ROOT.TCanvas('c1', 'c1', 1000, 800)
    height2 = 0.3

    pad1 = ROOT.TPad('pad1', 'pad1', 0, height2, 1, 1)
    pad1.SetBottomMargin(0.03)
    pad1.Draw()

    c.cd()
    pad2 = ROOT.TPad('pad2', 'pad2', 0, 0, 1, height2)
    pad2.SetBottomMargin(0.12 / height2)
    pad2.Draw()

    ### Initialize main pad plotter ###
    plotter1 = plot.Plotter(pad1, 
        title='ATLAS Dummy',
        subtitle='#sqrt{s}=13 TeV, 139 fb^{-1}',
        ytitle='Events',
        x_range=[50, 150],
        y_range=[0, None], # automatic top range
        remove_x_labels=True,
    )

    ### Plot the background histograms as a stack ###
    plotter1.add(h_bkgs,
        stack=True,
        opts='HIST',
        linewidth=0,
        fillcolor=plot.colors.pastel,
        legend=['Diboson', 'Single Top', 't#bar{t}', 'W+jets'],
    )

    ### Plot the total MC error as a hash ###
    plotter1.add([h_sum],
        fillcolor=plot.colors.gray,
        fillstyle=3145,
        linewidth=0,
        markerstyle=0,
        opts='E2',
        legend_opts='F',
        legend=['MC Stat'],
    )

    ### Plot the data points ###
    plotter1.add([h_data],
        opts='E',
        legend_opts='PE',
        legend=['Data'],
    )

    ### Create the ratio plot ###
    plotter2 = plot.Plotter(pad2, 
        objs=[h_ratio],
        ytitle='Data / MC',
        xtitle='m(J) [GeV]',
        x_range=[50, 150],
        y_range=[0.75, 1.25],
        ydivs=503,
        title=None,
    )

    ### Draw and save ###
    plotter1.draw()
    plotter2.draw()
    plotter2.draw_hline(1, style=ROOT.kDashed)
    plot.save_canvas(c, 'stack_plot')



def get_hists():
    import numpy as np
    
    hists = histograms.hists_mj_samples
    h_sum = hists[0].Clone()
    for h in hists[1:]:
        h_sum.Add(h)
    
    h_data = h_sum.Clone()
    for i in range(len(h_data)):
        if h_data[i] < 0: 
            h_data[i] = 0
            h_data.SetBinError(i, 0)
        else:
            h_data[i] += np.random.normal(scale=h_data[i]**0.5)
            if h_data[i] < 0: h_data[i] = 0
            h_data.SetBinError(i, h_data[i] ** 0.5)

    h_ratio = h_data.Clone()
    h_ratio.Divide(h_sum)

    return hists, h_sum, h_data, h_ratio
    

if __name__ == "__main__":
    plot.save_transparent = False
    stack_plot()