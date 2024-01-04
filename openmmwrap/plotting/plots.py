#!/usr/bin/env python
# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-

#    plots.py
#
#    Utilities to plot data.
#
#    Copyright (C) 2024 Valentina Sora 
#                       <sora.valentina1@gmail.com>
#
#    This software is released under the MIT license.


# Standard library
import logging as log
import warnings
# Third-party packages
import matplotlib.pyplot as plt
import pandas as pd
# openmmwrap
import openmmwrap.io as io
from . import defaults, _util


# Ignore warnigns (matplotlib's UserWarnings)
warnings.filterwarnings("ignore",
                        category = UserWarning)

# Get the module's logger
logger = log.getLogger(__name__)


def plot_state_data(df,
                    output_pdf,
                    config,
                    time_rep = "time",
                    quantities_to_plot = None):
    """Plot the information contained in 'state data' files.

    Parameters
    ----------
    df : ``pandas.DataFrame``
        The data frame containing the 'stata data'.

    output_pdf : ``str``
        The output PDF file where the plot will be saved.

    config : ``dict``
        The configuration for the plot.

    time_rep : ``str``, ``"time"``
        The representation of time (plotted on the x-axes of all
        plots). The selected representation must be available in
        the data frame.

        Supported time representations are: ``"step"`` and
        ``"time"``.

    quantities_to_plot : ``list``, optional
        A list of quantities to be plotted. The selected quantities
        must be available in the data frame.

        Supported quantities are: ``"potential_energy"``,
        ``"kinetic_energy"``, ``"total_energy"``, ``"temperature"``,
        ``"box_volume"``, ``"density"``, ``"mass"``.
    """


    #------------------------ Preprocess data ------------------------#


    # Set the time representation (steps or actual time) as
    # index of the data frame
    df = df.set_index(keys = io.QUANTITIES2COLS[time_rep],
                      drop = True)

    # Get only those columns containing data to be plotted
    quantities_to_plot = \
        quantities_to_plot if quantities_to_plot is not None \
        else defaults.QUANTITIES_TO_PLOT

    # Keep only those columns containing data to be plotted
    slices = \
        {q : df[io.QUANTITIES2COLS[q]] for q \
         in quantities_to_plot if io.QUANTITIES2COLS[q] \
         in df.columns}


    #----------------------------- Plot ------------------------------#


    # Close any figure that may be open
    plt.close()

    # Generate the figure and axes (there are a maximum of
    # seven sub-plots)
    fig, axes = plt.subplots(nrows = 3,
                             ncols = 3,
                             figsize = config.get("size_inches"))

    # For each extra axis
    for ax in axes.flatten()[len(slices):]:

        # Remove it
        ax.remove()

    # For each ax that will be used and associated column of data
    for ax, (quantity, col) \
    in zip(axes.flatten()[:len(slices)], slices.items()):

        # Get the configuration for the current line plot
        config_plot = config["plot"][quantity]
        ax.set_aspect("auto")

        #--------------------- Generate the plot ---------------------#


        # Get the values contained in the index
        time_rep_values = col.index.values

        # Get the values contained in the column of interest
        col_values = col.values

        # Generate the line plot
        ax.plot(time_rep_values,
                col_values,
                **config["plot"][quantity]["lineplot"])


        #----------------------- Set the title -----------------------#


        # Get the configuration for the title
        config_title = config_plot.get("title")

        # If there is a configuration for the title
        if config_title is not None:

            # Set the plot's title
            ax.set_title(**config_title)


        #---------------------- Set the spines -----------------------#


        # Hide the top and right spine
        for spine in ["top", "right"]:
            ax.spines[spine].set_visible(False)

        # Set the position of the bottom and left spine
        for spine in ["bottom", "left"]:
            ax.spines[spine].set_position(("outward", 5))


        #---------------------- Set the x-axis -----------------------#


        # Get the configuration of the axis
        config_x_axis = config_plot.get("xaxis")

        # If there is a configuration for the axis
        if config_x_axis is not None:

            # Get user-defined ticks, if provided
            x_ticks = config_x_axis.get("ticks")

            # If no user-defined ticks were provided
            if x_ticks is None:

                # Get the positions of the ticks on the axis
                x_ticks = \
                    _util.get_ticks_positions(\
                        values = time_rep_values,
                        options = config_x_axis["interval"])

            # Set the axis
            _util.set_axis(ax = ax,
                           which_axis = "x",
                           options = config_x_axis,
                           ticks = x_ticks)


        #---------------------- Set the y-axis -----------------------#


        # Get the configuration of the axis
        config_y_axis = config_plot.get("yaxis")

        # If there is a configuration for the axis
        if config_y_axis is not None:

            # Get user-defined ticks, if provided
            y_ticks = config_y_axis.get("ticks")

            # If no user-defined ticks were provided
            if y_ticks is None:
            
                # Get the positions of the ticks on the axis
                y_ticks = \
                    _util.get_ticks_positions(\
                        values = col_values,
                        options = config_y_axis["interval"])

            # Set the axis
            _util.set_axis(ax = ax,
                           which_axis = "y",
                           options = config_y_axis,
                           ticks = y_ticks)


    #------------------------- Save the plot -------------------------#


    # Write the plot in the output file
    plt.savefig(fname = output_pdf,
                **config["output"])