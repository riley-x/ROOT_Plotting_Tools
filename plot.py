#!/usr/bin/env python3

'''
@file plot.py
@author Riley Xu - riley.xu@gmail.com, riley.xu@cern.ch
@date June 22, 2021
@brief Declarative ROOT plotting tools
@requires Python >= 3.6 (setupATLAS && lsetup "root recommended" && lsetup "python centos7-3.9")

Riley's declarative ROOT plotting toolkit. Instead of manually adjusting each histogram,
you can specify style in aggregate. Typical usage would look like:

    import plot
    plot.plot([h1, h2],                         # plots two histograms in the same canvas
        opts = ['HIST', 'PE'],                  # plot h1 in 'HIST' format and h2 in 'PE' format
        linecolor = plot.colors.tableu,         # sets each histogram's line color using a MPL colormap
        linewidth = 3,                          # applied to both histograms
        subtitle = '#sqrt{s} = 13 TeV^{-1}',    # text options can accept TLatex formatters
        legend = ['Hist 1', 'Hist 2'],
        ytitle = 'Events',
        xtitle = 'm_{T}(W) [GeV]',              
        filename = 'my_plot.png',
    )

The input also doesn't have to be all histograms, you can include TF1s and TGraphs too. 
In addition, this script takes care of several things missing in ROOT: automatic axis
ranges, easier legend placement, title text and subtext, etc. It also defines helper
functions to make some common plot types, like ratio plots. A full list of top-level
functions is shown below, along with a list of common options they accept.

The [colors] class defines many useful colors and some Matplotlib colormaps, which can be
accessed easily as `plot.colors.tableu(0)`. See the docstring for the class for more info.

The format of the saved image is inferred by ROOT based on the extension in the filename.
If the extension is omitted, the canvas will be saved for each extension listed in
[plot.file_formats]. This is convenient to save a plot as both a pdf and a png, for 
example.

-----------------------------------------------------------------------------------------
TOP-LEVEL PLOTTING FUNCTIONS
-----------------------------------------------------------------------------------------
Most of these functions expect one or more lists of TObjects as the graph inputs, and 
accept a variety of common options listed below. See the individual docstring for more
info.
-----------------------------------------------------------------------------------------
plot
    The basic go-to plotting function. Plots everything onto the same axis.
plot_ratio
    Plots a ratio plot; a main plot is shown on top with a separate, smaller plot shown
    on bottom. This function doesn't calcualte any actual ratios, you pass it instead two
    lists of TObjects. 
plot_ratio3
    Similar to [plot_ratio] but with two subplots beneath a main plot.
plot_two_scale
    Plots two y-axes on a shared x-axis. TODO might be a bit outdated.
plot_tiered
    Similar to a violin plot. Plots each input histogram at separated y-values. Useful
    for eye-balling differences between many different distributions, which would get 
    crowded on a standard plot. 
_plot
    The underlying plotting function used by everything above. Basically the same as 
    [plot] but you need to pass it a TPad. Useful for creating custom images containing 
    multiple canvases.




-----------------------------------------------------------------------------------------
COMMON PLOTTING OPTIONS
-----------------------------------------------------------------------------------------

BASIC STYLE
--------------------------------------------------------
All of these options can be specified as a single value to apply to all input TObjects, a
list of values matching each input TObject, or a function that takes the index into the 
list of TObjects. 
--------------------------------------------------------
opts
    Options to TObject::Draw(), such as 'HIST' or 'PE'. Note that you don't need to
    specify 'SAME' or 'A', unless you're calling _plot on the same pad more than once. 
    For TH2s, you can also input things like 'TEXT:4.2f' to specify a printf formatter 
    when drawing with 'TEXT'.
linecolor
linestyle
linewidth
    Sets the corresponding TAttLine properties. See the ROOT documentation for input
    values.
markercolor
markerstyle
markersize
    Sets the corresponding TAttMarker properties. See the ROOT documentation for input
    values.
fillcolor
fillstyle
    Sets the corresponding TAttFill properties. See the ROOT documentation for input
    values.

TEXT AND FILE NAMES
--------------------------------------------------------
filename
    Path to save the image to. If the filename ends with an extension like '.png', the
    file will be saved in that format. If no extension is given, saves the file with
    each extension in [plot.file_formats].
textpos                                                 default: 'top left'
    Location of title / legend. Can be a combination of [top/bottom] and/or [left/right],
    so for example 'top' will place the title in the top-left corner and the legend in
    the top-right, while 'top left' will place both in the top-left corner. You can also 
    specify 'forward diagonal' or 'backward diagonal' to place the title and legend in
    diagonally opposite corners. You can add 'reverse' to some of these to reverse the 
    title and legend positions.
title                                                   default: 'Internal'
    A string that appears after the ATLAS logo. Set to None to omit the logo entirely.
subtitle
    Additional text that is displayed below the ATLAS logo. This can be a string or a 
    list of strings, with the latter putting each entry on a new line.
titlesize                                               default: 0.05
    ROOT text size for the title.

    WARNING ROOT has a bug with measuring text that isn't at some golden sizes. It seems 
    0.05 and 0.035 work well. This may cause right aligning to be broken; it seems the 
    longer the text the more off it'll be.
titlespacing                                           default: 1.0
    Multiplicative factor for increasing the spacing between title/subtitle/legend.

AXES
-----------------------------------------------------
logx/y/z
    Sets the canvas to use log x/y/z axes.
xtitle/ytitle
    Title for the x/y-axis.
xdivs/ydivs
    See TAxis::SetNdivisions. Sets the number of ticks on each axis. 
xrange/yrange                                           default: None / (None, None)
    Specify a list or a tuple of the (min, max) range of the axis to plot. You can set
    either entry to None to automatically fit plot contents. Set the entire argument to
    None to use default ROOT behavior. 
ydatapad_bot/top                                        default: 0.1
    If using an automatic y-axis range, amount of padding at the bottom/top so that the
    data points don't crowd the edges. Also useful to make room for titles and legends.
    The value is in axis coordinates, so a value of 0.1 on both bottom and top makes the
    data only appear in the center 80% of the plot. 
ignore_outliers_y
    If using an automatic y-axis range, will ignore points when calculating the min/max
    bounds if they're more than this many standard deviations away from the mean.

LEGEND
-----------------------------------------------------
legend                                                  default: []
    A list of labels that matches the order of the input TObjects. Can also be an empty
    list to auto-create labels using the object names, or None to not create a legend.
    An empty string omits that entry.
legend_order        
    Reorders and trims the legend. Input a list of indexes into the list in [legend], so
    for example [3, 0, 1] will place the 4th entry first and omit the 3rd. 
legend_opts
    A list matching the legend labels that changes how the symbol is drawn. Can be any 
    mix of the letters 'PEFL' for point, error bars, fill, line. 
legend_custom 
    Input a list of (TObject, label, legend_opt) tuples to create the legend instead of
    using the input TObjects. This nullifies the above options.



-----------------------------------------------------------------------------------------
UTILITY FUNCTIONS
-----------------------------------------------------------------------------------------
See each function's docstring for more info.
-----------------------------------------------------------------------------------------
colors_from_palette
    Returns a list of equally spaced colors from a ROOT palette.
save_canvas_transparent
    Saves a transparent canvas instead of the default white background. Set the global
    variable [plot.save_transparent] to True to enable in the plot functions above.
format
    Automatically formats a list of TObjects. 
'''

import ROOT
import itertools
import math
import ctypes
import numpy as np

ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gROOT.SetStyle("ATLAS")
ROOT.gROOT.ForceStyle()
ROOT.TGaxis.SetMaxDigits(4) # Number of digis to show on an axis, above which exponential notation is used

file_formats = ['png']
save_transparent = True

##############################################################################
###                                PLOTTING                                ###
##############################################################################

