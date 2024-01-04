#!/usr/bin/env python
# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-

#    _util.py
#
#    Private utilities to load configurations.
#
#    Copyright (C) 2024 Valentina Sora 
#                       <sora.valentina1@gmail.com>
#
#    This software is released under the MIT license.


# Standard library
import copy


def recursive_merge(d1, 
                    d2):
    """Recursively merges two dictionaries. In case of identical
    keys, the values in the first dictionary take precedence.

    Parameters
    ----------
    d1 : ``dict``
        The first dictionary.

    d2 : ``dict``
        The second dictionary.

    Returns
    -------
    merged : ``dict``
        The merged dictionary.
    """

    # Initialize the merged dictionary to the second
    # dictionary
    merged = copy.deepcopy(d2)

    # For each key, value pair in the first dictionary
    for key, value in d1.items():

        # If the key is present also in the second dictionary
        if key in d2:

            # If the values associated to the key in both
            # dictionaries are dictionaries
            if isinstance(value, dict) \
            and isinstance(d2[key], dict):
                
                # Recurse through the dictionary
                merged[key] = \
                    recursive_merge(d1 = value,
                                    d2 = d2[key])
            
            # Otherwise
            else:
                
                # If the keys are the same, the value from d1
                # will take precedence
                merged[key] = value
        
        # If the key is not in the second dictionary
        else:
            
            # Add it to the result
            merged[key] = value

    # Return the merged dictionary
    return merged