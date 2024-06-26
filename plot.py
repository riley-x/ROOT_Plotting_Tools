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

Please see the `examples/` folder for more examples!

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
plot_discrete_bins
    Plots histograms in discrete x bins, so histograms appear side by side (like a bar
    chart). Useful when histograms are very similar, and would overlap otherwise.
Plotter
    The underlying plotting class used by everything above. Useful for creating 
    custom images containing multiple canvases, or more complicated series plots.

    For example, if you want to plot a stack of histograms with some overlaid info, like
    data points and statistical errors, it's much easier to use the [Plotter] class 
    directly. See `examples/stack_plot.py` for an example.



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
line<color/style/width>                                 default: 'auto'
    Sets the corresponding TAttLine properties. See the ROOT documentation for input
    values. Set to None to do nothing. In the auto mode, linecolor will be set to the
    colors.tableu colormap, as long as all there are multiple objects and they are all 
    black. Otherwise, the default is None.
marker<color/style/size>                                default: 'auto'
    Sets the corresponding TAttMarker properties. See the ROOT documentation for input
    values. Set to None to do nothing. In the auto mode, markercolor will be set to the
    colors.tableu colormap, as long as all there are multiple objects and they are all 
    black. Otherwise, the default is None.
fill<color/style>                                       default: None
    Sets the corresponding TAttFill properties. See the ROOT documentation for input
    values. Set to None to do nothing.


TEXT AND FILE NAMES
--------------------------------------------------------
filename
    Path to save the image to. If the filename ends with an extension like '.png', the
    file will be saved in that format. If no extension is given, saves the file with
    each extension in [plot.file_formats].
text_pos                                                default: 'auto'
    Location of title / legend. 
    
    Can be a combination of (top/bottom) and/or (left/right),
    so for example 'top' will place the title in the top-left corner and the legend in
    the top-right, while 'top left' will place both in the top-left corner. You can also 
    specify 'forward diagonal' or 'backward diagonal' to place the title and legend in
    diagonally opposite corners. You can add 'reverse' to some of these to reverse the 
    title and legend positions.

    Set to 'auto' to automatically choose the best option (the one that requires the 
    least amount of whitespace), or a list of the options above to only do the optimization
    over specific options.

title                                                   default: 'ATLAS Internal'
    Title text to display in the plot. Any instance of "ATLAS" will be replaced by the 
    approriate bold, italic string.
subtitle
    Additional text that is displayed below the title. This can be a string or a 
    list of strings, with the latter putting each entry on a new line.
title_size                                              default: 0.05
    ROOT text size for the title.
text_size                                               default: 0.035
    ROOT text size for non-title text, including subtitle and legend.

    WARNING ROOT has a bug with measuring text that isn't at some golden sizes. It seems 
    0.05 and 0.035 work well. This may cause right aligning to be broken; it seems the 
    longer the text the more off it'll be.
text_spacing                                            default: 1.0
    Multiplicative factor for modifying the spacing between title/text/legend.
text_offset_<left/right/bottom/top>                     default: 0.05
    Offset of text elements (titles/legend) from the axes, in pad units. These are only
    used for relevant [text_pos] options. 


PAD/CANVAS
-----------------------------------------------------
<left/right/bottom/top>_margin
    Sets the pad margins.


AXES
-----------------------------------------------------
log<x/y/z>
    Sets the canvas to use log x/y/z axes.
<x/y/z>title
    Titles for the x/y/z axes.
<x/y/z>divs
    See TAxis::SetNdivisions. Sets the number of ticks on each axis. 
<x/y/z>_range                                           default: (None, None)
    Specify a list or a tuple of the (min, max) range of the axis to plot. You can set
    either entry to None to automatically fit plot contents. Set the entire argument to
    None to use default ROOT behavior. 
y_pad_bot/top                                           default: 0.05
    If using an automatic y-axis range, minimum amount of padding at the bottom/top so that 
    the data points don't crowd the edges. Also useful to make room for titles and legends.
    The value is in axis coordinates, so a value of 0.05 on both bottom and top makes the
    data only appear (at most) in the center 90% of the axes. 

    The automatic text placement procedure may increase the actual amount of padding used
    to fit the title text without overlapping the data.
y_min/max                                               default: None
    If using an automatic y-axis range, clamp the range to within the specified values.
    Set to `None` to disable.  
y_text_data_spacing                                     default: 0.02
    If using an automatic y-axis range, minimum amount of vertical padding between text 
    elements (titles and legend) and data points. Value is in pad coordinates.
x_pad_left/right                                        default: 0
    If using an automatic x-axis range, amount of padding at the left/right so that the
    data points don't crowd the edges. The value is in axes coordinates, so a value of 
    0.1 on both makes the data only appear in the center 80% of the plot. 
ignore_outliers_y                                       default: 0
    If using an automatic y-axis range, will ignore points when calculating the min/max
    bounds if they're more than this many standard deviations away from the mean. Set to
    0 to disable
title_offset_<x/y/z>
    ROOT TGaxis title offset.
x_bin_labels                                            default: None
    Specify a list of bin labels for the x axis. Should match the number of x bins. 
x_labels_option                                         default: None
    Set a ROOT TAxis.LabelsOption() option. 
    https://root.cern.ch/doc/master/classTAxis.html#a05dd3c5b4c3a1e32213544e35a33597c


LEGEND
-----------------------------------------------------
legend                                                  default: 'auto'
    Specification for the legend. Several different modes are available:
        1) None
            No legend is created.
        2) [label]
            Supply a list of string labels for each object. An empty string will omit
            the respective entry from the legend.
        3) 'auto'
            Auto creates the legend using the object ROOT names as labels. 
        4) [(obj, label, opt)]
            Manually set each legend entry using a ROOT.TObject as the formatter, a 
            string label, and the icon draw option.
    For options (2) and (3), the icon is drawn using the option(s) specified by 
    [legend_opts], and the order of the legend can be manipulated by [legend_order].
legend_order                                            default: None
    Reorders and trims the legend. Input a list of indexes into the list in [legend], so
    for example [3, 0, 1] will place the 4th entry first and omit the 3rd. 
legend_opts                                             default: context-dependent
    A list matching the legend labels that changes how the symbol is drawn. Can be any 
    mix of the letters 'PEFL' for point, error bars, fill, line. An empty string will omit
    the respective entry from the legend.
legend_columns                                          default: 1
    Number of columns to split the legend across.
legend_vertical_order                                   default: False
    When [legend_columns] > 1, the entries will go left to right by default. Set this
    option to true to go top to bottom instead.
    
OTHER
-----------------------------------------------------
stack                                                   default: False
    Plots a list of histograms as a stack. The histograms are added cumulatively to create
    the stack, with the first histogram being the bottom of the stack. The legend is 
    reversed to match the stack order visually.

    Note that this option only works with TH1s. See also `examples/stack_plot.py` for 
    adding extra plot items outside of the stack.

-----------------------------------------------------------------------------------------
COLORS
-----------------------------------------------------------------------------------------
See the color class docstring for more info, and the class implementation for a full list
of colors.
-----------------------------------------------------------------------------------------
Colormaps:
    colors.tableu: Matplotlib 'tableau' colormap
    colors.pastel: Matplotlib 'Pastel1' colormap



-----------------------------------------------------------------------------------------
UTILITY FUNCTIONS
-----------------------------------------------------------------------------------------
See each function's docstring for more info. There are many more than listed here too.
-----------------------------------------------------------------------------------------

HISTOGRAM MANIPULATION
-----------------------------------------------------
normalize
    Normalizes a histogram in multiple ways, such as forcing it to have unit area, or 
    convert it into a cumulative distribution.
rebin
    An easier histogram rebinning function that can handle various modes, like variable 
    bins or finding a user-width binning.
rebin2d
    Rebins a 2D histogram with variable bins on each axis.
integral_user
    Calculates the integral of a histogram using a user-coordinate range instead of a 
    bin range.
undo_width_scaling
    Undoes the scaling from h.Scale(1, 'width')
IterRoot
    Turns TH1 and TGraphs into iterators. Useful for defining generic functions that can
    operate on either.


OTHER
-----------------------------------------------------
colors_from_palette
    Returns a list of equally spaced colors from a ROOT palette.
save_canvas_transparent
    Saves a transparent canvas instead of the default white background. Set the global
    variable [plot.save_transparent] to True to enable in the plot functions above.
format
    Automatically formats a list of TObjects. 

