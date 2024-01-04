#!/usr/bin/env python
# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-

#    md.py
#
#    Utilities for preparing and performing MD simulations.
#
#    Copyright (C) 2024 Valentina Sora 
#                       <sora.valentina1@gmail.com>
#
#    This software is released under the MIT license.


# Standard library
import logging as log
import os
# Suppress warning messages from 'pymbar' that occur
# when importing the package
log.getLogger("pymbar").setLevel(log.ERROR)
# Third-party packages
from mdtraj import reporters
from openff.toolkit.topology import Molecule
from openmm.app import (
    checkpointreporter,
    forcefield,
    modeller,
    pdbfile,
    simulation,
    statedatareporter)
import openmm
from openmm import unit
from openmmforcefields.generators import (
    GAFFTemplateGenerator,
    SMIRNOFFTemplateGenerator)


# Get the module's logger
logger = log.getLogger(__name__)


def get_force_field(force_fields_files = None,
                    force_field_param_file = None,
                    mol_files = None):
    """Get the force field.

    Parameters
    ----------
    force_field_files : ``list``, optional
        A list of XML files containing the force fields to
        be used as they are (no parametrization).

    force_field_param_file : ``str``, optional
        The XML file of the force field whose parameters
        will be use to parametrize the molecules provided
        with ``mol_files``, if any

    mol_files : ``list``, optional
        A list of SDF files containing the molecules to be
        parametrized.

    Returns
    -------
    force_field : ``openmm.app.forcefield.ForceField``
        The force field.
    """

    # Initialize the force field
    force_field = forcefield.ForceField(*force_fields_files)

    # If the user passed some molecules to be parametrized
    if mol_files is not None:

        # Create an empty list to store the molecules
        molecules = []


        #-------------------- Load the molecules ---------------------#


        # For each molecule's file
        for mol_file in mol_files:

            # Add the molecule to the list
            molecules.append(Molecule.from_file(mol_file))


        #----------------- Parametrize the molecules -----------------#


        # If the force field is a GAFF force field
        if force_field_param_file.startswith("gaff-"):

            # Create the residue template generator using the
            # GAFFTemplateGenerator
            template_gen = \
                GAFFTemplateGenerator(\
                    molecules = molecules,
                    forcefield = force_field_param_file)

        # Otherwise
        else:

            # Create the residue template generator using the
            # SMIRNOFFemplateGenerator
            template_gen = \
                SMIRNOFFTemplateGenerator(\
                    molecules = molecules,
                    forcefield = force_field_param_file)

        # Register the new templates to the force field used
        # for the protein and the water molecules
        force_field.registerTemplateGenerator(\
            template_gen.generator)

    # Return the force field
    return force_field


def get_system(pdb_file,
               force_field,
               sys_options = None,
               solv_options = None):
    """Get the system to simulate.

    Parameters
    ----------
    pdb_file : ``str``
        The PDB file containing the structure from which
        to create the system.

    force_field : ``openmm.app.forcefield.ForceField``
        The force field to use for creating the system.
    
    sys_options : ``dict``, optional
        A dictionary of options for creating the systems.

    solv_options : ``dict``, optional
        A dictionary of options to solvate the structure.

        If not provided, the structure will not be solvated.

    Returns
    -------
    system : ``openmm.openmm.System``
        The system to simulate.

    mod : ``openmm.app.modeller.Modeller``
        The ``Modeller`` object containing the system's
        topology and atomic positions
    """

    # Get the options to create the system
    sys_options = sys_options if sys_options is not None else {}

    # Get the options to solvate the system
    solv_options = solv_options if solv_options is not None else {}

    
    #---------------------- Load the structure -----------------------#


    # Load the structure from the PDB file
    structure = pdbfile.PDBFile(file = pdb_file)

    # Inform the user that the structure was successfully loaded
    infostr = \
        "The structure was successfully loaded from " \
        f"'{pdb_file}'."
    logger.info(infostr)

    # Create a modeller object for the structure
    mod = \
        modeller.Modeller(# The topology
                          structure.topology,
                          # The atom positions
                          structure.positions)


    #--------------------- Solvate the structure ---------------------#


    # If the structure should be solvated
    if solv_options:

        # Add the solvent
        mod.addSolvent(\
            # The force field to use to determine van der Waals
            # radii and atomic charges
            forcefield = force_field,
            # The user-supplied options
            **solv_options)


        # Inform the user that the solvation was performed
        infostr = "The structure was successfully solvated."
        logger.info(infostr)


    #----------------------- Create the system -----------------------#


    # Create the system. Notes:
    #
    # * The Ewald interpolation order is always 5: 
    #   https://github.com/openmm/openmm/issues/2567
    #
    # * OpenMM chooses the constraint algorithm to use
    #   for each part of the system automatically
    #   https://github.com/openmm/openmm/issues/3013
    system = \
        force_field.createSystem(\
            # The system's topology
            topology = mod.topology,
            # The user-provided options
            **sys_options)

    # Return the system and the modeller object containing the
    # solvated system
    return system, mod


