#!/usr/bin/env python
# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-

#    _util.py
#
#    Private utilities to generate plots.
#
#    Copyright (C) 2024 Valentina Sora 
#                       <sora.valentina1@gmail.com>
#
#    This software is released under the MIT license.


# Third-party packages
import matplotlib.pyplot as plt
import numpy as np


def get_formatted_ticklabels(ticklabels,
                             fmt = "{:s}"):
    """Return the ticks' labels, formatted according to
    a given format string.

    Parameters
    ----------
    ticklabels : ``numpy.array`` or ``list``
        An array or list of labels for the ticks.

    fmt: ``str``
        The format string.

    Returns
    -------
    ticklabels : ``list``
        A list with the formatted labels for the ticks.
    """

    # Initialize an empty list to store the formatted
    # labels
    fmt_ticklabels = []

    # For each label
    for ticklabel in ticklabels:

        # Format the label
        fmt_ticklabel = fmt.format(ticklabel)

        # If the label is a single 0
        if fmt_ticklabel == "0":

            # Add it to the list
            fmt_ticklabels.append(fmt_ticklabel)

            # Go to the next one
            continue

        # If the label represents a float
        if "." in fmt_ticklabel:

            # Strip the label of any trailing zeroes
            fmt_ticklabel = fmt_ticklabel.rstrip("0")

        # If the label now ends with a dot (because
        # if was an integer expressed as 1.0, 3.00,
        # etc., and we removed all trailing zeroes)
        if fmt_ticklabel.endswith("."):

            # Remove the dot
            fmt_ticklabel = fmt_ticklabel.rstrip(".")

        # Add the label to the list
        fmt_ticklabels.append(fmt_ticklabel)

    # Return the formatted labels
    return fmt_ticklabels


def get_ticks_positions(values,
                        options):
    """Generate the positions that the ticks
    will have on a plot axis/colorbar/etc.

    This original code for this function was originally
    developed by Valentina Sora for the RosettaDDGPrediction
    package.
    
    The original function can be found at:

    https://github.com/ELELAB/RosettaDDGPrediction/
    blob/master/RosettaDDGPrediction/plotting.py

    Parameters
    ----------
    values : {``list``, ``numpy.ndarray``}
        The values from which the ticks' positions should be set.

    options : ``dict``
        The options for the interval that the ticks'
        positions should cover.

    Returns
    -------
    ticks : ``numpy.ndarray``
        An array containing the ticks' positions.
    """
    
    # Get the options
    int_type = options.get("type")
    rtn = options.get("round_to_nearest")
    top = options.get("top")
    bottom = options.get("bottom")
    steps = options.get("steps")
    spacing = options.get("spacing")
    ciz = options.get("center_in_zero")


    #--------------------------- Rounding ---------------------------#


    # If no rounding was specified
    if rtn is None:

        # If the interval is discrete
        if int_type == "discrete":

            # Default to rounding to the nearest 1
            rtn = 1

        # If the interval is continuous
        elif int_type == "continuous":
        
            # Default to rounding to the nearest 0.5
            rtn = 0.5


    #--------------------------- Top value ---------------------------#


    # If the maximum of the ticks interval was not specified
    if top is None:
        
        # If the interval is discrete
        if int_type == "discrete":
            
            # The default top value will be the
            # maximum of the values provided
            top = int(np.ceil(max(values)))
        
        # If the interval is continuous
        elif int_type == "continuous":
            
            # The default top value will be the
            # rounded-up maximum of the values
            top = \
                np.ceil(max(values)*(1/rtn)) / (1/rtn)


    #------------------------- Bottom value --------------------------#


    # If the minimum of the ticks interval was not specified
    if bottom is None:
        
        # If the interval is discrete
        if int_type == "discrete":

            # The default bottom value is the
            # minimim of the values provided
            bottom = int(min(values))
        
        # If the interval is continuous
        elif int_type == "continuous":
            
            # The default bottom value is the rounded
            # down minimum of the values
            bottom = \
                np.floor(min(values)*(1/rtn)) / (1/rtn)


    # If the two extremes of the interval coincide
    if top == bottom and top is not None:
        
        # Return only one value
        return np.array([bottom])


    #----------------------------- Steps -----------------------------# 


    # If the number of steps the interval should have
    # was not specified
    if steps is None:

        # A default of 10 steps will be set
        steps = 10


    #---------------------------- Spacing ----------------------------#


    # If the interval spacing was not specified
    if spacing is None:
        
        # If the interval is discrete
        if int_type == "discrete":

            # The default spacing is the one between two steps,
            # rounded up
            spacing = \
                int(np.ceil(np.linspace(bottom,
                                        top,
                                        steps,
                                        retstep = True)[1]))

        
        # If the interval is continuous
        elif int_type == "continuous":
            
            # The default spacing is the one between two steps,
            # rounded up
            spacing = np.linspace(bottom,
                                  top,
                                  steps,
                                  retstep = True)[1]

            # Get the spacing by rounding up the spacing
            # obtained above
            spacing = np.ceil(spacing*(1/rtn)) / (1/rtn)


    #------------------------ Center in zero -------------------------#


    # If the interval should be centered in zero
    if ciz:
        
        # Get the highest absolute value
        absval = \
            np.ceil(top) if top > bottom else np.floor(bottom)
        
        # Top and bottom will be opposite numbers with
        # absolute value equal to absval
        top, bottom = absval, -absval

        # Get an evenly-spaced interval between the bottom
        # and top value
        interval = np.linspace(bottom, top, steps)
        
        # Return the interval
        return interval

    # Get the interval
    interval = np.arange(bottom, top + spacing, spacing)

    # Return the interval
    return interval


