"""
A package providing full support for reading and writing data to midi files
and ports. The module has several layers:

* midimsg.py : a functional interface for creating low-level midi message lists.
* midievent.py : an object oriented layer above midimsg.py that represents
midi data as class instances with attributes time and message.
* midifile.py : reads and writes data to midi files.
"""

from .midimsg import *
from .midifile import *
from .midievent import *

