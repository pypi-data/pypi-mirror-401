import numpy as np


def cal_points_length(points: np.ndarray) -> float:
    """
    cal edge length.
    For example: \n
    [ \n
    0 0 0 0 \n
    0 1 0 0 \n
    0 1 0 0 \n
    0 0 1 0 \n
    ] \n
    length = 1 + 1 + sqrt(2) = 3.414
    """
    if len(points) == 0:
        return 0.
    elif len(points) == 1:
        return 1.
    else:
        diffs = np.diff(points, axis=0)
        distances = np.sqrt(np.sum(diffs ** 2, axis=1))
        return float(np.sum(distances)) + 1.
