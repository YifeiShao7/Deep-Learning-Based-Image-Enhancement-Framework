import cv2
import numpy as np
import PIL.Image as img

"""
Cutting the image
:param src_img: origin image
:param x_start: x starting point
:param x_end: x ending point
:param y_start: y starting point
:param y_end: y ending point
:return:
"""
def cutting_image(src_img, x_start, x_end, y_start, y_end):
    tmp_img = cv2.cvtColor(src_img, cv2.COLOR_BGR2RGB)
    tmp_img = tmp_img[y_start:y_end, x_start:x_end]

    return cv2.cvtColor(tmp_img, cv2.COLOR_RGB2BGR)

"""
Adjust lightness of the image
:param src_img: origin image
:param lightness_value: -100 - 100, expected lightness value
:return:
"""
def adjust_lightness(src_img, lightness_value):
    height, width, channel = src_img.shape

    empty_img = np.zeros([height, width, channel], src_img.dtype)
    cmb_img = cv2.addWeighted(src_img, 1, empty_img, 1, lightness_value)

    return cmb_img

"""
Adjust image to specified size
:param src_img: origin image
:param size: specified size
:return: 
"""
def compress_img(src_img, size):
    return cv2.resize(src_img, size, interpolation=cv2.INTER_AREA)

"""
Adjust image to specified ratio of contrast
:param src_img: origin image
:param contrast_value: specified contrast value (0-200, 100 in default)
:return: 
"""
def adjust_contrast(src_image, contrast_value):
    h, w, c = src_image.shape

    contrast_ratio = (contrast_value+100.0)/100.0

    blank_img = np.zeros([h,w,c], src_image.dtype)
    cmb_img = cv2.addWeighted(src_image, contrast_ratio, blank_img, 1-contrast_ratio, 1)
    return cmb_img

"""
Rotate the image to three kinds of form: 90degree clockwise(1), -90degree clockwise(2), 180degree(3)
:param src_img: origin image
:param transfer kind
:return: transformed image
"""
def rotate_transfer(src_img, type):
    if type == 1:
        result = np.rot90(src_img, -1)
        return result
    elif type == 2:
        result = np.rot90(src_img, 1)
        return result
    elif type == 3:
        result = np.rot90(src_img, -1)
        result = np.rot90(result, -1)
        return result

"""
Mirror the image to two kinds of form: horizontal mirror(1), vertical mirror(2)
:param src_img: origin image
:param transfer kind
:return transformed image
"""
def mirror_transfer(src_img, type):
    if type == 1:
        result = cv2.flip(src_img, 1)
    elif type == 2:
        result = cv2.flip(src_img, 0)
    return result

