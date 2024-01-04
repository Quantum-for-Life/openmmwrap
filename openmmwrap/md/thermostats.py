#!/usr/bin/env python
# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-

#    thermostats.py
#
#    Utilities regarding the thermostats.
#
#    Copyright (C) 2024 Valentina Sora 
#                       <sora.valentina1@gmail.com>
#
#    This software is released under the MIT license.


# Standard library
import logging as log
# Third-party packages
import openmm
# openmmwrap
from . import _util


# Get the module's logger
logger = log.getLogger(__name__)


def get_openmm_andersen_thermostat(options):
    """Get OpenMM's ``AndersenThermostat``.

    Parameters
    ----------
    options : ``dict``
        The options to set the thermostat.

    Returns
    -------
    ``openmm.openmm.AndersenThermostat``
        The thermostat.
    """

    # Set the name of the object (= the thermostat)
    # we are setting
    obj_name = "AndersenThermostat"


    #----------------------- Required settings -----------------------#


    # Get the temperature to be used
    temperature = \
        _util.get_temperature(options = options,
                              obj_name = obj_name)

    # Set the frequency of the interaction with the heat bath
    collision_frequency = \
        _util.get_collision_frequency(options = options,
                                      obj_name = obj_name)


    #--------------------- Create the thermostat ---------------------#


    # Create the thermostat
    thermostat = \
        openmm.AndersenThermostat(\
            temperature,
            collision_frequency)


    #----------------------- Optional settings -----------------------#


    # Set the force group the thermostat belongs to
    thermostat = \
        _util.set_force_group(options = options,
                              obj_name = obj_name,
                              obj = thermostat)

    # Set the seed to be used for the generation of random
    # numbers
    thermostat = \
         _util.set_random_number_seed(options = options,
                                      obj_name = obj_name,
                                      obj = thermostat)

    # Return the thermostat
    return thermostat


def get_thermostat(name,
                   is_from,
                   options):
    """Get a thermostat.

    Parameters
    ----------
    name : ``str``
        The name of the thermostat.

    is_from : ``str``, {``"openmm"``}
        Where the thermostat comes from.

        So far, only thermostats implemented
        in OpenMM are supported.

    options : ``dict``
        The options to be used to set the thermostat.

    Returns
    -------
    The thermostat.
    """

    # A dictionary mapping the name of the thermostat
    # to the function getting it
    name2function = \
        {"openmm" : \
            {"AndersenThermostat" : \
                get_openmm_andersen_thermostat},
        }

    # If the origin of the thermostat is invalid
    if is_from not in name2function:

        # Raise an error
        errstr = \
            f"No thermostats from '{is_from}' are " \
            "supported."
        raise ValueError(errstr)

    # If no such thermostat is implemented
    if name not in name2function[is_from]:

        # Raise an error
        errstr = \
            f"The '{name}' thermostat from '{is_from}' " \
            "has not been implemented yet or does not " \
            "exist."
        raise ValueError(errstr)

    # Get the correct function to get the thermostat
    get_func = name2function[is_from][name]

    # Get the thermostat with the given options
    thermostat = get_func(options)

    # Return the thermostat
    return thermostat


def add_thermostat(system,
                   name,
                   is_from,
                   options):
    """Add a thermostat to a system.

    Parameters
    ----------
    system : ``openmm.openmm.System``
        The system to add the thermostat to.

    name : ``str``
        The name of the thermostat.

    is_from : ``str``, {``"openmm"``}
        Where the thermostat comes from.

        So far, only thermostats implemented
        in OpenMM are supported.

    options : ``dict``
        The options to be used to set the thermostat.

    Returns
    -------
    system : ``openmm.openmm.System``
        The system, with the thermostat added.
    """
      
    # Get the thermostat
    thermostat = get_thermostat(name = name,
                                is_from = is_from,
                                options = options)

    # Add the thermostat to the system
    system.addForce(thermostat)

    # Return the system
    return system