from __future__ import division

import logging
import glob
import os
from PIL import Image, ImageFont, ImageDraw

from watermark.logutils import log_start
from watermark.validator import FontValidator
from watermark.color import Color
from watermark.constants import (
    Size, Position,
    IMAGE_FORMATS, MASK_AVAILABLE_MODES
)
from watermark.utils import get_watermark_box, get_new_filepath


logger = logging.getLogger('watermark.workflow')


@log_start(logger)
def create_text_image(
        img_width, img_height,
        text, img_bg=None,
        font_color=None, font=None,
        font_size=Size.AUTO
):
    """
    Creates an image object from provided text

    :param img_width:
    :param img_height:
    :param text:
    :param img_bg:
    :param font_color:
    :param font:
    :param font_size:
    :return:
    """
    # For a cleaner text rendering, 4x image is created
    if img_bg is None:
        img_bg = Color.TRANSPARENT
    if font_color is None:
        color = Color('white')
        font_color = color.get_dec_rgba()
    if font is None:
        fv = FontValidator()
        font = fv(font_string=None)
    img_size = (img_width * 4, img_height * 4)
    img = Image.new("RGBA", img_size, img_bg)
    try:
        font_obj = ImageFont.truetype(font, size=font_size)
    except IOError:
        logging.critical("Error loading Font: %s" % font)
        raise
    if font_size is Size.AUTO:
        # REF: http://bit.ly/1BlAkg0
        while font_obj.getsize(text)[0] < img_size[0]:
            # iterate until the text size is just larger than the criteria
            font_size += 2
            font_obj = ImageFont.truetype(font, font_size)

        # optionally de-increment to be sure it is less than criteria
        font_size -= 2
        font_obj = ImageFont.truetype(font, font_size)

    draw = ImageDraw.Draw(img)
    draw.text((0, 0), text, font=font_obj, fill=font_color)
    img = resize(img, percent=25, resample=Image.ANTIALIAS)
    return img


def identify(path_or_file):
    """
    Accepts a single file or list of files, Returns a list of Image file names
    :param path_or_file:
    :return: list of Image file names
    """

    files = []

    # Included capitalized formats
    supported_formats = set(
        IMAGE_FORMATS[0] + tuple(map(lambda x: x.upper(), IMAGE_FORMATS[0])))
    if os.path.isdir(path_or_file):
        for img_format in supported_formats:
            files.extend(
                glob.iglob(os.path.join(path_or_file, '*.%s' % img_format)))
    elif os.path.isfile(path_or_file):
        # If its a single file, ignoring file extensions
        files = [path_or_file]
    if files:
        return files

    raise IOError(
        "%s: No image files have been scheduled for processing" % path_or_file)


def preprocess(img_file_path):
    """
    Accepts image file url, Opens image and converts to Pillow Intermediate

    :param :img_file - An image file path
    :return: Returns back a list of opne file descriptors
    """
    try:
        return Image.open(img_file_path)
    except IOError:
        logging.warning("Failed to add file %s" % img_file_path)


@log_start(logger)
def resize(im, percent=None, width=None, height=None,
           resample=Image.NEAREST, keep_filename=False):
    """
    Resizes images to certain percentage or defined width & height.
    If percent is defined, width and height gets ignored

    :param im:
    :param percent:
    :param width:
    :param height:
    :return: Image
    """
    filename = None
    if percent is not None:
        size = map(lambda x: int(round(x * percent / 100)), im.size)
        # size = [int(v * percent / 100) for v in im.size]
    else:
        size = (width, height)
    if keep_filename:
        filename = im.__dict__.get('filename')

    im = im.resize(size, resample=resample)
    if filename:
        im.__dict__['filename'] = filename
    return im


@log_start(logger)
def image_watermark(im, wmim, posy=Position.BOTTOM, posx=Position.RIGHT):
    """
    Creates an image watermark on the existing image

    :param im:
    :param wmim:
    :param posy:
    :param posx:
    :return: PIL.Image
    """
    # TODO: Avoid auto sizing

    rel_width, rel_height = im.size[0] / 4, im.size[1] / 8
    # Find feasible percentage
    rel_perc_width = (rel_width / wmim.size[0]) * 100
    rel_perc_height = (rel_height / wmim.size[1]) * 100

    # TODO: Need to swap?
    if rel_perc_width < rel_perc_height:
        percent = rel_perc_width
    else:
        percent = rel_perc_height

    wmim = resize(wmim, percent=percent)
    box = get_watermark_box(im, wmim, posx=posx, posy=posy)
    # TODO: Why no perfect boxing?
    box = box[:2]
    paste_args = (wmim, box)
    if wmim.mode in MASK_AVAILABLE_MODES:
        paste_args = (wmim, box, wmim)
    im.paste(*paste_args)
    return im


@log_start(logger)
def post_process(im, outdir, ext=None):
    """
    Post Process/Converts images from Image format to desired file format

    :param im:
    :param outfile:
    :param ext:
    :return:
    """
    im_filename = im.__dict__.get('filename')

    new_image_path = get_new_filepath(im_filename, outdir, ext)
    logger.info("Saving output image at: %s" % new_image_path)
    im.save(new_image_path)
