#!/usr/bin/env python
# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-

#    defaults.py
#
#    Default values to load files.
#
#    Copyright (C) 2023 Valentina Sora 
#                       <sora.valentina1@gmail.com>
#
#    This software is released under the MIT license.


# The names of physical quantities mapped to
# the name of their corresponding columns in
# 'state data' files
QUANTITIES2COLS = \
    {"step" : "Step",
     "time" : "Time (ps)",
     "potential_energy" : "Potential Energy (kJ/mole)",
     "kinetic_energy" : "Kinetic Energy (kJ/mole)",
     "total_energy" : "Total Energy (kJ/mole)",
     "temperature" : "Temperature (K)",
     "box_volume" : "Box Volume (nm^3)",
     "density" : "Density (g/mL)",
     "mass" : "Mass"}