def _arg(val, i):
    '''
    Returns val(i) if val is a function and val[i] if val is a list. Otherwise 
    just returns val.
    '''
    if callable(val):
        return val(i)
    elif hasattr(val, '__getitem__') and not isinstance(val, str):
        return val[i]
    else:
        return val


def _auto_xrange(objs, xrange=(None,None), **kwargs):
    if xrange[0] is None or xrange[1] is None:
        x_min = None
        x_max = None
        for obj in objs:
            if 'TH1' not in obj.ClassName():
                continue
            o_min = None
            o_max = None
            for x in range(1, obj.GetNbinsX() + 1):
                if obj.GetBinContent(x) != 0 or obj.GetBinError(x) != 0:
                    if o_min is None: o_min = obj.GetBinLowEdge(x)
                    o_max = obj.GetBinLowEdge(x + 1)
            if o_min is None or o_max is None: continue
            x_min = o_min if x_min is None else min(x_min, o_min)
            x_max = o_max if x_max is None else max(x_max, o_max)

        newrange = (x_min if xrange[0] is None else xrange[0], x_max if xrange[1] is None else xrange[1])
        if isinstance(xrange, list):
            xrange[0] = newrange[0]
            xrange[1] = newrange[1]
    else:
        newrange = xrange

    if newrange[0] is None or newrange[1] is None:
        return None
    return newrange


def _get_minmax(obj, xrange = None, ignore_outliers_y=0, **kwargs):
    '''
    Returns (min, min>0, max) of [obj]

    @ignore_outliers_y     
        If nonzero, ignores point that are > that number of std dev away from the mean of [obj]
    '''
    if 'TH1' in obj.ClassName() or 'TProfile' in obj.ClassName():
        n = obj.GetNbinsX()
        def get(i):
            return (obj.GetBinCenter(i+1), obj.GetBinContent(i+1), obj.GetBinError(i+1))
    elif 'TGraph' in obj.ClassName():
        n = obj.GetN()
        def get(i):
            return (obj.GetPointX(i), obj.GetPointY(i), 1)
    else:
        raise RuntimeError('_get_minmax() unknown class ' + obj.ClassName())

    ### First pass: get mean and std dev ###
    if ignore_outliers_y:
        mean = 0
        std = 0
        w_sum = 0
        for i in range(n):
            x,y,e = get(i)
            if xrange:
                if x < xrange[0] or x > xrange[1]: continue
            if e == 0: continue
            w_sum += 1/e
            mean_old = mean
            mean += (y - mean_old) / (e * w_sum)
            std += (y - mean_old) * (y - mean) / e
        std = 0 if (std < 0 or w_sum <= 0) else (std / w_sum)**0.5 # float imprecision

    ### Second pass: get min/max ###
    o_min = None
    o_pos = None
    o_max = None
    for i in range(n):
        x,y,e = get(i)
        if y == 0 and e == 0: # ignore empty bins
            continue
        if y == math.inf:
            raise RuntimeError(f"_get_minmax() encountered math.inf at bin {i} of {obj.GetName()}")
        if xrange:
            if x < xrange[0] or x > xrange[1]: continue
        if ignore_outliers_y:
            if e != 0 and abs(y - mean) > ignore_outliers_y * std: continue

        o_min = y if o_min is None else min(o_min, y)
        o_max = y if o_max is None else max(o_max, y)
        if y > 0:
            o_pos = y if o_pos is None else min(o_pos, y)
    return (o_min, o_pos, o_max)


def _auto_yrange(objs, start_at_zero=False, at_least_zero=False, yrange=(None,None), logy=None, ydatapad_bot=0.1, ydatapad_top=0.1, **kwargs):
    '''
    Calculates automatic y-axis limits to fit the current content, with padding.

    @returns The new y-axis limits, as (y_min, y_max)

    @param objs
        A list of ROOT TObjects. This function will calculate the axis limits based on the
        min/max value among all these objects.
    @param yrange
        Initial y limit values. `None` indicates that this function should optimize that limit,
        while a set value will be kept as is. Note that if [yrange] is a list, any `None` will
        be replaced with the calculated the value.
    @param ydatapad_bot, ydatapad_top
        Amount of vertical padding to incorporate. These are in axis units, fractions of the
        axis height. The sum of these two parameters should be in [0, 1].
    '''
    if yrange[0] is None or yrange[1] is None:
        min_val = None
        max_val = None
        for obj in objs:
            if 'TF' in obj.ClassName(): continue
            min_obj,min_pos,max_obj = _get_minmax(obj, **kwargs)
            if not min_obj or not max_obj:
                continue
            if logy and min_pos:
                if not min_val or min_pos < min_val: 
                    min_val = min_pos
            elif min_val is None or min_obj < min_val:
                min_val = min_obj
            if max_val is None or max_obj > max_val:
                max_val = max_obj
        if min_val is None:
            print(f"WARNING! _auto_yrange() min_val is None, setting to 0. max_val =", max_val)
            min_val = 0
        if max_val is None:
            print(f"WARNING! _auto_yrange() max_val is None, setting to 0. min_val =", min_val)
            max_val = 0

        if logy:
            min_val = np.log10(min_val)
            max_val = np.log10(max_val)
        elif min_val >= 0:
            at_least_zero = True # If !start_at_zero but everything is positive, make sure that the y_min is at least 0

        data_height = 1.0 - ydatapad_bot - ydatapad_top
        if start_at_zero and not logy and min_val >= 0:
            y_min = 0
            y_max = max_val / data_height
        else:
            diff = (max_val - min_val)
            y_min = min_val - diff * ydatapad_bot / data_height
            y_max = max_val + diff * ydatapad_top / data_height

        if logy:
            newrange = (np.power(10, y_min) if yrange[0] is None else yrange[0], np.power(10, y_max) if yrange[1] is None else yrange[1])
        else:
            newrange = (y_min if yrange[0] is None else yrange[0], y_max if yrange[1] is None else yrange[1])

            ### Fix unoptimized ticks when ydivs is small ###
            if ydivs := kwargs.get('ydivs'):
                if ydivs % 100 <= 5:
                    for i in range(3): # try three times at most
                        nbins = ctypes.c_int(0)
                        bin_low = ctypes.c_double(0)
                        bin_high = ctypes.c_double(0)
                        bin_width = ctypes.c_double(0)
                        ROOT.THLimitsFinder.Optimize(*newrange, ydivs % 100, bin_low, bin_high, nbins, bin_width, '')
                        #print(newrange, bin_low, bin_high, nbins, bin_width)

                        # This seems to be when the ticks aren't optimized?
                        need_fix = (nbins.value == 0 or newrange[0] > bin_low.value or newrange[1] < bin_high.value)
                        if not need_fix: break
                        if newrange[0] == 0:
                            newrange = (0, newrange[1] * 1.1)
                        else:
                            diff = newrange[1] - newrange[0]
                            newrange = (newrange[0] - diff * 0.1, newrange[1] + diff * 0.1)
            
        if at_least_zero:
            newrange = (max(newrange[0], 0), newrange[1])
        if isinstance(yrange, list):
            yrange[0] = newrange[0]
            yrange[1] = newrange[1]
    else:
        newrange = yrange

    return newrange


def _max_width(leg_items, text_size):
    '''
    Gets the maximum width of a legend label

    @param leg_items: A list of (_, label, _)
    '''
    _max = 0
    for _,label,_ in leg_items:
        width = get_text_size(label, text_size)[0]
        if width > _max: _max = width
    return _max


def get_text_size(text, text_size):
    tex = ROOT.TLatex(0, 0, text)
    tex.SetTextFont(42)
    tex.SetTextSize(text_size)
    return tex.GetXsize(), tex.GetYsize()


