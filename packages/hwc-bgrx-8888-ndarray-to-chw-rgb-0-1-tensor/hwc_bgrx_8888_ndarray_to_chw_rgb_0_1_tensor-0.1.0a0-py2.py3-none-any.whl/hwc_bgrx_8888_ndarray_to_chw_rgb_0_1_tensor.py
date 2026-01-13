# Copyright (c) 2026 Jifeng Wu
# Licensed under the MIT License. See LICENSE file in the project root for full license information.
from numpy import ascontiguousarray, ndarray
from torch import Tensor


def hwc_bgrx_8888_ndarray_to_chw_rgb_0_1_tensor(
        hwc_brgx_8888_ndarray,  # type: ndarray
):
    # type: (...) -> Tensor
    chw_rgb_888_ndarray_view = hwc_brgx_8888_ndarray[..., 2::-1].transpose(2, 0, 1)
    chw_rgb_888_ndarray = ascontiguousarray(chw_rgb_888_ndarray_view)
    chw_rgb_0_1_tensor = Tensor(chw_rgb_888_ndarray)
    chw_rgb_0_1_tensor.div_(255)  # in-place normalization
    return chw_rgb_0_1_tensor
