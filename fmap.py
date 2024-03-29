# Version 2.4.2 by Tim Corrie

# This module is a wrapper for cartopy to save space in the main code, using matplotlib as well.
# It is necessary to run any notebooks where it's called without significant modification of code, specifically spatial plots.
# It is a WIP and may be updated at any time.
# Last update: 03/29/2024

import matplotlib.pyplot as plt
import xarray as xa
import numpy as np
import math
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
from matplotlib.ticker import FormatStrFormatter as FSF
from matplotlib.ticker import FuncFormatter as FF
import pandas as pd
import matplotlib as mpl
import matplotlib.patheffects as PE
mpl.use('Agg')


#ofile = xa.open_dataset("/mnt/lfs1/BMC/wrfruc/tcorrie/keepmehere.nc",engine="pynio")
#lats = ofile.variables['gridlat_0'][::]
#lons = ofile.variables['gridlon_0'][:]


def isiterable(obj): # Function to determine if more than one axes were created. For some reason, one axis is not iterable. Any object can be passed here
    try:
        a=iter(obj)
        if True:
            return True
    except TypeError:
        return False

# Creates a plot with one subaxis (i.e. one figure). Returns fig, ax pair.    
def one_plot(wlon = -112, elon = -103, nlat = 46, slat = 40, figtitle="", lonticks=1, latticks=1, titlesize=18):
    #wlon,elon,nlat,slat are the west, east, north, and south coordinates of the map boundaries, respectively. Default domain is listed above.
    #figtitle: Give this plot a name. Default is blank but can be added later.
    #lonticks,latticks: Degree interval for labelling coordinates for longitude and latitude, respectively, in degrees. Default is 1 degree.
    fig, ax = plt.subplots(1, 1, subplot_kw=dict(projection=ccrs.PlateCarree()), figsize=(8,10), dpi=1200)
    ax.set_extent([wlon,elon,slat,nlat])
    ax.add_feature(cfeature.STATES,edgecolor="gray",zorder=100)
    ax.add_feature(cfeature.BORDERS, edgecolor="black",zorder=99)
    xticks = np.arange(wlon,elon+1,lonticks)
    yticks = np.arange(slat,nlat+1,latticks)
    ax.set_xticks(xticks, crs=ccrs.PlateCarree())
    ax.set_yticks(yticks, crs=ccrs.PlateCarree())
    ax.set_xticklabels(xticks,fontsize=8)
    ax.set_yticklabels(yticks,fontsize=8)
    # Formats the longitude and latidude to exclude negative signs. No observed way around it.
    def lon_formatter(x, pos):
        if x==0 or x==180:
            return '{}°'.format(abs(x))
        elif x<0:
            return '{}°W'.format(abs(x))
        elif x>0:
            return '{}°E'.format(abs(x))
    def lat_formatter(y, pos):
        if y<0:
            return '{}°S'.format(abs(y))
        elif y>0:
            return '{}°N'.format(abs(y))
        elif y==0:
            return '{}°'.format(abs(y))
    ax.xaxis.set_major_formatter(FF(lon_formatter))
    ax.yaxis.set_major_formatter(FF(lat_formatter))
    ax.set_title(figtitle,fontsize=titlesize)
    #fig.tight_layout(pad=0.1)
    return fig, ax
        