def _plot(c, objs, opts="",
    textpos='topleft', titlesize=0.05, titlespacing=1, title='Internal', subtitle=None,
    legend=[], legend_order=None, legend_split=1, legend_width=0.2, legend_opts=None, legend_custom=None,
    rightmargin=None,
    logx=None, logy=None, logz=None, stack=False,
    canvas_callback=None,
    **kwargs):
    '''
    Main plotting helper function. Plots [objs] on [c], and also a title and legend.
    Returns any created ROOT objects (THStack is first), which must not be garbage collected
    until the canvas is drawn.

    See file header for list of options.
    '''
    cache = [] # Store ROOT objects so python doesn't garbage collect these, otherwise they won't plot.

    ### Canvas
    c.cd()
    if logx is not None: c.SetLogx(logx)
    if logy is not None: c.SetLogy(logy)
    if logz is not None: c.SetLogz(logz)
    if rightmargin is None:
        if 'COLZ' in opts:
            rightmargin = 0.13
        else:
            rightmargin = 0.05
    c.SetRightMargin(rightmargin)

    ### Create legend
    do_legend = legend is not None and len(objs) > 1 and not legend_custom
    if do_legend:
        leg_items = [] # (TObject, label, drawing option)
        if not legend_opts:
            if isinstance(opts, str):
                legend_opts = opts.replace('SAME', '').replace('HIST', 'L') or 'PE'
            else:
                legend_opts = [x.replace('SAME', '').replace('HIST', 'L') or 'PE' for x in opts]

    ### Create stack
    if stack:
        stack_hists = []
        stack_opts = []
        cache.append(stack_hists)
        stack_reorder_legend = False
        if do_legend and legend_order is None:
            stack_reorder_legend = True
            legend_order = []

    ### Process histograms
    for i in range(len(objs)):
        if 'linecolor' in kwargs:
            objs[i].SetLineColor(_arg(kwargs['linecolor'], i))
        if 'linestyle' in kwargs:
            objs[i].SetLineStyle(_arg(kwargs['linestyle'], i))
        if 'linewidth' in kwargs:
            objs[i].SetLineWidth(_arg(kwargs['linewidth'], i))

        if 'markerstyle' in kwargs:
            objs[i].SetMarkerStyle(_arg(kwargs['markerstyle'], i))
        if 'markercolor' in kwargs:
            objs[i].SetMarkerColor(_arg(kwargs['markercolor'], i))
        if 'markersize' in kwargs:
            objs[i].SetMarkerSize(_arg(kwargs['markersize'], i))

        if 'fillcolor' in kwargs:
            objs[i].SetFillColor(_arg(kwargs['fillcolor'], i))
        if 'fillstyle' in kwargs:
            objs[i].SetFillStyle(_arg(kwargs['fillstyle'], i))

        if 'xtitle' in kwargs:
            objs[i].GetXaxis().SetTitle(kwargs['xtitle'])
        if 'ytitle' in kwargs:
            objs[i].GetYaxis().SetTitle(kwargs['ytitle'])

        if 'xdivs' in kwargs:
            objs[i].GetXaxis().SetNdivisions(kwargs['xdivs'], True)
        if 'ydivs' in kwargs:
            objs[i].GetYaxis().SetNdivisions(kwargs['ydivs'], True)

        if do_legend:
            label = legend[i] if legend else objs[i].GetName()
            opt = _arg(legend_opts, i)
            leg_items.append((objs[i], label, opt))
            #if 'TH1' in objs[i].ClassName():
            #    for func in objs[i].GetListOfFunctions():
            #        leg_items.append((func, func.GetName(), 'l'))
        if stack and stack_reorder_legend:
            if 'TH1' in objs[i].ClassName():
                legend_order.insert(0, i)
            else:
                legend_order.append(i)

        opt = _arg(opts, i)
        if opt is None:
            continue
        elif 'TH1' in objs[i].ClassName():
            if stack:
                if len(stack_hists) > 0:
                    objs[i].Add(stack_hists[-1])
                stack_hists.append(objs[i])
                stack_opts.append(opt)
            else:
                if i > 0: 
                    if opt: opt = 'SAME ' + opt
                    else: opt = 'SAME' # very important that there's no extraneous space here
                objs[i].Draw(opt)
        elif 'TGraph' in objs[i].ClassName():
            if 'SAME' in opt:
                pass
            elif i > 0:
                opt = 'SAME ' + opt
            else:
                opt = opt + 'A'
            objs[i].Draw(opt)
        elif 'TF' in objs[i].ClassName():
            if i > 0:
                opt = 'SAME ' + opt
            objs[i].Draw(opt)
        else: # TH2
            if 'TEXT:' in opt:
                # Custom text format. It seems this is the only way to have differing formats per histograms
                # https://root-forum.cern.ch/t/draw-two-h2d-histograms-on-the-same-pad-as-text-but-in-different-formats/25234/2
                temp = opt.split(':')
                opt = temp[0]
                ex = ROOT.TExec('ex', 'gStyle->SetPaintTextFormat("{}");'.format(temp[1]))
                ex.Draw()
                cache.append(ex)
            if i > 0: opt = 'SAME ' + opt
            objs[i].Draw(opt)

    ### Draw stack ###
    if stack:
        if 'TH1' in objs[0].ClassName(): # plot this first since the first object drawn is used by ROOT for axis titles
            objs[0].Draw(opt)
        for h, opt in zip(reversed(stack_hists), reversed(stack_opts)):
            h.Draw('SAME ' + opt)

    ### Auto range
    xrange = None
    yrange = None
    if kwargs.get('xrange') is not None: # No autorange by default
        xrange = _auto_xrange(objs, **kwargs)
        if xrange is not None: 
            objs[0].GetXaxis().SetRangeUser(*xrange)
            kwargs['xrange'] = xrange
    if kwargs.get('yrange', True) is not None: # default value not used here, just needs to not be None to auto range by default
        kwargs.setdefault('start_at_zero', 'HIST' in _arg(opts, 0))
        yrange = _auto_yrange(objs, logy=logy, **kwargs)
        objs[0].GetYaxis().SetRangeUser(*yrange)

    ### TEXT AND LEGEND ###
    if subtitle is not None:
        if isinstance(subtitle, str):
            subtitle = [subtitle]
    if legend_custom:
        leg_items = legend_custom
        do_legend = leg_items
    elif do_legend:
        if legend_order: leg_items = [leg_items[i] for i in legend_order]
        leg_items = [x for x in leg_items if x[1] and x[2]]
        do_legend = leg_items and len(leg_items) > 0

    ### Text positioning ###
    x_left = kwargs.get('text_offset_left', 0.2)
    x_right = kwargs.get('text_offset_right', 1 - rightmargin - 0.05)
    y_top = kwargs.get('text_offset_top', 0.9)
    y_bottom = kwargs.get('text_offset_bottom', 0.2)

    if 'left' in textpos:
        _title_hori_pos = 'left'
        _legend_hori_pos = 'left'
    elif 'right' in textpos:
        _title_hori_pos = 'right'
        _legend_hori_pos = 'right'
    elif 'reverse' in textpos:
        _title_hori_pos = 'right'
        _legend_hori_pos = 'left'
    else:
        _title_hori_pos = 'left'
        _legend_hori_pos = 'right'
        
    if 'top' in textpos:
        _title_vert_pos = 'top'
        _legend_vert_pos = 'top'
    elif 'bottom' in textpos:
        _title_vert_pos = 'bottom'
        _legend_vert_pos = 'bottom'
    elif 'forward diagonal' in textpos:
        if 'reverse' in textpos:
            _title_vert_pos = 'top'
            _legend_vert_pos = 'bottom'
        else:
            _title_vert_pos = 'bottom'
            _legend_vert_pos = 'top'
    else:
        if 'reverse' in textpos:
            _title_vert_pos = 'bottom'
            _legend_vert_pos = 'top'
        else:
            _title_vert_pos = 'top'
            _legend_vert_pos = 'bottom'

    _legend_with_title = _title_hori_pos == _legend_hori_pos and _title_vert_pos == _legend_vert_pos

    ### Titles ###
    align_title = ROOT.kVAlignBottom
    title_atlas_width = 0.115*696*c.GetWh()/(472*c.GetWw())
    if _title_hori_pos == 'left':
        x_atlas = x_left
        x_title = x_left + title_atlas_width
        x_subtitle = x_left
        align_title += ROOT.kHAlignLeft
    else:  
        title_width = get_text_size(title, titlesize)[0] if title else 0
        x_atlas = x_right - title_width - title_atlas_width
        x_title = x_right
        x_subtitle = x_right
        align_title += ROOT.kHAlignRight

    ### Get initial y positions (remember text is bottom-aligned) ###
    _subtitle_size = titlesize * 0.7
    _title_spacing = titlesize * titlespacing * 0.1
    _subtitle_spacing = titlesize * titlespacing * 0.15

    title_height = get_text_size('ATLAS', titlesize)[1] if title is not None else 0
    subtitle_height = (_subtitle_size + _subtitle_spacing) * len(subtitle) if subtitle is not None else 0
    legend_height = (_subtitle_size + _subtitle_spacing) * math.ceil(len(leg_items) / legend_split) - _subtitle_spacing if do_legend else 0

    if _title_vert_pos == 'top':
        y_title = y_top - title_height
    else:
        y_title = y_bottom + subtitle_height
        if _legend_with_title:
            y_title += legend_height + _subtitle_spacing
        
    ### Place text ###
    if title is not None:
        if title:
            tex = ROOT.TLatex(x_title, y_title, title)
            tex.SetNDC()
            tex.SetTextFont(42)
            tex.SetTextSize(titlesize)
            tex.SetTextAlign(align_title)
            tex.Draw()
            cache.append(tex)
            title_width = tex.GetXsize()

        tex = ROOT.TLatex(x_atlas, y_title, 'ATLAS')
        tex.SetNDC()
        tex.SetTextFont(72)
        tex.SetTextSize(titlesize)
        tex.SetTextAlign(ROOT.kVAlignBottom)
        tex.Draw()
        cache.append(tex)

        y_title -= _title_spacing

    if subtitle is not None:
        for sub in subtitle:
            y_title -= _subtitle_size
            tex = ROOT.TLatex(x_subtitle, y_title, sub)
            tex.SetNDC()
            tex.SetTextFont(42)
            tex.SetTextSize(_subtitle_size)
            tex.SetTextAlign(align_title)
            tex.Draw()
            cache.append(tex)
            y_title -= _subtitle_spacing
        y_title -= _subtitle_spacing # extra pad before legend

    ### Legend ###
    if do_legend: 
        # These are in pad units, i.e. fraction of pad width
        leg_symbol_width = 0.05
        leg_symbol_pad = 0.01
        leg_label_width = _max_width(leg_items, _subtitle_size) * legend_split
        leg_width = leg_symbol_width + leg_symbol_pad + leg_label_width

        ### Get align and x_legend (left) and y_legend (top) positions
        align_legend = ROOT.kVAlignTop
        if _legend_hori_pos == 'left':
            x_legend = x_left
            align_legend += ROOT.kHAlignLeft
        else:  
            x_legend = x_right - leg_width
            align_legend += ROOT.kHAlignRight
        if _legend_vert_pos == 'top':
            if _legend_with_title:
                y_legend = y_title - legend_height
            else:
                y_legend = y_top - legend_height
        else:
            y_legend = y_bottom

        leg = ROOT.TLegend()
        leg.SetFillColor(colors.transparent_white)
        leg.SetLineColor(0)
        leg.SetBorderSize(0)
        leg.SetMargin(leg_symbol_width / leg_width) # SetMargin expects the fractional width relative to the legend...cause that's intuitive
        leg.SetTextSize(_subtitle_size)
        leg.SetTextFont(42) # Default ATLAS font
        leg.SetTextAlign(kwargs.get('legend_align', align_legend))
        leg.SetNColumns(legend_split)

        leg.SetX1(x_legend)
        leg.SetX2(x_legend + leg_width)
        leg.SetY1(y_legend)
        leg.SetY2(y_legend + legend_height)
        for i in leg_items:
            leg.AddEntry(*i)
        leg.Draw()
        cache.append(leg)

    if canvas_callback: cache.append(canvas_callback(c))

    return cache


