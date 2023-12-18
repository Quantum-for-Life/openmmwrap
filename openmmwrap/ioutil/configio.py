#!/usr/bin/env python
# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-

#    configio.py
#
#    Utilities for I/O operations on configuration files.
#
#    Copyright (C) 2023 Valentina Sora 
#                       <sora.valentina1@gmail.com>
#
#    This software is released under the MIT license.


# Standard library
import copy
import logging as log
import os
import sys
# Third-party packages
import openmm
from openmm import unit
import yaml


# Get the module's logger
logger = log.getLogger(__name__)


#------------------------- Private functions -------------------------#


def _load_config_system(config):
    """Load the configuration for the 'system' section.

    Parameters
    ----------
    config : ``dict``
        The raw configuration for the section.

    Returns
    -------
    config_updated : ``dict``
        The updated configuration for the section.
    """

    # Create a copy of the configuration
    config_updated = copy.deepcopy(config)

    # If 'nonbondedMethod' was specified
    if config.get("nonbondedMethod") is not None:

        # Set it to the appropriate instance
        config_updated["nonbondedMethod"] = \
            getattr(sys.modules["openmm.app.forcefield"],
                    config["nonbondedMethod"])

    # If 'nonbondedCutoff' was specified
    if config.get("nonbondedCutoff") is not None:

        # Set it with the appropriate units
        config_updated["nonbondedCutoff"] = \
            config["nonbondedCutoff"] * unit.nanometer

    # If 'constraints' was specified
    if config.get("constraints") is not None:

        # Set it to the appropriate instance
        config_updated["constraints"] = \
            getattr(sys.modules["openmm.app.forcefield"],
                    config["constraints"])

    # Return the updated configuration
    return config_updated


def _load_config_solvation(config):
    """Load the configuration for the 'solvation' section.

    Parameters
    ----------
    config : ``dict``
        The raw configuration for the section.

    Returns
    -------
    config_updated : ``dict``
        The updated configuration for the section.
    """

    # Create a copy of the configuration
    config_updated = copy.deepcopy(config)

    # If 'padding' was specified
    if config.get("padding") is not None:

        # Set it with the appropriate units
        config_updated["padding"] = \
            config["padding"] * unit.nanometer

    # If 'ionicStrength' was specified
    if config.get("ionicStrength") is not None:

        # Set it with the appropriate units
        config_updated["ionicStrength"] = \
            config["ionicStrength"] * unit.molar

    # Return the updated configuration
    return config_updated


def _load_config_minimization(config):
    """Load the configuration for the 'minimization' section.

    Parameters
    ----------
    config : ``dict``
        The raw configuration for the section.

    Returns
    -------
    config_updated : ``dict``
        The updated configuration for the section.
    """

    # Create a copy of the configuration
    config_updated = copy.deepcopy(config)

    # If 'tolerance' was specified
    if config.get("tolerance") is not None:

        # Set it with the appropriate units
        config_updated["tolerance"] = \
            config["tolerance"] * \
                (unit.kilojoule / (unit.nanometer * unit.mole))

    # Return the updated configuration
    return config_updated


#------------------------- Public functions --------------------------#


def load_config(config_file):
    """Load the configuration from a YAML file.

    Parameters
    ----------
    config_file : ``str``
        The configuration file.
    """

    # Load the raw configuration
    config = yaml.safe_load(open(config_file, "r"))


    #---------------------------- System -----------------------------#


    # If there is a section for the system's creation in the
    # configuration
    if "system" in config:

        # Load the configuration for the section
        config["system"] = \
            _load_config_system(config = config["system"])


    #--------------------------- Solvation ---------------------------#


    # If there is a section for solvation in the configuration
    if "solvation" in config:

        # Load the configuration for the section
        config["solvation"] = \
            _load_config_solvation(config = config["solvation"])


    #------------------------- Minimization --------------------------#


    # If there is a section for energy minimization in the
    # configuration
    if "minimization" in config:

        # Load the configuration for the section
        config["minimization"] = \
            _load_config_minimization(config = config["minimization"])


    #--------------------- Updated configuration ---------------------#


    # Return the updated configuration
    return config