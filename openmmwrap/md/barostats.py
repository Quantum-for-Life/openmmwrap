#!/usr/bin/env python
# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-

#    barostats.py
#
#    Utilities regarding the barostats.
#
#    Copyright (C) 2023 Valentina Sora 
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


def get_openmm_monte_carlo_barostat(options):
    """Get OpenMM's ``MonteCarloBarostat``.

    Parameters
    ----------
    options : ``dict``
        The options to set the barostat.

    Returns
    -------
    ``openmm.openmm.MonteCarloBarostat``
        The barostat.
    """

    # Set the name of the object (= the barostat)
    # we are setting
    obj_name = "MonteCarloBarostat"


    #----------------------- Required settings -----------------------#


    # Get the pressure to be used
    pressure = \
        _util.get_pressure(options = options,
                           obj_name = obj_name)

    # Get the temperature to be used
    temperature = \
        _util.get_temperature(options = options,
                              obj_name = obj_name)


    #---------------------- Create the barostat ----------------------#


    # Create the barostat
    barostat = \
        openmm.MonteCarloBarostat(pressure,
                                  temperature)


    #----------------------- Optional settings -----------------------#


    # Set the frequency at which Monte Carlo pressure changes
    # should be attempted
    barostat = \
        _util.set_monte_carlo_frequency(options = options,
                                        obj_name = obj_name,
                                        obj = barostat)

    # Set the force group the barostat belongs to
    barostat = \
        _util.set_force_group(options = options,
                              obj_name = obj_name,
                              obj = barostat)

    # Set the seed to be used for the generation of random
    # numbers
    barostat = \
         _util.set_random_number_seed(options = options,
                                      obj_name = obj_name,
                                      obj = barostat)

    # Return the barostat
    return barostat


def get_openmm_monte_carlo_anisotropic_barostat(options):
    """Get OpenMM's ``MonteCarloAnisotropicBarostat``.

    Parameters
    ----------
    options : ``dict``
        The options to set the barostat.

    Returns
    -------
    ``openmm.openmm.MonteCarloAnisotropicBarostat``
        The barostat.
    """

    # Set the name of the object (= the barostat)
    # we are setting
    obj_name = "MonteCarloAnisotropicBarostat"


    #----------------------- Required settings -----------------------#


    # Get the pressure to be used
    pressure = \
        _util.get_pressure(options = options,
                           obj_name = obj_name)

    # Get the temperature to be used
    temperature = \
        _util.get_temperature(options = options,
                              obj_name = obj_name)

    # Get whether to scale the x-axis
    scale_x = \
        _util.get_scale_x(options = options,
                          obj_name = obj_name,
                          default = True)

    # Get whether to scale the y-axis
    scale_y = \
        _util.get_scale_y(options = options,
                          obj_name = obj_name,
                          default = True)

    # Get whether to scale the z-axis
    scale_z = \
        _util.get_scale_z(options = options,
                          obj_name = obj_name,
                          default = True)


    #---------------------- Create the barostat ----------------------#


    # Create the barostat
    barostat = \
        openmm.MonteCarloAnisotropicBarostat(\
            pressure,
            temperature,
            scale_x,
            scale_y,
            scale_z)


    #----------------------- Optional settings -----------------------#


    # Set the frequency at which Monte Carlo pressure changes
    # should be attempted
    barostat = \
        _util.set_monte_carlo_frequency(options = options,
                                        obj_name = obj_name,
                                        obj = barostat)

    # Set the force group the barostat belongs to
    barostat = \
        _util.set_force_group(options = options,
                              obj_name = obj_name,
                              obj = barostat)

    # Set the seed to be used for the generation of random
    # numbers
    barostat = \
         _util.set_random_number_seed(options = options,
                                      obj_name = obj_name,
                                      obj = barostat)

    # Return the barostat
    return barostat


