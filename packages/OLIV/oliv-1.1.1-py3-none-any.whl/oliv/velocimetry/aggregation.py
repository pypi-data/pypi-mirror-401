######################################################################
# Image Velocimetry Python API
# Copyright (C) 2025 EDF
######################################################################

from oliv.velocimetry.filters.base import *


class AggregationMethod(Enum):
    MEDIAN = auto()
    MEAN = auto()


@dataclass
class AggregationParams:
    """ Parameters class for time-average of velocimetry results"""
    method: AggregationMethod
    time_filter: list[bool] = field(default_factory=list)

def aggregate(res_in: VelocimetryResults, params: AggregationParams,
              filter_list: list[FilterSimple]) -> VelocimetryResults:

    """ Average matrice velocimetry results applying the list of filters """
    if len(params.time_filter) == res_in.n_times():
        time_filter = params.time_filter
    else:
        time_filter = [True] * res_in.n_times()

    communication.display("=== Aggregate results using method {} ===".format(str(params.method)))

    g_fil = global_filter(res_in, filter_list)

    res_out = VelocimetryResults(res_in.grid)
    for field_name in res_in.names:
        field_in = res_in.__getattribute__(field_name)
        field_out = np.zeros((1, field_in.shape[1]), dtype=field_in.dtype)

        for point in range(field_in.shape[1]):
            tmp = []

            for time in range(len(time_filter)):
                if time_filter[time] and g_fil.arr[time, point]:
                    tmp.append(field_in[time, point])
            if len(tmp) > 0:
                if params.method == AggregationMethod.MEDIAN:
                    if field_out.dtype == float:
                        field_out[0, point] = np.nanmedian(tmp)
                elif params.method == AggregationMethod.MEAN:
                    field_out[0, point] = np.nanmean(tmp)
            else:
                field_out[0, point] = 0

        res_out.__setattr__(field_name, field_out)
    communication.display("=== Done ===")
    return res_out
