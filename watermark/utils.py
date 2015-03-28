from __future__ import print_function, division

import logging
# Helper functions
import os

from watermark.logutils import log_start
from watermark.constants import Position

logger = logging.getLogger('watermark.utils')


@log_start(logger)
def get_new_filepath(file_path, new_path, ext=None):
    """
    Get image name from old path, and assigns to new path

    :param file_path:
    :param new_path:
    :param ext: extension of output file eg: jpg
    :return:
    """
    filename = os.path.basename(file_path)
    if ext is not None:
        _filename, _fileext = filename.rsplit('.', 1)
        if _fileext is not ext:
            _fileext = ext
            filename = '.'.join([_filename, _fileext])
    return os.path.join(new_path, filename)


def get_watermark_box(im, wmim, posy=Position.BOTTOM,
                      posx=Position.RIGHT, wmspacing=.037):
    """
    Get box sizes of watermark image and sends back box and location
    :param im:
    :param wmim:
    :param position:
    :param wmspacing: .037 default
    :return: tuple: Position of watermark eg : (12,
    """
    # TODO: Rethink about the calulation
    # TODO: Ensure watermark image is smaller than image
    # left, right, top, bottom = 0, 0, 0, 0

    delta_width = im.size[0] - wmim.size[0]
    delta_height = im.size[1] - wmim.size[1]

    width_spacing = wmspacing * im.size[0]
    height_spacing = wmspacing * im.size[1]

    if posx is Position.LEFT:
        left = width_spacing
        right = left + wmim.size[0]
    elif posx is Position.RIGHT:
        right = im.size[0] - width_spacing
        left = right - wmim.size[0]
    else:
        left = delta_width / 2
        right = im.size[0] - left

    if posy is Position.TOP:
        top = height_spacing
        bottom = top + wmim.size[1]
    elif posy is Position.BOTTOM:
        bottom = im.size[1] - height_spacing
        top = bottom - wmim.size[1]
    else:
        # CENTER
        top = delta_height / 2
        bottom = im.size[1] - top
    result = [left, top, right, bottom]
    # Validating
    for i, item in enumerate(result):
        if item < 0:
            raise ValueError(
                "Watermark image is larger than source image, Skipping")
        result[i] = int(round(item))
    return tuple(result)
