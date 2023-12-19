#!/usr/bin/env python
# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-

#    openmmwrap_conv.py
#
#    Convert between trajectory formats.
#
#    Copyright (C) 2023 Valentina Sora 
#                       <sora.valentina1@gmail.com>
#
#    This software is released under the MIT license.


# Standard library
import argparse
import logging as log
import os
import sys
# openmmwrap
from openmmwrap.md import conversion


def main():


    #--------------- Parse the command-line arguments ----------------#


    # Create the argument parser
    prog = "openmmwrap-conv"
    description = \
        "Convert between trajectory formats."
    parser = argparse.ArgumentParser(prog = prog,
                                     description = description)

    ip_help = \
        "The PDB file containing the atomic coordinates of the " \
        "input system."
    parser.add_argument("-ip", "--input-structure",
                        required = True,
                        help = ip_help)

    it_help = "The input trajectory."
    parser.add_argument("-it", "--input-trajectory",
                        required = True,
                        help = it_help)

    ot_help = "The output trajectory."
    parser.add_argument("-ot", "--output-trajectory",
                        required = True,
                        help = ot_help)

    d_help = \
        "The working directory. The default is the current " \
        "working directory."
    parser.add_argument("-d", "--work-dir",
                        default = os.getcwd(),
                        help = d_help)

    lf_default = "logfile.log"
    lf_help = \
        "The name of the plain text log file. The file will " \
        "be written in the working directory. The default " \
        f"file name is '{lf_default}'."
    parser.add_argument("-lf", "--log-file",
                        default = lf_default,
                        help = lf_help)

    lc_help = "Show log messages also on the console."
    parser.add_argument("-lc", "--log-console",
                        action = "store_true",
                        help = lc_help)

    v_help = "Enable verbose logging (INFO level)."
    parser.add_argument("-v", "--log-verbose",
                        action = "store_true",
                        help = v_help)

    vv_help = \
        "Enable maximally verbose logging for debugging " \
        "purposes (DEBUG level)."
    parser.add_argument("-vv", "--log-debug",
                        action = "store_true",
                        help = vv_help)

    start_help = \
        "The starting point (in frame number) of the " \
        "output trajectory. By default, the output " \
        "trajectory will start at the same frame as " \
        "the input trajectory."
    parser.add_argument("--start",
                        help = start_help)

    end_help = \
        "The ending point (in frame number) of the " \
        "output trajectory. By default, the output " \
        "trajectory will end at the same frame as " \
        "the input trajectory."
    parser.add_argument("--end",
                        help = end_help)

    stride_help = \
        "The stride (in number of frames). By default, " \
        "no frames will be skipped when writing the " \
        "output trajectory."
    parser.add_argument("--stride",
                        help = stride_help)

    frames = \
        "A list of specific frames to be included in the " \
        "output trajectory, or a method to select specifc " \
        "If 'selection_frames' is provided, " \
        "'begin', 'end', and 'stride' are ignored, if " \
        "provided."
    parser.add_argument("--frames",
                        help = frames,
                        nargs = "*")

    selection_help = \
        "The selection string (in MDAnalysis format) " \
        "defining which atoms will be included in the " \
        "output trajectory."
    parser.add_argument("--selection",
                        help = selection_help)

    center_help = \
        "Whether to center the 'center_selection' " \
        "atoms in the box."
    parser.add_argument("--center",
                        action = "store_true")

    center_selection_help = \
        "The selection string (in MDAnalysis format) " \
        "defining which atoms will be centered in the " \
        "box."
    parser.add_argument("--center-selection",
                        help = center_selection_help)

    # Parse the arguments
    args = parser.parse_args()
    input_structure = args.input_structure
    input_trajectory = args.input_trajectory
    output_trajectory = args.output_trajectory
    wd = args.work_dir
    log_file = args.log_file
    log_console = args.log_console
    v = args.log_verbose
    vv = args.log_debug
    start = args.start
    end = args.end
    stride = args.stride
    selection = args.selection
    frames = [int(frame) for frame in args.frames]
    center = args.center
    center_selection = args.center_selection


    #---------------------------- Logging ----------------------------#


    # Get the module's logger
    logger = log.getLogger(__name__)

    # Set WARNING logging level by default
    level = log.WARNING

    # If the user requested verbose logging
    if v:

        # The minimal logging level will be INFO
        level = log.INFO

    # If the user requested logging for debug purposes
    # (-vv overrides -v if both are provided)
    if vv:

        # The minimal logging level will be DEBUG
        level = log.DEBUG

    # Initialize the logging handlers to a list containing only
    # the FileHandler (to log to the log file)
    handlers = [log.FileHandler(# The log file
                                filename = log_file,
                                # How to open the log file ('w' means
                                # re-create it every time the
                                # executable is called)
                                mode = "w")]

    # If the user requested logging to the console, too
    if log_console:

        # Append a StreamHandler to the list
        handlers.append(log.StreamHandler())

    # Set the logging level
    log.basicConfig(# The level below which log messages are silenced
                    level = level,
                    # The format of the log strings
                    format = "{asctime}:{levelname}:{name}:{message}",
                    # The format for dates/time
                    datefmt="%Y-%m-%d,%H:%M",
                    # The format style
                    style = "{",
                    # The handlers
                    handlers = handlers)


    #-------------------- Convert the trajectory ---------------------#


    # Set the path to the output trajectory
    output_trajectory_path = os.path.join(wd, output_trajectory)

    # Inform the user that we are starting the conversion
    infostr = "Starting the conversion..."
    logger.info(infostr)

    # Try to convert the trajectory
    try:

        conversion.convert_trajectory(\
            input_structure = input_structure,
            input_trajectory = input_trajectory,
            output_trajectory = output_trajectory_path,
            start = start,
            end = end,
            stride = stride,
            selection = selection,
            frames = frames,
            center = center,
            center_selection = center_selection)

    # If something went wrong
    except Exception as e:

        # Log it and exit
        errstr = \
            "It was not possible to convert the trajectory. " \
            f"Error: {e}"
        logger.exception(errstr)
        sys.exit(errstr)

    # Inform the user that the trajectory was successfully converted
    infostr = \
        "The trajectory was successfully converted and " \
        f"written in '{output_trajectory_path}'."
    logger.info(infostr)