def _outliers(hists, yrange=None):
    markers = []
    ydiff = (yrange[1] - yrange[0]) / 20.
    for h in hists:
        for i in range(1, h.GetNbinsX()+1): # TH1 bins are 1-indexed
            v = h.GetBinContent(i)
            #e = h.GetBinError(i)
            if v == 0:
                continue
            elif v >= yrange[1]:
                m = ROOT.TMarker(h.GetXaxis().GetBinCenter(i), yrange[1] - ydiff, ROOT.kFullTriangleUp)
                m.SetMarkerColor(ROOT.kBlue)
                m.Draw()
                markers.append(m)
            elif v < yrange[0]:
                m = ROOT.TMarker(h.GetXaxis().GetBinCenter(i), yrange[0] + ydiff, ROOT.kFullTriangleDown)
                m.SetMarkerColor(ROOT.kBlue)
                m.Draw()
                markers.append(m)

    return markers

##############################################################################
###                            CANVAS WRAPPERS                             ###
##############################################################################


def plot(objs, canvas_size=(1000,800), **kwargs):
    c = ROOT.TCanvas('c1', 'c1', *canvas_size)
    cache = _plot(c, objs, **kwargs)
    c.RedrawAxis() # Make the tick marks go above any fill
    save_canvas(c, kwargs.get('filename', objs[0].GetName()))


def _copy_ratio_args(args, postfix):
    '''
    Copies arguments for ratio plots. Arguments like 'ytitle2' are copied to 'ytitle',
    and common arguments like x-axis options are copied as-is.
    '''
    out = {}
    for k,v in args.items():
        if k[-1] == postfix: out[k[:-1]] = v
        elif k[0] == 'x': out[k] = v
        elif k == 'rightmargin': out[k] = v
    return out


