# Copyright (c) 2026 Jifeng Wu
# Licensed under the MIT License. See LICENSE file in the project root for full license information.
from numpy import ndarray
from PIL import Image


def hwc_bgrx_8888_ndarray_to_pil_image(
        hwc_bgrx_8888_ndarray, # type: ndarray
):
    # type: (...) -> Image
    """Convert an HWC BGR 888 or BGRX 8888 NumPy ndarray to an HWC RGB 888 PIL.Image, with the alpha/unused channel discarded."""
    hwc_rgb_888_ndarray_view = hwc_bgrx_8888_ndarray[:, :, 2::-1]
    pil_image = Image.fromarray(hwc_rgb_888_ndarray_view)
    return pil_image
