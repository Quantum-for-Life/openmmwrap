#!/usr/bin/env python
# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-

#    frameselections.py
#
#    Utilities for selecting specific frames from a trajectory.
#
#    Copyright (C) 2024 Valentina Sora 
#                       <sora.valentina1@gmail.com>
#
#    This software is released under the MIT license.


# Standard library
import logging as log
# openmmwrap
import openmmwrap.io as io


# Get the module's logger
logger = log.getLogger(__name__)


def _get_frame_closest_to_average(df,
                                  quantity,
                                  use_second_half):
    """Get the frame whose corresponding value
    of a given quantity is closest to the average
    value of that quantity either throughout the
    entire simulation or the second half of it.

    Parameters
    ----------
    df : ``pandas.DataFrame``
        The data frame containing the stata data
        of the simulation.

    quantity : ``str``
        The quantity of interest.

    use_second_half : ``bool``
        Whether to use the second half of the
        simulation, or all of it.
    """

    # Determine the middle index
    middle_index = len(df) // 2

    # Split the data frame into two halves
    first_half = df.iloc[:middle_index]
    second_half = df.iloc[middle_index:]

    # Get the target column
    col = io.QUANTITIES2COLS[quantity]

    # If we only use the second half of the data
    # frame (= the second half of the simulation)
    if use_second_half:

        # Use only the second half of the data frame
        df = second_half

    # Calculate the mean of the target column
    mean_value = df[col].mean()

    # Find the absolute difference from the mean
    df["diff"] = (df[col] - mean_value).abs()

    # Identify the frame with the smallest difference
    closest_frame = df.loc[second_half["diff"].idxmin()]

    # Drop the 'diff' column
    closest_frame = closest_frame.drop("diff")

    # Return the frame
    return closest_frame


def find_frame(df,
               method):
    """Get a specific frame of interest from a
    data frame containing the state data of a
    simulation.

    Parameters
    ----------
    df : ``pandas.DataFrame``
        The data frame containing the stata data
        of the simulation.

    method : ``str``
        The method to use to find the  frame.
    """
    
    # If the user requested the frame where the
    # temperature of the system is closest to the
    # mean temperature of the system throughout the
    # simulation whose data are reported in the data
    # frame
    if method == "closest_to_mean_temperature":

        # Find it
        closest_frame = \
            _get_frame_closest_to_average(\
                df = df,
                quantity = "temperature",
                use_second_half = False)

    # If the user requested the frame where the
    # temperature of the system is closest to the
    # mean temperature of system throughout the second
    # half of the simulation whose data are reported
    # in the data frame
    elif method == "closest_to_mean_temperature_second_half":

        # Find it
        closest_frame = \
            _get_frame_closest_to_average(\
                df = df,
                quantity = "temperature",
                use_second_half = True)  

    # If the user requested the frame where the
    # density of the system is closest to the mean
    # density of the system throughout the
    # simulation whose data are reported in the
    # data frame
    elif method == "closest_to_mean_density":

        # Find it
        closest_frame = \
            _get_frame_closest_to_average(\
                df = df,
                quantity = "density",
                use_second_half = False)

    # If the user requested the frame where the
    # density of the system is closest to the mean
    # density of the system throughout the second
    # half of the simulation whose data are reported
    # in the data frame
    elif method == "closest_to_mean_density_second_half":

        # Find it
        closest_frame = \
            _get_frame_closest_to_average(\
                df = df,
                quantity = "density",
                use_second_half = True)    

    # If the user requested the frame where the
    # volume of the box of the system is closest
    # to the mean volume of the box throughout the
    # simulation whose data are reported in the data
    # frame
    elif method == "closest_to_mean_volume":

        # Find it
        closest_frame = \
            _get_frame_closest_to_average(\
                df = df,
                quantity = "box_volume",
                use_second_half = False)

    # If the user requested the frame where the
    # volume of the box of the system is closest
    # to the mean volume of the box throughout the
    # second half of the simulation whose data are
    # reported in the data frame
    elif method == "closest_to_mean_volume_second_half":

        # Find it
        closest_frame = \
            _get_frame_closest_to_average(\
                df = df,
                quantity = "box_volume",
                use_second_half = True)

    # Return the frame
    return closest_frame

    