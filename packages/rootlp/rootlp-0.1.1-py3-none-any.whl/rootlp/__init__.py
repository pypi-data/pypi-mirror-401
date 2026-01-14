#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Date          : 2026-01-10
# Author        : Lancelot PINCET
# GitHub        : https://github.com/LancelotPincet
# Library       : rootLP

"""
A library that gathers root functions for custom script execution.
"""



# %% Lazy imports
from corelp import getmodule
__getattr__, __all__ = getmodule(__file__)



# %% Test function run
if __name__ == "__main__":
    from corelp import test
    test(__file__)