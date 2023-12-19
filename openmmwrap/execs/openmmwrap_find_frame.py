#!/usr/bin/env python
# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-

#    openmmwrap_find_frame.py
#
#    Find a frame in a simulation using a state data file.
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
import openmmwrap.io as io
from openmmwrap.md import frameselection


def main():


    #--------------- Parse the command-line arguments ----------------#


    # Create the argument parser
    prog = "openmmwrap-find-frame"
    description = \
        "Find a frame in a simulation using a state data file."
    parser = argparse.ArgumentParser(prog = prog,
                                     description = description)

    isd_help = \
        "The CSV file containing the state data of the " \
        "simulation."
    parser.add_argument("-isd", "--input-state-data",
                        required = True,
                        help = isd_help)

    of_default = "frame.csv"
    of_help = \
        "The name of the CSV file where to write the details " \
        "of the frame of interest. The file wil be " \
        "written in the working directory. The default " \
        f"file name is '{of_default}'."
    parser.add_argument("-of", "--output-frame",
                        default = of_default,
                        help = of_help)

    m_choices = \
        ["closest_to_mean_temperature",
         "closest_to_mean_temperature_second_half",
         "closest_to_mean_density",
         "closest_to_mean_density_second_half",
         "closest_to_mean_volume",
         "closest_to_mean_volume_second_half"]
    m_choices_str = ", ".join([f"'{c}'" for c in m_choices])
    m_help = \
        "The method to use to select the frame. Supported " \
        f"methods are: {m_choices_str}."
    parser.add_argument("-m", "--method",
                        required = True,
                        help = m_help)

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

    sep_default = ","
    sep_help = \
        "The column separator in the input state data " \
        f"file. By default, '{sep_default}' is used."
    parser.add_argument("--sep",
                        default = sep_default,
                        help = sep_help)


    # Parse the arguments
    args = parser.parse_args()
    input_state_data = args.input_state_data
    output_frame = args.output_frame
    method = args.method
    wd = args.work_dir
    log_file = args.log_file
    log_console = args.log_console
    v = args.log_verbose
    vv = args.log_debug
    sep = args.sep


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


    #---------------------- Load the state data ----------------------#

    
    # Try to load the state data
    try:
        
        df_state_data = \
            io.load_state_data(input_csv = input_state_data,
                               sep = sep)

    # If something went wrong
    except Exception as e:

        # Log it and exit
        errstr = \
            "It was not possible to load the state data from " \
            f"'{input_state_data}'. Error: {e}"
        logger.exception(errstr)
        sys.exit(errstr)

    # Inform the user that the state data were successfully loaded
    infostr = \
        "The state data were successfully loaded from " \
        f"'{input_state_data}'."
    logger.info(infostr)


    #------------------------- Get the frame -------------------------#


    # Try to find the frame
    try:

        frame = \
            frameselection.find_frame(df = df_state_data,
                                      method = method)

    # If something went wrong
    except Exception as e:

        # Log it and exit
        errstr = \
            "It was not possible to find the frame with method " \
            f"'{method}'. Error: {e}"
        logger.exception(errstr)
        sys.exit(errstr)

    # Inform the user that the frame was successfully found
    infostr = \
        "The frame was successfully found with method " \
        f"'{method}'."
    logger.info(infostr)


    #------------------- Save the frame's details --------------------#


    # Set the path to the output file
    output_frame_path = os.path.join(wd, output_frame)

    # Try to save the frame's details
    try:

        frame.to_csv(output_frame_path,
                     sep = ",",
                     header = False)

    # If something went wrong
    except Exception as e:

        # Log it and exit
        errstr = \
            "It was not possible to save the frame's details " \
            f"in '{output_frame_path}'. Error: {e}"
        logger.exception(errstr)
        sys.exit(errstr)

    # Inform the user that the frame's details were successfully
    # saved
    infostr = \
        "The frame's details were successfully saved in " \
        f"'{output_frame_path}'."
    logger.info(infostr)