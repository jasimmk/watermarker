from __future__ import division

from colour import rgb2hsl
from colour import Color as _Color

# HACK: Patching colour library for additional functionality


class Color(_Color):
    TRANSPARENT = (0, 0, 0, 0)

    def __getattr__(self, label):
        return getattr(self, 'get_' + label)()

    def get_dec_rgba(self):
        """
        Returns color in RGBA Format
        eg: White -> (255, 255, 255, 255)
        """
        rgb = self.get_rgb()
        dec_rgb = tuple(int(v * 255) for v in rgb)

        # HACK: Add alpha value
        dec_rgb += (255,)
        return dec_rgb

    def set_dec_rgba(self, value):
        """
        Hack for RGBA to RGB, still a little buggy
        :param value: Tuple in RGBA format eg: (255, 255, 255, 255)
        """
        rgb = tuple(v / 255 for v in value[:3])
        self.hsl = rgb2hsl(rgb)
