"""
Constants
"""


class ConstantType(type):
    # Meta class for constant definition
    def __new__(cls, name, bases, attrs):
        new_attrs = {}
        for aname, aval in attrs.iteritems():
            # Avoid Inheritance and mro
            if aname == '_consts':
                for k in aval:
                    new_attrs[k] = k
            else:
                new_attrs[aname] = aval
        return super(ConstantType, cls).__new__(cls, name, bases, new_attrs)


class Position:
    """
    Position constants
    """
    __metaclass__ = ConstantType
    _consts = ('TOP', 'LEFT', 'RIGHT', 'BOTTOM', 'CENTER')


class RelativePosition:
    """
    Relative position of watermark based on image
    """
    __metaclass__ = ConstantType
    _consts = ('TOP_LEFT', 'TOP_CENTER', 'TOP_RIGHT', 'CENTER_LEFT', 'CENTER_CENTER', 'CENTER_RIGHT', 'BOTTOM_LEFT',
               'BOTTOM_CENTER', 'BOTTOM_RIGHT')

    @classmethod
    def split(cls, pos):
        """
        Splits the Relative postition to Individual positions
        :param pos: RelativePosition Attribute eg: RelativePosition.TOP_LEFT
        """
        try:
            posy_name, posx_name = pos.split('_')
            posx = getattr(Position, posx_name)
            posy = getattr(Position, posy_name)
            return posx, posy
        except (ValueError, AttributeError):
            raise ValueError("Invalid Position Variable passed")

    @classmethod
    def all(cls):
        """
        Return all constants
        """
        # upper case attributes are all constants
        return [key for key in cls.__dict__.keys() if ord('A') < ord(key[0]) < ord('Z')]


class Size:
    """
    Font size constants
    """
    AUTO = 0

# Input and Output supported formats
IMAGE_FORMATS = (('png', 'jpg', 'jpeg', 'gif', 'bmp', 'eps', 'webp', 'psd'), ('png', 'jpg', 'gif'))