def minimize_energy(system,
                    mod,
                    options):
    """Perform an energy minimization of a system using
    the BFGSM algorithm as implemented in OpenMM.

    Parameters
    ----------
    system : ``openmm.openmm.System``
        The system to be energy-minimized.

    mod : ``openmm.app.modeller.Modeller``
        A ``Modeller`` object containing the topology
        of the system and the atomic positions of all
        of the system's particles.

    options : ``dict``
        A dictionary of options used for the energy
        minimization (they are passed to the
        ``openmm.app.simulation.Simulation.minimizeEnergy``
        method).

    Returns
    -------
    system : ``openmm.openmm.System``
        The energy-minimized system.

    mod : ``openmm.app.modeller.Modeller``
        A ``Modeller`` object containing the topology
        of the energy-minimized system and the atomic
        positions of all of the system's particles.
    """

    # Create the integrator (it is necessary to create the
    # simulation object, but it is not used)
    integrator = \
        openmm.LangevinIntegrator(300 * unit.kelvin,
                                  1 / unit.picosecond,
                                  0.004 * unit.picosecond)

    # Create the 'Simulation' object
    sim = \
        simulation.Simulation(\
            # The system
            system = system,
            # The topology
            topology = mod.topology,
            # The integrator
            integrator = integrator)

    # Set the positions
    sim.context.setPositions(mod.positions)

    # Inform the user that the minimization is starting
    infostr = "Starting the energy minimization..."
    logger.info(infostr)

    # Perform energy minimization
    sim.minimizeEnergy(**options)

    # Inform the user that the minimization finished
    infostr = "The energy minimization finished successfully."
    logger.info(infostr)

    # Get the positions of the minimized structure
    final_positions = \
        sim.context.getState(getPositions = True).getPositions()

    # Create a new 'Modeller' object containing the final
    # atomic positions
    mod_updated = modeller.Modeller(topology = mod.topology,
                                    positions = final_positions)

    # Return the system and the updated modeller object
    return sim.context.getSystem(), mod_updated


