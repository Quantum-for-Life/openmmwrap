#!/usr/bin/env python
# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-

#    openmmwrap_plot_state_data.py
#
#    Plot information about a molecular dynamics simulation
#    from a 'state data' file.
#
#    Copyright (C) 2024 Valentina Sora 
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
import openmmwrap.plotting as plotting


def main():


    #--------------- Parse the command-line arguments ----------------#


    # Create the argument parser
    prog = "openmmwrap-plot-state-data"
    description = \
        "Plot information about a molecular dynamics simulation " \
        "from a 'state data' file."
    parser = argparse.ArgumentParser(prog = prog,
                                     description = description)

    isd_help = \
        "The CSV file containing the state data of the " \
        "simulation."
    parser.add_argument("-isd", "--input-state-data",
                        required = True,
                        help = isd_help)

    opl_default = "plot.pdf"
    opl_help = \
        "The name of the PDF file that will contain the output " \
        "plot. The file wil be written in the working " \
        f"directory. The default file name is '{opl_default}'."
    parser.add_argument("-opl", "--output-plot",
                        default = opl_default,
                        help = opl_help)

    c_help = "The YAML configuration file for plotting."
    parser.add_argument("-c", "--config-file",
                        required = True,
                        help = c_help)

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

    time_rep_default = "step"
    time_rep_help = \
        "Which column of the input state data file will be " \
        "used to represent the simulation time ('step' " \
        f"or 'time'). By default, '{time_rep_default}' is used."
    parser.add_argument("--time-rep",
                        default = time_rep_default,
                        help = time_rep_help)

    quantities_str = \
        ", ".join(f"'{q}'" for q in plotting.QUANTITIES_TO_PLOT)
    quantities_to_plot_help = \
        "Which quantities to plot. By default, all " \
        "quantities reported in the input state data file " \
        "will be plotted. Supported quantities (if present " \
        f"in the input file) are: {quantities_str}." 
    parser.add_argument("--quantities-to-plot",
                        help = quantities_to_plot_help)

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
    output_plot = args.output_plot
    config_file = args.config_file
    wd = args.work_dir
    log_file = args.log_file
    log_console = args.log_console
    v = args.log_verbose
    vv = args.log_debug
    time_rep = args.time_rep
    quantities_to_plot = args.quantities_to_plot
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


    #-------------------- Load the configuration ---------------------#


    # Try to load the configuration
    try:

        config = io.load_config_plot(config_file = config_file)

    # If something went wrong
    except Exception as e:

        # Log it and exit
        errstr = \
            "It was not possible to load the configuration from " \
            f"'{config_file}'. Error: {e}"
        logger.exception(errstr)
        sys.exit(errstr)

    # Inform the user that the configuration was successfully loaded
    infostr = \
        "The configuration was successfully loaded from " \
        f"'{config_file}'."
    logger.info(infostr)


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


    #----------------------------- Plot ------------------------------#


    # Set the path to the output plot
    output_plot_path = os.path.join(wd, output_plot)

    # Try to generate the plot
    try:

        plotting.plot_state_data(\
            df = df_state_data,
            output_pdf = output_plot,
            config = config,
            time_rep = time_rep,
            quantities_to_plot = quantities_to_plot)

    # If something went wrong
    except Exception as e:

        # Log it and exit
        errstr = \
            f"It was not possible to generate the plot. Error: {e}"
        logger.exception(errstr)
        sys.exit(errstr)

    # Inform the user that the plot was successfully generated
    infostr = \
        "The plot was successfully generated and saved in " \
        f"'{output_plot_path}'."
    logger.info(infostr)
