import numpy as np
from scipy.ndimage import convolve
from skimage.measure import label, regionprops

KERNEL_4 = np.array([
    [0, 1, 0],
    [1, 0, 1],
    [0, 1, 0],
], dtype=np.uint8)

KERNEL_8 = np.array([
    [1, 1, 1],
    [1, 0, 1],
    [1, 1, 1],
], dtype=np.uint8)


def get_degrees(skeleton_img: np.ndarray):
    """ skeleton image to degrees map """
    assert isinstance(skeleton_img, np.ndarray)
    assert skeleton_img.ndim == 2
    skeleton = (skeleton_img > 0).astype(np.uint8)
    degrees = convolve(skeleton, KERNEL_8, mode='constant', cval=0)
    degrees = degrees * skeleton
    return degrees


def get_regions(degree_map: np.ndarray):
    """ get endpoint/edge/branch regions via skimage.measure """
    canvas = np.zeros_like(degree_map)
    canvas[degree_map == 1] = 1
    endpoint_labels = label(canvas, connectivity=2)
    endpoint_regions = regionprops(endpoint_labels)

    canvas = np.zeros_like(degree_map)
    canvas[degree_map == 2] = 1
    edge_labels = label(canvas, connectivity=2)
    edge_regions = regionprops(edge_labels)

    canvas = np.zeros_like(degree_map)
    canvas[degree_map >= 3] = 1
    branch_labels = label(canvas, connectivity=2)
    branch_regions = regionprops(branch_labels)

    return endpoint_regions, edge_regions, branch_regions
