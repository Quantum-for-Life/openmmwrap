#!/usr/bin/env python
# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-

#    openmmwrap_run.py
#
#    Run a molecular dynamics simulation.
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
from openmmwrap import ioutil
from openmmwrap.mdutil import (
    barostats,
    integrators,
    md,
    restraints,
    thermostats)


def main():


    #--------------- Parse the command-line arguments ----------------#


    # Create the argument parser
    prog = "openmmwrap-run"
    description = \
        "Run a molecular dynamics simulation."
    parser = argparse.ArgumentParser(prog = prog,
                                     description = description)

    # Add the arguments
    is_help = \
        "The input system as a XML file containing the " \
        "serialized 'openmm.openmm.System' object representing " \
        "the full system."
    parser.add_argument("-is", "--input-system",
                        required = True,
                        help = is_help)

    ip_help = "The input system's atomic coordinates as a PDB file."
    parser.add_argument("-ip", "--input-structure",
                        required = True,
                        help = ip_help)

    os_default = "output.xml"
    os_help = \
        "The output system as an XML file containing the " \
        "serialized 'openmm.openmm.System' object representing " \
        "the full system. The file will be written in the " \
        f"working directory. The default file name is '{os_default}'."
    parser.add_argument("-os", "--output-system",
                        default = os_default,
                        help = os_help)

    op_default = "output.pdb"
    op_help = \
        "The output system's atomic coordinates as a PDB file. " \
        "The file will be written in the working directory. " \
        f"The default file name is '{op_default}'."
    parser.add_argument("-op", "--output-structure",
                        default = op_default,
                        help = op_help)

    ot_default = "trajectory.xtc"
    ot_help = \
        "The output trajectory for the simulation as an XTC " \
        "file. The file will be written in the working " \
        f"directory. The default file name is '{ot_default}'. " \
        "The options used to write this file are specified " \
        "in the configuration file."
    parser.add_argument("-ot", "--output-trajectory",
                        default = ot_default,
                        help = ot_help)

    od_default = "state_data.csv"
    od_help = \
        "The output state data file for the simulation as a " \
        "CSV file. The file will be written in the working " \
        f"directory. The default file name is '{od_default}'. " \
        "The options used to write this file are specified " \
        "in the configuration file."
    parser.add_argument("-od", "--output-state-data",
                        default = od_default,
                        help = od_help)

    oc_default = "checkpoint.xml"
    oc_help = \
        "The checkpoint file for the simulation. It can be " \
        "either a XML file containing the serialized state " \
        "of the simulation (portable) or a CHK checkpoint " \
        "binary file (platform-dependent, but more thorough). " \
        "The file will be written in the working directory. " \
        f"The default file name is '{oc_default}'. The options " \
        "used to write this file are specified in the " \
        "configuration file."
    parser.add_argument("-oc", "--output-checkpoint",
                        default = oc_default,
                        help = oc_help)

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

    lf_default = "log.txt"
    lf_help = \
        "The name of the TXT log file. The file wil be " \
        "written in the working directory. The default " \
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
    output_trajectory = args.output_trajectory
    output_state_data = args.output_state_data
    output_checkpoint = args.output_checkpoint
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

        config = ioutil.load_config(config_file = config_file)

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
        
        system = ioutil.load_system(input_xml = input_system)

    # If something went wrong
    except Exception as e:

        # Log it and exit
        errstr = \
            "It was not possible to load the system from " \
            f"'{input_system}'."
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
            ioutil.load_system_coordinates(input_pdb = input_structure)

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


    #------------------ Set the system's restraints ------------------#


    # If there is a section for restraints in the configuration
    if config.get("restraints") is not None:

        # Get the section of the configuration for restraints
        config_restr = config["restraints"]

        # For each restraint defined
        for restraint in config_restr:

            # Get the current restraint's type
            restraint_type = \
                config_restr[restraint]["restraint_type"]

            # Get the curren restraint's options
            restraint_options = \
                config_restr[restraint]["restraint_options"]

            # Add the restraint to the system
            system = \
                restraints.add_restraint(\
                    system = system,
                    mod = mod,
                    restraint_type = restraint_type,
                    restraint_options = restraint_options)


    #---------------------- Set the themorstat -----------------------#


    # If there is a section for the thermostat in the configuration
    if config.get("thermostat") is not None:

        # Get the section of the configuration for the thermostat
        config_thermo = config["thermostat"]

        # Get the name of the thermostat
        thermo_name = config_thermo["name"]

        # Get where the thermostat is from
        thermo_is_from = config_thermo["is_from"]

        # Get the options to set up the thermostat
        thermo_options = config_thermo["options"]

        # Add the thermostat to the system
        system = \
            thermostats.add_thermostat(system = system,
                                       name = thermo_name,
                                       is_from = thermo_is_from,
                                       options = thermo_options)

        # Inform the user that the thermostat was added
        infostr = \
            "The thermostat was successfully added to the " \
            f"system ('{thermo_name}' from '{thermo_is_from}')."
        logger.info(infostr)


    #----------------------- Set the barostat ------------------------#


    # If there is a section for the barostat in the configuration
    if config.get("barostat") is not None:

        # Get the section of the configuration for the barostat
        config_bar = config["barostat"]

        # Get the name of the barostat
        bar_name = config_bar["name"]

        # Get where the barostat is from
        bar_is_from = config_bar["is_from"]

        # Get the options to set up the barostat
        bar_options = config_bar["options"]

        # Add the barostat to the system
        system = \
            barostats.add_barostat(system = system,
                                   name = bar_name,
                                   is_from = bar_is_from,
                                   options = bar_options)

        # Inform the user that the barostat was added
        infostr = \
            "The barostat was successfully added to the " \
            f"system ('{bar_name}' from '{bar_is_from}')."
        logger.info(infostr)


    #---------------------- Set the integrator -----------------------#


    # Get the configuration for the integrator
    config_integr = config["integrator"]

    # Get the name of the integrator
    integr_name = config_integr["name"]

    # Get where the integrator is from
    integr_is_from = config_integr["is_from"]

    # Get the options to set up the integrator
    integr_options = config_integr["options"]

    # Set the integrator
    integrator = \
        integrators.get_integrator(name = integr_name,
                                   is_from = integr_is_from,
                                   options = integr_options)

    # Inform the user that the integrator was set
    infostr = \
        "The integrator was successfully set " \
        f"('{integr_name}' from '{integr_is_from}')."
    logger.info(infostr)


    #---------------------- Run the simulation -----------------------#


    # Inform the user that the simulation is starting
    infostr = "Starting the simulation..."
    logger.info(infostr)

    # Run the simulation      
    system_updated, mod_updated = \
        md.run_simulation(\
            system = system,
            mod = mod,
            integrator = integrator,
            n_steps = config["run"]["n_steps"],
            trajectory_file = output_trajectory,
            state_data_file = output_state_data,
            checkpoint_file = output_checkpoint,
            trajectory_options = config["trajectory"],
            state_data_options = config["state_data"],
            checkpoint_options = config["checkpoint"])

    # Inform the user that the simulation finished successfully
    infostr = "The simulation finished successfully."
    logger.info(infostr)


    #------------------------ Save the system ------------------------#


    # Set the path to the output XML file
    output_system_path = os.path.join(wd, output_system)

    # Try to write the serialized system
    try:
        
        ioutil.save_system(system = system_updated,
                           output_xml = output_system_path)

    # If something went wrong
    except Exception as e:

        # Log it an exit
        errstr = \
            "It was not possible to save the final " \
            f"system in '{output_system_path}'. Error: {e}"
        logger.exception(errstr)
        sys.exit(errstr)

    # Inform the user that the final system was successfully saved
    infostr = \
        "The final system was successfully saved in " \
        f"'{output_system_path}'."


    #------------- Save the system's atomic coordinates --------------#


    # Set the path to the output structure
    output_structure_path = os.path.join(wd, output_structure)

    # Try to save the system's atomic coordinates
    try:
        
        ioutil.save_system_coordinates(\
            mod = mod_updated,
            output_pdb = output_structure_path)

    # If something went wrong
    except Exception as e:

        # Log it and exit
        errstr = \
            "It was not possible to save the atomic coordinates " \
            "of the final system in " \
            f"'{output_structure_path}'."
        logger.exception(errstr)
        sys.exit(errstr)

    # Inform the user that the coordinates of the final
    # system were successfully saved
    infostr = \
        "The atomic coordinates of the final system " \
        f"were successfully saved in '{output_structure_path}'."
    logger.info(infostr)