# Creates a horizontal line of plots (i.e. row=1). Returns fig, ax pair. 
def row_plot(wlon = -112, elon = -103, nlat = 46, slat = 40, figtitle = "", lonticks=1, latticks=1, cols=2, titlesize=20):
    #wlon,elon,nlat,slat are the west, east, north, and south coordinates of the map boundaries, respectively. Default domain is listed above.
    #figtitle: Give this plot a name. Default is blank but can be added later.
    #lonticks,latticks: Degree interval for labelling coordinates for longitude and latitude, respectively, in degrees. Default is 1 degree.
    #cols: Number of figure columns. Default is 2.
    
    fig, axs = plt.subplots(1, cols, subplot_kw=dict(projection=ccrs.PlateCarree()), figsize=(cols*8,10))
    for ax in axs:
        ax.set_extent([wlon,elon,slat,nlat])
        ax.add_feature(cfeature.STATES,edgecolor="black",zorder=100)
        ax.add_feature(cfeature.BORDERS, edgecolor="black",zorder=99)
        xticks = np.arange(wlon,elon+1,lonticks)
        yticks = np.arange(slat,nlat+1,latticks)
        ax.set_xticks(xticks, crs=ccrs.PlateCarree())
        ax.set_yticks(yticks, crs=ccrs.PlateCarree())
        ax.set_xticklabels(xticks,fontsize=16)
        ax.set_yticklabels(yticks,fontsize=16)
        # Formats the longitude and latidude to exclude negative signs. No observed way around it.
        def lon_formatter(x, pos):
            if x==0 or x==180:
                return '{}°'.format(abs(x))
            elif x<0:
                return '{}°W'.format(abs(x))
            elif x>0:
                return '{}°E'.format(abs(x))
        def lat_formatter(y, pos):
            if y<0:
                return '{}°S'.format(abs(y))
            elif y>0:
                return '{}°N'.format(abs(y))
            elif y==0:
                return '{}°'.format(abs(y))
        ax.xaxis.set_major_formatter(FF(lon_formatter))
        ax.yaxis.set_major_formatter(FF(lat_formatter))
    fig.suptitle(figtitle, fontsize=titlesize)
    return fig, axs


