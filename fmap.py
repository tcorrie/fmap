# Version 3.0.0 by Tim Corrie

# This module is a wrapper for cartopy to save space in the main code, using matplotlib as well.
# It is necessary to run any notebooks where it's called without significant modification of code, specifically spatial plots.
# It is a WIP and may be updated at any time.
# Last updated: 04/02/2024
# See end for changelog


import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.ticker import FuncFormatter as FF
import matplotlib as mpl


# isiterable: Determines if passed object can be iterated.
def isiterable(obj):
    # obj: Any object/datatype.
    try:
        iter(obj)
        if True:
            return True
    except TypeError:
        return False

# axes_2d: takes an axs object and transforms it into a 2d array if necessary.
def axes_2d(axs, rows, cols):
    # axs: axs object created in make_plots function (see below)
    # rows: number of rows specified in the grid
    # cols: number of columns specified in the grid
    if rows == 1 and cols == 1:
        return np.array([[axs]])
    elif rows > 1 and cols == 1:
        return np.array([axs]).transpose()
    elif rows == 1 and cols > 1:
        return np.array([axs])
    else:
        return axs


# make_plots: Creates a plot with one subaxis (i.e. one figure). Returns fig, ax pair.
def make_plots(bounds, rows, cols, figtitle="", titlesize=18, adjusty=1.0, hpad=0, wpad=0):
    # bounds: The west, east, north, and south coordinates of the map boundaries, respectively. Required parameter. Careful that the data you're working with may have different reference coordinates.
    # rows: number of rows in the figure. Required parameter.
    # cols: number of columns in the figure. Required parameter.
    # figtitle: Give this plot a name. Default is blank but can be added later.
    # titlesize: Size of plot title. Default is 18.
    # adjusty: move the title up and down. Default is 1.0 (standard).
    # hpad: How much space to put between the rows (negative brings them closer together). Default is 0 (no change).
    # wpad: How much space to put between the columns (negative brings them closer together). Default is 0 (no change).
    # Note: To disable tight_layout, just set the hpad and wpad parameter to a ridiculosly high number. Sometimes multi-panel plots look better without tight_layout.

    fig, axs = plt.subplots(rows, cols, subplot_kw=dict(projection=ccrs.PlateCarree()), figsize=(8*cols, 8*rows+2))
    axs = axes_2d(axs, rows, cols)
    for i in range(axs.size):
        ax = axs[i // cols, i % cols]
        ax.set_extent([bounds[0], bounds[1], bounds[3], bounds[2]])
        ax.add_feature(cfeature.STATES, edgecolor="black", zorder=100)
        ax.add_feature(cfeature.BORDERS, edgecolor="black", zorder=99)
    fig.suptitle(figtitle, fontsize=titlesize, y=adjusty)
    if rows >= 2:
        fig.tight_layout(h_pad=hpad)
    if cols >= 2:
        fig.tight_layout(w_pad=wpad)
    return fig, axs


# axes_labels: Update the axes labels with coordinate information.
def axes_labels(fig, axs, bounds, lonspacing, latspacing, label_size=10, order='latin'):
    # fig: Overall figure object. Required parameter.
    # axs: 2d array of axs (see axes_2d and make_plots for the creation). Required parameter.
    # bounds: The west, east, north, and south coordinates of the map boundaries, respectively. Required parameter. Ideally this is the same as in the make_plots.
    # lonspacing: The spacing interval of longitude ticks labeled. Required parameter.
    # latspacing: The spacing interval of latitude ticks labeled. Required parameter.
    # label_size: Size of the labels. Default is 10.
    # order: Order in which labels are created. Default is 'latin' (by row), but 'asian' is available (by column).

    # lon_formatter (lat_formatter): Formats the longitude (latidude) to exclude negative signs. No observed way around it.
    # parameters: x (y), pos. x (y) is each longitude (latitude) tick, and pos is the position of each.
    # Note no parameters are passed when these are called.
    def lon_formatter(x, pos):
        if x % 180 == 0:
            return '{}°'.format(abs(x))
        elif x < 0:
            return '{}°W'.format(abs(x))
        elif x > 0:
            return '{}°E'.format(abs(x))

    def lat_formatter(y, pos):
        if y < 0:
            return '{}°S'.format(abs(y))
        elif y > 0:
            return '{}°N'.format(abs(y))
        elif y == 0:
            return '{}°'.format(abs(y))

    rows = axs.shape[0]
    cols = axs.shape[1]
    for i in range(axs.size):
        if order == 'latin':
            ax = axs[i // cols, i % cols]
        elif order == 'asian':
            ax = axs[i % rows, i // rows]
        xticks = np.arange(bounds[0], bounds[1]+1, lonspacing)
        yticks = np.arange(bounds[3], bounds[2]+1, latspacing)
        ax.set_xticks(xticks, crs=ccrs.PlateCarree())
        ax.set_yticks(yticks, crs=ccrs.PlateCarree())
        ax.set_xticklabels(xticks, fontsize=label_size)
        ax.set_yticklabels(yticks, fontsize=label_size)
        ax.xaxis.set_major_formatter(FF(lon_formatter))
        ax.yaxis.set_major_formatter(FF(lat_formatter))


def plot_var(fig, axis, varnames, style, cmap='rainbow', colors='black', normalization=False, prange=np.arange(0, 1.1, 0.1), alpha=0.8, crange=np.arange(0, 1.1, 0.1), extend='neither'):
    # fig: Figure to plot to. Required parameter.
    # axis: Axis to plot to. Required parameter.
    # varnames: Variable names to plot. Requires x, y, and z variables as a 1-D list of 3 variables (e.g. [longitude, latitude, field]). Required parameter.
    # style: Either 'contour' or 'contourf'. Required parameter.
    # cmap: For contourf, sets the color scheme. Default is 'rainbow'.
    # colors: For countor, sets the contour colors. Default is 'black'.
    # normalization: Determines if the colorbar should be normalized to better represent the data scale. Default is False.
    # prange: Range used for contourf. Default is 0 to 1 in 0.1 intervals.
    # alpha: Opacity of the contourf levels. Default is 0.8.
    # crange: Range used for contour. Default is 0 to 1 in 0.1 intervals.
    # cbar_include: Include colorbar in the plot. Default is False.
    # extend: extend the range past the given bounds. Default is neither, can be set to 'min', 'max', or 'both'.

    if isiterable(axis):
        raise TypeError('axis must be a single instance, not an iterable')
    else:
        if style == "contourf":
            varplot = axis.contourf(
                varnames[0], varnames[1], varnames[2], prange,
                norm=mpl.colors.LogNorm(vmin=prange[0], vmax=prange[-1]) if normalization else None,
                cmap=cmap, alpha=alpha, transform=ccrs.PlateCarree(), extend=extend)
        elif style == "contour":
            varplot = axis.contour(varnames[0], varnames[1], varnames[2], crange, colors=colors)
    return varplot


# make_colorbar: If contourf is plotted, this will add a colorbar.
def make_colorbar(fig, axis, varplot, prec, cbar_orient, ticks, hide=1, cbar_axes=None, label='', shrink=1.0, pad=0.1, ticksize=10, ticklabelsize=14, labelsize=18):
    # fig: Figure to plot to. Required parameter.
    # axis: Axis to plot to. Required parameter.
    # varplot: The contourf map created with plot_var. Required parameter.
    # prec: How to format the tick labels in the colorbar or contour labels in contour. Required parameter. 
    #     Options are:
    #         'precision, x' (uses np.round),
    #         'int' (uses .astype(int)),
    #         'strings' (use this if your tick labels are non-numerical.)
    #     Note: there may be more options in future versions.
    # cbar_orient: Orientation of the colorbar. Options are 'horizontal' or 'vertical'. Required parameter.
    # ticks: Ticks to show. Required parameter.
    # hide: Hides all ticks except the first and every nth after. Default is 1, which shows all of them.
    # cbar_axes: Axis for which the colorbar applies to. Default is None, which defaults to the axis being plotted, but is recommended to be passed axis/axes.
    # label: label to give the colorbar. Default is blank, although it's generally a good idea to pass this.
    # shrink: Shrinks the colorbar by a given multiplication factor. Default is 1.0 (no shrink).
    # pad: Adjusts the position of the colorbar's y-position relative to the plot. Default is 0.1.
    # ticksize: Size of the actual ticks. Default is 10.
    # ticklabelsize: Size of the tick labels. Default is 14.
    # labelsize: Size of the colorbar label. Default is 18.

    cbar = fig.colorbar(varplot, orientation=cbar_orient, ax=cbar_axes, shrink=shrink, pad=pad)
    cbar.set_label(label, fontsize=labelsize)
    cbar.set_ticks(ticks)
    if 'precision' in prec:
        int_round = int([p.lstrip().rstrip() for p in prec.split(',')][1])
        cbar.set_ticklabels(np.around(ticks, int_round))
    elif 'int' in prec:
        cbar.set_ticklabels(ticks.astype(int))
    else:
        cbar.set_ticklabels(ticks)
    cbar.ax.tick_params(labelsize=ticklabelsize, size=ticksize)
    for ct, tick in enumerate(cbar.ax.xaxis.get_ticklabels()):
        if ct % hide != 0:
            tick.set_visible(False)


def show_contours(fig, axis, varplot, prec, labels, fontsize=10):
    # fig: Figure to plot to. Required parameter.
    # axis: Axis to plot to. Required parameter.
    # varplot: The contourf map created with plot_var. Required parameter.
    # labels: The labels to plot. Required parameter.
    # prec: SEE make_colorbar FOR USAGE. Required Parameter.
    # linewidths: Thickness of contour lines. Default is 1.0.
    # linestyles: How the lines are styles. Default is solid, options are None, 'solid', 'dashed', 'dashdot', 'dotted'
    # fontsize: Size of label font. Default is 10.

    if 'precision' in prec:
        int_round = int([p.lstrip().rstrip() for p in prec.split(',')][1])
        axis.clabel(varplot, labels, inline=1, fontsize=fontsize, fmt='%.{}f'.format(int_round))
    elif 'int' in prec:
        axis.clabel(varplot, labels, inline=1, fontsize=fontsize, fmt='%.d')
    else:
        axis.clabel(varplot, labels, inline=1, fontsize=fontsize)


def plot_point_value(fig, ax, x, y, s, bgcolor='black', fontsize='small'):
    ax.text(x, y, s, color=bgcolor, fontsize=fontsize, transform=ccrs.PlateCarree())


def plot_points(fig, ax, x, y, c, cmap, s=20):
    ax.scatter(x, y, c=c, cmap=cmap, marker='o', s=s, edgecolors='black', transform=ccrs.PlateCarree())


def add_text(fig, ax, x, y, s, c):
    ax.text(x, y+0.05, s, color=c, transform=ccrs.PlateCarree())


def save(fig, path, tight_layout=True, dpi=300):
    if tight_layout:
        fig.savefig(path, dpi=dpi, bbox_inches='tight')
    else:
        fig.savefig(path, dpi=dpi)

'''
CHANGELOG:
v2.4.2: First tracked update

v.3.0.0: Major update:
- Condensed one_plot, row_plot, multi_plot to one function, make_plots.
-	Added axes_2d, which make_plots uses, to convert any axes object to a workable 2d indexer.
- axes_labels is its own separate function.
- plot_var is simplified, and make_colorbar, show_contours have been worked into their own functions.
	- make_colorbar can now hide various tick labels for clarity
	- many of the size parameters have been re-arranged to better fit their respective functions.
	- many optional parameters are now required, partially from the broken up functions.
- ability to directly adjust subplot padding and suptitle in both directions.
- removed unused dependencies
- removed code depending on outside parameters, including csv files and shapefiles.
'''