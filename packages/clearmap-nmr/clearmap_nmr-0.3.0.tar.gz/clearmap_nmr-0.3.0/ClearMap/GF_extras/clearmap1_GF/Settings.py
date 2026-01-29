#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module to set *ClearMap's* internal parameter and paths to external programs.


"""

import os


def clearMapPath():
    """Returns root path to the ClearMap software
    
    Returns:
        str: root path to ClearMap
    """
    fn = os.path.split(__file__)
    fn = os.path.abspath(fn[0]);
    return fn;

ClearMapPath = clearMapPath();
"""str: Absolute path to the ClearMap root folder"""