'''
from __future__ import annotations

import ROOT # type: ignore
import itertools
import math
import ctypes
import numpy as np
import os
import sys
import bisect

ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gROOT.SetStyle("ATLAS")
ROOT.gROOT.ForceStyle()
ROOT.TGaxis.SetMaxDigits(4) # Number of digis to show on an axis, above which exponential notation is used

file_formats = ['png', 'pdf']
save_transparent_png = False

##############################################################################
###                                PLOTTING                                ###
##############################################################################

class Plotter:
    '''
    Main plotting class. Usually you should not bother with this class itself 
    and use the wrapper functions instead.
    
    The main workflow is:
    1. __init__()
        Sets the pad and title text configuration. Most pad-level configuration options
        should be supplied here.
    2. add()
        Adds a list of ROOT objects to the draw stack, with formatting and legend. This
        function can be called repeatedly. All style options should be passed here.
    3. compile()
        Processes object-dependent configuration, such as auto ranging, text placement,
        and creating the legend object. Note that many properties such as [y_range] are
        not set until [compile] is called.
    3. draw()
        Draws all objects in the draw stack. 

    An optional shortcut is to supply the [objs] arguement to __init__(), which will call
    the other steps automatically.
    
    See this file's docstring for configuration options, that can be passed in kwargs to
    the various functions. 

    -------------------------------- Implementation Details --------------------------------
    Much of the confusion in ROOT plotting is caused by the coupling of axes to individual
    histograms. This leads to such confusing things as needing to call "SAME" in the draw
    options, or errors such as
        h1.Draw()
        h2.Draw('SAME')
        h2.GetXaxis().SetTitle('this will not show up!')
    because the axes being drawn are from h1, not h2. This class remedies this problem by
    defining a dedicated "frame" histogram, that is always drawn first using the 'AXIS'
    option. This also solves the annoying problem that TGraphs behave differently from TH1s,
    especially regarding axis limits.

    The frame histogram is not created until the call to [compile], which first processes 
    all objects input with [add] to calculate things like automatic axis ranges, etc. Note
    that you normally don't have to call [compile] yourself, since it is called in [draw].
    However, sometimes it useful to create the frame histogram before drawing. For example,
    if you want to retrieve the axis limits before initiating the draw step. You can also 
    supply your own frame histogram by using the [_frame] option in [__init__].

    --------------------------------- Object Properties ---------------------------------
    These properties are empty initially and extended by calls to [add].

    @property objs : [TObject]
        Main list of ROOT objects which dictate algorithms like auto axis ranges and text 
        placement.
    @property draw_objs : [TObject]
        This is a superset of [objs] that may also contain things like TMarker added via
        [add_primitives]. The order of this list is the draw order of the objects (which
        is therefore also the z-ordering of the objects). Note that if you modify this
        list, make sure to also modify [draw_opts].
    @property draw_opts : [str]
        A list of plotting options in parallel with [draw_objs], passed to the ROOT 
        TObject.Draw() function.
    @property legend_items : [(TObject, str label, str draw_option)]
        A list of ROOT TLegend entry parameters, in the order they appear. You can modify 
        it manually, for example to add custom legend entries.

    -------------------------------- Compiled Properties --------------------------------
    These properties only exist after calling [compile].
    
    @property <x/y/z>_range : (float min, float max) or None
        The axis limits in user coordinates. These may be None, in which case default
        ROOT behavior is used (you will have to retrieve the ranges yourself via ROOT).
    @property frame : TH1F or TObject
        The frame histogram as mentioned above. Generally this will be a custom created
        TH1F, unless you pass a [_frame] to [__init__]. Also, if plotting a TH2 or one
        of the ranges above is None, will be the first object in [objs] instead.
    @property legends : [TLegend]
        A list of all the legends. Note that this class generates one TLegend per legend 
        entry to have fine-grained control over the entry placement.
    @property legend_<width/height/rows/columns>
    @property data_y_<min/max/pos> : float or None
        The min/max/min-positive value of the data in [objs].

    -------------------------------- Internal Properties --------------------------------
    @property text_<...>
    @property title_<...>
    @property _y_min_pad_<bot/top> : float
        The axis-units padding supplied by the user.
    @property _y_pad_<bot/top> : float
        A mutable member used to calculate the actual padding needed, which may be 
        increased from the minimum specified above.
    @property auto_y_<bot/top> : bool
        Whether the yrange is fixed or can be adjusted.

    '''

    def __init__(self, pad,
            objs=None,  
            y_pad=None, y_pad_bot=0.05, y_pad_top=0.05, 
            _do_draw=True, _frame=None,
            **kwargs
        ):
        '''
        See file docstring for [kwarg] options.

        @param _do_draw
            Skip draw if false. Only applies when [objs] is not None.
        @param _frame
            Supply a custom frame object.
        '''
        ### Initialize ###
        self.frame = _frame

        self.objs = []          
        self.draw_objs = []     
        self.draw_opts = []     
        self.legend_items = []  
        self.cache = []
        
        self.compiled = False   # If False, need to call compile()
        self.is_2d = False

        ### Pad ###
        self.pad = pad
        self._set_pad_properties(**kwargs)

        ### Titles ###
        self._set_text_properties(**kwargs)
        self._make_titles(**kwargs)

        ### Axis ###
        if y_pad is not None:
            self._y_min_pad_bot = y_pad
            self._y_min_pad_top = y_pad
        else:
            self._y_min_pad_bot = y_pad_bot
            self._y_min_pad_top = y_pad_top
        self._y_pad_bot = self._y_min_pad_bot 
        self._y_pad_top = self._y_min_pad_top

        ### Other ###
        self.args = kwargs # This is a cache of kwargs that we pass to [compile] and [draw] so that you can specify all the relevant args up front

        ### Draw ###
        # Shorcut: if objs is supplied to the constructor, draw immediately.
        if objs: 
            self.add(objs, **kwargs)
            self.compile(**kwargs)
            if _do_draw:
                self.draw()

    #####################################################################################
    ###                                 PAD AND FRAME                                 ###
    #####################################################################################

    def _set_frame_ranges(self):
        if self.x_range is not None:
            if 'TGraph' in self.frame.ClassName():
                self.frame.GetXaxis().SetLimits(*self.x_range)
            else:
                self.frame.GetXaxis().SetRangeUser(*self.x_range)
        if self.y_range is not None:
            self.frame.GetYaxis().SetRangeUser(*self.y_range)
        if self.z_range is not None:
            self.frame.GetZaxis().SetRangeUser(*self.z_range)

    def _create_frame(self, **kwargs):
        if self.x_range and self.y_range and not self.is_2d:
            if labels := kwargs.get('x_bin_labels'):
                for h in self.objs:
                    if 'TGraph' not in h.ClassName() and h.GetXaxis().GetNbins() == len(labels):
                        self.frame = h.Clone()
                        break
                else:
                    self.frame = ROOT.TH1F('h_frame', '', len(labels), *self.x_range)
                    self.frame.SetDirectory(0)

            else:
                self.frame = ROOT.TH1F('h_frame', '', 1, *self.x_range)
                self.frame.SetDirectory(0)
        else: 
            # use objs[0] as the frame to preserve default ROOT behavior 
            # Note Z axis settings MUST be applied on the histogram drawn with 'Z' option, don't clone!
            self.frame = self.objs[0]

    def _set_pad_properties(self, logx=None, logy=None, logz=None, left_margin=None, right_margin=None, bottom_margin=None, top_margin=None, **_):
        self.logy = logy
        self.pad.cd()
        if logx is not None: self.pad.SetLogx(logx)
        if logy is not None: self.pad.SetLogy(logy)
        if logz is not None: self.pad.SetLogz(logz)
        if bottom_margin is not None: self.pad.SetBottomMargin(bottom_margin)
        if top_margin is not None: self.pad.SetTopMargin(top_margin)
        if left_margin is not None: self.pad.SetLeftMargin(left_margin)
        if right_margin is None:
            self.auto_right_margin = True
        else:
            self.auto_right_margin = False
            self.pad.SetRightMargin(right_margin)

    def _auto_right_margin(self):
        '''
        This needs to be called after objects have been added, so we can test against
        the 'COLZ' option.
        '''
        if not self.auto_right_margin: return
        if not self.is_2d: return
        if not 'Z' in self.draw_opts[0]: return
        if self.frame.GetZaxis().GetTitle():
            self.pad.SetRightMargin(0.18)
        else:
            self.pad.SetRightMargin(0.15)

    def user_to_axes_x(self, x):
        return user_to_axes_x(self.pad, self.frame, x)
    def user_to_axes_y(self, y):
        return user_to_axes_y(self.pad, self.frame, y)
    def user_to_axes(self, x, y):
        return user_to_axes(self.pad, self.frame, (x, y))

    def user_to_pad(self, x, y):
        return user_to_pad(self.pad, self.frame, (x, y))

    def pad_to_axes_x(self, x):
        return pad_to_axes_x(self.pad, self.frame, x)
    def pad_to_axes_y(self, y):
        return pad_to_axes_y(self.pad, self.frame, y)
    def pad_to_axes_height(self, height):
        return pad_to_axes_height(self.pad, self.frame, height)
    def pad_to_axes(self, x, y):
        return pad_to_axes(self.pad, self.frame, (x, y))
    
    def axes_to_pad_x(self, x):
        return axes_to_pad_x(self.pad, self.frame, x)
    def axes_to_pad_y(self, y):
        return axes_to_pad_y(self.pad, self.frame, y)
 
    def reset_pad(self, pad):
        self.compiled = False
        self.pad = pad
        self._set_pad_properties(**self.args)
        self._set_text_properties(**self.args)
        self._make_titles(**self.args)

    #####################################################################################
    ###                                     RANGES                                    ###
    #####################################################################################

    def _auto_x_range(self, **kwargs):
        if self.is_2d: return kwargs.get('x_range')
        return _auto_x_range(objs=self.objs, **kwargs)

    def _get_padded_range(self, data_min, data_max, pad_bot, pad_top):
        '''
        Returns the user-coordinate range given the data min/max (also user coords) and 
        the amount of padding. Here the padding is given in canvas or axis units.
        '''
        data_height = 1.0 - pad_bot - pad_top
        diff = data_max - data_min
        out_min = data_min - pad_bot * diff / data_height
        out_max = data_max + pad_top * diff / data_height
        return out_min, out_max

    def _pad_y_range(self, y_min=None, y_max=None, **kwargs):
        '''
        If using auto axis limits, updates [self.y_range] with extra padding defined by
        [self._y_pad_bot/top]. Respects the threholds [y_min] and [y_max] which take
        priority. Also resets the limits on [self.frame].
        '''
        if self.is_2d: return None
        if not self.auto_y_bot and not self.auto_y_top: return 

        ### Data units ###
        data_min, data_max = self.y_range
        if data_min >= 0 and not self.pad.GetLogy(): 
            if y_min is None or y_min < 0: y_min = 0
            # Here we enforce that y_min >= 0 when the data is all positive

        ### Adjust for log ###
        if self.logy:
            data_min = np.log10(data_min)
            data_max = np.log10(data_max)
            if y_min is not None: 
                y_min = np.log10(y_min) if y_min > 0 else None
            if y_max is not None: 
                if y_max <= 0: warning(f'Plotter._pad_y_range() passed a negative y_max={y_max} but plot is in logy mode')
                y_max = np.log10(y_max) if y_max > 0 else None

        ### First pass padding ###
        pad_bot = self._y_pad_bot if self.auto_y_bot else 0
        pad_top = self._y_pad_top if self.auto_y_top else 0
        out_min, out_max = self._get_padded_range(data_min, data_max, pad_bot, pad_top)

        ### Apply constraints ###
        rerun = False
        if y_min is not None and out_min < y_min:
            data_min = y_min
            pad_bot = 0
            rerun = True
        if y_max is not None and out_max > y_max:
            data_max = y_max
            pad_top = 0
            rerun = True
        if rerun:
            out_min, out_max = self._get_padded_range(data_min, data_max, pad_bot, pad_top)        
        
        ### Undo log, fix ticks ###
        if self.logy:
            out_min = np.power(10, out_min)
            out_max = np.power(10, out_max)
        else:
            out_min, out_max = _fix_bad_yticks(out_min, out_max, pad_bot == 0, pad_top == 0, ydivs=kwargs.get('ydivs'))

        ### Output ###
        self.y_range = (out_min, out_max)
        if self.frame:
            self.frame.GetYaxis().SetRangeUser(*self.y_range)

    def _auto_y_range(self, y_range='auto', y_min=None, y_max=None, ignore_outliers_y=0, **_):
        '''
        This function 
            - parses [y_range] to determine the auto behavior
            - sets the members listed below
            - returns (min, max) to be used as the base y range. It does not do any
              padding, but does respect [y_min] and [y_max].

        @sets
            self.data_y_[min/max/pos]
            self.auto_y_[bot/top]
        '''
        self.data_y_min = None
        self.data_y_max = None
        self.data_y_pos = None
        self.auto_y_bot = False
        self.auto_y_top = False

        ### No auto range ###
        if y_range is None: return None
        if self.is_2d: 
            if y_range != 'auto': return y_range
            else: return None
        
        ### Set tracking members ###
        if y_range == 'auto': y_range = (None, None)
        self.auto_y_bot = y_range[0] is None
        self.auto_y_top = y_range[1] is None
        if not self.auto_y_bot and not self.auto_y_top: # short circuit
            return y_range

        ### Get data min/max ###
        self.data_y_min, self.data_y_pos, self.data_y_max = get_minmax_y(self.objs, x_range=self.x_range, ignore_outliers_y=ignore_outliers_y)
        if self.data_y_min is None or self.data_y_max is None or (self.data_y_pos is None and self.pad.GetLogy()): 
            self.auto_y_bot = False
            self.auto_y_top = False
            return None
        
        ### Output ###
        # No padding here! See _pad_y_range
        out_min = self.data_y_pos if self.pad.GetLogy() else self.data_y_min
        out_max = self.data_y_max

        if not self.auto_y_bot: 
            out_min = y_range[0]
        elif y_min is not None and out_min < y_min:
            out_min = y_min
            self.auto_y_bot = False

        if not self.auto_y_top: 
            out_max = y_range[1]
        elif y_max is not None and out_max > y_max:
            out_max = y_max
            self.auto_y_top = False

        return out_min, out_max
        
    def _auto_z_range(self, z_range=None, **kwargs):
        if z_range is None: return None
        if z_range[0] is not None and z_range[1] is not None: return z_range
        
        min_val = None
        max_val = None
        for obj in self.objs:
            if 'TH2' in obj.ClassName():
                for y in range(1, obj.GetNbinsY() + 1):
                    for x in range(1, obj.GetNbinsX() + 1):
                        v = obj.GetBinContent(x, y)
                        if v == 0: continue
                        if min_val is None or v < min_val: min_val = v
                        if max_val is None or v > max_val: max_val = v
        if z_range[0] is not None: min_val = z_range[0]
        if z_range[1] is not None: max_val = z_range[1]
        return (min_val, max_val)


    #####################################################################################
    ###                                MAIN PROCESSING                                ###
    #####################################################################################

    def add(self, objs, 
            opts='', pos=None, legend_pos=None,
            stack=False, reverse_legend_for_stack=True,  
            **kwargs):
        '''
        Adds a list of objects to the plotter.

        @param opts
            The ROOT drawing option for each object. Like the formatting options, this
            can be a single string, applied to each of [objs], a list in parallel with
            [objs], or a function that takes an index into [objs] and returns the string
            option.
        @param pos
            By default, objects from subsequent calls of [add] are plotted on top of 
            current objects. Set [pos] to an index in the list [draw_objs] to alter
            the z-order of the drawing.
        @param legend_pos
            Index of where to insert the legend entries for these [objs]. By default
            will append them to the end.
        @param stack
            If True, [objs] must be a list of TH1s that will be added into a stack. No
            other objects should be included.
        @param reverse_legend_for_stack
            By default, if [stack], the legend will be reversed, which matches the visual 
            order of the histograms in the plot. Supplying [legend_order] will override
            this option.
        @param kwargs
            Options for [_apply_common_opts] and [_get_legend_list].

        @modifies
            self.objs
            self.draw_objs
            self.draw_opts
            self.legend_items
        '''
        if not objs: return
        if not self.objs:
            self.is_2d = 'TH2' in objs[0].ClassName()
        
        ### Replace objs ###
        orig_objs = objs
        objs = list(objs)
        if stack:
            objs = _make_stack(objs)
        for i,obj in enumerate(objs):
            if obj.ClassName().startswith('TF'):
                objs[i] = obj.GetHistogram().Clone() 
                # the histogram is maintained by the TF1 and will be updated with parameter 
                # changes, so it must be cloned.

        ### Styles ###
        apply_common_root_styles(objs, **kwargs)

        ### Styles ###
        draw_opts = []
        for i,obj in enumerate(objs):
            draw_opts.append(_arg(opts, i))
            obj.__rxplot_draw_opt = draw_opts[-1] # this just sets a python attribute for convenience

            if draw_opts[i] == '' and orig_objs[i].ClassName().startswith('TF'):
                draw_opts[i] = 'C' # this is default draw option for TF1, but since we replace it with the hist, must manually set
            if (len(draw_opts) > 1 or self.draw_opts) and 'TH2' in objs[0].ClassName() and 'Z' in draw_opts[-1]:
                warning('plotter::add() 2D histograms plotted with "Z" option must be passed first in order for z-axis settings to work!')
            if 'E1' in draw_opts[-1] and ROOT.gStyle.GetEndErrorSize() == 0:
                warning("It looks like you're trying to draw a histogram with the 'E1' option, but the style is forcing the end caps to 0. Use ROOT.gStyle.SetEndErrorSize(4) to fix.")
                
        ### Legend ###
        if stack and 'legend_opts' not in kwargs:
            kwargs['legend_opts'] = 'F'
        legend_items = self._get_legend_list(objs, draw_opts, **kwargs)

        ### Plot stack in reverse order ###
        if stack: 
            objs.reverse()
            draw_opts.reverse()
            if reverse_legend_for_stack and 'legend_order' not in kwargs:
                legend_items.reverse()

        ### Output ###
        self.objs.extend(objs)
        if pos is not None:
            self.draw_objs[pos:pos] = objs
            self.draw_opts[pos:pos] = draw_opts
        else:
            self.draw_objs.extend(objs)
            self.draw_opts.extend(draw_opts)
        if legend_pos is not None:
            self.legend_items[legend_pos:legend_pos] = legend_items
        else:
            self.legend_items.extend(legend_items)

    def add_primitives(self, objs, opts='', pos=None, **kwargs):
        '''
        Similar to [add] but for ROOT primitives like TMarker or TBox. This function does
        not create legend entries, and the added objects do not participate in auto 
        ranging and text placement.

        @modifies
            self.draw_objs
            self.draw_opts
        '''
        draw_opts = [_arg(opts, i) for i in range(len(objs))]
        if pos is not None:
            self.draw_objs[pos:pos] = objs
            self.draw_opts[pos:pos] = draw_opts
        else:
            self.draw_objs.extend(objs)
            self.draw_opts.extend(draw_opts)
       
    def compile(self, **kwargs):
        '''
        This function should be called after all [add] calls. This will calculate ranges,
        make the legend, and place the text.

        TODO due to ROOT weirdness, calls to GetXsize() may break after saving the canvas. 
        So be careful when calling compile() again after saving the canvas. Can use 
        [reset_pad] though.

        https://root-forum.cern.ch/t/tlatex-getxsize-bug/57515
        '''
        self.compiled = True
        self.args.update(kwargs)

        ### Range parsing ###
        self.x_range = self._auto_x_range(**self.args)
        self.y_range = self._auto_y_range(**self.args)
        self.z_range = self._auto_z_range(**self.args)

        ### Frame ###
        if self.frame is None:
            self._create_frame(**self.args) # This needs x_range
        self._set_frame_ranges()
        _apply_frame_opts(self.frame, **self.args)
        self._auto_right_margin()
        _fix_axis_sizing(self.frame, self.pad, **self.args)

        ### Legend and Text ###
        # These are the actual text locations in pad coordinates. They have to wait until
        # the pad margins are finalized.
        self.text_left = self.pad.GetLeftMargin() + self.text_offset_left
        self.text_right = 1 - self.pad.GetRightMargin() - self.text_offset_right
        self.text_top = 1 - self.pad.GetTopMargin() - self.text_offset_top
        self.text_bottom = self.pad.GetBottomMargin() + self.text_offset_bottom

        self._make_legend(**self.args)
        self._auto_text_pos_and_pad(**self.args)
        self._place_text_from_textpos(self.text_pos)
        self._pad_y_range(**self.args)


    #####################################################################################
    ###                                    TITLES                                     ###
    #####################################################################################

    def _create_atlas_title(self):
        tex = ROOT.TLatex(0, 0, 'ATLAS')
        tex.SetNDC()
        tex.SetTextFont(72)
        tex.SetTextSize(self.title_size)
        tex.SetTextAlign(ROOT.kVAlignBottom + ROOT.kHAlignLeft)
        return tex

    def _create_title(self, y, title):
        '''
        Creates the title text and appends it to [self.title_lines]. Custom treament for the
        ATLAS logo.

        @param y
            Starting y to place the title line (i.e. the top of the text).
        @returns 
            The height of the added text.
        '''
        x = 0
        texts = []
        
        ### ATLAS logo ###
        if 'ATLAS' in title:
            atlas = self._create_atlas_title()
            texts.append([x, atlas])
            self.titles.append(atlas)
            x += atlas.GetXsize() + 0.01 # 0.115*696*c.GetWh()/(472*c.GetWw())
            height = atlas.GetYsize()
            title = title[len('ATLAS '):]
        
        ### Remaining title ###
        if title:
            tex = ROOT.TLatex(0, 0, title)
            tex.SetNDC()
            tex.SetTextFont(42)
            tex.SetTextSize(self.title_size)
            tex.SetTextAlign(ROOT.kVAlignBottom + ROOT.kHAlignLeft)
            texts.append([x, tex])
            self.titles.append(tex)
            height = tex.GetYsize()

        # Here we align bottom so the text has the same baseline, but then we need to add the height first
        y += height
        self.title_lines.append((y, texts))
        return y

    def _make_titles(self, title='ATLAS Internal', subtitle=None, **kwargs):
        '''
        Creates all title and subtitle text, and places them relative to their bounding
        box. All text is aligned bottom, i.e. the y coordinate is the baseline.

        @sets
            self.title_lines          
                List of lines, where each line is a pair (y, texts) and `texts` is a list
                of pairs (x, ROOT.TLatex). The x and y are offsets from the top-left of 
                the text bounding box, and are used to directly place the TLatex depending
                on its alignment. For example, when left-top aligned, the x-y refer to the 
                left edge and baseline.
            self.titles
                A flattened version of the above list, with just the TLatex objects.
            self.title_height
        '''
        self.title_lines = [] 
        self.titles = []
        y = 0 # running offset (downwards) from top-left of all text

        if title:
            y = self._create_title(y, title)
            y += self.text_spacing

        if subtitle is not None:
            if isinstance(subtitle, str):
                subtitle = [subtitle]
            for i,sub in enumerate(subtitle):
                if i > 0: y += self.text_spacing

                tex = ROOT.TLatex(0, 0, sub)
                tex.SetNDC()
                tex.SetTextFont(42)
                tex.SetTextSize(self.text_size)
                tex.SetTextAlign(ROOT.kVAlignTop + ROOT.kHAlignLeft)
                # We use top align here and add the full height of the text below. This 
                # ensures that the subtitle lines never overlap, but will make the baselineskip
                # between each line inconsistent. 
                
                self.title_lines.append([y, [[0, tex]]])
                self.titles.append(tex)
                y += get_tlatex_size(tex)[1]

        self.title_height = y
        self._format_titles()

    def _format_titles(self):
        for t in self.titles:
            if self.text_back_color is not None:
                pass #TODO

    def _get_line_width(self, line):
        '''
        @param line
            A list of (x, ROOT.TLatex) pairs. Assumes the entries are in left-to-right 
            order.
        '''
        x_start = line[0][0] # left edge of first text
        x_end = line[-1][0] + line[-1][1].GetXsize() # right edge of last text
        return x_end - x_start
    
    def _place_titles(self, x0, y0, align):
        '''
        Sets the x/y positions of the TLatex objects in self.titles

        @param x0 left or right edge of the texts, depending on [align]
        @param y0 top edge of the texts
        @param align either 'left' or 'right'
        '''
        for line in self.title_lines:
            y = y0 - line[0]
            line_width = self._get_line_width(line[1])
            for x_offset,tex in line[1]:
                if align == 'left':
                    x = x0 + x_offset
                else:
                    x = x0 - line_width + x_offset
                tex.SetX(x)
                tex.SetY(y)


    #####################################################################################
    ###                                    LEGEND                                     ###
    #####################################################################################

    def _default_legend_opt(self, plot_opt):
        '''
        Returns the default legend option given a plotting option.
        '''
        opt = ''
        if 'HIST' in plot_opt or 'L' in plot_opt or 'C' in plot_opt:
            opt += 'L'
        if 'P' in plot_opt: 
            opt += 'P'
        if 'E' in plot_opt:
            if not 'P' in opt and not 'L' in opt:
                opt += 'LE'
            else:
                opt += 'E'
        return opt or 'L'

    def _get_legend_list(self, objs, opts, legend='auto', legend_order=None, legend_opts=None, **_):
        '''
        Returns a list of (obj, label, opt).
        '''
        ### No legend ###
        if legend is None: return []

        ### Auto legend ###
        if legend == 'auto':
            if len(objs) < 2: return []
            legend = [x.GetName() for x in objs] # use list machinery below

        ### Custom legend ###
        if not isinstance(legend[0], str): return legend

        ### List of labels ###
        if len(legend) != len(objs):
            raise RuntimeError(f'Plotter._get_legend_list() mismatched lengths. Got {len(legend)}, expected {len(objs)}.')
        if legend_opts is None:
            legend_opts = lambda i: self._default_legend_opt(_arg(opts, i))

        out = []
        for i,(obj,label) in enumerate(zip(objs, legend)):
            out.append([obj, label, _arg(legend_opts, i)])

        ### Reorder ###
        if legend_order: 
            out = [out[i] for i in legend_order]
        out = [x for x in out if x[1] and x[2]] # filter empty labels/opts

        return out

    def _max_legend_label_width(self, items):
        '''
        Gets the maximum width of a legend label.

        @param items: A list of (_, label, _)
        '''
        _max = 0
        for _,label,_ in items:
            width = get_text_size(label, self.text_size)[0]
            if width > _max: _max = width
        return _max

    def _make_legend(self, legend_columns=1, legend_vertical_order=False, **_):
        '''
        Creates a ROOT.TLegend with entries from [self.legend_items]. Also measures the 
        legend sizing. Does not place the legend yet.

        @sets
            self.legends
            self.legend_width
            self.legend_height
            self.legend_rows
            self.legend_columns
        '''
        self.legends = []
        self.legend_height = 0
        self.legend_column_separation = 0.01
        if not self.legend_items:
            self.legend_rows = 0
            self.legend_columns = 0
            self.legend_width = 0
            self.legend_column_width = 0
            return
        
        ### Legend size ###
        # These are in pad units, i.e. fraction of pad width
        leg_symbol_width = 0.05 # Symbol size
        leg_symbol_pad = 0.01   # Whitespace between symbol and label
        leg_label_width = self._max_legend_label_width(self.legend_items)
        self.legend_columns = legend_columns
        self.legend_rows = math.ceil(len(self.legend_items) / legend_columns)
        self.legend_column_width = leg_symbol_width + leg_symbol_pad + leg_label_width
        self.legend_width = self.legend_column_width * legend_columns + self.legend_column_separation * (legend_columns - 1)
        
        ### Legend ###
        # We use a single ROOT.TLegend per entry to have better fine-grained control
        # on entry placement.
        for column in range(self.legend_columns):
            column_height = 0
            if legend_vertical_order:
                column_items = self.legend_items[column * self.legend_rows:(column + 1) * self.legend_rows]
            else:
                column_items = self.legend_items[column:len(self.legend_items):self.legend_columns]
            for i,entry in enumerate(column_items):
                legend = ROOT.TLegend()
                legend.SetFillColor(colors.transparent_white)
                legend.SetLineColor(0)
                legend.SetBorderSize(0)
                legend.SetMargin(leg_symbol_width / self.legend_column_width) # SetMargin expects the fractional width relative to the legend...cause that's intuitive
                legend.SetTextSize(self.text_size)
                legend.SetTextFont(42) # Default ATLAS font
                legend.AddEntry(*entry)
                legend.height = max(self.text_size, get_text_size(entry[1], self.text_size)[1]) # this merely sets a python attribute
                self.legends.append(legend)

                if i != 0:
                    column_height += self.text_spacing
                column_height += legend.height
            self.legend_height = max(self.legend_height, column_height)

    def _place_legend(self, x, y, align):
        '''
        @param y top edge of the legend
        @param x left or right edge of the legend, depending on [align]
        @param align either 'left' or 'right'
        '''
        if align == 'left':
            al = ROOT.kHAlignLeft
        else:
            al = ROOT.kHAlignRight
            x -= self.legend_width
        for column in range(self.legend_columns):
            start_x = x + (self.legend_column_width + self.legend_column_separation) * column
            current_y = y
            for legend in self.legends[column*self.legend_rows:(column+1)*self.legend_rows]:
                legend.SetTextAlign(al + ROOT.kVAlignCenter)
                legend.SetX1(start_x)
                legend.SetX2(start_x + self.legend_column_width)
                legend.SetY1(current_y - legend.height)
                legend.SetY2(current_y)
                current_y -= legend.height + self.text_spacing


    #####################################################################################
    ###                                    TEXTPOS                                    ###
    #####################################################################################

    def _set_text_properties(self,
            text_pos='auto', 
            title_size=0.05, text_size=0.035, text_spacing=1,     
            text_back_color=None,
            text_offset_left=0.05, text_offset_right=0.05, text_offset_top=0.05, text_offset_bottom=0.05,
            **_,
        ):
        '''
        All text sizes/positions are in pad units.

        @requires
            Pad margins should be set already.
        '''
        self.text_pos = text_pos
        self.text_back_color = text_back_color

        pad_height = self.pad.GetHNDC()
        self.title_size = title_size / pad_height
        self.text_size = text_size / pad_height
        self.text_spacing = text_size * text_spacing * 0.15

        self.text_offset_left = text_offset_left
        self.text_offset_right = text_offset_right
        self.text_offset_top = text_offset_top
        self.text_offset_bottom = text_offset_bottom

    def has_text(self):
        return bool(self.title_lines or self.legends)

    def _auto_text_pos_and_pad(self, **_):
        '''
        Finds the best 'text_pos' to not overlap text with the plot, and the y_pad_top
        needed.

        @requires
            Assumes self.frame has been set with yrange = data range to use the member
            coordinate conversion functions, and the titles and legend have been created.
        @sets
            self.text_pos
            self._y_pad_top

        Note this function will temporarily place the text items. Make sure to reset if 
        needed.
        '''
        ### No auto ###
        if self.is_2d: return
        if not self.has_text(): return
        # if self.data_y_max == self.data_y_min: return

        ### Test textpos list ###
        if self.text_pos == 'auto':
            test_pos = ['top', 'top reverse', 'topleft', 'topright'] # list of textpos options to test (in order of priority)
        elif isinstance(self.text_pos, str):
            test_pos = [self.text_pos]
        else:
            test_pos = self.text_pos
        for x in test_pos:
            if 'top' not in x:
                return warning(f'_auto_text_pos_and_pad() only implemented for top-aligned options only, not {x}')
            
        ### No auto ###
        if len(test_pos) == 1 and not self.auto_y_top: return
        
        ### Parse data ###
        occlusions = Occlusion() # in user coordiantes
        for obj,draw_opt in zip(self.objs, self.draw_opts):
            for entry in IterRoot(obj):
                x_low = self.user_to_axes_x(entry.x_low())
                x_high = self.user_to_axes_x(entry.x_high())
                y_low = self.user_to_axes_y(entry.y_low())
                y_high = self.user_to_axes_y(entry.y_high())
                occlusions.add(x_low, x_high, y_low, y_high)
                # if draw_opt != 'P' and ('TH1' in obj.ClassName() or 'TProfile' in obj.ClassName()):
                #     # All other plot options use the full width of the bin, so only 'P' is where
                #     # we don't check the x_low/x_high
                #     update_loc(entry.x_low(), entry.y_high())
                #     update_loc(entry.x_high(), entry.y_high())

        ### Test ###
        min_pad = None
        min_pad_pos = 'top'
        for text_pos in test_pos:
            self._place_text_from_textpos(text_pos)
            req_pad = self._get_required_top_padding(occlusions)
            if min_pad is None or req_pad < min_pad:
                min_pad = req_pad
                min_pad_pos = text_pos
                if min_pad < self._y_min_pad_top: break

        ### Set outputs ###
        self.text_pos = min_pad_pos
        self._y_pad_top = max(self._y_min_pad_top, min_pad)
                
    def _get_required_top_padding(self, data_occs : Occlusion, y_text_data_spacing=0.02):
        '''
        Helper function for [_auto_text_pos_and_pad].

        Returns the necessary top padding to ensure that no text elements overlap the 
        data. Text should be placed first.
        '''
        ### Get text locations ###
        occlusions = [] # (left, right, bottom, tex) in axes coordinates
        for tex in self.titles:
            size = get_tlatex_size(tex)
            v_align = tex.GetTextAlign() % 10
            
            ### Get y_bottom based on alignment ###
            y = tex.GetY() - y_text_data_spacing
            if v_align == ROOT.kVAlignTop:
                y -= size[1]
            elif v_align == ROOT.kVAlignCenter:
                y -= size[1] / 2

            occlusions.append((
                self.pad_to_axes_x(tex.GetX()),
                self.pad_to_axes_x(tex.GetX() + size[0]),
                self.pad_to_axes_y(y),
            ))
        if len(self.legends) > 0:
            for legend in self.legends:
                occlusions.append((
                    self.pad_to_axes_x(legend.GetX1()),
                    self.pad_to_axes_x(legend.GetX2()),
                    self.pad_to_axes_y(legend.GetY1() - y_text_data_spacing), 
                ))

        ### Iterate over data points ###
        max_pad = 0
        pad_bot = self._y_pad_bot if self.auto_y_bot else 0
        for r in data_occs.ranges:
            for left,right,bottom in occlusions:
                if r.overlaps_x(left, right) and r.y_max > bottom:
                    # y' = y (1 - pad_top - pad_bot) + pad_bot
                    # Set y' == bottom and solve for pad_top
                    pad_req = 1 - pad_bot - (bottom - pad_bot) / r.y_max
                    max_pad = max(max_pad, pad_req)
        return max_pad

    def _place_text_from_textpos(self, textpos):
        '''
        Parses [textpos] to determine the quadrant of the title text and legend.

        @sets
            self._title_hori_pos
            self._title_vert_pos
            self._legend_hori_pos
            self._legend_vert_pos
        '''
        if textpos == 'auto': # failed/skipped auto, default to topleft
            textpos = 'topleft'

        if 'left' in textpos:
            self._title_hori_pos = 'left'
            self._legend_hori_pos = 'left'
        elif 'right' in textpos:
            self._title_hori_pos = 'right'
            self._legend_hori_pos = 'right'
        elif 'reverse' in textpos:
            self._title_hori_pos = 'right'
            self._legend_hori_pos = 'left'
        else:
            self._title_hori_pos = 'left'
            self._legend_hori_pos = 'right'
            
        if 'top' in textpos:
            self._title_vert_pos = 'top'
            self._legend_vert_pos = 'top'
        elif 'bottom' in textpos:
            self._title_vert_pos = 'bottom'
            self._legend_vert_pos = 'bottom'
        elif 'forward diagonal' in textpos:
            if 'reverse' in textpos:
                self._title_vert_pos = 'top'
                self._legend_vert_pos = 'bottom'
            else:
                self._title_vert_pos = 'bottom'
                self._legend_vert_pos = 'top'
        else:
            if 'reverse' in textpos:
                self._title_vert_pos = 'bottom'
                self._legend_vert_pos = 'top'
            else:
                self._title_vert_pos = 'top'
                self._legend_vert_pos = 'bottom'

        self._place_titles_and_legend()

    def _place_titles_and_legend(self):
        '''
        Uses self._(title/legend)_(hori/vert)_pos to place the titles and legend. This
        sets the ROOT objects' coordinates.
        '''
        legend_with_title = self._title_hori_pos == self._legend_hori_pos and self._title_vert_pos == self._legend_vert_pos

        texts_pos = [0, 0, self._title_hori_pos]
        legend_pos = [0, 0, self._legend_hori_pos]
        if self._title_hori_pos == 'left':
            texts_pos[0] = self.text_left
        else:
            texts_pos[0] = self.text_right

        if self._legend_hori_pos == 'left':
            legend_pos[0] = self.text_left
        else:
            legend_pos[0] = self.text_right

        if self._title_vert_pos == 'top':
            texts_pos[1] = self.text_top
        elif legend_with_title:
            texts_pos[1] = self.text_bottom + self.title_height + 2 * self.text_spacing + self.legend_height
        else:
            texts_pos[1] = self.text_bottom + self.title_height

        if self._legend_vert_pos == 'bottom':
            legend_pos[1] = self.text_bottom + self.legend_height
        elif legend_with_title:
            legend_pos[1] = self.text_top - self.title_height - 2 * self.text_spacing
        else:
            legend_pos[1] = self.text_top

        self._place_titles(*texts_pos)
        self._place_legend(*legend_pos)

    #####################################################################################
    ###                                     DRAW                                      ###
    #####################################################################################

    def _draw_objs(self):
        for i,(obj,opt) in enumerate(zip(self.draw_objs, self.draw_opts)):
            if opt is None: continue
            opt = 'SAME ' + opt 

            ### Custom text format ###
            # It seems this is the only way to have differing formats per histograms
            # https://root-forum.cern.ch/t/draw-two-h2d-histograms-on-the-same-pad-as-text-but-in-different-formats/25234/2
            if 'TH2' in obj.ClassName() and 'TEXT:' in opt:
                ex = ROOT.TExec('ex', 'gStyle->SetPaintTextFormat("{}");'.format(opt.split(':')[1]))
                ex.Draw()
                self.cache.append(ex)
                opt = 'TEXT'

            ### Draw ###
            if opt == 'SAME ': opt = 'SAME' # very important that there's no extraneous space here (???)
            obj.Draw(opt)

            ### 2+ joint option ###
            if 'TGraph' in obj.ClassName() and '2+' in opt: # Specify 2+ to draw both error rectangles and bars
                obj.Draw(opt.replace('2+', ''))
    
    def _draw_all(self, _draw_frame=True, **kwargs):
        if _draw_frame:
            if 'TGraph' in self.frame.ClassName():
                self.frame.Draw('A')
            else:
                self.frame.Draw('AXIS')
        self._draw_objs()
        for tex in self.titles: tex.Draw()
        for legend in self.legends: 
            legend.Draw()

    def draw(self, **kwargs):
        self.pad.cd() # Make sure this is before _compile! So that textsizes are accurate.
        if not self.compiled:
            self.compile(**kwargs)
        self._draw_all(**self.args)
        self.pad.RedrawAxis()

    def draw_marker(self, x, y, axes_units=False):
        '''
        @param axes - If true x and y are in axes units, otherwise they are in user units
        '''
        self.pad.cd()
        if axes_units:
            x, y = self.axes_to_pad(x, y)
            m = ROOT.TMarker(x, y, ROOT.kFullSquare)
            m.SetNDC()
        else:
            m = ROOT.TMarker(x, y, ROOT.kFullSquare)
        m.Draw()
        self.cache.append(m)

    def draw_hline(self, y, style=ROOT.kSolid, width=2, color=ROOT.kBlack):
        '''
        Draws a horizontal line at [y] through the entire pad's x range. Should be called
        after [draw].
        '''
        if y is None: return
        if self.y_range:
            if y < self.y_range[0] or y > self.y_range[1]:
                return
        self.pad.cd()
        line = ROOT.TLine(self.x_range[0], y, self.x_range[1], y)
        line.SetLineStyle(style)
        line.SetLineColor(color)
        line.SetLineWidth(width)
        line.Draw()
        self.cache.append(line)

    def draw_vline(self, x, style=ROOT.kSolid, width=2, color=ROOT.kBlack):
        '''
        Draws a vertical line at [x] through the entire pad's y range. Should be called
        after [draw].
        '''
        if x is None: return
        y_range = self.y_range or (self.frame.GetMinimum(), self.frame.GetMaximum())
        self.pad.cd()
        line = ROOT.TLine(x, y_range[0], x, y_range[1])
        line.SetLineStyle(style)
        line.SetLineColor(color)
        line.SetLineWidth(width)
        line.Draw()
        self.cache.append(line)

    def draw_outliers(self):
        self.pad.cd()
        self.cache.append(_outliers(self.frame, self.objs))




##############################################################################
###                                 HELPERS                                ###
##############################################################################

### RANGES ###

def _minmax_x(obj):
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
    elif obj.ClassName().startswith('TF'):
        return None, None
    else: 
        raise RuntimeError('_minmax_x() unknown class ' + obj.ClassName())

def get_minmax_x(objs):
    x_min = None
    x_max = None
    for obj in objs:
        o_min, o_max = _minmax_x(obj)
        if o_min is None or o_max is None: continue
        if x_min is None or o_min < x_min: x_min = o_min
        if x_max is None or o_max > x_max: x_max = o_max
    return x_min, x_max    

def _auto_x_range(objs, x_range=(None, None), x_pad=None, x_pad_left=0, x_pad_right=0, **kwargs):
    '''
    Finds an automatic x-range given a list of plot objects.

    @returns The new x-range.
    '''
    if x_range is None: return None
    if x_range[0] is not None and x_range[1] is not None: return x_range

    if x_pad is not None:
        x_pad_left = x_pad
        x_pad_right = x_pad
    data_width = 1.0 - x_pad_left - x_pad_right
        
    x_min, x_max = get_minmax_x(objs)
    if x_min is None or x_max is None: return None

    if x_range[0] is not None: x_min = x_range[0]
    if x_range[1] is not None: x_max = x_range[1]
    
    diff = x_max - x_min
    if x_range[0] is None: x_min -= x_pad_left * diff / data_width
    if x_range[1] is None: x_max += x_pad_right * diff / data_width

    return (x_min, x_max)

def _minmax_y(obj, x_range=None, ignore_outliers_y=0, **kwargs):
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
        raise RuntimeError('_minmax_y() unknown class ' + obj.ClassName())

    ### First pass: get mean and std dev ###
    if ignore_outliers_y:
        mean = 0
        std = 0
        w_sum = 0
        for i in range(n):
            x,y,e = get(i)
            if x_range:
                if x < x_range[0] or x > x_range[1]: continue
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
        if x_range:
            if x < x_range[0] or x > x_range[1]: continue
        if ignore_outliers_y:
            if e != 0 and abs(y - mean) > ignore_outliers_y * std: continue

        if o_min is None or y < o_min: o_min = y
        if o_max is None or y > o_max: o_max = y
        if y > 0:
            if o_pos is None or y < o_pos: o_pos = y

    return (o_min, o_pos, o_max)

def get_minmax_y(objs, **kwargs):
    min_val = None
    min_pos = None
    max_val = None
    for obj in objs:
        if 'TF' in obj.ClassName(): continue
        min_obj, min_pos_obj, max_obj = _minmax_y(obj, **kwargs)
        if min_obj is None or max_obj is None: continue

        if min_val is None or min_obj < min_val: min_val = min_obj
        if max_val is None or max_obj > max_val: max_val = max_obj
        if min_pos_obj is not None:
            if min_pos is None or min_pos_obj < min_pos: min_pos = min_pos_obj

    if min_val is None:
        print(f"WARNING! get_minmax_y() min_val is None")
    if max_val is None:
        print(f"WARNING! get_minmax_y() max_val is None")
    
    return min_val, min_pos, max_val



### COMMON OPTS ###

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

def apply_common_root_styles(
        objs : list,
        linecolor='auto', 
        markercolor='auto', 
        fillcolor=None,
        **kwargs,
    ):
    '''
    Applies common ROOT styles for TAttLine, TAttMarker, and TAttFill to a list of
    objects.

    All of these options can be specified in multiple forms:
        - None: does nothing, and will keep the parameter already set in the object.
        - Single value: applied to all objects
        - List of values: must have length > len(objs), and will be applied elementwise
        - Function: takes a single input, the index into [objs], and returns the property
          value
    '''
    ### Auto color when colorless with the tableu color map ###
    if linecolor == 'auto':
        if len(objs) > 1 and fillcolor is None and np.all([o.GetLineColor() == ROOT.kBlack and o.GetFillColor() == 0 for o in objs]):
            linecolor = colors.tableu
        else:
            linecolor = None
    if markercolor == 'auto':
        if len(objs) > 1 and fillcolor is None and np.all([o.GetMarkerColor() == ROOT.kBlack and o.GetFillColor() == 0 for o in objs]):
            markercolor = colors.tableu
        else:
            markercolor = None
    
    ### Apply ###
    for i,obj in enumerate(objs):
        if linecolor is not None:
            obj.SetLineColor(_arg(linecolor, i))
        if 'linestyle' in kwargs:
            obj.SetLineStyle(_arg(kwargs['linestyle'], i))
        if 'linewidth' in kwargs:
            obj.SetLineWidth(_arg(kwargs['linewidth'], i))

        if 'markerstyle' in kwargs:
            obj.SetMarkerStyle(_arg(kwargs['markerstyle'], i))
        if markercolor is not None:
            obj.SetMarkerColor(_arg(markercolor, i))
        if 'markersize' in kwargs:
            obj.SetMarkerSize(_arg(kwargs['markersize'], i))

        if fillcolor is not None:
            obj.SetFillColor(_arg(fillcolor, i))
        if 'fillstyle' in kwargs:
            obj.SetFillStyle(_arg(kwargs['fillstyle'], i))

    if x := kwargs.get('ztitle'): # this needs to be applied to the histogram which was drawn with colz
        obj.GetZaxis().SetTitle(x)

def _apply_frame_opts(
        obj, 
        x_bin_labels : list[str]=None, 
        x_labels_option : str=None, 
        **kwargs,
    ):
    if 'xtitle' in kwargs:
        obj.GetXaxis().SetTitle(kwargs['xtitle'])
    if 'ytitle' in kwargs:
        obj.GetYaxis().SetTitle(kwargs['ytitle'])
    if 'ztitle' in kwargs:
        obj.GetZaxis().SetTitle(kwargs['ztitle'])

    if 'xdivs' in kwargs:
        obj.GetXaxis().SetNdivisions(kwargs['xdivs'], True)
    if 'ydivs' in kwargs:
        obj.GetYaxis().SetNdivisions(kwargs['ydivs'], True)
    if x := kwargs.get('zdivs'):
        obj.GetZaxis().SetNdivisions(x, True)

    if x_bin_labels is not None:
        for i,label in enumerate(x_bin_labels):
            obj.GetXaxis().SetBinLabel(i+1, label)
    if x_labels_option is not None:
        obj.GetXaxis().LabelsOption(x_labels_option)


### MISC ###

def _fix_axis_sizing(h, pad, 
        remove_x_labels=False, 
        text_size=0.05,
        title_offset_x=1.0,
        title_offset_y=1.4,
        title_offset_z=None,
        tick_length_x=0.015,
        tick_length_y=0.03,
        label_offset_x=0.005, 
        label_size_x=0.05, 
        **_
    ):
    '''
    Fixes various axes sizing issues when you have multiple pads, since ROOT sizes 
    things based on the pad size not the canvas size.
    '''
    height = pad.GetHNDC()

    if remove_x_labels:
        h.GetXaxis().SetLabelOffset(999)
        h.GetXaxis().SetLabelSize(0)
        h.GetXaxis().SetTitleSize(0)
    else:
        h.GetXaxis().SetLabelOffset(label_offset_x / height)
        h.GetXaxis().SetLabelSize(label_size_x / height)
        h.GetXaxis().SetTitleSize(text_size / height)
        h.GetXaxis().SetTitleOffset(title_offset_x)

    h.GetYaxis().SetLabelSize(text_size / height)
    h.GetYaxis().SetTitleSize(text_size / height)
    h.GetYaxis().SetTitleOffset(title_offset_y * height)

    h.GetZaxis().SetLabelSize(text_size / height)
    h.GetZaxis().SetTitleSize(text_size / height)
    if title_offset_z is not None: h.GetZaxis().SetTitleOffset(title_offset_z)

    height -= height * (pad.GetBottomMargin() + pad.GetTopMargin())
    h.GetXaxis().SetTickLength(tick_length_x / height) 
    h.GetYaxis().SetTickLength(tick_length_y / (1 - pad.GetTopMargin() - pad.GetBottomMargin())) 
    # See https://root-forum.cern.ch/t/inconsistent-tick-length/18563/9
    # The tick scale is affected by the margins: tick_length = pixel_size / ((pad2H - marginB - marginT) / pad2H * pad2W)
    # Note there seems to be a minimum tick length for the y axis...

def _fix_bad_yticks(y_min, y_max, bot_is_fixed, top_is_fixed, ydivs):
    '''
    When the number of ydivs is small, ROOT sometimes messes up the y axis ticks. 
    This function tries to fix this by just expanding the axis limits iteratively.
    '''
    if bot_is_fixed and top_is_fixed: return y_min, y_max
    if ydivs is not None and ydivs % 100 <= 5:
        for i in range(3): # try three times at most
            # This is the funciton ROOT seems to use for the ticks
            nbins = ctypes.c_int(0)
            bin_low = ctypes.c_double(0)
            bin_high = ctypes.c_double(0)
            bin_width = ctypes.c_double(0)
            ROOT.THLimitsFinder.Optimize(y_min, y_max, ydivs % 100, bin_low, bin_high, nbins, bin_width, '')
            #print(newrange, bin_low, bin_high, nbins, bin_width)

            # This seems to be when the ticks aren't optimized?
            need_fix = (nbins.value == 0 or y_min > bin_low.value or y_max < bin_high.value)
            if not need_fix: break
                
            diff = y_max - y_min
            if not bot_is_fixed: y_min -= diff * 0.1
            if not top_is_fixed: y_max += diff * 0.1
    return y_min, y_max

def _outliers(frame, hists):
    '''
    Draws outlier arrows for points that aren't in the yrange of the graph. 
    '''
    x_min = frame.GetXaxis().GetXmin()
    x_max = frame.GetXaxis().GetXmax()

    y_min = frame.GetMinimum() # user coordinates
    y_max = frame.GetMaximum()
    y_pad = (y_max - y_min) / 50

    markers = []
    for h in hists:
        if not('TH1' in h.ClassName() or 'TGraph' in h.ClassName() or 'TProfile' in h.ClassName()): continue
        for entry in IterRoot(h):
            x = entry.x()
            v = entry.y()
            if x < x_min or x > x_max: continue
            if v == 0 and entry.e() == 0: continue
            elif y_max is not None and v > y_max:
                m = ROOT.TMarker(x, y_max - y_pad, ROOT.kOpenTriangleUp)
            elif y_min is not None and v < y_min:
                m = ROOT.TMarker(x, y_min + y_pad, ROOT.kOpenTriangleDown)
            else: continue
            
            m.SetMarkerColor(h.GetLineColor())
            m.Draw()
            markers.append(m)

    return markers

def _make_stack(objs):
        '''
        Assumes objs is a list of TH1s, and adds them cumulatively to create a list
        of stack histograms insteads.
        '''
        new_objs = []
        for i,obj in enumerate(objs):
            obj = obj.Clone()
            if len(new_objs) > 0:
                obj.Add(new_objs[-1])
            new_objs.append(obj)
        return new_objs


### OCCLUSION ###

class Occlusion:
    '''
    This class represents a list of occlusions on a y-axis given an x-axis. For every x
    value in a range, it stores a min and max y value.

    The underlying representation includes two lists, one for ranges and one for points.
    The ranges array consists of non-overlapping ranges sorted by x-value.
    '''
    class Range:
        def __init__(self, x_min, x_max, y_min, y_max) -> None:
            self.x_min = x_min
            self.x_max = x_max
            self.y_min = y_min
            self.y_max = y_max
        
        def __lt__(self, other):
            if isinstance(other, Occlusion.Range):
                return self.x_min < other.x_min
            else:
                return self.x_min < other
            
        def __str__(self) -> str:
            return f'[{self.x_min:.2g},{self.x_max:.2g}] -> [{self.y_min:.2g},{self.y_max:.2g}]'
        
        def __repr__(self) -> str:
            return str(self)
            
        def split(self, other : Occlusion.Range):
            '''
            Splits [self] based on the addition of [other]. Note, does not split
            the remainder of [other] if [other] is wider.
            '''
            y_min = min(self.y_min, other.y_min)
            y_max = max(self.y_max, other.y_max)
            ### Split not necessary ###
            if other.y_min >= self.y_min and other.y_max <= self.y_max:
                return [self]
            ### Other does not overlap ###
            elif other.x_min >= self.x_max or other.x_max <= self.x_min:
                return [self]
            ### Other is internal ###
            elif other.x_min > self.x_min and other.x_max < self.x_max:
                return [
                    Occlusion.Range(self.x_min, other.x_min, self.y_min, self.y_max),
                    Occlusion.Range(other.x_min, other.x_max, y_min, y_max),
                    Occlusion.Range(other.x_max, self.x_max, self.y_min, self.y_max),
                ]
            ### Other is external ###
            elif other.x_min <= self.x_min and other.x_max >= self.x_max:
                return [Occlusion.Range(self.x_min, self.x_max, y_min, y_max)]
            ### Overlap other.right edge (includes other.left == self.left) ###
            elif other.x_max < self.x_max:
                return [
                    Occlusion.Range(self.x_min, other.x_max, y_min, y_max),
                    Occlusion.Range(other.x_max, self.x_max, self.y_min, self.y_max),
                ]
            ### Overlap other.left edge (includes other.right == self.right) ###
            elif other.x_min > self.x_min:
                return [
                    Occlusion.Range(self.x_min, other.x_min, self.y_min, self.y_max),
                    Occlusion.Range(other.x_min, self.x_max, y_min, y_max),
                ]
            else:
                raise RuntimeError('Occlusion.Range.split() How did we get here?')

        def overlaps_x(self, x_min, x_max):
            return (x_min >= self.x_min and x_min < self.x_max) or \
                (x_max > self.x_min and x_max <= self.x_max) or \
                (x_min <= self.x_min and x_max >= self.x_max)

    def __init__(self) -> None:
        self.ranges : list[Occlusion.Range] = [] 
        self.points = [] 

    def __str__(self):
        out = 'Occlusion:'
        for x in self.ranges:
            out += f'\n    {x}'
        return out

    def _find(self, r : Occlusion.Range):
        '''
        @returns i_min, i_max
            [i_min, i_max) is the range of indices into self.ranges that intersects with [r].
        '''
        if len(self.ranges) == 0:
            return (0, 0)
        i_min = bisect.bisect_left(self.ranges, r.x_min)
        if i_min > 0 and self.ranges[i_min - 1].x_max > r.x_min:
            i_min -= 1
        i_max = bisect.bisect_left(self.ranges, r.x_max)
        return i_min, i_max

    def add(self, x_min, x_max, y_min, y_max):
        r = Occlusion.Range(x_min, x_max, y_min, y_max)
        i_min, i_max = self._find(r)
        if i_min == len(self.ranges):
            self.ranges.append(r)
        elif i_min == i_max:
            self.ranges.insert(i_min, r)
        else:
            new_slice = []
            for i in range(i_min, i_max):
                new_slice.extend(self.ranges[i].split(r))
            self.ranges[i_min:i_max] = new_slice




##############################################################################
###                            PLOT COORDINATES                            ###
##############################################################################

'''
These functions convert coordinates between various coordinate systems:

1. User (Data)
    This is the actual data values. So for example if you are plotting a m(X) histogram 
    the x coordinates are in GeV and the y coordinates are in number of events.
2. Axes
    This ranges from (0,0) at the bottom-left of the axes to (1,1) at the top-right.
3. Pad (NDC)
    ROOT calls this NDC. It ranges from (0,0) at the bottom-left of the pad to (1,1) at
    the top-right.

The functions require you to pass a pad (a ROOT.TPad, which is inherited by ROOT.TCanvas)
and a frame histogram. The frame is usually the first histogram/graph plotted, and the
one that determines axis ranges and titles. This can be accessed from the [Plotter] class
with member `plotter.frame`.
'''

def user_to_axes_x(pad, frame, x):
    user_width = frame.GetXaxis().GetXmax() - frame.GetXaxis().GetXmin()
    return (x - frame.GetXaxis().GetXmin()) / user_width
def user_to_axes_y(pad, frame, y):
    if 'TH2' in frame.ClassName():
        fmin = frame.GetYaxis().GetXmin()
        fmax = frame.GetYaxis().GetXmax()
    else:
        fmin = frame.GetMinimum()
        fmax = frame.GetMaximum()
    if pad.GetLogy(): 
        if y <= 0: return 0
        y = np.log10(y)
        fmin = np.log10(fmin)
        fmax = np.log10(fmax)
    user_width = fmax - fmin
    return (y - fmin) / user_width
def user_to_axes(pad, frame, coord):
    return user_to_axes_x(pad, frame, coord[0]), user_to_axes_y(pad, frame, coord[1])

def axes_to_pad_x(pad, frame, x):
    pad_width = 1 - pad.GetLeftMargin() - pad.GetRightMargin()
    return x * pad_width + pad.GetLeftMargin()
def axes_to_pad_y(pad, frame, y):
    pad_height = 1 - pad.GetTopMargin() - pad.GetBottomMargin()
    return y * pad_height + pad.GetBottomMargin()
def axes_to_pad(pad, frame, coord):
    return axes_to_pad_x(pad, frame, coord[0]), axes_to_pad_y(pad, frame, coord[1])

def user_to_pad_x(pad, frame, x):
    return axes_to_pad_x(pad, frame, user_to_axes_x(frame, x))
def user_to_pad_y(pad, frame, y):
    return axes_to_pad_y(pad, frame, user_to_axes_y(frame, y))
def user_to_pad(pad, frame, coord):
    return user_to_pad_x(pad, frame, coord[0]), user_to_pad_y(pad, frame, coord[1])

def pad_to_axes_x(pad, frame, x):
    pad_width = 1 - pad.GetLeftMargin() - pad.GetRightMargin()
    return (x - pad.GetLeftMargin()) / pad_width
def pad_to_axes_y(pad, frame, y):
    pad_height = 1 - pad.GetTopMargin() - pad.GetBottomMargin()
    return (y - pad.GetBottomMargin()) / pad_height
def pad_to_axes_height(pad, frame, height):
    pad_height = 1 - pad.GetTopMargin() - pad.GetBottomMargin()
    return height / pad_height
def pad_to_axes(pad, frame, coord):
    return pad_to_axes_x(pad, frame, coord[0]), pad_to_axes_y(pad, frame, coord[1])


_x1 = ctypes.c_double(1.)
_x2 = ctypes.c_double(1.)
_y1 = ctypes.c_double(1.)
_y2 = ctypes.c_double(1.)

def get_text_size(text, text_size):
    '''
    Returns the (width, height) of [text] in NDC (canvas) units.

    NOTE that GetXsize() returns the size in user coordinates. The user coordinates are 
    [0, 1] on both axes by default. These then seem to be set to correspond with the 
    user units on the current axes, accounting for the proportionate padding/placement of 
    the axes (see TPad.GetRangeAxis). This happens when the canvas is PRINTED, not just 
    drawn on; in general happens when you call Update() I think.

    https://root.cern/manual/graphics/#coordinate-systems-of-a-pad
    '''
    ROOT.gPad.GetRange(_x1, _y1, _x2, _y2)
    tex = ROOT.TLatex(0, 0, text)
    tex.SetTextFont(42)
    tex.SetTextSize(text_size)
    return get_tlatex_size(tex)


def get_tlatex_size(tex):
    ROOT.gPad.GetRange(_x1, _y1, _x2, _y2)
    return tex.GetXsize() / (_x2.value - _x1.value), tex.GetYsize() / (_y2.value - _y1.value)



##############################################################################
###                               RATIO PADS                               ###
##############################################################################


class RatioPads:
    '''
    This class creates default pads for ratio plots. Prefer using [plot_ratio]
    for simple cases; this class is only needed if you need direct access to the
    [Plotter] before drawing the main objects.

    Workflow:

        ### Method 1 (object) ###
        pads = RatioPads()
        plotter1 = pads.make_plotter1(...)
        plotter1.add(...)
        plotter1.draw(...)
        # repeat for plotter2

        ### Method 2 (static) ###
        plotter1 = Plotter(pads.pad1, ..., **RatioPads.default_args1)
        plotter1.add(...)
        plotter1.draw(...)
        # repeat for plotter2
    '''
    def __init__(self, height1=0.7, canvas_size=(1000, 800), bottom_margin=0.12, **_):
        self.c = ROOT.TCanvas("c1", "c1", *canvas_size)
        self.c.SetFillColor(colors.transparent_white)

        ### Create pads ###
        height2 = 1 - height1

        self.pad1 = ROOT.TPad("pad1", "pad1", 0, height2, 1, 1)
        self.pad1.SetFillColor(colors.transparent_white)
        self.pad1.SetBottomMargin(0.03)
        self.pad1.Draw()

        self.c.cd()
        self.pad2 = ROOT.TPad("pad2", "pad2", 0, 0, 1, height2)
        self.pad2.SetFillColor(colors.transparent_white)
        self.pad2.SetBottomMargin(bottom_margin / height2)
        self.pad2.Draw()

    default_args1 = {
        'text_offset_bottom': 0.07,
        'remove_x_labels': True,
    }
    default_args2 = { 
        'ydivs': 504, 
        'ignore_outliers_y': 4, 
        'title_offset_x': 1.0, 
        'title': None, 
        'legend': None,
    }

    def make_plotter1(self, **kwargs):
        args = self.default_args1.copy()
        args.update(kwargs)
        return Plotter(self.pad1, **args)
    
    def make_plotter2(self, **kwargs):
        args = self.default_args2.copy()
        args.update(kwargs)
        return Plotter(self.pad2, **args)
    

##############################################################################
###                            CANVAS WRAPPERS                             ###
##############################################################################


def _plot(c, objs, **kwargs):
    return Plotter(c, objs=objs, **kwargs)


def plot(objs, canvas_size=(1000,800), canvas_name='c1', callback=None, filename=None, **kwargs):
    c = ROOT.TCanvas(canvas_name, canvas_name, *canvas_size)
    plotter = _plot(c, objs, **kwargs)
    if callback: 
        callback(plotter)
    save_canvas(c, filename or objs[0].GetName())


def _copy_ratio_args(plotter, args, postfix):
    '''
    Copies arguments for ratio plots. Arguments like 'ytitle2' are copied to 'ytitle',
    and common arguments like x-axis options are copied as-is.
    '''
    out = {}
    for k,v in args.items():
        if k[-1] == postfix: out[k[:-1]] = v
        elif k.startswith('x'): out[k] = v
        elif k.endswith('_x'): out[k] = v
        elif k in ['rightmargin', 'logx']: out[k] = v
    out['x_range'] = plotter.x_range
    return out


def plot_ratio(objs1, objs2, outlier_arrows=True, hline=None, hline2=None, callback=None, save_plot=True, **kwargs):
    '''
    Plots [hists1] in a main pad on top and [hists2] in a secondary pad below. The two 
    sets of objects should share the same x axis. Set options in the secondary pad by 
    postpending the kwargs with a '2'.

    @returns canvas, plotter1, plotter2

    @param hline
        Draws a horizontal line in the secondary pad. The value sets the y position in
        user coordinates. Set to None to omit. Can also be a dictionary of arguments
        to [plotter.draw_hline].
    @param hline2
        Alias to [hline]
    @param outlier_arrows
        Draws small triangles at the top/bottom of the ratio pad to indicate points that
        are outside of the plot range.
    @param callback
        A function (plotter1, plotter2) -> None called after everything else, useful to 
        access the plotters if this function is deeply nested. 
    @param save_plot
        Will save the file using kwargs['filename']. Set to false if you want to modify
        the plotters still, like to add extra markers.
    '''
    if hline is None:
        hline = hline2

    ### Create pads ###
    bottom_margin = kwargs.pop('bottom_margin', 0.12)
    pads = RatioPads(bottom_margin=bottom_margin, **kwargs)

    ### Draw main histo, get error histos
    plotter1 = pads.make_plotter1(objs=objs1, **kwargs)

    ### Draw ratio plot ###
    args2 = _copy_ratio_args(plotter1, kwargs, '2')
    plotter2 = pads.make_plotter2(objs=objs2, **args2)

    ### Draw y=1 line ###
    if hline is not None:
        if isinstance(hline, dict):
            plotter2.draw_hline(**hline)
        else:
            plotter2.draw_hline(hline, style=ROOT.kDashed)
        
    ### Draw out-of-bounds arrows ###
    if outlier_arrows: plotter2.draw_outliers()

    ### Callback ###
    if callback:
        callback(plotter1, plotter2)
    if save_plot:
        save_canvas(pads.c, kwargs.get('filename', objs1[0].GetName()))
    
    return pads.c, plotter1, plotter2


def plot_ratio3(objs1, objs2, objs3, height1=0.55, canvas_size=(1000, 800), outlier_arrows=True, hline2=None, hline3=None, callback=None, save_plot=True, **kwargs):
    '''
    A ratio plot with two ancillary pads. Plots [hists1] in a main pad on top and 
    [hists2] and [hists3] in the middle and bottom ancillary pads respectively. The 
    objects should all share the same x axis. Set options in the middle and bottom pad by
    post-pending the kwargs with a '2' or '3' respectively.

    @param hline2/3
        Draws a horizontal line in the middle/bottom pad. The value sets the y position 
        in user coordinates. Set to None to omit. 
    '''
    c = ROOT.TCanvas("c1", "c1", *canvas_size)
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
    kwargs.setdefault('text_offset_bottom', 0.07)
    kwargs.setdefault('remove_x_labels', True) 
    plotter1 = _plot(pad1, objs1, **kwargs)

    ### Draw first ratio plot ###
    args2 = { 
        'ydivs': 204, 
        'ignore_outliers_y': 3, 
        'title': None, 
        'legend': None, 
    }
    args2.update(_copy_ratio_args(plotter1, kwargs, '2'))
    plotter2 = _plot(pad2, objs2, **args2)

    ### Draw second ratio plot
    args3 = { 
        'ydivs': 204, 
        'ignore_outliers_y': 3, 
        'title': None, 
        'legend': None, 
    }
    args3.update(_copy_ratio_args(plotter1, kwargs, '3'))
    plotter3 = _plot(pad3, objs3, **args3)

    ### Draw hlines ###
    if hline2 is not None:
        if isinstance(hline2, dict):
            plotter2.draw_hline(**hline2)
        else:
            plotter2.draw_hline(hline2)
    if hline3 is not None:
        if isinstance(hline3, dict):
            plotter3.draw_hline(**hline3)
        else:
            plotter3.draw_hline(hline3)

    ### Draw out-of-bounds arrows ###
    if outlier_arrows:
        plotter2.draw_outliers()
        plotter3.draw_outliers()

    ### Callback ###
    if callback:
        callback(plotter1, plotter2, plotter3)
    if save_plot:
        save_canvas(c, kwargs.get('filename', objs1[0].GetName()))

    return c, plotter1, plotter2, plotter3


def plot_two_scale(objs1, objs2, canvas=None, **kwargs):
    '''
    Plots a graph with two y-axes sharing the same x-axis

    TODO auto legend
    '''
    c = canvas or ROOT.TCanvas('c1', 'c1', 1000, 800)

    ### Style
    ROOT.gStyle.SetPadTickY(0) # remove right tick marks
    kwargs.setdefault('rightmargin', 0.12)
    kwargs.setdefault('rightmargin2', kwargs.get('rightmargin', 0.12))
    if v := kwargs.get('ydatapad_top'): kwargs.setdefault('ydatapad_top2', v)
    kwargs.setdefault('xdivs', 506)

    ### Plot the left histograms
    c.SetFillColor(colors.transparent_white)
    cache = _plot(c, objs1, **kwargs)
    c.Update() # So that GetUymin works below

    ### Get args2
    args2 = _copy_ratio_args(kwargs, '2')

    ### Fix opts to plot 'SAME'
    opts2 = args2.pop('opts', '')
    if isinstance(opts2, str):
        opts2 = [opts2] * len(objs2)
    opts2[0] = 'SAME ' + opts2[0]

    ### Scale histograms to new yrange
    yrange2 = _auto_yrange(objs2, **args2)
    args2['yrange'] = yrange2
    scale = (c.GetUymax() - c.GetUymin()) / (yrange2[1] - yrange2[0])
    objs2 = [h.Clone() for h in objs2]
    for h in objs2:
        if 'TH' in h.ClassName():
            for i in range(h.GetNbinsX()):
                h.SetPointY(i, c.GetUymin() + (h.GetBinContent(i) - yrange2[0]) * scale)
        elif 'TGraph' in h.ClassName():
            for i in range(h.GetN()):
                h.SetPointY(i, c.GetUymin() + (h.GetPointY(i) - yrange2[0]) * scale)

    ### Plot the right histograms
    cache.append(_plot(c, objs2, opts=opts2, do_legend=False, **args2))

    ### Draw the second axis
    xmax = c.GetUxmax()
    if kwargs.get('logx'):
        xmax = (np.power(10, xmax))
    axis = ROOT.TGaxis(xmax, c.GetUymin(), xmax, c.GetUymax(), yrange2[0], yrange2[1], 510, '+L')
    axis.SetLabelFont(objs1[0].GetXaxis().GetLabelFont()) # 42
    axis.SetLabelSize(objs1[0].GetXaxis().GetLabelSize()) # 0.5
    axis.SetLabelColor(colors.red)
    axis.SetTitle(kwargs.get('ytitle2', ''))
    axis.SetTitleFont(objs1[0].GetXaxis().GetLabelFont()) # 42
    axis.SetTitleSize(objs1[0].GetXaxis().GetLabelSize()) # 0.5
    axis.SetTitleColor(colors.red)
    axis.SetLineColor(colors.red)
    axis.Draw()
    cache.append(axis)

    if not canvas:
        save_canvas(c, kwargs.get('filename', objs1[0].GetName()))
    return cache


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


def _draw_tier_line(h, y, i, linecolor=None, linewidth=None, x_range=None, **kwargs):
    cache = []
    color = _arg(linecolor, i) if linecolor else h.GetLineColor()
    width = _arg(linewidth, i) if linewidth else h.GetLineWidth()
    y_last = None
    for x in range(1, h.GetNbinsX() + 1):
        v = h.GetBinContent(x)
        x1 = h.GetXaxis().GetBinLowEdge(x)
        x2 = h.GetXaxis().GetBinLowEdge(x + 1)
        if x_range:
            if x1 < x_range[0]: continue
            if x2 > x_range[1]: continue

        y2 = y + v if v > 0 else y
        lines = []
        lines.append(ROOT.TLine(x1, y2, x2, y2))
        if y_last is not None: 
            lines.append(ROOT.TLine(x1, y_last, x1, y2))
        y_last = y2

        for l in lines:
            l.SetLineColor(color)
            l.SetLineWidth(width)
            l.Draw()
        cache.append(lines)
    return cache


def plot_tiered(
        hists, 
        tier_labels=None, 
        tier_title=None, 
        plot_style=None, 
        tier_spacing=0.1, 
        y_pad_top=0,
        logy=False, 
        callback=None, 
        **kwargs,
    ):
    '''
    Similar to a violin plot, this plots each histogram in its own equi-height y-bin.
    Negative values are supressed.

    @param hists
        A list of histograms with shape (#ybins, #series). The y-bins are listed from
        bottom to top. The series histograms in each ybin are normalized to each other.
    @param tier_labels
        The label of each tier, in matching order as `hists.shape[0]`.
    @param tier_title
        Horizontal title placed above the tier labels.
    @param plot_style
        How to draw the histograms. This can be
            - "fill": Filled boxes from 0. Default option if #series == 1.
            - "line": Similar to ROOT "hist" mode. Default option if #series > 1.
            - "point": Similar to ROOT "PE" mode. Not implemented yet.
    @param tier_spacing
        Empty space between each tier's plot elements, as a fraction of the total tier height.
    @param y_pad_top
        Empty space added to the top of the canvas, i.e. for text elements, as fraction of
        axes height.
    '''
    hists_flat = [x for y in hists for x in y]
    n_hists = len(hists_flat)
    n_tiers = len(hists)
    n_fake_tiers_total = round(n_tiers / (1 - y_pad_top))
    c = ROOT.TCanvas('c1', 'c1', 1000, 800)

    ### Handle some opts that are usually done in _plot ###
    yrange = kwargs.pop('y_range', None)
    kwargs.setdefault('legend_opts', 'L')
    if tier_labels is not None: 
        kwargs.setdefault('left_margin', 0.2)
        kwargs.setdefault('title_offset_y', 2)
    if legend := kwargs.get('legend'):
        if isinstance(legend[0], str):
            kwargs['legend'] = list(legend) + [''] * (n_hists - len(legend))
    else:
        kwargs['legend'] = None

    ### Create the frame ###
    axis = hists[0][0].GetXaxis()
    if axis.IsVariableBinSize():
        h_frame = ROOT.TH2F('tiers', '', axis.GetNbins(), axis.GetXbins().GetArray(), n_fake_tiers_total, 0, n_fake_tiers_total)
    else:
        h_frame = ROOT.TH2F('tiers', '', axis.GetNbins(), axis.GetXmin(), axis.GetXmax(), n_fake_tiers_total, 0, n_fake_tiers_total)
    h_frame.SetDirectory(0)
    h_frame.Draw('AXIS')

    ### Labels ###
    if tier_labels is not None:
        for y,label in enumerate(tier_labels):
            h_frame.GetYaxis().SetBinLabel(y + 1, label)
    
    ### Initialize plotter ###
    plotter = Plotter(
        pad=c,
        objs=hists_flat,
        y_range=(0, n_fake_tiers_total),
        _do_draw=False,
        _frame=h_frame,
        **kwargs,
    )
    h_frame.GetXaxis().SetRangeUser(*plotter.x_range)

    ### Draw histograms ###
    cache = [plotter]
    kwargs['x_range'] = plotter.x_range
    for y,series in enumerate(hists):
        # Normalize the histograms to the maximum value. In user coordinates, defined
        # by the frame histogram above, the max height of each y bin is just 1.
        _, min_pos, max_val = get_minmax_y(series, **kwargs)
        if not max_val: continue

        if logy:
            if yrange and yrange[0] is not None:
                min_pos = yrange[0]
            max_val = np.log(max_val) - np.log(min_pos)
            series = [log_hist(h, min_val=min_pos) for h in series]

        for i,h in enumerate(series):
            h.Scale((1 - tier_spacing) / max_val)
            if plot_style == 'fill' or plot_style is None and len(series) == 1:
                cache.append(_draw_tier_fill(h, y, i, **kwargs))
            elif plot_style == 'line' or plot_style is None and len(series) > 1:
                cache.append(_draw_tier_line(h, y, i, **kwargs))

    ### Draw hlines ###
    for y in range(1, n_tiers):
        plotter.draw_hline(y, width=1)

    ### Draw text and y-bin title ###
    for tex in plotter.titles: tex.Draw()
    for l in plotter.legends: l.Draw()
    if tier_title:
        c.SetTopMargin(0.06)
        tex = ROOT.TLatex(0, 0.95, tier_title)
        tex.SetTextFont(42)
        tex.SetTextSize(0.035)
        tex.SetNDC()
        width = tex.GetXsize()
        tex.SetX(max(0.05, c.GetLeftMargin() - width))
        tex.Draw()
    c.RedrawAxis()

    ### Callback ###
    if callback:
        callback(plotter)

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
        # xrange = _auto_xrange(hists1, **kwargs) # TODO
        xrange = None
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

    ### Adjust labels of x axis ###
    user_callback = kwargs.get('callback')
    def callback(*args):
        for i in range(bin_start + 1, bin_end + 2): # ticks are 1-indexed
            label = edge_labels[i - 1] if edge_labels else f'{h_check.GetBinLowEdge(i):.0f}'
            args[-1].frame.GetXaxis().ChangeLabel(i, 30, -1, -1, -1, -1, label)
        if user_callback:
            user_callback(*args)
    kwargs['callback'] = callback
    kwargs.setdefault('label_size_x', 0.03) # don't set this in ChangeLabel(), or else the labels get duplicated
    kwargs.setdefault('label_offset_x', 0.01) 

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
            elif 'TGraphAsymmErrors' in obj.ClassName():
                v = obj.GetPointY(bin_start + i)
                e_low = obj.GetErrorYlow(bin_start + i)
                e_high = obj.GetErrorYhigh(bin_start + i)
            else:
                raise NotImplementedError(f'plot_discrete_bins() class {obj.ClassName()}')
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
        return out

    hists1 = convert_objs(hists1)
    hists2 = convert_objs(hists2)
    hists3 = convert_objs(hists3)

    ### Fix args ###
    kwargs['xdivs'] = -nbins
    kwargs['x_range'] = (0, nbins)

    ### Plot ###
    pos_args = [hists1]
    if hists2: pos_args.append(hists2)
    if hists3: pos_args.append(hists3)
    plotter(*pos_args, **kwargs)



##############################################################################
###                                COLORS                                  ###
##############################################################################

def _wb(x, alpha):
    return x + (1 - x) * (1 - alpha)


def whiteblend(color, alpha):
    return ROOT.TColor(
        _wb(color.GetRed(), alpha), 
        _wb(color.GetGreen(), alpha), 
        _wb(color.GetBlue(), alpha)
    )


class colors:
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

    _tableu_40 = [ # Tableau but with 40% alpha, good for fill plots. 
        whiteblend(x, 0.4) for x in _tableu
        # Setting the alpha parameter in ROOT.TColor absolutely does not work...thanks ROOT
        # Manually calculate white blended version instead
    ]

    _pastel_base = _pastel[0].GetNumber()
    _tableu_base = _tableu[0].GetNumber()
    _tableu_40_base = _tableu_40[0].GetNumber()

    def pastel(i):
        return colors._pastel_base + i % len(colors._pastel)
    def tableu(i):
        return colors._tableu_base + i % len(colors._tableu)
    def tableu_40(i):
        return colors._tableu_40_base + i % len(colors._tableu_40)

    # list comprehensions are iffy inside a class scope
    # https://stackoverflow.com/questions/13905741/accessing-class-variables-from-a-list-comprehension-in-the-class-definition
    pastel_l = (lambda x=_pastel_base, y=_pastel: [x + i for i in range(len(y))])()
    tableu_l = (lambda x=_tableu_base, y=_tableu: [x + i for i in range(len(y))])()
    tableu_40_l = (lambda x=_tableu_40_base, y=_tableu_40: [x + i for i in range(len(y))])()

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
        colors.tableu_40_l,
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
            file_types = [t]
            filename = filename[:-len(t)-1]
            break
    
    ### Save for each filetype ###
    for t in file_types:
        if save_transparent_png and t == 'png':
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
    success('Wrote ' + filename + '.png')


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
###                          HISTOGRAM UTILITIES                           ###
##############################################################################

# Null pointer for string arguments. If you just pass a python 0 to the ROOT char*, I
# think it gets interpreted as '0' or something.
nullptr_char = ctypes.c_char_p(0)


def rebin(h, val=None, clone=True):
    '''
    Rebins a histogram [h] with a variety of modes based on [val].
    
    @param val
        - If a list, will return a new histogram with the supplied bins.
        - If a positive number, will modify [h] such that each bin has width [val], 
          assuming that [h] has equal width bins.
        - If a negative number, will merge |val| bins together
    @param clone
        When True, will always clone [h] first. When False, will use default ROOT
        behavior: 
            - When [val] is a list, a new histogram will be created always.
            - Other modes of [val] will modify [h] in-place.
    '''
    if clone:
        h = h.Clone()
    if val is None:
        return h
    elif isinstance(val, float) or isinstance(val, int):
        if val < 0:
            nbins = -val
        else:
            nbins = int(round(val / h.GetBinWidth(1)))
        if nbins > 1:
            return h.Rebin(nbins)
        else:
            return h
    else:
        if isinstance(val, list):
            val = np.array(val, dtype=float)
        return h.Rebin(len(val) - 1, h.GetName() + '_rebin', val)
    

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


def integral_user(h, user_range=None, use_width=False, return_error=False):
    '''
    Calculates the integral of [h] using a user-coordinate range instead of a bin range.

    @param range
        data values [min, max], exclusive upper end (MUST ALIGN WITH BINS).
        Can also be a string "min,max".
    @param use_width
        If true, multiply each bin content by the bin width.
    '''
    ### Parse string version ###
    if isinstance(user_range, str):
        user_range = [float(x) for x in user_range.split(',')]
        
    ### Get bin indices ###
    if user_range is None:
        y0 = 0
        y1 = -1
    else:
        y0 =  0 if user_range[0] is None else h.GetXaxis().FindFixBin(user_range[0])
        y1 = -1 if user_range[1] is None else h.GetXaxis().FindFixBin(user_range[1]) - 1
        if y1 >= 0 and y1 < y0:
            raise RuntimeError(f'integral_user() invalid range: {user_range}; found bins ({y0},{y1})')

    ### Integral ###
    option = 'width' if use_width else ''
    if return_error:
        import ctypes
        err = ctypes.c_double(1.)
        out = h.IntegralAndError(y0, y1, err, option)
        return out, err.value
    return h.Integral(y0, y1, option)


def undo_width_scaling(h):
    '''
    Given a histogram scaled by its bin width, i.e. via `h.Scale(1, 'width')`,
    undoes this scaling. Returns the same histogram, modified in-place.
    '''
    for i in range(len(h)):
        w = h.GetBinWidth(i)
        h.SetBinContent(i, h.GetBinContent(i) * w)
        h.SetBinError(i, h.GetBinError(i) * w)
    return h


def normalize(h, mode="integral"):
    '''
    Normalizes a histogram with multiple different modes. This function leaves the
    original histogram untouched. Always includes underflow/overflow bins.

    @param mode
        - "integral": Divides [h] by its integral.
        - "integral%": As above, but scales by 100.
        - "abs integral": Divides [h] by the sum of its |bin contents|.
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
            warning("plot.normalize() Integral is 0, doing nothing")
        elif '%' in mode:
            h.Scale(100 / integral)
        else:
            h.Scale(1 / integral)
    elif mode == "abs integral":
        tot = 0
        for i in range(0, h.GetNbinsX()+2): # TH1 bins are 1-indexed
            tot += abs(h.GetBinContent(i))
        if tot == 0:
            warning("plot.normalize() Integral is 0, doing nothing")
        else:
            h.Scale(1 / tot)
    elif mode == "cumulative":
        tot = h.Integral(0, -1)
        if tot == 0:
            warning("plot.normalize() Integral is 0, doing nothing")
        else:
            running_sum = 0
            for i in range(0, h.GetNbinsX() + 2): 
                running_sum += h.GetBinContent(i)
                h.SetBinContent(i, running_sum / tot)
                h.SetBinError(i, 0)
    elif mode == "cumulativer":
        tot = h.Integral(0, -1)
        if tot == 0:
            warning("plot.normalize() Integral is 0, doing nothing")
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
        if splitline: return "#splitline{Cumulative}{Fraction}"
        return "Cumulative Fraction of Events"
    else:
        return "Events"


def normalize_2d(h, mode):
    h = h.Clone()
    if 'integral' in mode:
        integral = h.Integral(0, -1, 0, -1)
        if integral == 0:
            warning("plot.normalize_2d() Integral is 0, doing nothing")
        elif '%' in mode:
            h.Scale(100 / integral)
        else:
            h.Scale(1 / integral)
    elif mode == 'y_bin':
        for y in range(0, h.GetNbinsY() + 2):
            sum_bin = 0
            for x in range(0, h.GetNbinsX() + 2):
                sum_bin += h.GetBinContent(x, y)
            if sum_bin <= 0: continue
            for x in range(0, h.GetNbinsX() + 2):
                h.SetBinContent(x, y, h.GetBinContent(x, y) / sum_bin)
                h.SetBinError(x, y, h.GetBinError(x, y) / sum_bin)
    return h
                

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
            if current_index > axis.GetNbins(): # Failsafe
                raise RuntimeError(f'get_bin_indexes() Unable to find fid bin edge {bin_edge}')
            current_index += 1

        ### Check to make sure the bin edges are aligned ###
        old_bin_edge = axis.GetBinLowEdge(current_index)
        if old_bin_edge != bin_edge:
            raise RuntimeError(f"get_bin_indexes() Bins don't align: requested={bin_edge}, found={old_bin_edge}")

        ### Save ###
        indexes.append(current_index)

    return indexes


def projectX(h, yrange, new_name=None):
    '''
    Projects a 2d histogram onto its x-axis using user (data) coordinates.

    @param yrange 
        Data values [min, max], exclusive upper end (MUST ALIGN WITH BINS).
        Can also be a string "min,max".
    '''
    if isinstance(yrange, str):
        yrange = [float(x) for x in yrange.split(',')]
    y0 = h.GetYaxis().FindFixBin(yrange[0])
    y1 = h.GetYaxis().FindFixBin(yrange[1]) - 1
    if y1 < y0:
        raise RuntimeError(f'projectX() invalid yrange: {yrange}')
    if new_name is None:
        base_name = f'{h.GetName()}_px{y0}-{y1}'
        new_name = base_name
        i = 1
        while ROOT.gDirectory.FindObject(new_name):
            new_name = base_name + '_' + str(i)
            i += 1
    return h.ProjectionX(new_name, y0, y1)


def projectY(h, xrange, new_name=None):
    '''
    Projects a 2d histogram onto its y-axis using user (data) coordinates.
    
    @param xrange 
        Data values [min, max], exclusive upper end (MUST ALIGN WITH BINS).
        Can also be a string "min,max".
    '''
    if isinstance(xrange, str):
        xrange = [float(x) for x in xrange.split(',')]
    x0 = h.GetXaxis().FindFixBin(xrange[0])
    x1 = h.GetXaxis().FindFixBin(xrange[1]) - 1
    if x1 < x0:
        raise RuntimeError(f'projectY() invalid xrange: {xrange}')
    if new_name is None:
        base_name = f'{h.GetName()}_py{x0}-{x1}'
        new_name = base_name
        i = 1
        while ROOT.gDirectory.FindObject(new_name):
            new_name = base_name + '_' + str(i)
            i += 1
    return h.ProjectionY(new_name, x0, x1)


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


class IterRoot:
    '''
    This class is a uniform iterator for ROOT TObjects. It is used simply like

        for entry in IterRoot(obj):
            # entry is the same IterRoot object
            print(entry.x(), entry.y())

    Each method accepts a [delta] arguement, which lets you access neighboring bins
    easily:

        diff = entry.y() - entry.y(-1)
    '''
    def __init__(self, obj):
        self.obj = obj
        self.i = -1
        if 'TH1' in obj.ClassName() or 'TProfile' in obj.ClassName():
            self.n = obj.GetNbinsX()
        elif 'TGraph' in obj.ClassName():
            self.n = obj.GetN()
        else:
            raise NotImplementedError('IterRoot() unknown class ' + obj.ClassName())
        
    def __iter__(self):
        self.i = -1
        return self

    def __next__(self):
        self.i += 1
        if self.i >= self.n:
            raise StopIteration
        return self
    
    def _get_i(self, delta):
        i = self.i + delta
        if i < 0 or i >= self.n:
            raise NotImplementedError(f'IterRoot._get_i() out of bounds: {i} (size: {self.n})')
        return i
    
    def x(self, delta=0):
        i = self._get_i(delta)
        if 'TH1' in self.obj.ClassName() or 'TProfile' in self.obj.ClassName():
            return self.obj.GetBinCenter(i + 1)
        elif 'TGraph' in self.obj.ClassName():
            return self.obj.GetPointX(i)
        else:
            raise NotImplementedError('IterRoot.x() unknown class ' + self.obj.ClassName())

    def y(self, delta=0):
        i = self._get_i(delta)
        if 'TH1' in self.obj.ClassName() or 'TProfile' in self.obj.ClassName():
            return self.obj.GetBinContent(i + 1)
        elif 'TGraph' in self.obj.ClassName():
            return self.obj.GetPointY(i)
        else:
            raise NotImplementedError('IterRoot.y() unknown class ' + self.obj.ClassName())
    
    def y_low(self, delta=0):
        i = self._get_i(delta)
        if 'TH1' in self.obj.ClassName() or 'TProfile' in self.obj.ClassName():
            return self.obj.GetBinContent(i + 1) - self.obj.GetBinError(i + 1)
        elif self.obj.ClassName() == 'TGraph':
            return self.obj.GetPointY(i)
        elif self.obj.ClassName() == 'TGraphErrors':
            return self.obj.GetPointY(i) - self.obj.GetErrorY(i)
        elif self.obj.ClassName() == 'TGraphAsymmErrors':
            return self.obj.GetPointY(i) - self.obj.GetErrorYlow(i)
        else:
            raise NotImplementedError('IterRoot.y_low() unknown class ' + self.obj.ClassName())

    def y_high(self, delta=0):
        i = self._get_i(delta)
        if 'TH1' in self.obj.ClassName() or 'TProfile' in self.obj.ClassName():
            return self.obj.GetBinContent(i + 1) + self.obj.GetBinError(i + 1)
        elif self.obj.ClassName() == 'TGraph':
            return self.obj.GetPointY(i)
        elif self.obj.ClassName() == 'TGraphErrors':
            return self.obj.GetPointY(i) + self.obj.GetErrorY(i)
        elif self.obj.ClassName() == 'TGraphAsymmErrors':
            return self.obj.GetPointY(i) + self.obj.GetErrorYhigh(i)
        else:
            raise NotImplementedError('IterRoot.y_high() unknown class ' + self.obj.ClassName())
        
    def e(self, delta=0):
        '''Average error in case of TGraphAsymmErrors'''
        i = self._get_i(delta)
        if 'TH1' in self.obj.ClassName() or 'TProfile' in self.obj.ClassName():
            return self.obj.GetBinError(i + 1)
        elif 'TGraph' == self.obj.ClassName():
            return 0
        elif 'TGraphErrors' == self.obj.ClassName() or 'TGraphAsymmErrors' == self.obj.ClassName():
            return self.obj.GetErrorY(i)
        else:
            raise NotImplementedError('IterRoot.e() unknown class ' + self.obj.ClassName())

    def x_low(self, delta=0):
        i = self._get_i(delta)
        if 'TH1' in self.obj.ClassName() or 'TProfile' in self.obj.ClassName():
            return self.obj.GetBinLowEdge(i + 1)
        elif self.obj.ClassName() == 'TGraph':
            return self.obj.GetPointX(i)
        elif self.obj.ClassName() == 'TGraphErrors':
            return self.obj.GetPointX(i) - self.obj.GetErrorX(i)
        elif self.obj.ClassName() == 'TGraphAsymmErrors':
            return self.obj.GetPointX(i) - self.obj.GetErrorXlow(i)
        else:
            raise NotImplementedError('IterRoot.x_low() unknown class ' + self.obj.ClassName())
    
    def x_high(self, delta=0):
        i = self._get_i(delta)
        if 'TH1' in self.obj.ClassName() or 'TProfile' in self.obj.ClassName():
            return self.obj.GetBinLowEdge(i + 2)
        elif self.obj.ClassName() == 'TGraph':
            return self.obj.GetPointX(i)
        elif self.obj.ClassName() == 'TGraphErrors':
            return self.obj.GetPointX(i) + self.obj.GetErrorX(i)
        elif self.obj.ClassName() == 'TGraphAsymmErrors':
            return self.obj.GetPointX(i) + self.obj.GetErrorXhigh(i)
        else:
            raise NotImplementedError('IterRoot.x_high() unknown class ' + self.obj.ClassName())

    def set_y(self, value, delta=0):
        i = self._get_i(delta)
        if 'TH1' in self.obj.ClassName() or 'TProfile' in self.obj.ClassName():
            self.obj.SetBinContent(i + 1, value)
        elif 'TGraph' in self.obj.ClassName():
            self.obj.SetPointY(i, value)
        else:
            raise RuntimeError('IterRoot() unknown class ' + self.obj.ClassName())
        
    def set_e(self, value, delta=0):
        '''
        Sets both up and down y-errors
        '''
        i = self._get_i(delta)
        if 'TH1' in self.obj.ClassName() or 'TProfile' in self.obj.ClassName():
            self.obj.SetBinError(i + 1, value)
        elif 'TGraph' == self.obj.ClassName():
            return
        elif 'TGraphErrors' == self.obj.ClassName():
            ex = self.obj.GetErrorX(i)
            self.obj.SetPointError(i, ex, value)
        elif 'TGraphAsymmErrors' == self.obj.ClassName():
            self.obj.SetPointEYlow(i, value)
            self.obj.SetPointEYhigh(i, value)
        else:
            raise RuntimeError('IterRoot() unknown class ' + self.obj.ClassName())


##############################################################################
###                                LOGGING                                 ###
##############################################################################

def notice(x):
    '''Prints a blue message to the terminal.'''
    print('\033[36m' + x + '\033[0m')


def success(x):
    '''Prints a green message to the terminal.'''
    print('\033[92m' + x + '\033[0m')


def warning(x):
    '''Prints a yellow warning message to the terminal.'''
    print('\033[93mWARNING ' + x + '\033[0m')


def error(x):
    '''Prints a red error message to the terminal.'''
    print('\033[91mERROR ' + x + '\033[0m')


class StreamRedirect:
    # https://stackoverflow.com/questions/24277488/in-python-how-to-capture-the-stdout-from-a-c-shared-library-to-a-variable
    def __init__(self, target, stream, target_open_mode):
        self.target = target
        self.stream_fd = stream.fileno()
        self.target_open_mode = target_open_mode
    
    def __enter__(self):
        self.stream_dup = os.dup(self.stream_fd)
        self.target_file = open(self.target, self.target_open_mode)
        os.dup2(self.target_file.fileno(), self.stream_fd)
    
    def __exit__(self, type, value, traceback):
        os.dup2(self.stream_dup, self.stream_fd)
        os.close(self.stream_dup)
        self.target_file.close()


def redirect(target=os.devnull, stream=sys.stdout, target_open_mode='w'):
    '''
    Redirects printouts to [stream] towards [target] instead. Use as

        with redirect('log.txt'):
            do_stuff()
    '''
    return StreamRedirect(target, stream, target_open_mode)

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