def plot_ratio(hists1, hists2, height1=0.7, outlier_arrows=False, hline=None, save_plot=True, **kwargs):
    '''
    Plots [hists1] in a main pad on top and [hists2] in a secondary pad below. The two 
    sets of objects should share the same x axis. Set options in the secondary pad by 
    postpending the kwargs with a '2'.

    @param hline
        Draws a horizontal line in the secondary pad. The value sets the y position in
        user coordinates. Set to None to omit.
    '''
    c = ROOT.TCanvas("c1", "c1", 1000, 800)
    c.SetFillColor(colors.transparent_white)

    ### Create pads
    height2 = 1 - height1
    height_ratio = height2 / height1

    pad1 = ROOT.TPad("pad1", "pad1", 0, height2, 1, 1)
    pad1.SetFillColor(colors.transparent_white)
    pad1.SetBottomMargin(0.03)
    pad1.Draw()

    c.cd()
    pad2 = ROOT.TPad("pad2", "pad2", 0, 0, 1, height2)
    pad2.SetFillColor(colors.transparent_white)
    pad2.SetBottomMargin(0.12 / height2)
    pad2.Draw()

    ### Draw main histo, get error histos
    kwargs['titlesize'] = kwargs.get('titlesize', 0.05) / height1
    kwargs.setdefault('text_offset_bottom', 0.07) 
    cache = _plot(pad1, hists1, **kwargs)
    pad1.RedrawAxis() # Make the tick marks go above any fill

    ### Draw ratio plot
    args2 = { 'ydivs': 504, 'ignore_outliers_y': 2, 'title': None, 'legend': None }
    args2.update(_copy_ratio_args(kwargs, '2'))
    cache.append(_plot(pad2, hists2, do_legend=False, **args2))
    pad2.RedrawAxis() # Make the tick marks go above any fill

    ### Draw y=1 line
    if hline is not None:
        if xrange := kwargs.get('xrange'):
            l = ROOT.TLine(xrange[0], hline, xrange[1], hline)
        else:
            l = ROOT.TLine(hists2[0].GetXaxis().GetXmin(), hline, hists2[0].GetXaxis().GetXmax(), hline)
        l.SetLineStyle(ROOT.kDashed)
        l.Draw()
        cache.append(l)

    ### Remove x-axis labels from top plot
    hists1[0].GetXaxis().SetLabelOffset(999)
    hists1[0].GetXaxis().SetLabelSize(0)
    hists1[0].GetXaxis().SetTitleSize(0)

    ### Fix text / tick sizes (ROOT shrinks text sizes based on pad size). These should be hard coded in case
    ### the histogram is reused.
    old_size = 0.05    # hists1[0].GetYaxis().GetTitleSize()
    old_offset_x = 1.4 # hists1[0].GetXaxis().GetTitleOffset()
    old_offset_y = 1.4 # hists1[0].GetYaxis().GetTitleOffset()

    hists1[0].GetYaxis().SetLabelSize(old_size / height1)
    hists1[0].GetYaxis().SetTitleSize(old_size / height1)
    hists1[0].GetYaxis().SetTitleOffset(old_offset_y * height1)

    hists2[0].GetXaxis().SetLabelSize(old_size / height2)
    hists2[0].GetXaxis().SetTitleSize(old_size / height2)
    hists2[0].GetXaxis().SetTitleOffset(1)
    hists2[0].GetXaxis().SetTickLength(0.03 / height_ratio) # default is 0.03; this makes it equal to pad 1

    hists2[0].GetYaxis().SetLabelSize(old_size / height2)
    hists2[0].GetYaxis().SetTitleSize(old_size / height2)
    hists2[0].GetYaxis().SetTitleOffset(old_offset_y * height2)
    #hists2[0].GetYaxis().SetTickLength(0.03 * (0.97 * height1) / (height2 - 0.12)) # adjust for the bottom margins too ?

    ### Draw out-of-bounds arrows
    if outlier_arrows:
        yrange = kwargs['yrange2']
        ydiff = (yrange[1] - yrange[0]) / 20.
        for i in range(1, hists2[0].GetNbinsX()+1): # TH1 bins are 1-indexed
            v = hists2[0].GetBinContent(i)
            e = hists2[0].GetBinError(i)
            if v == 0:
                continue
            elif v >= yrange[1]:
                m = ROOT.TMarker(hists2[0].GetXaxis().GetBinCenter(i), yrange[1] - ydiff, ROOT.kFullTriangleUp)
                m.SetMarkerColor(ROOT.kBlue)
                m.Draw()
                cache.append(m)
            elif v < yrange[0]:
                m = ROOT.TMarker(hists2[0].GetXaxis().GetBinCenter(i), yrange[0] + ydiff, ROOT.kFullTriangleDown)
                m.SetMarkerColor(ROOT.kBlue)
                m.Draw()
                cache.append(m)

    if save_plot:
        save_canvas(c, kwargs.get('filename', hists1[0].GetName()))
    
    return c, cache


def plot_ratio3(hists1, hists2, hists3, height1=0.55, outlier_arrows=False, hline2=None, hline3=None, **kwargs):
    '''
    A ratio plot with two ancillary pads. Plots [hists1] in a main pad on top and 
    [hists2] and [hists3] in the middle and bottom ancillary pads respectively. The 
    objects should all share the same x axis. Set options in the middle and bottom pad by
    post-pending the kwargs with a '2' or '3' respectively.

    @param hline2/3
        Draws a horizontal line in the middle/bottom pad. The value sets the y position 
        in user coordinates. Set to None to omit. 
    '''
    c = ROOT.TCanvas("c1", "c1", 1000, 800)
    c.SetFillColor(colors.transparent_white)

    ### Create pads
    height2 = (1 - height1) / 2 - 0.06
    height3 = height2 + 0.12
    tick_length_y = 0.03

    pad1 = ROOT.TPad("pad1", "pad1", 0, height2 + height3, 1, 1)
    pad1.SetFillColor(colors.transparent_white)
    pad1.SetBottomMargin(0)
    pad1.Draw()

    c.cd()
    pad2 = ROOT.TPad("pad2", "pad2", 0, height3, 1, height2 + height3)
    pad2.SetFillColor(colors.transparent_white)
    pad2.SetTopMargin(0)
    pad2.SetBottomMargin(0)
    pad2.Draw()

    c.cd()
    pad3 = ROOT.TPad("pad3", "pad3", 0, 0, 1, height3)
    pad3.SetFillColor(colors.transparent_white)
    pad3.SetTopMargin(0)
    pad3.SetBottomMargin(0.12 / height3)
    pad3.Draw()

    ### Draw main histo
    kwargs['titlesize'] = kwargs.get('titlesize', 0.05) / height1
    kwargs['yrange'] = list(kwargs.get('yrange', [None, None]))
    kwargs.setdefault('text_offset_bottom', 0.1 * (1 - height1)) # guess
    cache1 = _plot(pad1, hists1, **kwargs)
    hists1[0].Draw('sameaxis') # Make the tick marks go above any fill

    ### Draw first ratio plot
    args2 = { 'ydivs': 503, 'ignore_outliers_y': 3, 'title': None }
    args2.update(_copy_ratio_args(kwargs, '2'))
    cache2 = _plot(pad2, hists2, do_legend=False, **args2)
    hists2[0].Draw('sameaxis') # Make the tick marks go above any fill

    ### Draw y=1 line
    if hline2 is not None:
        if xrange := kwargs.get('xrange'):
            l2 = ROOT.TLine(xrange[0], hline2, xrange[1], hline2) # make sure xrange is a list if it has None elements
        else:
            l2 = ROOT.TLine(hists2[0].GetXaxis().GetXmin(), hline2, hists2[0].GetXaxis().GetXmax(), hline2)
        l2.SetLineStyle(ROOT.kDashed)
        l2.Draw()

    ### Draw second ratio plot
    args3 = { 'ydivs': 503, 'ignore_outliers_y': 3, 'title': None }
    args3.update(_copy_ratio_args(kwargs, '3'))
    cache3 = _plot(pad3, hists3, do_legend=False, **args3)
    hists3[0].Draw('sameaxis') # Make the tick marks go above any fill

    ### Draw y=1 line
    if hline3 is not None:
        if xrange := kwargs.get('xrange'):
            l3 = ROOT.TLine(xrange[0], hline3, xrange[1], hline3)
        else:
            l3 = ROOT.TLine(hists2[0].GetXaxis().GetXmin(), hline3, hists2[0].GetXaxis().GetXmax(), hline3)
        l3.SetLineStyle(ROOT.kDashed)
        l3.Draw()

    ### Remove x-axis labels from top plots
    hists1[0].GetXaxis().SetLabelOffset(999)
    hists1[0].GetXaxis().SetLabelSize(0)
    hists1[0].GetXaxis().SetTitleSize(0)

    hists2[0].GetXaxis().SetLabelOffset(999)
    hists2[0].GetXaxis().SetLabelSize(0)
    hists2[0].GetXaxis().SetTitleSize(0)

    ### Remove y labels that might get cut off
    if kwargs['yrange'][0] == 0:
        hists1[0].GetYaxis().ChangeLabel(1, -1, 0) # remove the bottom tick label, since it usually gets cut off

    ### Fix text / tick sizes (ROOT shrinks text sizes based on pad size),
    old_size = hists1[0].GetYaxis().GetTitleSize()
    old_offset_x = hists1[0].GetXaxis().GetTitleOffset()
    old_offset_y = hists1[0].GetYaxis().GetTitleOffset()

    hists1[0].GetYaxis().SetLabelSize(old_size / height1)
    hists1[0].GetYaxis().SetTitleSize(old_size / height1)
    hists1[0].GetYaxis().SetTitleOffset(old_offset_y * height1)
    hists1[0].GetYaxis().SetTickLength(tick_length_y / (1 - pad1.GetTopMargin()))
    # See https://root-forum.cern.ch/t/inconsistent-tick-length/18563/9
    # The tick scale is affected by the margins: tick_length = pixel_size / ((pad2H - marginB - marginT) / pad2H * pad2W)
    # Note there seems to be a minimum tick length

    hists2[0].GetXaxis().SetLabelSize(old_size / height2)
    hists2[0].GetXaxis().SetTitleSize(old_size / height2)
    hists2[0].GetXaxis().SetTitleOffset(1)
    hists2[0].GetXaxis().SetTickLength(0.03 * height1 / height2) # default is 0.03; this makes it equal to pad 1

    hists2[0].GetYaxis().SetLabelSize(old_size / height2)
    hists2[0].GetYaxis().SetTitleSize(old_size / height2)
    hists2[0].GetYaxis().SetTitleOffset(old_offset_y * height2)
    hists2[0].GetYaxis().SetTickLength(tick_length_y)

    hists3[0].GetXaxis().SetLabelSize(old_size / height3)
    hists3[0].GetXaxis().SetTitleSize(old_size / height3)
    hists3[0].GetXaxis().SetTitleOffset(1)
    hists3[0].GetXaxis().SetTickLength(0.03 * height1 / height3) # default is 0.03; this makes it equal to pad 1

    hists3[0].GetYaxis().SetLabelSize(old_size / height3)
    hists3[0].GetYaxis().SetTitleSize(old_size / height3)
    hists3[0].GetYaxis().SetTitleOffset(old_offset_y * height3)
    hists3[0].GetYaxis().SetTickLength(tick_length_y / (1 - pad3.GetBottomMargin()))

    ### Draw out-of-bounds arrows
    if outlier_arrows:
        markers = []
        yrange = kwargs['yrange2']
        ydiff = (yrange[1] - yrange[0]) / 20.
        for i in range(1, hists2[0].GetNbinsX()+1): # TH1 bins are 1-indexed
            v = hists2[0].GetBinContent(i)
            e = hists2[0].GetBinError(i)
            if v == 0:
                continue
            elif v >= yrange[1]:
                m = ROOT.TMarker(hists2[0].GetXaxis().GetBinCenter(i), yrange[1] - ydiff, ROOT.kFullTriangleUp)
                m.SetMarkerColor(ROOT.kBlue)
                m.Draw()
                markers.append(m)
            elif v < yrange[0]:
                m = ROOT.TMarker(hists2[0].GetXaxis().GetBinCenter(i), yrange[0] + ydiff, ROOT.kFullTriangleDown)
                m.SetMarkerColor(ROOT.kBlue)
                m.Draw()
                markers.append(m)

    save_canvas(c, kwargs.get('filename', hists1[0].GetName()))


