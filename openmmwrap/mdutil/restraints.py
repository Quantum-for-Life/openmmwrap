#!/usr/bin/env python
# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-

#    restraints.py
#
#    Utilities regarding restraints that can be applied
#    to the system.
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


def add_periodic_distance_restraint(system,
                                    mod,
                                    k):

    # Set the restraint's definition
    definition = "k * periodicdistance(x, y, z, x0, y0, z0)^2"

    # Create the restraint
    restraint = openmm.CustomExternalForce(definition)

    # Add the constraint to the system
    system.addForce(restraint)

    # Get the 'k' constant with the correct units
    k_value = \
        k * (unit.kilojoules_per_mole / \
             (unit.nanometer * unit.nanometer))

    # Add a global parameter storing the 'k' constant
    restraint.addGlobalParameter("k", k_value)

    # Add the particles' variables 'x0', 'y0', and 'z0'
    restraint.addPerParticleParameter("x0")
    restraint.addPerParticleParameter("y0")
    restraint.addPerParticleParameter("z0")

    # For each atom
    for atom in mod.topology.atoms():

        # Add the restraint to the atom
        restraint.addParticle(atom.index, mod.positions[atom.index])

    # Return the updated system
    return system


def add_restraint(system,
                  mod,
                  restraint_type,
                  restraint_options):
    
    # If we are adding a periodic distance restraints on atoms
    if restraint_type == "periodic_distance":

        # Update the system using the correct method
        system_updated = \
            add_periodic_distance_restraint(system = system,
                                            mod = mod,
                                            **restraint_options)

    # Return the updated system
    return system_updated



