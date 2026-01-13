# Copyright (c) 2026 Jifeng Wu
# Licensed under the MIT License. See LICENSE file in the project root for full license information.
from typing import Tuple

from cv2 import BORDER_CONSTANT, INTER_LINEAR, copyMakeBorder, resize as cv2_resize
from numpy import eye, matmul, ndarray


def copy_make_empty_border(
        hwc_ndarray,  # type: ndarray
        current_homogeneous_transformation_matrix,  # type: ndarray
        top,  # type: int
        bottom,  # type: int
        left,  # type: int
        right,  # type: int
):
    # type: (...) -> Tuple[ndarray, ndarray]
    dst = copyMakeBorder(
        hwc_ndarray,
        top,
        bottom,
        left,
        right,
        BORDER_CONSTANT
    )

    delta = eye(3)
    delta[0, 2] = left
    delta[1, 2] = top

    return dst, matmul(delta, current_homogeneous_transformation_matrix)


def resize_linear_interpolation(
        hwc_ndarray,  # type: ndarray
        current_homogeneous_transformation_matrix,  # type: ndarray
        width_scaling_factor,  # type: float
        height_scaling_factor,  # type: float
):
    dst = cv2_resize(
        hwc_ndarray,
        (0, 0),
        fx=width_scaling_factor,
        fy=height_scaling_factor,
        interpolation=INTER_LINEAR
    )

    delta = eye(3)
    delta[0, 0] = width_scaling_factor
    delta[1, 1] = height_scaling_factor

    return dst, matmul(delta, current_homogeneous_transformation_matrix)


def hwc_ndarray_letterbox(
        hwc_ndarray,  # type: ndarray
        current_homogeneous_transformation_matrix,  # type: ndarray
        width,  # type: int
        height,  # type: int
):
    # type: (...) -> Tuple[ndarray, ndarray]
    """
    Letterbox an HWC image to fit the target width and height while updating the homogeneous transformation matrix.

    Args:
        hwc_ndarray (ndarray): Input image as an HWC ndarray.
        current_homogeneous_transformation_matrix (ndarray): Current 3x3 homogeneous transformation matrix.
        width (int): Target width.
        height (int): Target height.

    Returns:
        Tuple[ndarray, ndarray]: Tuple containing:
            - The letterboxed image as an HWC ndarray.
            - The updated homogeneous transformation matrix.
    """
    old_height, old_width = hwc_ndarray.shape[:2]

    scaling_factor = min(height / old_height, width / old_width)

    unpad, unpad_cumulative_homogeneous_transformation_matrix = resize_linear_interpolation(
        hwc_ndarray=hwc_ndarray,
        current_homogeneous_transformation_matrix=current_homogeneous_transformation_matrix,
        width_scaling_factor=scaling_factor,
        height_scaling_factor=scaling_factor,
    )

    # Compute padding
    unpad_height, unpad_width = unpad.shape[:2]

    dh = (height - unpad_height) / 2
    dw = (width - unpad_width) / 2

    top = int(round(dh - 0.1))
    bottom = int(round(dh + 0.1))
    left = int(round(dw - 0.1))
    right = int(round(dw + 0.1))

    return copy_make_empty_border(
        hwc_ndarray=unpad,
        current_homogeneous_transformation_matrix=unpad_cumulative_homogeneous_transformation_matrix,
        top=top,
        bottom=bottom,
        left=left,
        right=right,
    )