def plot_two_scale(hists1, hists2, **kwargs):
    '''
    Plots a graph with two y-axes sharing the same x-axis

    TODO auto legend
    '''

    ### Style
    ROOT.gStyle.SetPadTickY(0) # remove right tick marks
    kwargs.setdefault('rightmargin', 0.12)
    kwargs.setdefault('rightmargin2', kwargs.get('rightmargin', 0.12))
    if v := kwargs.get('ydatapad_top'): kwargs.setdefault('ydatapad_top2', v)
    kwargs.setdefault('xdivs', 506)

    ### Plot the left histograms
    c = ROOT.TCanvas('c1', 'c1', 1000, 800)
    c.SetFillColor(colors.transparent_white)
    cache = _plot(c, hists1, **kwargs)
    c.Update() # So that GetUymin works below

    ### Get args2
    args2 = { k[:-1]:v for k,v in kwargs.items() if k[-1] == '2' }

    ### Fix opts to plot 'SAME'
    opts2 = args2.pop('opts', '')
    if isinstance(opts2, str):
        opts2 = [opts2] * len(hists2)
    opts2[0] = 'SAME ' + opts2[0]

    ### Scale histograms to new yrange
    yrange2 = _auto_yrange(hists2, **args2)
    args2.pop('yrange', None)
    scale = (c.GetUymax() - c.GetUymin()) / (yrange2[1] - yrange2[0])
    for h in hists2:
        if 'TH' in h.ClassName():
            h.Scale(scale)
        elif 'TGraph' in h.ClassName():
            for i in range(h.GetN()):
                h.SetPointY(i, c.GetUymin() + (h.GetPointY(i) - yrange2[0]) * scale)

    ### Plot the right histograms
    cache2 = _plot(c, hists2, opts=opts2, yrange=yrange2, do_legend=False, **args2)

    ### Draw the second axis
    axis = ROOT.TGaxis(c.GetUxmax(), c.GetUymin(), c.GetUxmax(), c.GetUymax(), yrange2[0], yrange2[1], 510, '+L')
    axis.SetLabelFont(hists1[0].GetXaxis().GetLabelFont()) # 42
    axis.SetLabelSize(hists1[0].GetXaxis().GetLabelSize()) # 0.5
    axis.SetLabelColor(colors.red)
    axis.SetTitle(kwargs.get('ytitle2'))
    axis.SetTitleFont(hists1[0].GetXaxis().GetLabelFont()) # 42
    axis.SetTitleSize(hists1[0].GetXaxis().GetLabelSize()) # 0.5
    axis.SetTitleColor(colors.red)
    axis.SetLineColor(colors.red)
    axis.Draw()

    save_canvas(c, kwargs.get('filename', hists1[0].GetName()))


def plot_tiered(hists, y_labels = None, ydatapad_top = 0.1, **kwargs):
    '''
    Similar to a violin plot, this plots each hist in its own equi-height y-bin.
    Negative values are supressed.

    @param hists
        Each hist will get its own y-bin, in increasing (bottom to top) order.
    @param y_labels
        The label of each y-bin, in matching order as `hists`.
    '''
    c = ROOT.TCanvas('c1', 'c1', 1000, 800)

    ### Create the frame ###
    axis = hists[0].GetXaxis()
    if axis.IsVariableBinSize():
        h = ROOT.TH2F('tiers', '', hists[0].GetNbinsX(), axis.GetXbins().GetArray(), len(hists), 0, len(hists))
    else:
        h = ROOT.TH2F('tiers', '', hists[0].GetNbinsX(), axis.GetXmin(), axis.GetXmax(), len(hists), 0, len(hists))
    h.Draw('AXIS')

    ### Set bin labels ###
    if y_labels is not None:
        c.SetLeftMargin(kwargs.get('leftmargin', 0.2))
        h.GetYaxis().SetTitleOffset(kwargs.get('ytitle_offset', 2))
        for y,label in enumerate(y_labels):
            h.GetYaxis().SetBinLabel(y + 1, label)

    ### Pop some opts before the call to _plot ###
    fillcolor = kwargs.pop('fillcolor', None)

    ### Draw boxes ###
    cache = []
    for y in range(len(hists)):
        # Normalize the histogram to the maximum value. In user coordinates, defined
        # by the frame histogram above, the max height of each y bin is just 1.
        if m := hists[y].GetMaximum():
            hists[y].Scale((1 - ydatapad_top) / m)

        for x in range(1, h.GetNbinsX() + 1):
            height = hists[y].GetBinContent(x)
            if height <= 0: continue

            bin_x = h.GetXaxis().GetBinLowEdge(x)
            bin_width = h.GetXaxis().GetBinWidth(x)

            box = ROOT.TBox(bin_x, y, bin_x + bin_width, y + height)
            if fillcolor:
                if callable(fillcolor):
                    color = fillcolor(hists[y], x, y)
                else:
                    color = _arg(_arg(fillcolor, y), x)
                box.SetFillColor(color)
                box.SetLineColor(color)
            else:
                box.SetFillColor(hists[y].GetFillColor())
                box.SetLineColor(hists[y].GetLineColor())
            box.Draw()
            cache.append(box)

    ### Draw labels and text ###
    cache.append(_plot(c, [h], opts='AXIS SAMES', yrange=None, **kwargs)) # Make the tick marks / titles go above the boxes

    save_canvas(c, kwargs.get('filename', hists[0].GetName()))


