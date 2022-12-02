#!/usr/bin/env python
# Copyright (c) 2022, openradar developers.
# Distributed under the MIT License. See LICENSE for more info.

"""
XRadar Accessors
================

To extend :py:class:`xarray:xarray.DataArray` and  :py:class:`xarray:xarray.Dataset`
xradar provides accessors which downstream libraries can hook into.

This module contains the functionality to create those accessors.

.. autosummary::
   :nosignatures:
   :toctree: generated/

   {}
"""

__all__ = ['create_xradar_dataarray_accessor']

__doc__ = __doc__.format('\n   '.join(__all__))

import sys

import datatree as dt
import xarray as xr

from .georeference import get_x_y_z, get_x_y_z_tree


def accessor_constructor(self, xarray_obj):
    self._obj = xarray_obj


def create_function(func):
    def function(self):
        return func(self._obj)

    return function


def create_methods(funcs):
    methods = {}
    for name, func in funcs.items():
        methods[name] = create_function(func)
    return methods


def create_xradar_dataarray_accessor(name, funcs):
    if sys.version_info < (3, 9):
        methods = {'__init__': accessor_constructor, **create_methods(funcs)}
    else:
        methods = {'__init__': accessor_constructor} | create_methods(funcs)
    cls_name = ''.join([name.capitalize(), 'Accessor'])
    accessor = type(cls_name, (object,), methods)
    return xr.register_dataarray_accessor(name)(accessor)


class XradarAccessor:
    """
    Common Datatree, Dataset, DataArray accessor functionality.
    """

    def __init__(self, xarray_obj: xr.Dataset | xr.DataArray | dt.DataTree):
        self.xarray_obj = xarray_obj


@xr.register_dataarray_accessor('xradar')
class XradarDataArrayAccessor(XradarAccessor):
    """Adds a number of xradar specific methods to xarray.DataArray objects."""

    def georeference(self) -> xr.DataArray:
        """
        Add georeference information
        """
        radar = self.xarray_obj
        return radar.pipe(get_x_y_z)


@xr.register_dataset_accessor('xradar')
class XradarDataSetAccessor(XradarAccessor):
    """Adds a number of xradar specific methods to xarray.DataArray objects."""

    def georeference(self) -> xr.DataArray:
        """
        Add georeference information
        """
        radar = self.xarray_obj
        return radar.pipe(get_x_y_z)


@dt.register_datatree_accessor('xradar')
class XradarDataTreeAccessor(XradarAccessor):
    """Adds a number of xradar specific methods to datatree.DataTree objects."""

    def georeference(self) -> dt.DataTree:
        radar = self.xarray_obj
        return radar.pipe(get_x_y_z_tree)
