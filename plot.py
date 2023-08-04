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
normalize
    Normalizes a histogram in multiple ways.
rebin2d
    Rebins a 2D histogram with variable bins on each axis.
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


def _auto_xrange(objs, xrange=(None,None), xdatapad=None, xdatapad_left=0, xdatapad_right=0, **kwargs):
    def min_max(obj):
        o_min = None
        o_max = None
        if 'TH1' in obj.ClassName() or 'TProfile' in obj.ClassName():
            for x in range(1, obj.GetNbinsX() + 1):
                if obj.GetBinContent(x) != 0 or obj.GetBinError(x) != 0:
                    if o_min is None: o_min = obj.GetBinLowEdge(x)
                    o_max = obj.GetBinLowEdge(x + 1)
            return o_min, o_max
        elif 'TGraph' in obj.ClassName():
            for i in range(obj.GetN()):
                x = obj.GetPointX(i)
                if o_min is None or x < o_min: o_min = x
                if o_max is None or x > o_max: o_max = x
            return o_min, o_max
        else: 
            raise RuntimeError('_get_minmax() unknown class ' + obj.ClassName())
    
    if xrange is None:
        return None
    elif xrange[0] is None or xrange[1] is None:
        x_min = None
        x_max = None
        for obj in objs:
            o_min, o_max = min_max(obj)
            if o_min is None or o_max is None: continue
            x_min = o_min if x_min is None else min(x_min, o_min)
            x_max = o_max if x_max is None else max(x_max, o_max)

        diff = x_max - x_min
        if xdatapad is not None:
            xdatapad_left = xdatapad
            xdatapad_right = xdatapad
        x_min -= xdatapad_left * diff
        x_max += xdatapad_right * diff
        newrange = (x_min if xrange[0] is None else xrange[0], x_max if xrange[1] is None else xrange[1])
        if isinstance(xrange, list):
            xrange[0] = newrange[0]
            xrange[1] = newrange[1]
    else:
        newrange = xrange

    if newrange[0] is None or newrange[1] is None:
        return None
    return newrange


def _get_minmax(obj, xrange=None, ignore_outliers_y=0, **kwargs):
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
                if not xrange[0] is None and x < xrange[0]: continue
                if not xrange[1] is None and x > xrange[1]: continue
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
            if not xrange[0] is None and x < xrange[0]: continue
            if not xrange[1] is None and x > xrange[1]: continue
        if ignore_outliers_y:
            if e != 0 and abs(y - mean) > ignore_outliers_y * std: continue

        o_min = y if o_min is None else min(o_min, y)
        o_max = y if o_max is None else max(o_max, y)
        if y > 0:
            o_pos = y if o_pos is None else min(o_pos, y)
    return (o_min, o_pos, o_max)


def _get_minmax_all(objs, **kwargs):
    min_val = None
    min_pos = None
    max_val = None
    for obj in objs:
        if 'TF' in obj.ClassName(): continue
        min_obj, min_pos_obj, max_obj = _get_minmax(obj, **kwargs)
        if min_obj is None or max_obj is None: continue

        if min_val is None or min_obj < min_val: 
            min_val = min_obj

        if min_pos_obj is not None:
            if min_pos is None or min_pos_obj < min_pos: min_pos = min_pos_obj

        if max_val is None or max_obj > max_val:
            max_val = max_obj
    if min_val is None:
        print(f"WARNING! _get_minmax_all() min_val is None, setting to 0")
        min_val = 0
    if min_pos is None:
        print(f"WARNING! _get_minmax_all() min_pos is None, setting to 0")
        min_pos = 0
    if max_val is None:
        print(f"WARNING! _get_minmax_all() max_val is None, setting to 0")
        max_val = 0
    
    return min_val, min_pos, max_val


def _auto_yrange(objs, at_least_zero=False, yrange=(None,None), logy=None, ydatapad_bot=0.1, ydatapad_top=0.1, **kwargs):
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
        min_val, min_pos, max_val = _get_minmax_all(objs, **kwargs)
        min_val = min_val if yrange[0] is None else yrange[0]
        max_val = max_val if yrange[1] is None else yrange[1]

        if logy:
            min_val = min_pos
            min_val = np.log10(min_pos)
            max_val = np.log10(max_val)
        elif min_val >= 0:
            at_least_zero = True # If everything is positive, make sure that the y_min is at least 0

        data_height = 1.0 - ydatapad_bot - ydatapad_top
        diff = (max_val - min_val)
        min_val = min_val - diff * ydatapad_bot / data_height if yrange[0] is None else yrange[0]
        max_val = max_val + diff * ydatapad_top / data_height if yrange[1] is None else yrange[1]
        if at_least_zero:
            min_val = max(min_val, 0)

        if logy:
            newrange = (np.power(10, min_val), np.power(10, max_val))
        else:
            newrange = (min_val, max_val)

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
        
        if isinstance(yrange, list):
            yrange[0] = newrange[0]
            yrange[1] = newrange[1]
    else:
        newrange = yrange

    return newrange


