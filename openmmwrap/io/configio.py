#!/usr/bin/env python
# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-

#    configio.py
#
#    Utilities for I/O operations on configuration files.
#
#    Copyright (C) 2024 Valentina Sora 
#                       <sora.valentina1@gmail.com>
#
#    This software is released under the MIT license.


# Standard library
import copy
import logging as log
import sys
# Third-party packages
import openmm
from openmm import unit
import yaml
# openmmwrap
from . import _util


# Get the module's logger
logger = log.getLogger(__name__)


#------------------------- Private functions -------------------------#


def _get_config_system_section(config):
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


def _get_config_solvation_section(config):
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


def _get_config_minimization_section(config):
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


def _get_config_output_section(config):
    """Load the configuration for the 'output' section of
    the plotting configuration.
    
    Parameters
    ----------
    config : ``dict``
        The raw configuration for the section.

    Returns
    -------
    config_updated : ``dict``
        The updated configuration for the section.
    """

    # The list of options to be ignored, if present
    OPTIONS_IGNORED = \
        ["fname", "format", "bbox_extra_artists", "pil_kwargs"]

    # Update the configuration
    config_updated = \
        {key : val for key, val in config.items() \
        if key not in OPTIONS_IGNORED}

    # Return the updated configuration
    return config_updated


def _get_config_title_section(config):
    """Load the configuration for the 'title' section of
    the plotting configuration.
    
    Parameters
    ----------
    config : ``dict``
        The raw configuration for the section.

    Returns
    -------
    config_updated : ``dict``
        The updated configuration for the section.
    """

    # The list of options to be ignored, if present
    OPTIONS_IGNORED = \
        ["clip_box", "clip_path", "figure",
         "path_effects", "text", "transform"]

    # Update the configuration
    config_updated = \
        {key : val for key, val in config.items() \
        if key not in OPTIONS_IGNORED}

    # Return the updated configuration
    return config_updated


def _get_config_axis_section(config):
    """Load the configuration for the 'xaxis' or 'yaxis' section
    of the plotting configuration.
    
    Parameters
    ----------
    config : ``dict``
        The raw configuration for the section.

    Returns
    -------
    config_updated : ``dict``
        The updated configuration for the section.
    """

    # The list of options to be ignored when setting the axis'
    # label, if present
    OPTIONS_IGNORED_LABEL = \
        ["clip_box", "clip_path", "figure", "label",
         "path_effects", "text", "transform"]

    # The list of options to be ignored when setting the ticks'
    # labels, if present
    OPTIONS_IGNORED_TICKLABELS = \
        ["labels", "clip_box", "clip_path", "figure", "label",
         "path_effects", "text", "transform"]

    # Create a copy of the configuration
    config_updated = copy.deepcopy(config)

    # If there is a 'label' section
    if "label" in config:

        # Remove unwated options
        config_updated["label"] = \
            {key : val for key, val in config["label"].items() \
            if key not in OPTIONS_IGNORED_LABEL}

    # If there is a 'ticklabels' section
    if "ticklabels" in config:

        # Remove unwanted options
        config_updated["ticklabels"] = \
            {key : val for key, val in config["ticklabels"].items() \
            if key not in OPTIONS_IGNORED_TICKLABELS}

    # Return the updated configuration
    return config_updated


def _get_config_lineplot_section(config):
    """Load the configuration for the 'lineplot' section
    of the plotting configuration.
    
    Parameters
    ----------
    config : ``dict``
        The raw configuration for the section.

    Returns
    -------
    config_updated : ``dict``
        The updated configuration for the section.
    """

    # The list of options to be ignored, if present
    OPTIONS_IGNORED = \
        ["x", "y", "data", "agg_filter", "clip_box", "clip_path",
         "figure", "label", "path_effects", "picker", "transform",
         "xdata", "ydata"]

    # Update the configuration
    config_updated = \
        {key : val for key, val in config.items() \
        if key not in OPTIONS_IGNORED}

    # Return the updated configuration
    return config_updated


