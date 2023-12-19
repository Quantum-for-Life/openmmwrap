#!/usr/bin/env python
# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-

#    openmmwrap_minimize.py
#
#    Energy-minimize a system. The energy minimization is
#    performed using the BFGSM algorithm as implemented in
#    OpenMM.
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
# Suppress warning messages from 'pymbar' that occur
# when importing the package
log.getLogger("pymbar").setLevel(log.ERROR)
# openmmwrap
import openmmwrap.io as io
from openmmwrap.md import simulation


def main():


    #--------------- Parse the command-line arguments ----------------#


    # Create the argument parser
    prog = "openmmwrap-minimize"
    description = \
        "Energy-minimize a system. The energy minimization is " \
        "performed using the BFGSM algorithm as implemented in " \
        "OpenMM."
    parser = \
        argparse.ArgumentParser(prog = prog,
                                description = description)

    is_help = \
        "The XML file containing the serialized " \
        "'openmm.openmm.System' object representing " \
        "the system."
    parser.add_argument("-is", "--input-system",
                        required = True,
                        help = is_help)

    ip_help = \
        "The PDB file containing the atomic coordinates of the " \
        "input system."
    parser.add_argument("-ip", "--input-structure",
                        required = True,
                        help = ip_help)

    os_default = "output.xml"
    os_help = \
        "The name of the XML file that will contain the " \
        "serialized 'openmm.openmm.System' object representing " \
        "the output system. The file will be written in the " \
        "working directory. The default file name " \
        f"is '{os_default}'."
    parser.add_argument("-os", "--output-system",
                        default = os_default,
                        help = os_help)

    op_default = "output.pdb"
    op_help = \
        "The name of the PDB file that will contain the " \
        "atomic coordinates of the output system. The file " \
        "will be written in the working directory. The " \
        f"default file name is '{op_default}'."
    parser.add_argument("-op", "--output-structure",
                        default = op_default,
                        help = op_help)

    c_help = "The YAML configuration file."
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

    # Parse the arguments
    args = parser.parse_args()
    input_system = args.input_system
    input_structure = args.input_structure
    output_system = args.output_system
    output_structure = args.output_structure
    config_file = args.config_file
    wd = args.work_dir
    log_file = args.log_file
    log_console = args.log_console
    v = args.log_verbose
    vv = args.log_debug


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

        config = io.load_config(config_file = config_file)

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


    #------------------------ Load the systen ------------------------#

    
    # Try to load the system
    try:
        
        system = io.load_system(input_xml = input_system)

    # If something went wrong
    except Exception as e:

        # Log it and exit
        errstr = \
            "It was not possible to load the system from " \
            f"'{input_system}'. Error: {e}"
        logger.exception(errstr)
        sys.exit(errstr)

    # Inform the user that the system was successfully loaded
    infostr = \
        f"The system was successfully loaded from '{input_system}'."
    logger.info(infostr)


    #----------------- Load the system's coordinates -----------------#


    # Try to load the system's coordinates into a 'Modeller' object
    try:
        
        mod = \
            io.load_system_coordinates(input_pdb = input_structure)

    # If something went wrong
    except Exception as e:

        # Log it and exit
        errstr = \
            "It was not possible to load the system's atomic " \
            f"coordinates from '{input_structure}'. Error: {e}"
        logger.exception(errstr)
        sys.exit(errstr)

    # Inform the user that the system's coordinates were successfully
    # loaded
    infostr = \
        "The system's atomic coordinates were successfully " \
        f"loaded from '{input_structure}'."
    logger.info(infostr)


    #--------------------- Run the minimization ----------------------#


    # Inform the user that the minimization is starting
    infostr = "Starting the energy minimization..."
    logger.info(infostr)

    # Minimize the system's energy
    system_updated, mod_updated = \
        simulation.minimize_energy(\
            system = system,
            mod = mod,
            options = config["minimization"])

    # Inform the user that the minimization finished successfully
    infostr = "The energy minimization finished successfully."
    logger.info(infostr)


    #------------------------ Save the system ------------------------#


    # Set the path to the output XML file
    output_system_path = os.path.join(wd, output_system)

    # Try to write the serialized system
    try:
        
        io.save_system(system = system_updated,
                       output_xml = output_system_path)

    # If something went wrong
    except Exception as e:

        # Log it an exit
        errstr = \
            "It was not possible to save the energy-minimized " \
            f"system in '{output_system_path}'. Error: {e}"
        logger.exception(errstr)
        sys.exit(errstr)

    # Inform the user that the energy-minimized system was
    # successfully saved
    infostr = \
        "The energy-minimized system was successfully " \
        f"saved in '{output_system_path}'."


    #------------- Save the system's atomic coordinates --------------#


    # Set the path to the output structure
    output_structure_path = os.path.join(wd, output_structure)

    # Try to save the system's atomic coordinates
    try:
        
        io.save_system_coordinates(\
            mod = mod_updated,
            output_pdb = output_structure_path)

    # If something went wrong
    except Exception as e:

        # Log it and exit
        errstr = \
            "It was not possible to save the atomic coordinates " \
            "of the energy-minimized system in " \
            f"'{output_structure_path}'. Error: {e}"
        logger.exception(errstr)
        sys.exit(errstr)

    # Inform the user that the coordinates of the energy-minimized
    # system were successfully saved
    infostr = \
        "The atomic coordinates of the energy-minimized system " \
        f"were successfully saved in '{output_structure_path}'."
    logger.info(infostr)