# Returns a matrix of plots where each dimension is at least 2.
def multi_plot(wlon = -112, elon = -103, nlat = 46, slat = 40, figtitle = "", lonticks=1, latticks=1, rows=2, cols=2, titlesize=20, figsize=None, adjusty=None):
    #wlon,elon,nlat,slat are the west, east, north, and south coordinates of the map boundaries, respectively. Default domain is listed above.
    #figtitle: Give this plot a name. Default is blank but can be added later.
    #lonticks,latticks: Degree interval for labelling coordinates for longitude and latitude, respectively, in degrees. Default is 1 degree.
    #rows,cols: Number of figure rows and columns, respectively. Default for both is 2.
    if figsize == None:
        figsize = (rows*8,cols*8+2)
    
    fig, axs = plt.subplots(rows, cols, subplot_kw=dict(projection=ccrs.PlateCarree()), figsize=figsize)
    for a_n in range(rows*cols):
        axs[a_n//rows,a_n%cols].set_extent([wlon,elon,slat,nlat])
        axs[a_n//rows,a_n%cols].add_feature(cfeature.STATES,edgecolor="gray",zorder=100)
        axs[a_n//rows,a_n%cols].add_feature(cfeature.BORDERS, edgecolor="black",zorder=99)
        xticks = np.arange(wlon,elon+1,lonticks)
        yticks = np.arange(slat,nlat+1,latticks)
        axs[a_n//rows,a_n%cols].set_xticks(xticks, crs=ccrs.PlateCarree())
        axs[a_n//rows,a_n%cols].set_yticks(yticks, crs=ccrs.PlateCarree())
        axs[a_n//rows,a_n%cols].set_xticklabels(xticks,fontsize=16)
        axs[a_n//rows,a_n%cols].set_yticklabels(yticks,fontsize=16)
        # Formats the longitude and latidude to exclude negative signs. No observed way around it.
        def lon_formatter(x, pos):
            if x==0 or x==180:
                return '{}°'.format(abs(x))
            elif x<0:
                return '{}°W'.format(abs(x))
            elif x>0:
                return '{}°E'.format(abs(x))
        def lat_formatter(y, pos):
            if y<0:
                return '{}°S'.format(abs(y))
            elif y>0:
                return '{}°N'.format(abs(y))
            elif y==0:
                return '{}°'.format(abs(y))
        axs[a_n//rows,a_n%cols].xaxis.set_major_formatter(FF(lon_formatter))
        axs[a_n//rows,a_n%cols].yaxis.set_major_formatter(FF(lat_formatter))
    if adjusty is not None:
        fig.suptitle(figtitle, fontsize=titlesize,y=adjusty)
    else:
        fig.suptitle(figtitle, fontsize=titlesize)
    return fig, axs

        
# https://simplemaps.com/data/us-cities
# The above link is required by license for free copies of uscities.csv
uscities = pd.read_csv('uscities.csv')
uscities.drop(['military', 'county_fips', 'population', 'density', 'source', 'incorporated', 'timezone', 'ranking', 'zips', 'id'], axis=1, inplace=True)
def cdb(): # Just a helper function to play around with to make sure I can get the column names correct.
    return uscities
def find_town(location):
    loc = [l.lstrip().rstrip() for l in location.split(',')]
    town_name=loc[0]
    state_name=loc[1]
    if len(state_name)==2:
        return uscities.loc[(uscities['city_ascii']==town_name) & (uscities['state_id']==state_name)]
    else:
        return uscities.loc[(uscities['city_ascii']==town_name) & (uscities['state']==state_name)]
# Plot a location
def plot_town(axis, location, markersize=5, marker='o', color='black', xoffset=-0.3, yoffset=0.2, zorder=101):
    #axis: Axis or axes to plot the town on. Can be one or all. Required parameter.
    #location: String location of city/town you want to plot. Must be "City, ST" or "City, State". Required parameter.
    #markersize: How big to make the dot. Default is 5.
    #marker: Shape of the marker. Default is 'o'.
    #color: Color of both the text and dot. Default is black.
    #[xy]offset: Offset of the text in the [xy] direction relative to the dot. Default is (x,y)=(-0.3,0.2).
    #zorder: Puts the plot in front of or behind something. Default is 101, advised not to mess with this.
    loc = [l.lstrip().rstrip() for l in location.split(',')]
    town_name=loc[0]
    state_name=loc[1]
    if len(state_name)==2:
        lon=uscities.loc[(uscities['city_ascii']==town_name) & (uscities['state_id']==state_name)]['lng'].values[0]
        lat=uscities.loc[(uscities['city_ascii']==town_name) & (uscities['state_id']==state_name)]['lat'].values[0]
    else:
        lon=uscities.loc[(uscities['city_ascii']==town_name) & (uscities['state']==state_name)]['lng'].values[0]
        lat=uscities.loc[(uscities['city_ascii']==town_name) & (uscities['state']==state_name)]['lat'].values[0]
        
    if isiterable(axis):
        for ax in axis:
            ax.plot(lon,lat,markersize=markersize,marker=marker,color=color, transform=ccrs.Geodetic())
            ax.text(lon+xoffset,lat+yoffset, s=town_name, color=color, transform=ccrs.Geodetic())
    else:
        axis.plot(lon,lat,markersize=markersize,marker=marker,color=color, transform=ccrs.Geodetic())
        axis.text(lon+xoffset,lat+yoffset, s=town_name, color=color, transform=ccrs.Geodetic())
         
        
def plot_var(fig, axis, varnames, style, cmap='rainbow', colors='black', prange=np.arange(0,1.1,0.1), alpha=0.8, crange=np.arange(0,1.1,0.1), cbar_include = True, cbarorient='vertical', label='', shrink=0.75, cbar_axes = None, prec='', linewidths=1.0, linestyles='solid', fontsize=10, normalization=False, extend='neither', ticklabelrotation=0, ticklabelsize=16):
    #fig: Figure to plot to. Required parameter.
    #axis: Axis to plot to. Required parameter.
    #varnames: Variable names to plot. Requires x, y, and z variables as a 2-D list of 3 variables (e.g. [longitude, latitude, field]). Required parameter.
    #style: Either 'contour' or 'contourf'. Required parameter.
    #cmap: For contourf, sets the color scheme. Default is 'rainbow'.
    #colors: For contour, sets the contour colors. Default is 'black'.
    #prange: Range used for contourf. Default is 0 to 1 in 0.1 intervals.
    #alpha: Opacity of the contourf levels. Default is 0.8.
    #crange: Range used for contour. Default is 0 to 1 in 0.1 intervals.
    #cbar_include: Include colorbar in the plot. Default is True.
    #cbarorient: Orientation of the colorbar. Options are 'horizontal' or 'vertical', default is 'vertical'.
    #label: label to give the colorbar. Default is blank.
    #shrink: Shrinks the colorbar by a given multiplication factor. Default is 0.75.
    #cbar_axes: Axis for which the colorbar applies to. Default is None, which defaults to the axis being plotted.
    #prec: How to format the tick labels in the colorbar or contour labels in contour. Default is '' (none). Options are 'precision, 'x' (uses np.round), 'int' (.astype(int)). May come up with more options later.
    #linewidths: Thickness of contour lines. Default is 1.0.
    #linestyles: How the lines are styles. Default is solid, options are None, 'solid', 'dashed', 'dashdot', 'dotted'
    #fontsize: Size of label font. Default is 10.
    #labelrotation: Rotation of labels, in degrees. Default is 0 (no rotation)
    
    
# TO-DO: May bring the colorbar parameters into a separate function itself to give flexibility there.
    if isiterable(axis):
        raise TypeError('axis must be a single instance, not an iterable')
 
    else:
        if style=="contourf":
            if normalization==False:
                varplot = axis.contourf(varnames[0],varnames[1],varnames[2],prange,cmap=cmap,alpha=alpha,transform=ccrs.PlateCarree(), extend=extend)
                if cbar_include:
                    cbar= fig.colorbar(varplot, orientation=cbarorient, ax=cbar_axes, shrink=shrink, pad=0.05)
                    cbar.set_label(label, fontsize=24) 
                    cbar.set_ticks(prange)
                    if 'precision' in prec:
                        int_round = int([p.lstrip().rstrip() for p in prec.split(',')][1])
                        cbar.set_ticklabels(np.around(prange,int_round))
                    elif 'int' in prec:
                        cbar.set_ticklabels(prange.astype(int))
                    else:
                        cbar.set_ticklabels(prange)
                    cbar.ax.tick_params(labelsize=ticklabelsize,size=14,labelrotation=ticklabelrotation)
            else:
                varplot = axis.contourf(varnames[0],varnames[1],varnames[2], prange, norm=mpl.colors.LogNorm(vmin=prange[0],vmax=prange[-1]), cmap=cmap, transform=ccrs.PlateCarree(), extend=extend)
                if cbar_include:
                    cbar= fig.colorbar(varplot, orientation=cbarorient, ax=cbar_axes, shrink=shrink, pad=0.05)
                    cbar.set_label(label, fontsize=24)
                    cbar.set_ticks(prange)
                    if 'precision' in prec:
                        int_round = int([p.lstrip().rstrip() for p in prec.split(',')][1])
                        cbar.set_ticklabels(np.around(prange,int_round))
                    elif 'int' in prec:
                        cbar.set_ticklabels(prange.astype(int))
                    else:
                        cbar.set_ticklabels(prange)
                    cbar.ax.tick_params(labelsize=ticklabelsize,size=14,labelrotation=ticklabelrotation)
        elif style=="contour":
            varplot=axis.contour(varnames[0],varnames[1],varnames[2],crange,colors=colors,linewidths=linewidths,linestyles=linestyles)
            if 'precision' in prec:
                int_round = int([p.lstrip().rstrip() for p in prec.split(',')][1])
                axis.clabel(varplot, crange, inline=1, fontsize=fontsize, fmt='%.{}f'.format(int_round))
            elif 'int' in prec:
                axis.clabel(varplot, crange, inline=1, fontsize=fontsize, fmt='%.d')
            else:
                axis.clabel(varplot, crange, inline=1, fontsize=fontsize)
        
        
def plot_point_value(fig,ax,x,y,s,bgcolor='black',fontsize='small'):
    ax.text(x,y,s,color=bgcolor, fontsize=fontsize,transform = ccrs.PlateCarree())
    
def plot_points(fig,ax,x,y,c,cmap,size=20):
    ax.scatter(x,y,c=c,cmap=cmap,marker='o',s=size,edgecolors='black',transform = ccrs.PlateCarree())
    
def add_text(fig,ax,x,y,s,c,fsize=16):
    ax.text(x,y+0.05,s,color=c, transform=ccrs.PlateCarree(), fontsize=fsize)
    
def save(fig, path, tight_layout = True, dpi=300):
    if tight_layout:
        fig.savefig(path, dpi=dpi, bbox_inches='tight')
    else:
        fig.savefig(path, dpi=dpi)
    