#!/usr/bin/env python
# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-

#    systemio.py
#
#    Utilities for I/O operations on systems.
#
#    Copyright (C) 2023 Valentina Sora 
#                       <sora.valentina1@gmail.com>
#
#    This software is released under the MIT license.


# Standard library
import logging as log
import os
# Third-party packages
from openmm.app import (
    modeller,
    pdbfile)
import openmm


# Get the module's logger
logger = log.getLogger(__name__)


def load_system(input_xml):
    """Load a serialized ``openmm.openmm.System`` object
    from an XML file.

    Parameters
    ----------
    input_xml : ``str``
        The XML file where the system is stored.

    Returns
    -------
    system : ``openmm.openmm.System``
        The system.
    """

    # Open the input file
    with open(input_xml) as f:

        # Load and return the system
        return openmm.XmlSerializer.deserialize(f.read())


def load_system_coordinates(input_pdb):
    """Load a system's atomic coordinates into an
    ``openmm.app.modeller.Modeller`` object from a
    PDB file.

    Parameters
    ----------
    input_pdb : ``str``
        The PDB file where the atomic coordinates
        are stored.

    Returns
    -------
    mod : ``openmm.app.modeller.Modeller``
        The ``Modeller`` object.
    """

    # Load the structure
    structure = pdbfile.PDBFile(file = input_pdb)

    # Create the 'Modeller' object
    mod = \
        modeller.Modeller(# The topology
                          structure.topology,
                          # The atom positions
                          structure.positions)

    # Return the 'Modeller' object
    return mod


def save_system(system,
                output_xml):
    """Save a serialized ``openmm.openmm.System`` object to
    an XML file.

    Parameters
    ----------
    system : ``openmm.openmm.System``
        The system to be saved.

    output_xml : ``str``
        The XML file where to save the system.
    """

    # Open the output file
    with open(output_xml, "w") as out:

        # Write out the system
        out.write(openmm.XmlSerializer.serialize(system))


def save_system_coordinates(mod,
                            output_pdb):
    """Save a system's atomic coordinates from a
    ``openmm.app.modeller.Modeller`` object to a
    PDB file.

    Parameters
    ----------
    mod : ``openmm.app.modeller.Modeller``
        The ``Modeller`` object containing the
        atomic coordinates for the system of interest.

    output_pdb : ``str``
        The PDB file where to save the coordinates.
    """

    pdbfile.PDBFile.writeFile(topology = mod.topology,
                              positions = mod.positions,
                              file = open(output_pdb, "w"),
                              keepIds = True)
