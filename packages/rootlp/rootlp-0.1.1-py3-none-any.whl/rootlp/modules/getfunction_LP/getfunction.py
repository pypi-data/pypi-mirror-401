#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Date          : 2026-01-11
# Author        : Lancelot PINCET
# GitHub        : https://github.com/LancelotPincet
# Library       : rootLP
# Module        : getmodule

"""
This function is to be used in a script source __init__ file It creates lazy imports of the module imported and defines __getattr__ and __all__ for this source.
"""



# %% Libraries
from pathlib import Path
import importlib



# %% Function
def getfunction(file) :
    '''
    This function is to be used in a script source __init__ file It creates lazy imports of the module imported and defines __getattr__ and __all__ for this source.
    
    Parameters
    ----------
    file : str
        __file__ string in the __init__.py file.

    Returns
    -------
    _getattr : function
        Function to replace __getattr__ variable.
    _all : list
        list of module names corresponding to __all__.

    Raises
    ------
    AttributeError
        When trying to import a module which is not in the library.

    Examples
    --------
    >>> from rootlp import getmodule
    ...
    >>> # In __init__.py file
    ... __getattr__, __all__ = getmodule(__file__)
    '''

    # Get paths
    file = Path(file)
    srcfolder = file.parent
    name = srcfolder.name

    # Function folders
    modules = {}
    for folder in srcfolder.iterdir() :
        if not folder.name.endswith('_functions') :
            continue
        for file in folder.iterdir() :
            if file.stem.startswith('__') or file.suffix != '.py':
                continue
            name = file.stem
            modules[name] = folder

    # Objects to return
    _lazy = {}
    _all = [module for module in modules]
    def _getattr(attr) :
        
        # Cached
        if attr in _lazy:
            return _lazy[attr]

        try :
            folder = modules.get(attr, None)
            if folder is None :
                raise KeyError(f"{attr} was not found in modules")
        except KeyError:
            raise AttributeError(f'module {name} has no attribute {attr}')

        mod = importlib.import_module(f"{name}.{folder}.{attr}")
        obj = getattr(mod, attr, None)
        if obj is None :
            raise AttributeError(f"module {name}.{folder}.{attr} has no attribute {attr}")
        _lazy[attr] = obj  # Cache it
        return obj

    return _getattr, _all



# %% Test function run
if __name__ == "__main__":
    from corelp import test
    test(__file__)