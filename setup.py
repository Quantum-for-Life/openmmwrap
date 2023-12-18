#!/usr/bin/env python
# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-

#    setup.py
#
#    openmmwrap setup.
#
#    Copyright (C) 2023 Valentina Sora 
#                       <sora.valentina1@gmail.com>
#
#    This software is released under the MIT license.


# Standard library
from setuptools import setup


# The name of the project
name = "openmmwrap"

# The URL where to find the project
url = \
    f"https://github.com/Quantum-for-Life/{name}"

# The project's author(s)
author = "Valentina Sora"

# The project's version
version = "0.0.1"

# A brief description of the project
description = \
    "Wrapper for OpenMM and OpenFF utilities to run " \
    "and analyze molecular dynamics simulations."

# Which packages are included
packages = \
    ["openmmwrap",
     "openmmwrap.execs",
     "openmmwrap.ioutil",
     "openmmwrap.mdutil"]

# Command-line executables
entry_points = \
    {"console_scripts" : \
        [f"{name}-create-system = " \
         f"{name}.execs.{name}_create_system:main",
         f"{name}-minimize = " \
         f"{name}.execs.{name}_minimize:main",
         f"{name}-run = " \
         f"{name}.execs.{name}_run:main",
        ],
    }

# Run the setup
setup(name = name,
      url = url,
      author = author,
      version = version,
      description = description,
      packages = packages,
      entry_points = entry_points)