"""
A package providing support for reading and writeing notation data from MusicXml files.
The MusicXml schema is defined in the file musicxml.py, which was auto-generated
using the awesome [generateDS](https://pypi.org/project/generateDS/) package.
"""

from .barline import *
from .clef import *
from .key import *
from .mark import *
from .measure import *
from .meter import *
from .part import *
from .notation import *


__all__ = ['barline', 'clef', 'key', 'mark', 'measure', 'meter', 'part', 'notation']
