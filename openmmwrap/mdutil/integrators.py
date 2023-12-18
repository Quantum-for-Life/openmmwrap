#!/usr/bin/env python
# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-

#    integrators.py
#
#    Utilities regarding the integrators.
#
#    Copyright (C) 2023 Valentina Sora 
#                       <sora.valentina1@gmail.com>
#
#    This software is released under the MIT license.


# Standard library
import logging as log
# Suppress warning messages from 'pymbar' that occur
# when importing the package
log.getLogger("pymbar").setLevel(log.ERROR)
# Third-party packages
import openmm
from openmm import unit
# openmmwrap
from . import _util


# Get the module's logger
logger = log.getLogger(__name__)


def get_openm_verlet_integrator(options):
    """Get OpenMM's ``VerletIntegrator``.

    Parameters
    ----------
    options : ``dict``
        The options to set the integrator.

    Returns
    -------
    ``openmm.openmm.VerletIntegrator``
        The integrator.
    """

    # Set the name of the object (= the integrator)
    # we are setting
    obj_name = "VerletIntegrator"


    #----------------------- Required settings -----------------------#


    # Get the step size to be used
    step_size = \
        _util.get_step_size(options = options,
                            obj_name = obj_name)


    #--------------------- Create the integrator ---------------------#


    # Create the integrator
    integrator = \
        openmm.VerletIntegrator(step_size)


    #----------------------- Optional settings -----------------------#


    # Set the distance tolerance within with constraints
    # are maintained, as a fraction of the constrained distance
    integrator = \
        _util.set_constraint_tolerance(options = options,
                                       obj_name = obj_name,
                                       obj = integrator)

    # Set the force groups to use during the integration
    integrator = \
         _util.set_integration_force_groups(options = options,
                                            obj_name = obj_name,
                                            obj = integrator)

    # Return the integrator
    return integrator


def get_openmm_langevin_integrator(options):
    """Get OpenMM's ``LangevinIntegrator``.

    Parameters
    ----------
    options : ``dict``
        The options to set the integrator.

    Returns
    -------
    ``openmm.openmm.LangevinIntegrator``
        The integrator.
    """

    # Set the name of the object (= the integrator)
    # we are setting
    obj_name = "LangevinIntegrator"


    #----------------------- Required settings -----------------------#


    # Get the temperature to be used
    temperature = \
        _util.get_temperature(options = options,
                              obj_name = obj_name)

    # Get the friction coefficient to be used
    friction_coeff = \
        _util.get_friction_coeff(options = options,
                                 obj_name = obj_name)

    # Get the step size to be used
    step_size = \
        _util.get_step_size(options = options,
                            obj_name = obj_name)


    #--------------------- Create the integrator ---------------------#


    # Create the integrator
    integrator = \
        openmm.LangevinIntegrator(\
            temperature,
            friction_coeff,
            step_size)


    #----------------------- Optional settings -----------------------#


    # Set the distance tolerance within which constraints are
    # maintained, as a fraction of the constrained distance
    integrator = \
        _util.set_constraint_tolerance(options = options,
                                       obj_name = obj_name,
                                       obj = integrator)
    
    # Set the force groups to use during the integration
    integrator = \
         _util.set_integration_force_groups(options = options,
                                            obj_name = obj_name,
                                            obj = integrator)

    # Set the seed to be used for the generation of random
    # numbers
    integrator = \
        _util.set_random_number_seed(options = options,
                                     obj_name = obj_name,
                                     obj = integrator)

    # Return the integrator
    return integrator


