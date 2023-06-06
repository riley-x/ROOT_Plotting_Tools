
Riley's declarative ROOT plotting toolkit. Instead of manually adjusting each histogram,
you can specify style in aggregate. Typical usage would look like:

```py
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
```

The input also doesn't have to be all histograms, you can include TF1s and TGraphs too.
In addition, this script takes care of several things missing in ROOT: automatic axis
ranges, easier legend placement, title text and subtext, etc. It also defines helper
functions to make some common plot types, like ratio plots. A full list of top-level
functions is shown below, along with a list of common options they accept.

The `colors` class defines many useful colors and some Matplotlib colormaps, which can be
accessed easily as `plot.colors.tableu(0)`. See the docstring for the class for more info.

The format of the saved image is inferred by ROOT based on the extension in the filename.
If the extension is omitted, the canvas will be saved for each extension listed in
`plot.file_formats`. This is convenient to save a plot as both a pdf and a png, for
example.


## Top-level Plotting Functions
Most of these functions expect one or more lists of TObjects as the graph inputs, and
accept a variety of common options listed below. See the individual docstring for more
info.

* `plot`   
    The basic go-to plotting function. Plots everything onto the same axis.
* `plot_ratio`  
    Plots a ratio plot; a main plot is shown on top with a separate, smaller plot shown
    on bottom. This function doesn't calcualte any actual ratios, you pass it instead two
    lists of TObjects.
* `plot_ratio3`
    Similar to `plot_ratio` but with two subplots beneath a main plot.
* `plot_two_scale`
    Plots two y-axes on a shared x-axis. TODO might be a bit outdated.
* `plot_tiered`
    Similar to a violin plot. Plots each input histogram at separated y-values. Useful
    for eye-balling differences between many different distributions, which would get
    crowded on a standard plot.
* `_plot`
    The underlying plotting function used by everything above. Basically the same as
    `plot` but you need to pass it a TPad. Useful for creating custom images containing
    multiple canvases.



## Common Plotting Options

### Basic Style

All of these options can be specified as a single value to apply to all input TObjects, a
list of values matching each input TObject, or a function that takes the index into the
list of TObjects.

* `opts`. 
    Options to TObject::Draw(), such as 'HIST' or 'PE'. Note that you don't need to
    specify 'SAME' or 'A', unless you're calling _plot on the same pad more than once.
    For TH2s, you can also input things like 'TEXT:4.2f' to specify a printf formatter
    when drawing with 'TEXT'.
* `linecolor`, `linestyle`, `linewidth`
    Sets the corresponding TAttLine properties. See the ROOT documentation for input
    values.
* `markercolor`, `markerstyle`, `markersize`
    Sets the corresponding TAttMarker properties. See the ROOT documentation for input
    values.
* `fillcolor`, `fillstyle`
    Sets the corresponding TAttFill properties. See the ROOT documentation for input
    values.

### Text and File Names
* `filename`
    Path to save the image to. If the filename ends with an extension like '.png', the
    file will be saved in that format. If no extension is given, saves the file with
    each extension in [plot.file_formats].
* `textpos`                                                  
    Location of title / legend. Can be a combination of [top/bottom] and/or [left/right],
    so for example 'top' will place the title in the top-left corner and the legend in
    the top-right, while 'top left' will place both in the top-left corner. You can also
    specify 'forward diagonal' or 'backward diagonal' to place the title and legend in
    diagonally opposite corners. You can add 'reverse' to some of these to reverse the
    title and legend positions. Default: 'top left'.
* `title`                                                   
    A string that appears after the ATLAS logo. Set to None to omit the logo entirely.
* `subtitle`
    Additional text that is displayed below the ATLAS logo. This can be a string or a
    list of strings, with the latter putting each entry on a new line. Default: 'Internal'.
* `titlesize`                                              
    ROOT text size for the title. Default: 0.05.
    WARNING ROOT has a bug with measuring text that isn't at some golden sizes. It seems
    0.05 and 0.035 work well. This may cause right aligning to be broken; it seems the
    longer the text the more off it'll be.
* `titlespacing`                                           
    Multiplicative factor for increasing the spacing between title/subtitle/legend. Default: 1.0.

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
