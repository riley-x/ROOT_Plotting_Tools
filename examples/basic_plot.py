#!/usr/bin/env python3

'''
Run this file with 

    python3 examples/basic_plot.py

This script creates a simple, single-canvas plot with title text and a legend.
Notice the text and legend get placed automatically and do not overlap the data.
'''

import plot
import histograms

def basic_plot():
    plot.plot(histograms.hists_mj_samples,
        filename='basic_plot',
        ### Text ###
        title='ATLAS Simulation',
        subtitle='#sqrt{s}=13 TeV, 139 fb^{-1}',
        legend=['Diboson', 'Single Top', 't#bar{t}', 'W+jets'],
        ytitle='Events',
        xtitle='p_{T}(J) [GeV]',
        ### Style ###
        linecolor=plot.colors.tableu,
        markersize=0,
        ### Range ###
        x_range=[50, 250],
        y_range=[0, None], # automatic top range
    )


if __name__ == "__main__":
    plot.save_transparent = False
    plot.file_formats = ['png', 'pdf']
    basic_plot()