#!/usr/bin/env python
# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-

#    conversions.py
#
#    Utilities for converting trajectories between different formats.
#
#    Copyright (C) 2023 Valentina Sora 
#                       <sora.valentina1@gmail.com>
#
#    This software is released under the MIT license.


# Standard library
import logging as log
import os
import sys
import warnings
# Ignore MDAnalysis' UserWarning
warnings.filterwarnings("ignore",
                        category = UserWarning)
# Third-party packages
import MDAnalysis as mda
import MDAnalysis.transformations as trans
# openmmwrap
import openmmwrap.io as io


# Get the module's logger
logger = log.getLogger(__name__)


def convert_trajectory(input_structure,
                       input_trajectory,
                       output_trajectory,
                       input_state_data = None,
                       start = None,
                       end = None,
                       stride = None,
                       selection = None,
                       frames = None,
                       center = False,
                       center_selection = None):
    """Convert a trajectory into a different format.
    """

    #--------------- Load the structure and trajectory ---------------#


    # Create a 'Universe' object from the input
    # topology and trajectory
    u = mda.Universe(input_structure, input_trajectory)


    #--------------------- Center the trajectory ---------------------#


    # If the user requested centering the a subset of
    # atoms in the box
    if center:

        # If the user did not pass a selection to
        # be centered
        if center_selection is None:

            # Raise an error
            errstr = \
                "You must pass a 'center_selection' if " \
                "'center' is 'True'."
            raise ValueError(errstr)

        # Get the selection from the 'Universe'
        center_sel_universe = \
            u.select_atoms(center_selection)

        # Get the selection of what is NOT the
        # provided selection
        center_not_sel_universe = \
            u.select_atoms(f"not ({center_selection})")

        # Get the sequence of transformations to be
        # performed to center the selection in the box
        transforms = \
            [trans.unwrap(center_sel_universe),
             trans.center_in_box(center_sel_universe,
                                  wrap = True),
             trans.wrap(center_not_sel_universe)]

        # Add the transformations to the trajectory
        # on-the-fly
        u.trajectory.add_transformations(*transforms)


    #--------------------- Select specific atoms ---------------------#


    # Set the subset of atoms to be written to the
    # output trajectory
    sel = selection if selection is not None else "all"

    # Get the selection from the 'Universe'
    sel_universe = u.select_atoms(sel)


    #-------------------- Select specific frames ---------------------#


    # Set the starting point for writing the output
    # trajectory
    start = start if start is not None else 0

    # Set the ending point for writing the output
    # trajectory
    end = end if end is not None else len(u.trajectory)-1

    # Set the stride for writing the output
    # trajectory
    stride = stride if stride is not None else 1

    # Create the writer
    with mda.Writer(output_trajectory, sel_universe.n_atoms) as w:

        # If a list of frames was provided
        if frames is not None:

            # Get only those frames
            trajectory_slice = u.trajectory[frames]

        # Otherwise
        else:

            # Get the slice of trajectory to write
            trajectory_slice = u.trajectory[start:end+stride:stride]
            
        # For each frame in the trajectory
        for i, ts in enumerate(trajectory_slice):
            
            # Write out the progress
            sys.stdout.write(\
                f"\rConverting frame {i+1} / " \
                f"{len(trajectory_slice)}.")

            # Write out the selection at that frame
            w.write(sel_universe)

        # Leave the progress bar
        sys.stdout.write("\n")
