#!/usr/bin/env python
# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-

#    _util.py
#
#    Private utilities.
#
#    Copyright (C) 2023 Valentina Sora 
#                       <sora.valentina1@gmail.com>
#
#    This software is released under the MIT license.


# Standard library
import logging as log
# Third-party packages
import openmm
from openmm import unit


# Get the module's logger
logger = log.getLogger(__name__)


#------------------------------ Generic ------------------------------#


def get_option(options,
               option_name,
               obj_name,
               accepted_types,
               required = False,
               default = None,
               units = None):

    # Get the option's value
    option_value = options.get(option_name)

    # If no option was passed
    if option_value is None:

        # If there is a default value
        if default is not None:

            # If specific units were passed
            if units is not None:

                # Get the default value with the correct units
                default = default * units

            # Return the default value
            return default

        # If the option is required
        if required:

            # Raise an error
            errstr = \
                f"'{option_name}' must be defined to use " \
                f"'{obj_name}'."
            raise ValueError(errstr)

        # Return None
        return option_value

    # If the option's value is not of an accepted type
    if not isinstance(option_value, accepted_types):

        # Get a string represented the accepted types
        accepted_types_str = \
            ", ".join([f"'{t.__name__}'" for t in accepted_types])

        # Raise an error
        errstr = \
            f"'{option_name}' cannot be of type " \
            f"'{type(option_value)}'. Supported types are: " \
            f"{accepted_types}."
        raise TypeError(errstr)

    # If specific units were passed
    if units is not None:

        # Get the option's value with the correct units
        option_value = option_value * units

    # Return the option's value
    return option_value


#------------------ Getters (for required settings) ------------------#


def get_step_size(options,
                  obj_name,
                  obj_from = "openmm",
                  default = None):
    """Get the step size.
    """

    return get_option(options = options,
                      option_name = "step_size",
                      obj_name = obj_name,
                      accepted_types = (int, float),
                      required = True,
                      default = default,
                      units = unit.picosecond)


def get_temperature(options,
                    obj_name,
                    obj_from = "openmm",
                    default = None):
    """Get the target temperature.
    """

    return get_option(options = options,
                      option_name = "temperature",
                      obj_name = obj_name,
                      accepted_types = (int, float),
                      required = True,
                      default = default,
                      units = unit.kelvin)


def get_relative_temperature(options,
                             obj_name,
                             obj_from = "openmm",
                             default = None):
    """Get the target temperature for each pair’s relative motion.
    """

    return get_option(options = options,
                      option_name = "relative_temperature",
                      obj_name = obj_name,
                      accepted_types = (int, float),
                      required = True,
                      default = default,
                      units = unit.kelvin)


def get_error_tolerance(options,
                        obj_name,
                        obj_from = "openmm",
                        default = None):
    """Get the error tolerance.
    """

    return get_option(options = options,
                      option_name = "error_tolerance",
                      obj_name = obj_name,
                      accepted_types = (int, float),
                      required = True,
                      default = default)


def get_constraint_tolerance(options,
                             obj_name,
                             obj_from = "openmm",
                             default = None):
    """Get the constraint tolerance.
    """

    return get_option(options = options,
                      option_name = "constraint_tolerance",
                      obj_name = obj_name,
                      accepted_types = (int, float),
                      required = True,
                      default = default)


def get_friction_coeff(options,
                       obj_name,
                       obj_from = "openmm",
                       default = None):
    """Get the friction coefficient.
    """

    return get_option(options = options,
                      option_name = "friction_coeff",
                      obj_name = obj_name,
                      accepted_types = (int, float),
                      units = 1/unit.picosecond,
                      required = True,
                      default = default)


def get_collision_frequency(options,
                            obj_name,
                            obj_from = "openmm",
                            default = None):
    """Get the frequency of the interaction with the heat bath.
    """

    return get_option(options = options,
                      option_name = "collision_frequency",
                      obj_name = obj_name,
                      accepted_types = (int, float),
                      required = True,
                      default = default,
                      units = 1/unit.picosecond)


def get_relative_collision_frequency(options,
                                     obj_name,
                                     obj_from = "openmm",
                                     default = None):
    """Get the relative frequency of the interaction with the
    heat bath for the pairs’ relative motion.
    """

    return get_option(options = options,
                      option_name = "relative_collision_frequency",
                      obj_name = obj_name,
                      accepted_types = (int, float),
                      required = True,
                      default = default,
                      units = 1/unit.picosecond)


def get_chain_length(options,
                     obj_name,
                     obj_from = "openmm",
                     default = 3):
    """Get the number of beads in the Nose-Hoover chain.
    """

    return get_option(options = options,
                      option_name = "chain_length",
                      obj_name = obj_name,
                      accepted_types = (int,),
                      required = True,
                      default = default)

def get_num_mts(options,
                obj_name,
                obj_from = "openmm",
                default = 3):
    """Get the number of steps in the multiple time step
    chain propagation algorithm.
    """

    return get_option(options = options,
                      option_name = "num_mts",
                      obj_name = obj_name,
                      accepted_types = (int,),
                      required = True,
                      default = default)


