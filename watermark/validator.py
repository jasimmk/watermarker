"""
All the validation classes
"""
import argparse
import os

from PIL import ImageFont
from watermark.color import Color


DEFAULT_FONTS = ['arial', 'Ubuntu-M', 'Times New Roman']


class FontValidator(object):
    def __call__(self, font_string):
        if font_string:
            try:
                ImageFont.truetype(font_string, size=0)
                return font_string
            except Exception as e:
                raise argparse.ArgumentTypeError("True type Font: %s is not Installed / Not available" % font_string)

        for font in DEFAULT_FONTS:
            try:
                ImageFont.truetype(font, size=0)
                return font
            except Exception as e:
                pass

        raise argparse.ArgumentTypeError("True type Font: None of the default fonts are Installed. -> " % str(DEFAULT_FONTS))


class ColorValidator(object):
    """
    Checks the File/Directory exists
    """

    def __call__(self, color_string):
        try:
            if color_string.lower() == 'transparent':
                return Color.TRANSPARENT
            color = Color(color_string)
            return color.get_dec_rgba()
        except Exception as e:
            raise argparse.ArgumentTypeError("%s" % str(e))


class ExistingFileOrDirType(object):
    """
    Checks the File/Directory exists
    """

    def __call__(self, name_string):
        # TODO: the Integrate - for chaining; special argument "-" means sys.std{in,out}
        if os.path.exists(name_string):
            return name_string
        raise argparse.ArgumentTypeError("Expecting an existing image file/ Directory")


class ImageSizeValidator(object):
    """
    Checks the image sizes are in defined format, either in width height/ percentage
    Eg: 800x600
        50%
    """

    def __call__(self, string):
        try:
            width, height = string.split('x')
            width, height = int(width), int(height)
            # tuple
            return width, height
        except Exception:
            try:
                percentage = string.split('%')[0]
                percentage = int(percentage)
                # tuple
                return percentage,
            except Exception:
                pass
        except Exception:
            pass
        raise argparse.ArgumentTypeError("Invalid size specified: Eg1: 800x600, Eg2: 75%")


class ExistingFileType(object):
    """
    Checks whether File exists return string instead of file object
    """

    def __call__(self, name_string):
        # the special argument "-" means sys.std{in,out}
        if os.path.isfile(name_string):
            return name_string
        raise argparse.ArgumentTypeError("Expecting an existing image file")


class ExistingDirType(object):
    """
    Checks whether directory exists
    """

    def __call__(self, name_string):
        # the special argument "-" means sys.std{in,out}
        if os.path.isdir(name_string):
            return name_string

        raise argparse.ArgumentTypeError("Output directory doesn't exists. Please create one")
