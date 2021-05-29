"""
musx (pronounced *muse ex*) is a package for composing and processing symbolic
music information. It contains a large set of compositional tools adapted from
Common Music and Grace, including support for complex pattern generation,
randomness, mapping, enveloping, spectral composition, microtonality, and so on.
The package provides a back end that reads and writes midi files, but
the user can add other backends to produce different outputs, for
example audio, MusicXml, or realtime output via portmidi or osc.

The place to start is reading this documentation and trying out the material
in the demos package. After restoring the demos, you can generate output
by running them as scripts:

```bash
python3 -m demos.gamelan
```
"""

version="2.0.0"

from .rhythm import *
from .midi import gm
from .midi.midimsg import *
from .midi.midievent import *
from .midi.midifile import *
from .seq import *
from .generators import *
from .pitch import *
from .note import *
from .interval import *
from .scales import *
from .tools import *
from .ran import *
from .envelopes import *
from .score import *
from .spectral import *
from .pc import *
from .csound import *