def get_num_yoshida_suzuki(options,
                           obj_name,
                           obj_from = "openmm",
                           default = 7):
    """Get the number of terms in the Yoshida-Suzuki
    multi-time step decomposition used in the chain
    propagation algorithm (must be 1, 3, 5, or 7).
    """

    return get_option(options = options,
                      option_name = "num_yoshida_suzuki",
                      obj_name = obj_name,
                      accepted_types = (int,),
                      required = True,
                      default = default)


def get_thermostated_particles(options,
                               obj_name,
                               obj_from = "openmm",
                               default = None):
    """Get the list of IDs of the particles to be
    thermostated.
    """

    return get_option(options = options,
                      option_name = "thermostated_particles",
                      obj_name = obj_name,
                      accepted_types = (list,),
                      required = True,
                      default = default)


def get_thermostated_pairs(options,
                           obj_name,
                           obj_from = "openmm",
                           default = None):
    """Get the list of pairs of connected atoms whose
    absolute center of mass motion and motion relative
    to one another will be independently thermostated.
    """

    return get_option(options = options,
                      option_name = "thermostated_pairs",
                      obj_name = obj_name,
                      accepted_types = (list,),
                      required = True,
                      default = None)


def get_pressure(options,
                 obj_name,
                 obj_from = "openmm",
                 default = None):
    """Get the target pressure.
    """

    return get_option(options = options,
                      option_name = "pressure",
                      obj_name = obj_name,
                      accepted_types = (int, float, list),
                      required = True,
                      default = default,
                      units = unit.bar)


def get_surface_tension(options,
                        obj_name,
                        obj_from = "openmm",
                        default = None):
    """Get the surface tension.
    """

    return get_option(options = options,
                      obj_name = obj_name,
                      accepted_types = (int, float),
                      required = True,
                      default = default,
                      units = unit.bar * unit.nanometer)


def get_scale_x(options,
                obj_name,
                obj_from = "openmm",
                default = True):
    """Get whether to scale the x-axis - for barostats.
    """
    
    return get_option(options = options,
                      option_name = "scale_x",
                      obj_name = obj_name,
                      accepted_types = (bool,),
                      required = True,
                      default = default)


def get_scale_y(options,
                obj_name,
                obj_from = "openmm",
                default = True):
    """Get whether to scale the y-axis - for barostats.
    """

    return get_option(options = options,
                      option_name = "scale_y",
                      obj_name = obj_name,
                      accepted_types = (bool,),
                      required = True,
                      default = default)


def get_scale_z(options,
                obj_name,
                obj_from = "openmm",
                default = True):
    """Get whether to scale the z-axis - for barostats.
    """

    return get_option(options = options,
                      option_name = "scale_z",
                      obj_name = obj_name,
                      accepted_types = (bool,),
                      required = True,
                      default = default)


def get_xy_mode(options,
                obj_name,
                obj_from = "openmm",
                default = None):
    """Set the mode according to which the x- and y-axes will be
    treated - only for OpenMM's Monte Carlo membrane barostat,
    so far.
    """

    # Get the mode
    xy_mode = \
         get_option(options = options,
                    option_name = "xy_mode",
                    obj_name = obj_name,
                    accepted_types = (str,),
                    required = True,
                    default = default)

    # If the X and Y axes should be always scaled by the same amount,
    # so that the ratio of their lengths remains constant
    if xy_mode == "XYIsotropic":

        # Set it
        xy_mode = openmm.MonteCarloMembraneBarostat.XYIsotropic

    # If the X and Y axes are allows to vary independently of
    # each other
    elif xy_mode == "XYAnisotropic":

        # Set it
        xy_mode = openmm.MonteCarloMembraneBarostat.XYAnisotropic

    # If an invalid value was passed
    else:

        # Raise an error
        errstr = \
            f"'{xy_mode}' is an invalid value for 'xy_mode'. " \
            "Supported values are: 'XYIsotropic' and 'XYAnisotropic'."
        raise ValueError(errstr)

    # Return the mode
    return xy_mode


def get_z_mode(options,
               obj_name,
               obj_from = "openmm",
               default = None):
    """Set the mode according to which the z-axis will be
    treated - only for OpenMM's Monte Carlo membrane barostat,
    so far.
    """

    # Get the mode
    z_mode = \
         get_option(options = options,
                    option_name = "z_mode",
                    obj_name = obj_name,
                    accepted_types = (str,),
                    required = True,
                    default = default)

    # If the Z axis should be allowed to vary freely, independent
    # of the other two axes
    if z_mode == "ZFree":
        
        # Set it
        z_mode = openmm.MonteCarloMembraneBarostat.ZFree

    # If the Z axis should be held fixed
    elif z_mode == "ZFixed":
        
        # Set it
        z_mode = openmm.MonteCarloMembraneBarostat.ZFixed

    # If the Z axis should always be scaled in inverse proportion
    # to the other two axes so that the volume of the box remains
    # fixed
    elif z_mode == "ConstantVolume":
        
        # Set it
        z_mode = openmm.MonteCarloMembraneBarostat.ConstantVolume

    # If an invalid value was passed
    else:

        # Raise an error
        errstr = \
            f"'{z_mode}' is an invalid value for 'z_mode'. " \
            "Supported values are: 'ZFree', 'ZFixed', and " \
            "'ConstantVolume'."
        raise ValueError(errstr)

    # Return the mode
    return z_mode


