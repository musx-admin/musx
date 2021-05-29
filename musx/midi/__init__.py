"""
A package providing full support for reading and writing MIDI data to files
and ports. The module has several layers:

* midimsg.py : a functional interface for creating midi messages lists that 
can be easily converted to/from bytearrays.
* midievent.py : an object oriented layer above midimsg.py that represents
midi data as class instances with attributes, incuding time stamps..
* midifile.py : reads and writes data to midi files.
"""

from .midimsg import *
from .midifile import *
from .midievent import *

