######################################################################
# Image Velocimetry Python API
# Copyright (C) 2025 EDF
######################################################################

from .filters import *


def from_dict(input_dict: dict) -> list[FilterSimple]:
    """ Create filter from dictionary """
    list_filters = []
    if "velocimetry" in input_dict:
        list_dict = input_dict["velocimetry"]
        for f_dict in list_dict:
            fil = _one_from_dict(f_dict)
            if fil:
                list_filters.append(fil)
    else:
        fil = _one_from_dict(input_dict)
        if fil:
            list_filters.append(fil)
    return list_filters


##### INTERNAL FUNCTIONS #####
def _one_from_dict(f_dict: dict) -> FilterSimple | None:
    prop = f_dict["properties"]
    if f_dict["type"] == "FilterVelocityThreshold":
        return FilterVelocityThreshold(FilterVelocityThresholdParams
                                       (v_norm=prop["v_norm"], v_x=prop["v_x"], v_y=prop["v_y"]))
    elif f_dict["type"] == "FilterCorrelationThreshold":
        return FilterCorrelationThreshold(FilterCorrelationThresholdParams(c_min=prop["c_min"], c_max=prop["c_max"]))
    else:
        return None