#------------------ Setters (for optional settings) ------------------#


def set_step_size(options,
                  obj_name,
                  obj,
                  obj_from = "openmm"):
    """Set the step size.
    """
    
    # Get the step size
    step_size = \
        get_option(options = options,
                   option_name = "step_size",
                   obj_name = obj_name,
                   accepted_types = (int, float),
                   units = unit.picosecond)

    # If a step size was passed
    if step_size is not None:

        # Set it
        obj.setStepSize(step_size)

    # Return the object
    return obj


def set_maximum_step_size(options,
                          obj_name,
                          obj,
                          obj_from = "openmm"):
    """Set the maximum step size.
    """
    
    # Get the maximum step size
    maximum_step_size = \
        get_option(options = options,
                   option_name = "maximum_step_size",
                   obj_name = obj_name,
                   accepted_types = (int, float),
                   units = unit.picosecond)

    # If the maximum step size was passed
    if maximum_step_size is not None:

        # Set it
        obj.setMaximumStepSize(maximum_step_size)

    # Return the object
    return obj


def set_friction_coeff(options,
                       obj_name,
                       obj,
                       obj_from = "openmm"):
    """Set the friction coefficient.
    """

    # Get the friction coefficient
    friction_coeff = \
        get_option(options = options,
                   option_name = "friction_coeff",
                   obj_name = obj_name,
                   accepted_types = (int, float),
                   units = 1/unit.picosecond)

    # If a friction coefficient was passed
    if friction_coeff is not None:

        # Set it
        obj.setFriction(friction_coeff)

    # Return the object
    return obj


def set_constraint_tolerance(options,
                             obj_name,
                             obj,
                             obj_from = "openmm"):
    """Set the constraint tolerance.
    """

    # Get the constraint tolerance
    constraint_tolerance = \
        get_option(options = options,
                   option_name = "constraint_tolerance",
                   obj_name = obj_name,
                   accepted_types = (int, float))

    # If a constraint tolerance was passed
    if constraint_tolerance is not None:

        # Set it
        obj.setConstraintTolerance(constraint_tolerance)

    # Return the object
    return obj


def set_random_number_seed(options,
                           obj_name,
                           obj,
                           obj_from = "openmm"):
    """Set the seed for the generation of random numbers.
    """

    # Get the seed for the generation of random numbers
    random_number_seed = \
        get_option(options = options,
                   option_name = "random_number_seed",
                   obj_name = obj_name,
                   accepted_types = (int,))

    # If a seed was passed
    if random_number_seed is not None:

        # Set it
        obj.setRandomNumberSeed(random_number_seed)

    # Return the object
    return obj


def set_force_group(options,
                    obj_name,
                    obj,
                    obj_from = "openmm"):
    """Set the force group.
    """

    # Get the force group
    force_group = \
        get_option(options = options,
                   option_name = "force_group",
                   obj_name = obj_name,
                   accepted_types = (int,))

    # If a force group was passed
    if force_group is not None:

        # Set it
        obj.setForceGroup(force_group)

    # Return the object
    return obj


def set_integration_force_groups(options,
                                 obj_name,
                                 obj,
                                 obj_from = "openmm"):
    """Set the force groups to be used during the integration.
    """

    # Get the force groups to be used during the integration
    integration_force_groups = \
         get_option(options = options,
                    option_name = "integration_force_groups",
                    obj_name = obj_name,
                    accepted_types = (int, set))

    # If the force groups were passed
    if integration_force_groups is not None:

        # Set it
        obj.setIntegrationForceGroups(integration_force_groups)

    # Return the object
    return obj


def set_monte_carlo_frequency(options,
                              obj_name,
                              obj,
                              obj_from = "openmm"):
    """Set the frequency at which Monte Carlo pressure changes
    should be attempted - for barostats.
    """

    # Get the frequency
    frequency = \
        get_option(options = options,
                   option_name = "frequency",
                   obj_name = obj_name,
                   accepted_types = (int, float))

    # If the frequency was passed
    if frequency is not None:

        # Set it
        obj.setFrequency(frequency)

    # Return the object
    return obj


def set_maximum_pair_distance(options,
                              obj_name,
                              obj,
                              obj_from = "openmm"):
    """Set the maximum pair distance.
    """

    # Get the maximum pair distance
    maximum_pair_distance = \
        get_option(options = options,
                   option_name = "maximum_pair_distance",
                   obj_name = obj_name,
                   accepted_types = (int, float),
                   units = unit.nanometer)

    # If the maximum pair distance was passed
    if maximum_pair_distance is not None:

        # Set it
        obj.setMaximumPairDistance(maximum_pair_distance)

    # Return the object
    return obj
