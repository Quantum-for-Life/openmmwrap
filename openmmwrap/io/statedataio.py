#!/usr/bin/env python
# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-

#    statedataio.py
#
#    Utilities for I/O operations on 'state data' files obtained when
#    running a simulation.
#
#    Copyright (C) 2024 Valentina Sora 
#                       <sora.valentina1@gmail.com>
#
#    This software is released under the MIT license.


# Standard library
import logging as log
# Third-party packages
import pandas as pd


# Get the module's logger
logger = log.getLogger(__name__)


def load_state_data(input_csv,
                    sep = ","):
    """Load the 'state data' CSV file produced by a
    simulation.

    Parameters
    ----------
    input_csv : ``str``
        The input CSV file containing the 'state data'.

    sep : ``str``, ``","``
        The column separator in the input CSV file.

    Returns
    -------
    df : ``pandas.DataFrame``
        A data frame containing the 'state data'.
    """

    # Load the CSV file
    df = pd.read_csv(input_csv,
                     sep = sep,
                     header = 0,
                     index_col = False)

    # Format the first column correctly
    df.columns = \
        pd.Series(df.columns.str.lstrip("#\"").str.rstrip("\""))

    # Return the data frame
    return df