def run_simulation(system,
                   mod,
                   integrator,
                   n_steps,
                   trajectory_file = None,
                   state_data_file = None,
                   checkpoint_file = None,
                   trajectory_options = None,
                   state_data_options = None,
                   checkpoint_options = None,
                   restart_from = None):
    """Run a simulation.

    Parameters
    ----------
    system : ``openmm.openmm.System``
        The system to be simulated.

    mod : ``openmm.app.modeller.Modeller``
        A ``Modeller`` object containing the topology
        of the system and the atomic positions of all
        of the system's particles.

    integrator : an OpenMM or OpenMM Tools integrator
        The integrator to be used.

    n_steps : ``int``
        The number of steps to perform.

    trajectory_file : ``str``, optional
        The XTC file where to write the simulation's
        trajectory. If not passed, no trajectory will
        be written.

    state_data_file : ``str``, optional
        The CSV file where to write the simulation's
        state data. If not passed, no state data will
        be written.

    checkpoint_file : ``str``, optional
        The file file containing the state of the
        simulation at the last checkpoint. It can be
        either a XML file (portable) or a binary file
        (platform-dependent but more thorough in the
        data stored).

    trajectory_options : ``dict``, optional
        A dictionary of options used when writing
        the trajectory. If a ``trajectory_file`` is
        passed, a set of ``trajectory_options`` must
        be passed, too. You can find the supported
        options in the OpenMM's documentation for the
        ``openmm.app.statedatareporter.StateDataReporter``
        class.

    state_data_options : ``dict``, optional
        A dictionary of options used when writing the
        state data. If a ``state_data_file`` is passed,
        a set of ``state_data_options`` must be passed,
        too. You can find the supported options in the
        MDTraj's documentation for the
        ``mdtraj.reporters.xtcreporter.XTCReporter``.

    checkpoint_options : ``dict``, optional
        A dictionary of options used when writing the
        checkpoint files. If a ``checkpoint_file``
        is passed, a set of ``checkpoint_options`` must
        be passed, too. You can find the supported
        options in the OpenMM's documentation for the
        ``openmm.app.checkpointreporter.CheckpointReporter``
        class.

    restart_from : ``str``, optional
        A checkpoint file to use to restart the simulation.

    Returns
    -------

    """


    #---------------------- Set the simulation -----------------------#


    # Create the 'Simulation' object
    sim = \
        simulation.Simulation(\
            # The system
            system = system,
            # The topology
            topology = mod.topology,
            # The integrator
            integrator = integrator)

    # If a trajectory file was specified
    if trajectory_file is not None:

        # If no options were specified
        if trajectory_options is None:

            # Raise an error
            errstr = \
                "If 'trajectory_file' is specified, " \
                "'trajectory_options' must be specified, too. " \
                "'trajectory_options' must contain the " \
                "options to be passed to the " \
                "'mdtraj.reporters.XTCReporter' constructor. " \
                "The supported options can be found here: " \
                "https://github.com/mdtraj/mdtraj/blob/1.9.9/" \
                "mdtraj/reporters/xtcreporter.py"
            raise ValueError(errstr)

        # Add the XTC reporter to the 'Simulation' object
        sim.reporters.append(\
            reporters.XTCReporter(\
                trajectory_file,
                **trajectory_options))

    # If a state data file was specified
    if state_data_file is not None:

        # If no options were specified
        if state_data_options is None:

            # Raise an error
            errstr = \
                "If 'state_data_file' is specified, " \
                "'state_data_options' must be specified, too. " \
                "'state_data_options' must contain the " \
                "options to be passed to the " \
                "'openmm.app.statedatareporter.StateDataReporter' " \
                "constructor. The supported options can be found " \
                "in the documentation of the class at: " \
                "http://docs.openmm.org/latest/api-python/" \
                "generated/openmm.app.statedatareporter."\
                "StateDataReporter.html"
            raise ValueError(errstr)

        # Add the state data reporter to the
        # 'Simulation' object
        sim.reporters.append(\
            statedatareporter.StateDataReporter(\
                state_data_file,
                **state_data_options))

    # If a checkpoint file was specified
    if checkpoint_file is not None:

        # If no options were specified
        if not checkpoint_options:

            # Raise an error
            errstr = \
                "If 'checkpoint_file' is specified, " \
                "'checkpoint_options' must be specified, too. " \
                "'checkpoint_options' must contain the options " \
                "to be passed to the " \
                "'openmm.app.checkpointreporter.CheckpointReporter' " \
                "constructor. The supported options can be found " \
                "in the documentation of the class at: " \
                "http://docs.openmm.org/latest/api-python/" \
                "generated/openmm.app.checkpointreporter."\
                "CheckpointReporter.html"
            raise ValueError(errstr)

        # If the checkpoint file should contain the
        # serialized state of the simulation
        if checkpoint_file.endswith(".xml"):

            # Add the corresponding option to the
            # dictionary of options
            checkpoint_options["writeState"] = True

        # If the checkpoint file should be a binary
        # checkpoint file
        elif checkpoint_file.endswith(".chk"):

            # Add the corresponding option to the
            # dictionary of options
            checkpoint_options["writeState"] = False

        # If an invalid format was passed
        else:

            # Guess the invalid format from the name
            # of the file
            _, file_ext = \
                os.path.splitext(checkpoint_file)

            # Raise an error
            errstr = \
                f"Invalid '{file_ext}' format for the " \
                f"checkpoint file '{checkpoint_file}'. Supported " \
                "formats are: '.xml' and '.chk'."
            raise ValueError(errstr)

        # Add the checkpoint reporter to the
        # 'Simulation' object
        sim.reporters.append(\
            checkpointreporter.CheckpointReporter(\
                checkpoint_file,
                **checkpoint_options))

    # Inform the user that the simulation was
    # successfully set up
    infostr = "The simulation was successfully set up."
    logger.info(infostr)


    #-------------------------- Restarting? --------------------------#


    # If we need to restart the simulation from a given file
    if restart_from is not None:

        # If we are restarting from a state file
        if restart_from.endswith(".xml"):

            # Load the state
            sim.loadState(restart_from)

        # If we are restarting from a checkpoint file
        elif restart_from.endswith(".chk"):

            # Load the checkpoint
            sim.loadCheckpoint(restart_from)

        # If an invalid file type was passed
        else:

            # Raise an error
            errstr = \
                "Only files with '.xml' or '.chk' extension " \
                "are supported as checkpoint files."
            raise TypeError(errstr)

    # Otherwise
    else:

        # Set the positions
        sim.context.setPositions(mod.positions)


    #------------------------------ Run ------------------------------#


    # Inform the user that the simulation is starting
    infostr = "Starting the simulation..."
    logger.info(infostr)

    # Run the simulation
    sim.step(n_steps)

    # Inform the user that the simulation finished
    infostr = "The simulation finished successfully."
    logger.info(infostr)

    # Get the positions of the final structure
    final_positions = \
        sim.context.getState(getPositions = True).getPositions()

    # Create a new 'Modeller' object containing the final
    # atomic positions
    mod_updated = modeller.Modeller(topology = mod.topology,
                                    positions = final_positions)

    # Return the system and the updated modeller object
    return sim.context.getSystem(), mod_updated