def get_openmm_langevin_middle_integrator(options):
    """Get OpenMM's ``LangevinMiddleIntegrator``.

    Parameters
    ----------
    options : ``dict``
        The options to set the integrator.

    Returns
    -------
    ``openmm.openmm.LangevinMiddleIntegrator``
        The integrator.
    """

    # Set the name of the object (= the integrator)
    # we are setting
    obj_name = "LangevinMiddleIntegrator"


    #----------------------- Required settings -----------------------#


    # Get the temperature to be used
    temperature = \
        _util.get_temperature(options = options,
                              obj_name = obj_name)

    # Get the friction coefficient to be used
    friction_coeff = \
        _util.get_friction_coeff(options = options,
                                 obj_name = obj_name)

    # Get the step size to be used
    step_size = \
        _util.get_step_size(options = options,
                            obj_name = obj_name)


    #--------------------- Create the integrator ---------------------#


    # Create the integrator
    integrator = \
        openmm.LangevinMiddleIntegrator(\
            temperature,
            friction_coeff,
            step_size)


    #----------------------- Optional settings -----------------------#


    # Set the distance tolerance within which constraints are
    # maintained, as a fraction of the constrained distance
    integrator = \
        _util.set_constraint_tolerance(options = options,
                                       obj_name = obj_name,
                                       obj = integrator)

    # Set the force groups to use during the integration
    integrator = \
         _util.set_integration_force_groups(options = options,
                                            obj_name = obj_name,
                                            obj = integrator)

    # Set the seed to be used for the generation of random
    # numbers
    integrator = \
         _util.set_random_number_seed(options = options,
                                      obj_name = obj_name,
                                      obj = integrator)

    # Return the integrator
    return integrator


def get_openmm_nose_hoover_integrator(options):
    """Get OpenMM's ``NoseHooverIntegrator``.

    Parameters
    ----------
    options : ``dict``
        The options to set the integrator.

    Returns
    -------
    ``openmm.openmm.NoseHooverIntegrator``
        The integrator.
    """

    # Set the name of the object (= the integrator)
    # we are setting
    obj_name = "NoseHooverIntegrator"


    #----------------------- Required settings -----------------------#


    # Get the step size to be used
    step_size = \
        _util.get_step_size(options = options,
                            obj_name = obj_name)


    #--------------------- Create the integrator ---------------------#


    # Create the integrator
    integrator = \
        openmm.NoseHooverIntegrator(\
            step_size)


    #-------------------------- Thermostats --------------------------#


    # For each thermostat defined
    for thermostat in options["thermostats"]:

        # Get the options for the current thermostat
        options_thermo = options["thermostats"][thermostat]

        # Get the target temperature
        temperature = \
            _util.get_temperature(\
                options = options_thermo,
                obj_name = obj_name)

        # Get the collision frequency
        collision_frequency = \
            _util.get_collision_frequency(\
                options = options_thermo,
                obj_name = obj_name)
    
        # Get the number of beads in the Nose-Hoover chain
        chain_length = \
            _util.get_chain_length(\
                options = options_thermo,
                obj_name = obj_name)

        # Get the number of steps in the multiple time step
        # chain propagation algorithm
        num_mts = \
            _util.get_num_mts(\
                options = options,
                obj_name = obj_name)

        # Get the number of terms in the Yoshida-Suzuki
        # multi-time step decomposition used in the chain
        # propagation algorithm
        num_yoshida_suzuki = \
            _util.get_num_yoshida_suzuki(\
                options = options,
                obj_name = obj_name)

        # If it is the thermostat for the entire system
        if thermostat == "full_system":

            # Add the full-system thermostat to the integrator
            integrator.addThermostat(\
                temperature,
                collision_frequency,
                chain_length,
                num_mts,
                num_yoshida_suzuki)

        # If it is a thermostat for a portion of the system
        else:

            # Get the thermostated particles
            thermostated_particles = \
                _util.get_thermostated_particles(\
                    options = options,
                    obj_name = obj_name)

            # Get the thermostated pairs
            thermostated_pairs = \
                _util.get_thermostated_pairs(\
                    options = options,
                    obj_name = obj_name)

            # Get the target temperature for each pair’s
            # relative motion
            relative_temperature = \
                _util.get_relative_temperature(\
                    options = options,
                    obj_name = obj_name)

            # Get the frequency of the interaction with
            # the heat bath for the pairs’ relative motion
            relative_collision_frequency = \
                _util.get_relative_collision_frequency(\
                    options = options,
                    obj_name = obj_name)

            # Add the thermostat to the integrator
            integrator.addSubsystemThermostat(\
                thermostated_particles,
                thermostated_pairs,
                temperature,
                collision_frequency,
                relative_temperature,
                relative_collision_frequency,
                chain_length,
                num_mts,
                num_yoshida_suzuki)


    #----------------------- Optional settings -----------------------#


    # Set the distance tolerance within which constraints are
    # maintained, as a fraction of the constrained distance
    integrator = \
        _util.set_constraint_tolerance(options = options,
                                       obj_name = obj_name,
                                       obj = integrator)

    # Set the force groups to use during the integration
    integrator = \
         _util.set_integration_force_groups(options = options,
                                            obj_name = obj_name,
                                            obj = integrator)

    # Set the maximum distance that a connected pair may stray
    # from each other, implemented using a hard wall
    integrator = \
        _util.set_maximum_pair_distance(options = options,
                                        obj_name = obj_name,
                                        obj = integrator)

    # Return the integrator
    return integrator


