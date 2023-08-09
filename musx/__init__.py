"""
musx (pronounced *muse ex*) is a package for composing and processing symbolic
music information. It contains a large set of compositional tools adapted from
my Common Music and Grace systems, including support for complex pattern generation,
randomness, mapping, enveloping, spectral composition, microtonality, and musicxml
scores. The musx package currently provides back ends to read and write midi files
and Csound (thank you Michael Gogins!) and it is straightforward to add other
backends to connect to different systems, for example to send data to an app via
portmidi or to SuperCollider via osc. If you are new to musx or Python the place to
start is by reading this documentation and trying out the material in the demos and
tutorials directories. After restoring the demos, you can generate output by
running them as scripts or using the jupyter notebook versions:

```bash
python -m demos.gamelan

jupyter notebook demos/gamelan.ipynb
```
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
from .gens import *
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