def _auto_zrange(objs, zrange=(None,None)):
    if zrange[0] is None or zrange[1] is None:
        min_val = None
        max_val = None
        for obj in objs:
            if 'TH2' in obj.ClassName():
                for y in range(1, obj.GetNbinsY() + 1):
                    for x in range(1, obj.GetNbinsX() + 1):
                        v = obj.GetBinContent(x, y)
                        if v == 0: continue
                        if min_val is None or v < min_val: min_val = v
                        if max_val is None or v > max_val: max_val = v
        if zrange[0] is not None or min_val is None: min_val = zrange[0]
        if zrange[1] is not None or max_val is None: max_val = zrange[1]
        new_range = (min_val, max_val)

        if isinstance(zrange, list):
            zrange[0] = new_range[0]
            zrange[1] = new_range[1]
    else:
        new_range = zrange
    return new_range


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


def _apply_common_opts(obj, i, **kwargs):
    if 'linecolor' in kwargs:
        obj.SetLineColor(_arg(kwargs['linecolor'], i))
    if 'linestyle' in kwargs:
        obj.SetLineStyle(_arg(kwargs['linestyle'], i))
    if 'linewidth' in kwargs:
        obj.SetLineWidth(_arg(kwargs['linewidth'], i))

    if 'markerstyle' in kwargs:
        obj.SetMarkerStyle(_arg(kwargs['markerstyle'], i))
    if 'markercolor' in kwargs:
        obj.SetMarkerColor(_arg(kwargs['markercolor'], i))
    if 'markersize' in kwargs:
        obj.SetMarkerSize(_arg(kwargs['markersize'], i))

    if 'fillcolor' in kwargs:
        obj.SetFillColor(_arg(kwargs['fillcolor'], i))
    if 'fillstyle' in kwargs:
        obj.SetFillStyle(_arg(kwargs['fillstyle'], i))


def _apply_frame_opts(obj, **kwargs):
    if 'xtitle' in kwargs:
        obj.GetXaxis().SetTitle(kwargs['xtitle'])
    if 'ytitle' in kwargs:
        obj.GetYaxis().SetTitle(kwargs['ytitle'])
    if 'ztitle' in kwargs:
        obj.GetZaxis().SetTitle(kwargs['ztitle'])

    if x := kwargs.get('ztitleoffset'):
        obj.GetZaxis().SetTitleOffset(x)

    if 'xdivs' in kwargs:
        obj.GetXaxis().SetNdivisions(kwargs['xdivs'], True)
    if 'ydivs' in kwargs:
        obj.GetYaxis().SetNdivisions(kwargs['ydivs'], True)
    if x := kwargs.get('zdivs'):
        obj.GetZaxis().SetNdivisions(x, True)