def get_openmm_brownian_integrator(options):
    """Get OpenMM's ``BrownianIntegrator``.

    Parameters
    ----------
    options : ``dict``
        The options to set the integrator.

    Returns
    -------
    ``openmm.openmm.BrownianIntegrator``
        The integrator.
    """

    # Set the name of the object (= the integrator)
    # we are setting
    obj_name = "BrownianIntegrator"


    #----------------------- Required settings -----------------------#


    # Get the temperature to be used
    temperature = \
        _util.get_temperature(options = options,
                              obj_name = obj_name)

    # Get the friction coefficient to be used
    friction_coeff = \
        _util.get_friction_coeff(options = options,
                                 obj_name = obj_name)

    # Get the step size to be used
    step_size = \
        _util.get_step_size(options = options,
                            obj_name = obj_name)


    #--------------------- Create the integrator ---------------------#


    # Create the integrator
    integrator = \
        openmm.BrownianIntegrator(\
            temperature,
            friction_coeff,
            step_size)


    #----------------------- Optional settings -----------------------#


    # Set the distance tolerance within which constraints are
    # maintained, as a fraction of the constrained distance
    integrator = \
        _util.set_constraint_tolerance(options = options,
                                       obj_name = obj_name,
                                       obj = integrator)

    # Set the force groups to use during the integration
    integrator = \
         _util.set_integration_force_groups(options = options,
                                            obj_name = obj_name,
                                            obj = integrator)
    
    # Set the seed to be used for the generation of random
    # numbers
    integrator = \
         _util.set_random_number_seed(options = options,
                                      obj_name = obj_name,
                                      obj = integrator)

    # Return the integrator
    return integrator


def get_openmm_variable_verlet_integrator(options):
    """Get OpenMM's ``VariableVerletIntegrator``.

    Parameters
    ----------
    options : ``dict``
        The options to set the integrator.

    Returns
    -------
    ``openmm.openmm.VariableVerletIntegrator``
        The integrator.
    """

    # Set the name of the object (= the integrator)
    # we are setting
    obj_name = "VariableVerletIntegrator"


    #----------------------- Required settings -----------------------#


    # Get the error tolerance to be used
    error_tolerance = \
        _util.get_error_tolerance(options = options,
                                  obj_name = obj_name)


    #--------------------- Create the integrator ---------------------#


    # Create the integrator
    integrator = \
        openmm.VariableVerletIntegrator(\
            error_tolerance)


    #----------------------- Optional settings -----------------------#


    # Set the step size
    integrator = \
        _util.set_step_size(options = options,
                            obj_name = obj_name,
                            obj = integrator)

    # Set the maximum step size the integrator will ever use
    integrator = \
        _util.set_maximum_step_size(options = options,
                                    obj_name = obj_name,
                                    obj = integrator)

    # Set the distance tolerance within which constraints are
    # maintained, as a fraction of the constrained distance
    integrator = \
        _util.set_constraint_tolerance(options = options,
                                       obj_name = obj_name,
                                       obj = integrator)

    # Set the force groups to use during the integration
    integrator = \
         _util.set_integration_force_groups(options = options,
                                            obj_name = obj_name,
                                            obj = integrator)

    # Return the integrator
    return integrator