def set_axis(ax,
             which_axis,
             options,
             ticks = None,
             tick_labels = None):
    """Set up the x- or y-axis after generating a plot.

    Parameters
    ----------
    ax : ``matplotlib.axes.Axes``
        An Axes instance.

    which_axis : ``str``, {``"x"``, ``"y"``}
        Which axis is to be set.

    options : ``dict``
        The options for setting the axis.

    ticks : ``list`` or ``numpy.array``, optional
        A list or array of ticks' positions. If it is not passed,
        the ticks will be those already present on the axis
        (automatically determined by matplotlib when generating
        the plot).

    tick_labels : ``list``, optional
        A list of ticks' labels. If not passed, the ticks' labels
        will represent the ticks' positions.

    Returns
    -------
    ax : ``matplotlib.axes.Axes``
        The updated Axes instance. 
    """


    #----------------------------- Axes ------------------------------#


    # If the axis to be set is the x-axis
    if which_axis == "x":

        # Set the corresponding methods
        plot_ticks = plt.xticks
        set_label = ax.set_xlabel
        set_ticks = ax.set_xticks
        set_ticklabels = ax.set_xticklabels
        get_ticklabels = ax.get_xticklabels

        # Set the corresponding spine
        spine = "bottom"

    # If the axis to be set is the y-axis
    elif which_axis == "y":

        # Set the corresponding methods
        plot_ticks = plt.yticks
        set_label = ax.set_ylabel
        set_ticks = ax.set_yticks
        set_ticklabels = ax.set_yticklabels
        get_ticklabels = ax.get_yticklabels

        # Set the corresponding spine
        spine = "left"

    # If there are options for the axis label
    if options.get("label"):
        
        # Set the axis label with the given options
        set_label(**options["label"])        


    #----------------------------- Ticks -----------------------------#

    
    # If no ticks' positions were passed
    if ticks is None:

        # Default to the ticks' positions already present
        ticks = plot_ticks()[0]

    # If there are ticks on the axis
    if len(ticks) > 0:      
        
        # Set the axis' boundaries
        ax.spines[spine].set_bounds(ticks[0],
                                    ticks[-1])

    # If options for the tick parameters were provided
    if options.get("tick_params"):
        
        # Set the given options for the ticks
        ax.tick_params(axis = axis,
                       **options["tick_params"])

    # Set the ticks
    set_ticks(ticks = ticks)


    #------------------------- Ticks' labels -------------------------#

    
    # Get the configuration for ticks' labels
    tick_labels_options = options.get("ticklabels", {})
    
    # If no ticks' labels were passed
    if tick_labels is None:

        # Get the format to be used for the tick labels
        tick_labels_fmt = tick_labels_options.get("fmt", "{:.3f}")

        # Default to the string representations
        # of the ticks' positions
        tick_labels = \
            get_formatted_ticklabels(ticklabels = ticks,
                                     fmt = tick_labels_fmt)
    
    # If options for the ticks' labels were passed
    if tick_labels_options.get("options") is not None:

        # Set the ticks' labels
        set_ticklabels(labels = tick_labels,
                       **tick_labels_options["options"])

    # Return the updated axis
    return ax