##############################################################################
###                                COLORS                                  ###
##############################################################################

class colors():
    '''
    Utility wrappers for predefined colors and colormaps. This is a namespace class.
    There's no need to instantiate it. Colors can be accessed directly, for example 
    `plot.colors.red`. Refer to the code for all defines.
    
    Most colormaps can be accessed via three ways:
        1) A function like `pastel(n)`, which returns the [n]th color in the map,
           and will cycle through the map when [n] > length.
        2) The full list of colors in the colormap, for example `pastel_l`.
        3) The individual colors, for example `plot.colors.pastel_red`.
    '''
    
    ### Matplotlib Colormaps ###
    ''' 
    Retrieve colormaps from matplotlib with this:
        import matplotlib.cm
        cmap = matplotlib.cm.get_cmap('Pastel1')
        for i in range(cmap.N):
            print(cmap(i)[:-1])
    '''

    _pastel = [ # Matplotlib Pastel1 colormap (len: 9)
            ROOT.TColor(0.984313725490196, 0.7058823529411765, 0.6823529411764706),  # red
            ROOT.TColor(0.7019607843137254, 0.803921568627451, 0.8901960784313725),  # blue
            ROOT.TColor(0.8, 0.9215686274509803, 0.7725490196078432),                # green
            ROOT.TColor(0.8705882352941177, 0.796078431372549, 0.8941176470588236),  # purple
            ROOT.TColor(0.996078431372549, 0.8509803921568627, 0.6509803921568628),  # orange
            ROOT.TColor(1.0, 1.0, 0.8),                                              # yellow
            ROOT.TColor(0.8980392156862745, 0.8470588235294118, 0.7411764705882353), # brown
            ROOT.TColor(0.9921568627450981, 0.8549019607843137, 0.9254901960784314), # pink
            ROOT.TColor(0.9490196078431372, 0.9490196078431372, 0.9490196078431372), # gray
    ]

    _tableu = [ # Matplotlib tableau colormap (len: 10)
            ROOT.TColor( 31/255., 119/255., 180/255.), # blue
            ROOT.TColor(255/255., 127/255.,  14/255.), # orange
            ROOT.TColor( 44/255., 160/255.,  14/255.), # green
            ROOT.TColor(214/255.,  39/255.,  40/255.), # red
            ROOT.TColor(148/255., 103/255., 189/255.), # purple
            ROOT.TColor(140/255.,  86/255.,  75/255.), # brown
            ROOT.TColor(227/255., 119/255., 194/255.), # pink
            ROOT.TColor(127/255., 127/255., 127/255.), # gray
            ROOT.TColor(188/255., 189/255.,  34/255.), # olive
            ROOT.TColor( 23/255., 190/255., 207/255.), # cyan
    ]
    _pastel_base = _pastel[0].GetNumber()
    _tableu_base = _tableu[0].GetNumber()

    def pastel(i):
        return colors._pastel_base + i % len(colors._pastel)
    def tableu(i):
        return colors._tableu_base + i % len(colors._tableu)

    # list comprehensions are iffy inside a class scope
    # https://stackoverflow.com/questions/13905741/accessing-class-variables-from-a-list-comprehension-in-the-class-definition
    pastel_l = (lambda x=_pastel_base, y=_pastel: [x + i for i in range(len(y))])()
    tableu_l = (lambda x=_tableu_base, y=_tableu: [x + i for i in range(len(y))])()

    blue   = _tableu_base
    orange = _tableu_base + 1
    green  = _tableu_base + 2
    red    = _tableu_base + 3
    purple = _tableu_base + 4
    brown  = _tableu_base + 5
    pink   = _tableu_base + 6
    gray   = _tableu_base + 7
    olive  = _tableu_base + 8
    cyan   = _tableu_base + 9

    pastel_red    = _pastel_base
    pastel_blue   = _pastel_base + 1
    pastel_green  = _pastel_base + 2
    pastel_purple = _pastel_base + 3
    pastel_orange = _pastel_base + 4
    pastel_yellow = _pastel_base + 5
    pastel_brown  = _pastel_base + 6
    pastel_pink   = _pastel_base + 7
    pastel_gray   = _pastel_base + 8

    ### Custom colors ###
    _penn_green  = ROOT.TColor(  0/255, 164/255,  84/255)
    _penn_purple = ROOT.TColor(146/255,   0/255, 166/255)
    _transparent_black = ROOT.TColor(0, 0, 0, 0)
    _transparent_white = ROOT.TColor(1, 1, 1, 0)

    penn_green  = _penn_green.GetNumber()
    penn_purple = _penn_purple.GetNumber()
    transparent_black = _transparent_black.GetNumber()
    transparent_white = _transparent_white.GetNumber()