def get_openmm_variable_langevin_integrator(options):
    """Get OpenMM's ``VariableLangevinIntegrator``.

    Parameters
    ----------
    options : ``dict``
        The options to set the integrator.

    Returns
    -------
    ``openmm.openmm.VariableLangevinIntegrator``
        The integrator.
    """

    # Set the name of the object (= the integrator)
    # we are setting
    obj_name = "VariableLangevinIntegrator"


    #----------------------- Required settings -----------------------#


    # Get the temperature to be used
    temperature = \
        _util.get_temperature(options = options,
                              obj_name = obj_name)

    # Get the friction coefficient to be used
    friction_coeff = \
        _util.get_friction_coeff(options = options,
                                 obj_name = obj_name)

    # Get the error tolerance to be used
    error_tolerance = \
        _util.get_error_tolerance(options = options,
                                  obj_name = obj_name)


    #--------------------- Create the integrator ---------------------#


    # Create the integrator
    integrator = \
        openmm.VariableLangevinIntegrator(\
            temperature,
            friction_coeff,
            error_tolerance)


    #----------------------- Optional settings -----------------------#


    # Set the step size
    integrator = \
        _util.set_step_size(options = options,
                            obj_name = obj_name,
                            obj = integrator)

    # Set the maximum step size the integrator will ever use
    integrator = \
        _util.set_maximum_step_size(options = options,
                                    obj_name = obj_name,
                                    obj = integrator)

    # Set the distance tolerance within which constraints are
    # maintained, as a fraction of the constrained distance
    integrator = \
        _util.set_constraint_tolerance(options = options,
                                       obj_name = obj_name,
                                       obj = integrator)

    # Set the force groups to use during the integration
    integrator = \
         _util.set_integration_force_groups(options = options,
                                            obj_name = obj_name,
                                            obj = integrator)

    # Set the seed to be used for the generation of random
    # numbers
    integrator = \
         _util.set_random_number_seed(options = options,
                                      obj_name = obj_name,
                                      obj = integrator)

    # Return the integrator
    return integrator


def get_integrator(name,
                   is_from,
                   options):
    """Get an integrator.

    Parameters
    ----------
    name : ``str``
        The name of the integrator.

    is_from : ``str``, {``"openmm"``, ``"openmmtools"``}
        Where the integrator comes from.

        So far, only integrators implemented
        in OpenMM are supported.

    options : ``dict``
        The options to be used to set the integrator.

    Returns
    -------
    The integrator.
    """
      
    # A dictionary mapping the name of the integrator
    # to the function setting it
    name2function = \
        {"openmm" : \
            {"VerletIntegrator" : \
                get_openm_verlet_integrator,
             "LangevinIntegrator" : \
                get_openmm_langevin_integrator,
             "LangevinMiddleIntegrator" : \
                get_openmm_langevin_middle_integrator,
             "NoseHooverIntegrator" : \
                get_openmm_nose_hoover_integrator,
             "BrownianIntegrator" : \
                get_openmm_brownian_integrator,
             "VariableVerletIntegrator" : \
                get_openmm_variable_verlet_integrator,
             "VariableLangevinIntegrator" : \
                get_openmm_variable_langevin_integrator}}

    # If the origin of the integrator is invalid
    if is_from not in name2function:

        # Raise an error
        errstr = \
            f"No integrators from '{is_from}' are " \
            "supported."
        raise ValueError(errstr)

    # If no such integrator is implemented
    if name not in name2function[is_from]:

        # Raise an error
        errstr = \
            f"The '{name}' integrator from '{is_from}' " \
            "has not been implemented yet or does not " \
            "exist."
        raise ValueError(errstr)

    # Get the setting function
    get_func = name2function[is_from][name]

    # Call the setting function with the given options
    return get_func(options)