def _get_config_lineplots(config):
    """Load the configuration to plot several line plots
    representing the quantities stored in a 'state data' file.

    Parameters
    ----------
    config : ``dict``
        The raw configuration.

    Returns
    -------
    config_updated : ``dict``
        The updated configuration.
    """

    # Create a copy of the configuration
    config_updated = copy.deepcopy(config)

    # Initialize the 'general' configuration (= valid
    # for all the line plots) to None
    config_general = None

    # For each line plot
    for plot in config:

        # If we are in the 'general' configuration
        if plot == "general":

            # Get the 'general' configuration
            config_general = config_updated.pop("general")

            # Go on to the next plot
            continue

        # If there is a 'general' configuration
        if config_general is not None:

            # Update the one for the current plot
            config_plot = \
                _util.recursive_merge(d1 = config[plot],
                                      d2 = config_general)

        # Otherwise
        else:

            # The configuration for the current plot
            # will just be the one reported in the
            # configuration
            config_plot = config[plot]

        # If there is a 'lineplot' section
        if "lineplot" in config_plot:

            # Load the configuration for the section
            config_updated[plot]["lineplot"] = \
                _get_config_lineplot_section(\
                    config = config_plot["lineplot"])

        # If there is a 'title' section
        if "title" in config_plot:

            # Load the configuration for the section
            config_updated[plot]["title"] = \
                _get_config_title_section(\
                    config = config_plot["title"])

        # If there is a 'xaxis' section
        if "xaxis" in config_plot:

            # Load the configuration for the section
            config_updated[plot]["xaxis"] = \
                _get_config_axis_section(\
                    config = config_plot["xaxis"])

        # If there is a 'yaxis' section
        if "yaxis" in config_plot:

            # Load the configuration for the section
            config_updated[plot]["yaxis"] = \
                _get_config_axis_section(\
                    config = config_plot["yaxis"])

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
            _get_config_system_section(\
                config = config["system"])


    #--------------------------- Solvation ---------------------------#


    # If there is a section for solvation in the configuration
    if "solvation" in config:

        # Load the configuration for the section
        config["solvation"] = \
            _get_config_solvation_section(\
                config = config["solvation"])


    #------------------------- Minimization --------------------------#


    # If there is a section for energy minimization in the
    # configuration
    if "minimization" in config:

        # Load the configuration for the section
        config["minimization"] = \
            _get_config_minimization_section(\
                config = config["minimization"])


    #--------------------- Updated configuration ---------------------#


    # Return the updated configuration
    return config


def load_config_plot(config_file):
    """Load the configuration from plotting from a YAML file.

    Parameters
    ----------
    config_file : ``str``
        The configuration file.
    """

    # The supported plot types
    PLOT_TYPES = ["lineplots"]

    # Format the supported plot types
    plot_types_str = ", ".join([f"'{t}'" for t in PLOT_TYPES])

    # Load the raw configuration
    config = yaml.safe_load(open(config_file, "r"))

    # Get the plot type
    plot_type = config.get("type")

    # If no plot type is specified in the configuration
    if plot_type is None:

        # Raise an error
        errstr = \
            "The plot 'type' must be specified in the configuration " \
            f"file. Supported plot types are: {plot_types_str}."
        raise ValueError(errstr)

    # If the plot type is invalid
    if plot_type not in PLOT_TYPES:

        # Raise an error
        errstr = \
            f"The plot type '{plot_type}' is invalid. Supported " \
            f"plot types are: {plot_types_str}."
        raise ValueError(errstr)


    #---------------------------- Output -----------------------------#


    # If there is a section for the output file
    if "output" in config:

        # Load the configuration for the section
        config["output"] = \
            _get_config_output_section(\
                config = config["output"])


    #--------------------------- Lineplots ---------------------------#


    # If the plot to be generates is 'lineplots'
    if plot_type == "lineplots":

        # Load the configuration for the plot
        config["plot"] = \
            _get_config_lineplots(\
                config = config["plot"])


    #--------------------- Updated configuration ---------------------#


    # Return the updated configuration
    return config