def colors_from_palette(palette, n = None, trim_fraction = 0.1):
    '''
    Returns a set of [n] equally spaced colors (ROOT ordinal number) from a pre-defined 
    palette.

    If [n] is `None`, instead returns the first color of the palette.

    @param trim_fraction
        We sometimes want to trim the edges of the colormap since they're too white or
        black. A fraction of 0.1 means to ignore the first and last tenth of the palette.
    '''
    ROOT.gStyle.SetPalette(palette)
    colors = ROOT.TColor.GetPalette()
    if n is None:
        return colors[0]
    else:
        trim_size = int(len(colors) * trim_fraction)
        total_range = len(colors) - 2 * trim_size
        return [colors[(total_range - 1) * x // (n - 1) + trim_size] for x in range(n)]


def color_from_palette(palette, i, n, trim_fraction = 0.1):
    return colors_from_palette(palette, n = n, trim_fraction = trim_fraction)[i]


def rgba(val):
    '''
    Input val as int32 in ARGB form, returns (r, g, b, a)
    '''
    a = (val & 0xff000000) >> 24
    r = (val & 0x00ff0000) >> 16
    g = (val & 0x0000ff00) >> 8
    b = val & 0x000000ff
    return (r, g, b, a)


def create_gradient(colors):
    '''
    colors should be a list (np array) of stops with entries
                        (pos, r, g, b)
    which range from 0 to 1. This function sets the palette automatically.

    Returns the index of the first color.
    '''
    pos = np.copy(colors[:, 0]) # copy seems necessary to work with ROOT
    r = np.copy(colors[:, 1])
    g = np.copy(colors[:, 2])
    b = np.copy(colors[:, 3])
    i = ROOT.TColor.CreateGradientColorTable(len(pos), pos, r, g, b, 101)
    return i


def plot_colors():
    '''
    Plots a grid of the colors in each colormap
    '''
    # Colors to plot
    cols = [
        colors.tableu_l,
        colors.pastel_l,
        [colors.penn_green, colors.penn_purple],
    ]

    # Auto y-size
    c = ROOT.TCanvas('c1', 'c1', 800, 200)
    nx = max(len(x) for x in cols)
    ny = len(cols)
    aspect = nx / ny
    c.SetWindowSize(c.GetWw(), int(round(c.GetWw() / aspect)))

    # Box sizes in canvas coordinates
    boxes = []
    for y,cols_x in enumerate(reversed(cols)):
        for x,col in enumerate(cols_x):
            b = ROOT.TBox(x/nx, y/ny, (x+1)/nx, (y+1)/ny)
            b.SetFillColor(col)
            b.Draw()
            boxes.append(b)

    c.Print('colormaps' + file_format)


##############################################################################
###                         TRANSPARENT BACKGROUNDS                        ###
##############################################################################


def save_canvas(c, filename):
    file_types = file_formats

    ### Check if filename has a fixed filetype ###
    type_list = ['cxx', 'jpg', 'png', 'ps', 'pdf']
    for t in type_list:
        if filename.endswith(f'.{t}'):
            file_type = [t]
            filename = filename[:-len(t)-1]
            break
    
    ### Save for each filetype ###
    for t in file_types:
        if save_transparent and t == 'png':
            save_canvas_transparent(c, filename)
        else:
            c.Print(filename + '.' + t)


def save_canvas_transparent(c, filename):
    '''
    c.Draw() loses any transparent background. This seems to be because TImage initial-
    izes with full opacity black, and the canvas background gets blended into that. 
    However, instead of c.Draw() we use directly TImageDump, which is the backend used by 
    c.Draw(). Do note however that ROOT will incorrectly blend transparent objects onto 
    the background as if it had no transparency, but it keeps the alpha channel correct.

    Normally we could save the image with dump.Close(), but this looses the alpha channel 
    again. So we have to use Pillow. However Pillow expects RGBA format, which is really 
    ABGR due to endianness.

    There are also big problems with text anti-aliasing. It seems like ROOT tries to 
    blend the anti-aliasing, but then sets the alpha to 0. Another problem is that text 
    will blend entire letters instead of applying per-pixel checks, which causes problems 
    i.e. if text overlaps a thin line.

    So if we start with a transparent background that is fully white, values with 
    RGB = x < 255 and alpha = 0 is exactly where text is antialiased. ROOT seems to mess 
    something up though, every 'pad' subtracts 1 from the value, so i.e. the canvas 
    background has value 254 and the axis background has value 253. Now if the text is 
    fully black and not overlapping anything, we can set RGB = 0 and alpha = 255 - x. If
    the text is overlapping something, we can guess the alpha of the anti-aliasing by 
    using x = max(r, g, b), but we can't tell if the pixel is overlapping something or 
    not. So the anti-aliasing will block everything behind it.
    '''
    ### Save transparent png ###
    from PIL import Image
    import os

    w = c.GetWw()
    h = c.GetWh()
    n = w * h

    ### Initialize the image dump with transparent background ###
    dump = ROOT.TImageDump('fake', 114) # 114 = preview (don't save)
    img = dump.GetImage()
    img.SetImage(np.zeros(n), w, h)
    arr = img.GetArgbArray()
    for i in range(n):
        arr[i] = 0x00FFFFFF

    ### Paint the canvas ###
    c.SetFillColor(colors.transparent_white)
    c.Paint()

    ### Correct text aliasing, byte order, and pre-multiplied alpha ###
    for x in range(n):
        r, g, b, a = rgba(arr[x])
        if a == 0 and (r < 250 or g < 250 or b < 250): # an aliased text pixel. 250 here since the background is sometimes like ~253
            if (r != g or r != b or g != b): # overlapping something
                a = 255 # just keep the white-blended version
            else:
                a = 255 - max(r, g, b)
                r = 0
                g = 0
                b = 0
        elif a != 0 and a != 255: # this is an alpha channel that is blended onto the (opaqued) white background. The 4+ is an empircal correction...
            r = min(4 + int((255 * r + 253 * (a - 255)) / a), 255)
            g = min(4 + int((255 * g + 253 * (a - 255)) / a), 255)
            b = min(4 + int((255 * b + 253 * (a - 255)) / a), 255)
        arr[x] = (a << 24) + (b << 16) + (g << 8) + r

    ### Save ###
    image = Image.frombuffer('RGBA', (w, h), arr, 'raw', 'RGBA', 0, 1)
    image.save(filename + '.png')
    print('Wrote ' + filename + '.png')


##############################################################################
###                               FORMATTING                               ###
##############################################################################

_format_default_opts = {
        0: 'linecolor',
        1: 'linestyle',
        'linecolor': colors.tableu,
        'fillcolor': colors.pastel,
}

def _apply_style(h, user_opts, dim, index, size, apply_color_to_fill = False):
    '''
    Applies a style to a single histogram. The style is retrieved by (dim, index),
    and specified by opts. 

    @param user_opts
        A style dictionary. Keys should either be a dimension-style pair, which specifies
        what style to use for each dimension, or a style-specifier pair, to modify the 
        default style. 
    @param dim
        The dimension/series index. Each dimension should use an orthogonal style.
    @param index
        Index in the current dimension. I.e. maps to the specific color if the dimension
        style is color.
    @param size
        Max size of the dimension.
    '''
    opts = _format_default_opts.copy()
    if user_opts:
        opts.update(user_opts)
    
    style = opts.get(dim)
    if not style: return
    if ':' in style: index += int(style.split(':')[-1])

    if 'linecolor' in style or 'markercolor' in style:
        color_accessor = opts.get('linecolor', _format_default_opts['linecolor'])
        if callable(color_accessor):
            color = color_accessor(index)
        else:
            color = color_from_palette(color_accessor, index, size)
        h.SetLineColor(color)
        h.SetMarkerColor(color)
        if (apply_color_to_fill): h.SetFillColor(color)
    elif 'linestyle' in style:
        h.SetLineStyle(1 + index) # linestyles start at 1
    elif 'markerstyle' in style:
        h.SetMarkerStyle(ROOT.kFullCircle + index) # start at kFullCircle for easy iteration
    elif 'fillcolor' in style:
        color_accessor = opts.get('fillcolor', _format_default_opts['fillcolor'])
        if callable(color_accessor):
            color = color_accessor(index)
        else:
            color = color_from_palette(color_accessor, index, size)
        h.SetFillColor(color)
    elif 'linewidth' in style:
        h.SetLineWidth(opts['linewidth'][index])
    else:
        raise NameError("Unknown style: {}".format(style))


def format(hists, shape=None, opts=None):
    '''
    If a list of hists is multidimensional in how they differ, it's better to
    style each dimension separately (i.e. color for one dimension and line
    style for the other).

    [shape] should be a list of the sizes of each dimension, with the first entry
    being the slowest-varying.

    [opts] is a dictionary of `dim : style`, to set the style of dimension `dim`. `dim`
    should index into [shape], with `dim == 0` being the slowest varying. `style` is a
    Root style like 'linecolor'. It can also be postpended with an offset, such as ':4'
    to indicate an offset of 4 in the style.
    '''
    if shape is None:
        shape = (len(hists),)
    elif np.prod(shape) != len(hists):
        print(f"WARNING! plot.format() shape {shape} doesn't match hists of length {len(hists)}")
        return

    for i_flat,i_fold in enumerate(itertools.product(*[range(n) for n in shape])):
        # i_flat is the flattened index into [hists]
        # i_fold is the multidimensional index into [hists], len == nDims
        for dim,index in enumerate(i_fold):
            # dim is the dimension we're currently setting
            # index is the index/style value in this dimension
            _apply_style(hists[i_flat], opts, dim, index, shape[dim])


def reduced_legend_hists(shape, opts=None):
    '''
    @returns A list of histograms that can be used for a custom reduced legend,
    containing sum(shape) entries instead of prod(shape) entries.
    '''
    out = []
    for dim,size in enumerate(shape):
        for i in range(size):
            h = ROOT.TH1F(f'_plot_legend_{dim}_{i}', '', 1, 0, 1)
            _apply_style(h, opts, dim, i, size, apply_color_to_fill=True)
            out.append(h)
    return out


##############################################################################
###                                  MAIN                                  ###
##############################################################################


if __name__ == '__main__':
    # Arg parse
    import sys
    if len(sys.argv) > 1:
        file_formats = sys.argv[1:]

    # Run
    plot_colors()