def _plot(c, objs, opts="",
    textpos='topleft', titlesize=0.05, titlespacing=1, title='Internal', subtitle=None,
    legend=[], legend_order=None, legend_split=1, legend_width=0.2, legend_opts=None, legend_custom=None,
    rightmargin=None,
    logx=None, logy=None, logz=None, stack=False,
    canvas_callback=None, frame_callback=None, frame_histogram=False,
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
        if 'ztitle' in kwargs:
            rightmargin = 0.2
        elif 'Z' in _arg(opts, 0):
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

    ### Frame ###
    # ROOT uses the axis of the first object drawn for some ridiculous reason. So this
    # object controls all the axis properties even when other histograms are drawn.
    frame = objs[0]
    if frame_histogram:
        frame.Draw('')
        objs = objs[1:]
        if isinstance(opts, str):
            opts = 'SAME ' + opts
        else:
            opts[0] = 'SAME ' + opts[0]
    _apply_frame_opts(frame, **kwargs)

    ### Process histograms ###
    for i in range(len(objs)):
        _apply_common_opts(objs[i], i, **kwargs)

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
            if '2+' in opt: # Specify 2+ to draw both error rectangles and bars
                objs[i].Draw('SAME ' + opt.replace('2+', '').replace('A', ''))
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
        frame.Draw()
        for h, opt in zip(reversed(stack_hists), reversed(stack_opts)):
            h.Draw('SAME ' + opt)

    ### Auto range
    xrange = None
    yrange = None
    if kwargs.get('xrange') is not None: # No autorange by default
        xrange = _auto_xrange(objs, **kwargs)
        if xrange is not None: 
            if 'TGraph' in frame.ClassName():
                frame.GetXaxis().SetLimits(*xrange)
            else:
                frame.GetXaxis().SetRangeUser(*xrange)
            kwargs['xrange'] = xrange
    if kwargs.get('yrange', True) is not None: # default value not used here, just needs to not be None to auto range by default
        if 'TH2' not in frame.ClassName():
            yrange = _auto_yrange(objs, logy=logy, **kwargs)
            frame.GetYaxis().SetRangeUser(*yrange)
    if zrange := kwargs.get('zrange'):
        zrange = _auto_zrange(objs, zrange=zrange)
        frame.GetZaxis().SetRangeUser(*zrange)

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
    if frame_callback: cache.append(frame_callback(frame))

    return cache


def _outliers(hists):
    '''
    Draws outlier arrows for points that aren't in the yrange of the graph. hists[0]
    should be the axis histogram.
    '''
    y_min = hists[0].GetMinimum() # user coordinates
    y_max = hists[0].GetMaximum()
    y_pad = (y_max - y_min) / 50

    x_min = hists[0].GetXaxis().GetFirst() # bins
    x_max = hists[0].GetXaxis().GetLast()

    markers = []
    for h in hists:
        if 'TH1' in h.ClassName():
            for i in range(x_min, x_max + 1):
                v = h.GetBinContent(i)
                if v == 0: continue
                elif y_max is not None and v >= y_max:
                    m = ROOT.TMarker(h.GetXaxis().GetBinCenter(i), y_max - y_pad, ROOT.kFullTriangleUp)
                elif y_min is not None and v < y_min:
                    m = ROOT.TMarker(h.GetXaxis().GetBinCenter(i), y_min + y_pad, ROOT.kFullTriangleDown)
                else: continue
                
                m.SetMarkerColor(h.GetLineColor())
                m.Draw()
                markers.append(m)

    return markers


##############################################################################
###                            CANVAS WRAPPERS                             ###
##############################################################################


def plot(objs, canvas_size=(1000,800), canvas_name='c1', **kwargs):
    c = ROOT.TCanvas(canvas_name, canvas_name, *canvas_size)
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


def _fix_axis_sizing(h, pad, remove_x_labels=False, xlabeloffset=0.005, xlabelsize=0.05, **kwargs):
    '''
    Fixes various axes sizing issues when you have multiple pads, since ROOT sizes 
    things based on the pad size not the canvas size.
    '''
    old_size = 0.05    
    old_offset_x = 1.4 
    old_offset_y = 1.4 
    tick_length_x = 0.015
    tick_length_y = 0.03

    height = pad.GetHNDC()

    if remove_x_labels:
        h.GetXaxis().SetLabelOffset(999)
        h.GetXaxis().SetLabelSize(0)
        h.GetXaxis().SetTitleSize(0)
    else:
        h.GetXaxis().SetLabelOffset(xlabeloffset)
        h.GetXaxis().SetLabelSize(xlabelsize / height)
        h.GetXaxis().SetTitleSize(old_size / height)
        h.GetXaxis().SetTitleOffset(1)

    h.GetYaxis().SetLabelSize(old_size / height)
    h.GetYaxis().SetTitleSize(old_size / height)
    h.GetYaxis().SetTitleOffset(old_offset_y * height)

    h.GetXaxis().SetTickLength(tick_length_x / height) 
    h.GetYaxis().SetTickLength(tick_length_y / (1 - pad.GetTopMargin() - pad.GetBottomMargin())) 
    # See https://root-forum.cern.ch/t/inconsistent-tick-length/18563/9
    # The tick scale is affected by the margins: tick_length = pixel_size / ((pad2H - marginB - marginT) / pad2H * pad2W)
    # Note there seems to be a minimum tick length for the y axis...


def _draw_horizontal_line(pos, h, xrange):
    # TODO this will still draw the line out of the axes if pos is not in yrange
    if pos is not None:
        if xrange:
            # make sure xrange is a list if it has None elements
            line = ROOT.TLine(xrange[0], pos, xrange[1], pos)
        else:
            line = ROOT.TLine(h.GetXaxis().GetXmin(), pos, h.GetXaxis().GetXmax(), pos)
        line.SetLineStyle(ROOT.kDashed)
        line.Draw()
        return line


def plot_ratio(hists1, hists2, height1=0.7, outlier_arrows=True, hline=None, axes_callback=None, save_plot=True, **kwargs):
    '''
    Plots [hists1] in a main pad on top and [hists2] in a secondary pad below. The two 
    sets of objects should share the same x axis. Set options in the secondary pad by 
    postpending the kwargs with a '2'.

    @param hline
        Draws a horizontal line in the secondary pad. The value sets the y position in
        user coordinates. Set to None to omit.
    @param outlier_arrows
        Draws small triangles at the top/bottom of the ratio pad to indicate points that
        are outside of the plot range.
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

    ### Draw ratio plot ###
    args2 = { 'ydivs': 504, 'ignore_outliers_y': 4, 'title': None, 'legend': None }
    args2.update(_copy_ratio_args(kwargs, '2'))
    cache.append(_plot(pad2, hists2, do_legend=False, **args2))
    pad2.RedrawAxis() # Make the tick marks go above any fill

    ### Draw y=1 line ###
    cache.append(_draw_horizontal_line(hline, hists2[0], kwargs.get('xrange')))
    
    ### Fix axes sizing ### 
    _fix_axis_sizing(hists1[0], pad1, True)
    _fix_axis_sizing(hists2[0], pad2)
    
    ### Draw out-of-bounds arrows ###
    if outlier_arrows: cache.append(_outliers(hists2))

    ### Callback ###
    if axes_callback:
        axes_callback(hists1[0], hists2[0])
    if save_plot:
        save_canvas(c, kwargs.get('filename', hists1[0].GetName()))
    
    return c, cache


def plot_ratio3(hists1, hists2, hists3, height1=0.55, outlier_arrows=True, hline2=None, hline3=None, axes_callback=None, save_plot=True, **kwargs):
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

    ### Create pads ###
    height2 = (1 - height1) / 2 - 0.06
    height3 = height2 + 0.12

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

    ### Draw main histo ###
    titlesize = kwargs.get('titlesize', 0.05)
    kwargs['titlesize'] = titlesize / height1
    # kwargs['yrange'] = list(kwargs.get('yrange', [None, None]))
    kwargs.setdefault('text_offset_bottom', 0.1 * (1 - height1)) # guess
    cache = _plot(pad1, hists1, **kwargs)
    pad1.RedrawAxis() # Make the tick marks go above any fill

    ### Draw first ratio plot
    args2 = { 'ydivs': 204, 'ignore_outliers_y': 3, 'title': None, 'legend': None, 'titlesize': titlesize / height2 }
    args2.update(_copy_ratio_args(kwargs, '2'))
    cache.append(_plot(pad2, hists2, do_legend=False, **args2))
    pad2.RedrawAxis() # Make the tick marks go above any fill

    ### Draw y=1 line ###
    cache.append(_draw_horizontal_line(hline2, hists2[0], kwargs.get('xrange')))

    ### Draw out-of-bounds arrows ###
    if outlier_arrows: cache.append(_outliers(hists2))

    ### Draw second ratio plot
    args3 = { 'ydivs': 204, 'ignore_outliers_y': 3, 'title': None, 'legend': None, 'titlesize': titlesize / height3, 'text_offset_bottom': 0.15 / height3 }
    args3.update(_copy_ratio_args(kwargs, '3'))
    cache.append(_plot(pad3, hists3, do_legend=False, **args3))
    pad3.RedrawAxis() # Make the tick marks go above any fill

    ### Draw y=1 line ###
    cache.append(_draw_horizontal_line(hline3, hists3[0], kwargs.get('xrange')))

    ### Draw out-of-bounds arrows ###
    if outlier_arrows: cache.append(_outliers(hists3))

    ### Fix axes sizing ### 
    _fix_axis_sizing(hists1[0], pad1, True, **kwargs)
    _fix_axis_sizing(hists2[0], pad2, True, **args2)
    _fix_axis_sizing(hists3[0], pad3, **args3)

    ### Callback ###
    if axes_callback:
        axes_callback(hists1[0], hists2[0], hists3[0])
    if save_plot:
        save_canvas(c, kwargs.get('filename', hists1[0].GetName()))

    return c, cache


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
    args2 = _copy_ratio_args(kwargs, '2')

    ### Fix opts to plot 'SAME'
    opts2 = args2.pop('opts', '')
    if isinstance(opts2, str):
        opts2 = [opts2] * len(hists2)
    opts2[0] = 'SAME ' + opts2[0]

    ### Scale histograms to new yrange
    yrange2 = _auto_yrange(hists2, **args2)
    args2['yrange'] = yrange2
    scale = (c.GetUymax() - c.GetUymin()) / (yrange2[1] - yrange2[0])
    hists2 = [h.Clone() for h in hists2]
    for h in hists2:
        if 'TH' in h.ClassName():
            for i in range(h.GetNbinsX()):
                h.SetPointY(i, c.GetUymin() + (h.GetBinContent(i) - yrange2[0]) * scale)
        elif 'TGraph' in h.ClassName():
            for i in range(h.GetN()):
                h.SetPointY(i, c.GetUymin() + (h.GetPointY(i) - yrange2[0]) * scale)

    ### Plot the right histograms
    cache2 = _plot(c, hists2, opts=opts2, do_legend=False, **args2)

    ### Draw the second axis
    xmax = c.GetUxmax()
    if kwargs.get('logx'):
        xmax = (np.power(10, xmax))
    axis = ROOT.TGaxis(xmax, c.GetUymin(), xmax, c.GetUymax(), yrange2[0], yrange2[1], 510, '+L')
    axis.SetLabelFont(hists1[0].GetXaxis().GetLabelFont()) # 42
    axis.SetLabelSize(hists1[0].GetXaxis().GetLabelSize()) # 0.5
    axis.SetLabelColor(colors.red)
    axis.SetTitle(kwargs.get('ytitle2', ''))
    axis.SetTitleFont(hists1[0].GetXaxis().GetLabelFont()) # 42
    axis.SetTitleSize(hists1[0].GetXaxis().GetLabelSize()) # 0.5
    axis.SetTitleColor(colors.red)
    axis.SetLineColor(colors.red)
    axis.Draw()

    save_canvas(c, kwargs.get('filename', hists1[0].GetName()))


def _draw_tier_fill(h, y, i, fillcolor=None, **kwargs):
    cache = []
    color = _arg(fillcolor, y) if fillcolor else h.GetFillColor() # color each tier differently, instead of each series. Assume generally i == 1 in this function.
    for x in range(1, h.GetNbinsX() + 1):
        x1 = h.GetXaxis().GetBinLowEdge(x)
        x2 = h.GetXaxis().GetBinLowEdge(x + 1)
        height = h.GetBinContent(x)
        if height <= 0: continue

        box = ROOT.TBox(x1, y, x2, y + height)
        box.SetFillColor(color)
        box.SetLineColor(color)
        box.Draw()
        cache.append(box)
    return cache


def _draw_tier_line(h, y, i, linecolor=None, linewidth=None, xrange=None, **kwargs):
    cache = []
    color = _arg(linecolor, i) if linecolor else h.GetLineColor()
    width = _arg(linewidth, i) if linewidth else h.GetLineWidth()
    first = True
    for x in range(1, h.GetNbinsX() + 1):
        x1 = h.GetXaxis().GetBinLowEdge(x)
        x2 = h.GetXaxis().GetBinLowEdge(x + 1)
        y2 = y + h.GetBinContent(x)

        if xrange:
            if x1 < xrange[0]: continue
            if x2 > xrange[1]: continue

        lines = [ROOT.TLine(x1, y2, x2, y2)]
        if first: 
            first = False
        else:
            y_old = y + h.GetBinContent(x - 1)
            lines.append(ROOT.TLine(x1, y_old, x1, y2))

        for l in lines:
            l.SetLineColor(color)
            l.SetLineWidth(width)
            l.Draw()
        cache.append(lines)
    return cache


def plot_tiered(hists, y_labels=None, plot_style=None, ydatapad_top=0.1, **kwargs):
    '''
    Similar to a violin plot, this plots each histogram in its own equi-height y-bin.
    Negative values are supressed.

    @param hists
        A list of histograms with shape (#ybins, #series). The y-bins are listed from
        bottom to top. The series histograms in each ybin are normalized to each other.
    @param y_labels
        The label of each y-bin, in matching order as `hists.shape[0]`.
    @param plot_style
        How to draw the histograms. This can be
            - "fill": Filled boxes from 0. Default option if #series == 1.
            - "line": Similar to ROOT "hist" mode. Default option if #series > 1.
            - "point": Similar to ROOT "PE" mode. Not implemented yet.
    '''
    n_tiers = len(hists)
    c = ROOT.TCanvas('c1', 'c1', 1000, 800)

    ### Create the frame ###
    axis = hists[0][0].GetXaxis()
    if axis.IsVariableBinSize():
        h_frame = ROOT.TH2F('tiers', '', axis.GetNbins(), axis.GetXbins().GetArray(), n_tiers, 0, n_tiers)
    else:
        h_frame = ROOT.TH2F('tiers', '', axis.GetNbins(), axis.GetXmin(), axis.GetXmax(), n_tiers, 0, n_tiers)
    h_frame.Draw('AXIS')

    ### Set bin labels ###
    if y_labels is not None:
        c.SetLeftMargin(kwargs.get('leftmargin', 0.2))
        h_frame.GetYaxis().SetTitleOffset(kwargs.get('ytitle_offset', 2))
        for y,label in enumerate(y_labels):
            h_frame.GetYaxis().SetBinLabel(y + 1, label)

    ### Handle some opts that are usually done in _plot ###
    kwargs['xrange'] = _auto_xrange([x for s in hists for x in s], **kwargs)
    yrange = kwargs.pop('yrange', None)
    logy = kwargs.pop('logy', None)
    kwargs.pop('opts', None)

    if 'legend' in kwargs and 'legend_custom' not in kwargs:
        legend_custom = []
        for i,obj in enumerate(hists[0]): 
            _apply_common_opts(obj, i, **kwargs)
            legend_custom.append([obj, kwargs['legend'][i], 'L'])
        kwargs['legend_custom'] = legend_custom

    ### Draw histograms ###
    cache = []
    for y,series in enumerate(hists):
        # Normalize the histograms to the maximum value. In user coordinates, defined
        # by the frame histogram above, the max height of each y bin is just 1.
        _, min_pos, max_val = _get_minmax_all(series, **kwargs)
        if not max_val: continue

        if logy:
            if yrange and yrange[0] is not None:
                min_pos = yrange[0]
            max_val = np.log(max_val) - np.log(min_pos)
            series = [log_hist(h, min_val=min_pos) for h in series]

        for i,h in enumerate(series):
            h.Scale((1 - ydatapad_top) / max_val)
            if plot_style == 'fill' or plot_style is None and len(series) == 1:
                cache.append(_draw_tier_fill(h, y, i, **kwargs))
            elif plot_style == 'line' or plot_style is None and len(series) > 1:
                cache.append(_draw_tier_line(h, y, i, **kwargs))

    ### Draw labels and text ###
    cache.append(_plot(c, [h_frame], opts='AXIS SAMES', **kwargs)) # Make the tick marks / titles go above the boxes
    
    if bin_title := kwargs.get('bin_title'):
        c.SetTopMargin(0.06)
        tex = ROOT.TLatex(0, 0.95, bin_title)
        tex.SetTextFont(42)
        tex.SetTextSize(0.035)
        tex.SetNDC()
        width = tex.GetXsize()
        tex.SetX(max(0.05, c.GetLeftMargin() - width))
        tex.Draw()

    save_canvas(c, kwargs.get('filename', hists[0][0].GetName()))


def plot_2panel(hists1, hists2, **kwargs):
    '''
    Similar to [plot_ratio], but sets some default values to give the two pads the same 
    height.
    '''
    def setdefault_both(key, val):
        kwargs.setdefault(key, val)
        kwargs.setdefault(key + '2', kwargs[key]) # use the value set by the user, if present
    kwargs.setdefault('textpos', 'topsplit')
    kwargs.setdefault('height1', 0.5)
    setdefault_both('ydivs', 506)

    plot_ratio(hists1, hists2, **kwargs)


def plot_3panel(hists1, hists2, hists3, **kwargs):
    '''
    Similar to [plot_ratio3], but sets some default values to give the pads the same 
    height.
    '''
    def setdefault_all(key, val):
        kwargs.setdefault(key, val)
        kwargs.setdefault(key + '2', kwargs[key]) # use the value set by the user, if present
        kwargs.setdefault(key + '3', kwargs[key])
    kwargs.setdefault('textpos', 'topsplit')
    kwargs.setdefault('height1', 0.4)
    setdefault_all('ydivs', 504)

    plot_ratio3(hists1, hists2, hists3, **kwargs)


def plot_discrete_bins(hists1, hists2=None, hists3=None, plotter=plot, bin_width=0.6, edge_labels=None, **kwargs):
    '''
    This function plots histograms or graphs side-by-side in each bin (similar to a
    traditional bar plot), which makes it easier to compare similar histograms. The x-
    axis is converted to equally spaced bins.

    @param hists1, hists2, hists3
        A list of TH1s or TGraphs to plot. The first object of [hists1] should be TH1, or
        else specify [edge_labels].
        [hists2] and [hists3] are optional subplot histograms. All histograms/graphs 
        should have the exact same binning.
    @param plotter
        The plot function to use. For example if you want a ratio plot, you should pass
        [hists1] and [hists2] and set plotter=plot_ratio.
    @param bin_width
        The width of plot contents in each bin. This should be a number between 0 and 1,
        where 1 indicates using the full bin width (no margins).
    @param edge_labels
        Specify a list of replacement labels for the bin edges. This should have length
        equal to nbins+1, and will ignore the x values of the histograms.

    The function will create new TGraphAsymmErrors with a custom x axis that ranges from 
    0 to nbins, respecting any xrange specifications. We do this instead of using alphanu-
    meric bin labels because those are always drawn at the bin center, not the edges.
    '''
    ### Find bins ###
    if edge_labels:
        bin_start = 0 # these are 0-indexed
        bin_end = len(edge_labels) - 1 # exclusive
        nbins = bin_end
    else:
        bin_start = None # these are 0-indexed
        bin_end = None # exclusive
        xrange = _auto_xrange(hists1, **kwargs)
        h_check = hists1[0]
        if xrange is None:
            bin_start = 0
            bin_end = h_check.GetNbinsX()
        else:
            for i in range(1, h_check.GetNbinsX() + 2):
                if bin_start is None and h_check.GetBinLowEdge(i) >= xrange[0]:
                    bin_start = i - 1 # 0-index
                if bin_end is None and h_check.GetBinLowEdge(i) >= xrange[1]:
                    bin_end = i - 1 # 0-index
                    break
        nbins = bin_end - bin_start
        if nbins < 1: raise RuntimeError(f'plot_equiwidth_bins() nbins < 1: nbins={nbins}, xrange={xrange}')

    ### Create frame histogram ###
    h_frame = ROOT.TH1D(hists1[0].GetName() + '_frame', '', nbins, 0, nbins)

    ### Adjust labels of x axis ###
    arg_name = 'frame_callback' + ('3' if hists3 else '2' if hists2 else '')
    user_frame_callback = kwargs.get(arg_name)
    def frame_callback(frame):
        for i in range(bin_start + 1, bin_end + 2): # ticks are 1-indexed
            label = edge_labels[i - 1] if edge_labels else f'{h_check.GetBinLowEdge(i):.0f}'
            frame.GetXaxis().ChangeLabel(i, 30, -1, -1, -1, -1, label)
        if user_frame_callback:
            user_frame_callback(frame)
    kwargs[arg_name] = frame_callback
    kwargs.setdefault('xlabelsize', 0.03) # don't set this in ChangeLabel(), or else the labels get duplicated
    kwargs.setdefault('xlabeloffset', 0.02) 

    ### Convert objects to TGraphAsymmErrors ###
    def create_graph(obj, i, n):
        pad_start = (1 - bin_width) / 2
        width = bin_width / n
        x = pad_start + (i + 0.5) * width
        width *= 0.8 # leave some space between points
        
        ### Create the graph ###
        g = ROOT.TGraphAsymmErrors(nbins)
        for i in range(nbins):
            if 'TH1' in obj.ClassName():
                v = obj.GetBinContent(bin_start + i + 1)
                e_low = obj.GetBinError(bin_start + i + 1)
                e_high = e_low
            elif 'TGraph' in obj.ClassName():
                v = obj.GetPointY(bin_start + i)
                e_low = obj.GetErrorYlow(bin_start + i)
                e_high = obj.GetErrorYhigh(bin_start + i)
            g.SetPoint(i, i + x, v)
            g.SetPointError(i, width / 2, width / 2, e_low, e_high)

        ### Copy plot attributes ###
        g.SetLineColor(obj.GetLineColor())
        g.SetLineWidth(obj.GetLineWidth())
        g.SetLineStyle(obj.GetLineStyle())
        g.SetMarkerColor(obj.GetMarkerColor())
        g.SetMarkerSize(obj.GetMarkerSize())
        g.SetMarkerStyle(obj.GetMarkerStyle())
        g.SetFillColor(obj.GetFillColor())
        g.SetFillStyle(obj.GetFillStyle())
        return g

    def convert_objs(objs):
        if objs is None: return None
        out = [create_graph(obj, i, len(objs)) for i,obj in enumerate(objs)]
        return [h_frame.Clone()] + out

    hists1 = convert_objs(hists1)
    hists2 = convert_objs(hists2)
    hists3 = convert_objs(hists3)

    ### Fix args ###
    kwargs['xdivs'] = -nbins
    kwargs['xrange'] = (0, nbins)
    kwargs['frame_histogram'] = True
    kwargs['frame_histogram2'] = True
    kwargs['frame_histogram3'] = True

    ### Plot ###
    pos_args = [hists1]
    if hists2: pos_args.append(hists2)
    if hists3: pos_args.append(hists3)
    plotter(*pos_args, **kwargs)

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

    c.Print('colormaps.png')


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


def _clamp(x):
    return max(0, min(int(x), 255))


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
        elif a != 0 and a != 255: # this is an alpha channel that is blended onto the (opaqued) white background.
            # The alpha value is the true alpha of the blended content though.
            # So we simply undo the blending on an opaque background: c_new = c_old * a + c_b * (1 - a)
            # where c_b is the color of the background. With rounding and ROOT weirdness it seems 252 gives a good value.
            af = a / 255
            r = _clamp((r - 252 * (1 - af)) / af)
            g = _clamp((g - 252 * (1 - af)) / af)
            b = _clamp((b - 252 * (1 - af)) / af)
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
###                               UTILITIES                                ###
##############################################################################


def normalize(h, mode="integral"):
    '''
    Normalizes a histogram with multiple different modes. This function leaves the
    original histogram untouched.

    @param mode
        - "integral": Divides [h] by its integral, including overflow bins
        - "integral%": As above, but scales by 100.
        - "abs integral": Divides [h] by the sum of its |bin contents|, including over-
            flow bins.
        - "cumulative": Sets the bin x to (# events <= x / # total events).
        - "cumulativer": Sets the bin x to (# events >= x / # total events).
    @return the normalized histogram.
    '''
    h = h.Clone()
    if mode == True:
        mode = 'integral'

    if not mode:
        pass
    elif mode.startswith("integral"):
        integral = h.Integral(0, -1)
        if integral == 0:
            print("plot.normalize() Warning! Integral is 0, doing nothing")
        elif '%' in mode:
            h.Scale(100 / integral)
        else:
            h.Scale(1 / integral)
    elif mode == "abs integral":
        tot = 0
        for i in range(0, h.GetNbinsX()+2): # TH1 bins are 1-indexed
            tot += abs(h.GetBinContent(i))
        if tot == 0:
            print("plot.normalize() Warning! Integral is 0, doing nothing")
        else:
            h.Scale(1 / tot)
    elif mode == "cumulative":
        tot = h.Integral(0, -1)
        if tot == 0:
            print("plot.normalize() Warning! Integral is 0, doing nothing")
        else:
            running_sum = 0
            for i in range(0, h.GetNbinsX() + 2): 
                running_sum += h.GetBinContent(i)
                h.SetBinContent(i, running_sum / tot)
                h.SetBinError(i, 0)
    elif mode == "cumulativer":
        tot = h.Integral(0, -1)
        if tot == 0:
            print("plot.normalize() Warning! Integral is 0, doing nothing")
        else:
            running_sum = 0
            for i in range(h.GetNbinsX() + 1, -1, -1): 
                running_sum += h.GetBinContent(i)
                h.SetBinContent(i, running_sum / tot)
                h.SetBinError(i, 0)
    else:
        raise RuntimeError(f'graphs.normalize() unknown mode: {mode}')

    return h


def normalize_ytitle(mode, splitline=False):
    '''
    Returns a ytitle given a normalization mode as in [normalize].
    '''
    if mode is None:
        return "Events"
    if mode == "integral" or mode == True:
        if splitline: return "#splitline{Normalized}{Events}"
        return "Normalized Events"
    elif mode == "integral%":
        return "% of Total Events"
    elif "cumulative" in mode:
        if splitline: return "#splitline{Cumulative}{Events}"
        return "Cumulative Fraction of Events"
    else:
        return "Events"


def log_hist(h, min_val=None):
    h = h.Clone()
    for i in range(0, h.GetNbinsX() + 2):
        v = h.GetBinContent(i)
        if v > min_val or 0:
            h.SetBinContent(i, np.log(v / min_val))
        else:
            h.SetBinContent(i, 0)
        h.SetBinError(i, 0) # no asymmetric bin errors...
    return h


def get_bin_indexes(axis, bin_edges):
    '''
    Returns the bin indexes into `axis` that match `bin_edges`
    '''
    current_index = 1
    indexes = []
    for bin_edge in bin_edges:
        ### Increment until the current edge is equal to the requested edge ###
        while axis.GetBinLowEdge(current_index) < bin_edge:
            if current_index >= axis.GetNbins(): # Failsafe
                raise RuntimeError(f'get_bin_indexes() Unable to find fid bin edge {bin_edge}')
            current_index += 1

        ### Check to make sure the bin edges are aligned ###
        old_bin_edge = axis.GetBinLowEdge(current_index)
        if old_bin_edge != bin_edge:
            raise RuntimeError(f"get_bin_indexes() Bins don't align: requested={bin_edge}, found={old_bin_edge}")

        ### Save ###
        indexes.append(current_index)

    return indexes


def rebin2d(h, bins_x, bins_y, name = '_rebin2d'):
    '''
    Rebins a histogram with variable bin sizes, because somehow ROOT hasn't implemented 
    this. The bins must align!

    @param bins_x,bins_y
        These should be the N+1 bin edges that define the N bins. The bin edges MUST
        align with the bin edges of [h].
    @param name
        Name postfix to the newly created histogram. Must make sure Root names do not
        collide.
    '''
    h_new = ROOT.TH2F(h.GetName() + name, h.GetTitle(), len(bins_x) - 1, np.array(bins_x, dtype=float), len(bins_y) - 1, np.array(bins_y, dtype=float))

    ### Get the bin indices into `h` that align with the requested bins. These always point to the
    ### lower edge of the bin.
    bin_indexes_x = [0] + get_bin_indexes(h.GetXaxis(), bins_x) + [h.GetNbinsX() + 2] # add the underflow and overflow bins
    bin_indexes_y = [0] + get_bin_indexes(h.GetYaxis(), bins_y) + [h.GetNbinsY() + 2] # add the underflow and overflow bins

    ### Populate the new histogram ###
    for y_new in range(len(bin_indexes_y) - 1):     # index into the bin_indexes lists
        for x_new in range(len(bin_indexes_x) - 1): # since we include the underflow bin above, this also indexes into h_new
            v = 0
            e = 0
            for y_old in range(bin_indexes_y[y_new], bin_indexes_y[y_new + 1]): # ROOT bin index into h
                for x_old in range(bin_indexes_x[x_new], bin_indexes_x[x_new + 1]):
                    v += h.GetBinContent(x_old, y_old)
                    e += h.GetBinError(x_old, y_old)**2
            h_new.SetBinContent(x_new, y_new, v)
            h_new.SetBinError(x_new, y_new, e**0.5)

    return h_new


def graph_divide(a, b, errors_a=True, errors_b=True):
    '''
    Return a / b when a is a TGraphAsymmErrors. The output is also a TGraphAsymmErrors. The
    points of a should align with the bins of b.

    Assumes b has symmetric errors if it's also a TGraphAsymmErrors.
    '''
    out = a.Clone()
    for i in range(a.GetN()):
        va = a.GetPointY(i)
        vb = b.GetPointY(i) if 'TGraph' in b.ClassName() else b.GetBinContent(i + 1)
        if va == 0 or vb == 0:
            out.SetPointY(i, 0)
            out.SetPointEYhigh(i, 0)
            out.SetPointEYlow(i, 0)
            continue

        r = va / vb
        err_hi = 0
        err_lo = 0
        if errors_a: 
            err_hi += (out.GetErrorYhigh(i) / va)**2
            err_lo += (out.GetErrorYlow(i) / va)**2
        if errors_b:
            eb = b.GetErrorYhigh(i) if 'TGraph' in b.ClassName() else b.GetBinError(i + 1)
            err = (eb / vb)**2
            err_hi += err
            err_lo += err

        out.SetPointY(i, r)
        out.SetPointEYhigh(i, r * err_hi**0.5)
        out.SetPointEYlow(i, r * err_lo**0.5)

    return out


##############################################################################
###                                LOGGING                                 ###
##############################################################################

def success(x):
    '''Prints a green message to the terminal.'''
    print('\033[92m' + x + '\033[0m')


def warning(x):
    '''Prints a yellow warning message to the terminal.'''
    print('\033[93mWARNING ' + x + '\033[0m')


def error(x):
    '''Prints a red error message to the terminal.'''
    print('\033[91mERROR ' + x + '\033[0m')


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