def get_openmm_monte_carlo_membrane_barostat(options):
    """Get OpenMM's ``MonteCarloMembraneBarostat``.

    Parameters
    ----------
    options : ``dict``
        The options to set the barostat.

    Returns
    -------
    ``openmm.openmm.MonteCarloMembraneBarostat``
        The barostat.
    """

    # Set the name of the object (= the barostat)
    # we are setting
    obj_name = "MonteCarloMembraneBarostat"


    #----------------------- Required settings -----------------------#

    
    # Get the pressure to be used
    pressure = \
        _util.get_pressure(options = options,
                           obj_name = obj_name)

    # Get the surface tension to be used
    surface_tension = \
        _util.get_surface_tension(options = options,
                                  obj_name = obj_name)

    # Get the temperature to be used
    temperature = \
        _util.get_temperature(options = options,
                              obj_name = obj_name)

    # Get the mode according to which the x and y axes (the ones
    # assumed to contain the membrane) will be treated
    xy_mode = \
        _util.get_xy_mode(options = options,
                          obj_name = obj_name)

    # Get the mode according to which the z axis (the one assumed
    # to not contain the membrane) will be treated
    z_mode = \
        _util.get_z_mode(options = options,
                         obj_name = obj_name)


    #---------------------- Create the barostat ----------------------#


    # Create the barostat
    barostat = \
        openmm.MonteCarloMembraneBarostat(\
            pressure,
            surface_tension,
            temperature,
            xy_mode,
            z_mode)


    #----------------------- Optional settings -----------------------#


    # Set the frequency at which Monte Carlo pressure changes
    # should be attempted
    barostat = \
        _util.set_monte_carlo_frequency(options = options,
                                        obj_name = obj_name,
                                        obj = barostat)

    # Set the force group the barostat belongs to
    barostat = \
        _util.set_force_group(options = options,
                              obj_name = obj_name,
                              obj = barostat)

    # Set the seed to be used for the generation of random
    # numbers
    barostat = \
        _util.set_random_number_seed(options = options,
                                     obj_name = obj_name,
                                     obj = barostat)

    # Return the barostat
    return barostat


def get_barostat(name,
                 is_from,
                 options):
    """Get a barostat.

    name : ``str``
        The name of the barostat.

    is_from : ``str``, {``"openmm"``}
        Where the barostat comes from.

        So far, only barostats implemented
        in OpenMM are supported.

    options : ``dict``
        The options to be used to set the barostat.

    Returns
    -------
    The barostat.
    """

    # A dictionary mapping the name of the barostat
    # to the function getting it
    name2function = \
        {"openmm" : \
            {"MonteCarloBarostat" : \
                get_openmm_monte_carlo_barostat,
             "MonteCarloAnisotropicBarostat" : \
                get_openmm_monte_carlo_anisotropic_barostat,
             "MonteCarloMembraneBarostat" : \
                get_openmm_monte_carlo_membrane_barostat},
        }

    # If the origin of the barostat is invalid
    if is_from not in name2function:

        # Raise an error
        errstr = \
            f"No barostats from '{is_from}' are " \
            "supported."
        raise ValueError(errstr)

    # If no such barostat is implemented
    if name not in name2function[is_from]:

        # Raise an error
        errstr = \
            f"The '{name}' barostat from '{is_from}' " \
            "has not been implemented yet or does not " \
            "exist."
        raise ValueError(errstr)

    # Get the correct function to get the barostat
    get_func = name2function[is_from][name]

    # Get the barostat with the given options
    barostat = get_func(options)

    # Return the barostat
    return barostat


def add_barostat(system,
                 name,
                 is_from,
                 options):
    """Add a barostat to a system.

    Parameters
    ----------
    system : ``openmm.openmm.System``
        The system to add the barostat to.

    name : ``str``
        The name of the barostat.

    is_from : ``str``, {``"openmm"``}
        Where the barostat comes from.

        So far, only barostats implemented
        in OpenMM are supported.

    options : ``dict``
        The options to be used to set the barostat.

    Returns
    -------
    system : ``openmm.openmm.System``
        The system, with the barostat added.
    """
      
    # Get the barostat
    barostat = get_barostat(name = name,
                            is_from = is_from,
                            options = options)

    # Add the barostat to the system
    system.addForce(barostat)

    # Return the system
    return system
