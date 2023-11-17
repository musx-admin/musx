"""
# musx
musx (pronounced *muse ex*) is a package for composing and processing symbolic
music information. It was originaly created for teaching my CS+Music classes
and it now contains all the compositional tools developed in my Common Music
and Grace systems, including support for complex pattern generation, randomness,
mapping, enveloping, spectral composition, and microtonality. The 'base' musx
package provides a back end to read/write midi files and MusicXML; to compose
with audio files or send/receive real time midi or osc, see the 'Additional
support and customizations' section of
[INSTALL.md](https://github.com/musx-admin/musx/blob/main/INSTALL.md).

musx requires the [lxml](https://pypi.org/project/lxml/),
[numpy](https://pypi.org/project/numpy/),
[matplotlib](https://matplotlib.org/),
and [jupyter](https://pypi.org/project/jupyter/) packages.

musx [documentation](https://musx-admin.github.io/musx/),
[tutorials](https://github.com/musx-admin/musx/tree/main/tutorials), 
and [demos](https://github.com/musx-admin/musx/tree/main/demos)
are available on the github [website](https://github.com/ricktaube/musx).

----

Rick Taube

Emeritus Professor, Composition/Theory/CS+Music  
School of Music 
University of Illinois Urbana-Champaign  
Email: taube@illinois.edu  

President, Illiac Software Inc.  
https://harmonia.cloud/  
Email: taube@illiacsoftware.com   
"""

# Do not alter this version line, it is automatically replaced by the correct
# version number when the software is released.

version="N.N.N"
#from fractions import Fraction
from .rhythm import *
from .midi import gm
from .midi.midimsg import *
from .midi.midievent import *
from .midi.midifile import *
from .seq import *
#from .gens import *
from .patterns import *
from .paint import *
from .pitch import *
from .note import *
from .interval import *
from .tools import *
from .ran import *
from .envs import *
from .score import *
from .spectral import *
from .pc import *
from .csound import *
from .mxml.notation import *
# importing the frac module adds musx methods to python's Fraction class,
# there are no symbols to import from the module itself.
from .frac import *
