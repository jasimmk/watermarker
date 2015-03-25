"""
Multiprocessing job distribution
"""
import logging

from PIL import Image

from .logutils import log_start
from .constants import RelativePosition
from .workflow import (
    post_process, image_watermark, resize, preprocess
)

logger = logging.getLogger('watermark.job')


@log_start(logger)
def job_function(input_img_path, output_dir, wm_img=None,
                 output_size=None, output_format=None,
                 wm_position=RelativePosition.BOTTOM_RIGHT):
    """
    A watermarking/resizing/conversion job is created and distributed between multiple processes

    :param input_image_path: Image file path eg: '/Users/xyz/abc.jpg'
    :param output_size: Output size either in (width, height) or (percentage)
    :param output_format: jpg, png or gif
    :param output_dir: Output directory
    :param wm_img: watermark image, PIL.Image object
    :param wm_position: Position of Watermark
    """
    try:
        input_img = preprocess(input_img_path)
        w_im = input_img

        posx, posy = RelativePosition.split(wm_position)
        if wm_img is not None:
            w_im = image_watermark(input_img, wm_img, posx=posx, posy=posy)
        # Image resizing flow
        if output_size:
            percent = None
            width = None
            height = None
            if len(output_size) == 1:
                percent = output_size[0]
            else:
                width, height = output_size

            w_im = resize(w_im, percent=percent, width=width,
                          height=height, resample=Image.ANTIALIAS,
                          keep_filename=True)
        post_process(w_im, output_dir, output_format)
    except Exception as e:
        logger.critical("%s" % e)
