import cv2
import numpy as np
import os


def imread(path: str, flag: int = 0):
    if not os.path.exists(path):
        raise RuntimeError('File does not exist.')

    try:
        img_array = np.fromfile(path, dtype=np.uint8)
        img = cv2.imdecode(img_array, flag)
    except Exception as e:
        raise RuntimeError(f'Error occurred while reading the image: {e}')

    return img


def imwrite(img: np.ndarray, path: str):
    try:
        ext = os.path.splitext(path)[1]
        rst, img_array = cv2.imencode(ext, img)
        if rst:
            img_array.tofile(path)
        else:
            raise RuntimeError('Error occurred while saving the image')
    except Exception as e:
        raise RuntimeError(f'Error occurred while saving the image: {e}')


def imshow(img: np.ndarray):
    cv2.imshow('Show', img)
    cv2.waitKey(0)

