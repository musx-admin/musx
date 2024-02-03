"""
A module providing support for reading and writing audio files using
Todd Ingall's [pysndlib package](https://pypi.org/project/pysndlib/):

```bash
% pip install pysndlib
```

### Example:

```python
from musx import Seq, Score, between
import pysndlib.clm as CLM

# Define a simple audio instrument:
def simp(start, dur, freq, amp=.5):
    start = CLM.seconds2samples(start)
    end = start + CLM.seconds2samples(dur) 
    osc = CLM.make_oscil(freq)
    for i in range(start, end):
        CLM.outa(i, amp * CLM.oscil(osc))

# Create an audio note class for it:
SimpNote = AudioNote(simp)

# Define a part composer that will add instances of
# SimpNote to a score:
def playsimp(score, num, rate, dur, low, high, amp):
    for _ in range(num):
        freq = between(low, high)
        # add SimpNotes to the score
        score.add(SimpNote(score.now, dur, freq, amp)) 
        yield rate           

# Compose the score:
score = Score(out=Seq())
score.compose(playsimp(score, 10, .3, .3, 200, 440, .2))

# Print the score:
score.out.print()

# Write the score to a sound file and play it:
file = AudioFile("test.wav", score.out).write(play=True)
```
"""

try: 
    import pysndlib.clm as CLM 
except ModuleNotFoundError as err:
    pad='    '
    print("****Error while loading musx.audio:")
    print(f"{pad*2}{repr(err)}")
    print(f"{pad}musx.audio requires the pysndlib package.")
    print(f"{pad}Type 'pip install pysndlib' in your terminal to install it.")
    exit()


import inspect
from .seq import Seq


class AudioFile:
    '''
    A class for reading and writing audio files using pysndlib.

    Parameters
    ----------
    path : string
        The pathname of the audio file to be written, e.g. '/tmp/sweet.wav'.
    seq : Seq
        A sequence containing the instrument notes to render.
    '''
    def __init__(self, path, seq):
        if not isinstance(path, str) or len(path) == 0:
            raise TypeError(f"SoundFile(): '{path}' is not a valid pathname string.")
        self.pathname = path
        
        if not isinstance(seq, Seq):
            raise TypeError(f"SoundFile(): '{seq}' is not a sequence.")
        self.seq = seq

    def read(self):
        """Implement me!"""
        return self

    def write(self, **kwargs):
        '''
        Render the notes in the SoundFile to an audio file on the disk. 
        
        Parameters
        ----------
        kwargs : keyword args
            Any keywords that are supported by pysndlib's 
            [Sound Context](https://testcase.github.io/pysndlib/with_sound.html)
        '''
        with CLM.Sound(self.pathname, **kwargs):
            for note in self.seq:
                note._write()
        return self

    def __str__(self):
        name = self.__class__.__name__
        seq = f'<Seq: len={len(self.seq)}, endtime={self.seq.endtime()}>'
        return f'<{name}: path="{self.pathname}", seq={seq}>'
    
    __repr__ = __str__


def AudioNote(ins, classname=''):
    """
    Defines a note class given a pysndlib instrument (function). Once defined,
    instances of the new note class can be added to Score and Seq objects and 
    will generate audio when rendered by AudioFile.write(). 

    Parameters
    ----------
    ins : function
        The CLM instrument (function) to create the new note class for. The first
        parameter to the instrument must contain the start time of the instrument call.
    classname : string 
        An optional argument providing the full name for the new Note class. 
        Defaults to '', in which case the name will be the capitalized instrument name
        with all "_" removed and appended with "Note". For example, if the instrument is
        hi_ho() the default name for the new note class will be HiHoNote.
 
    Return
    ------
    The function returns a Python class whose instances hold parameter values
    for the instument to render when a sound file is written, e.g.:
    
    ```python
    # Immediate instrument call inside a Sound context:
    with Sound():
        simp(1,2,3,4)

    # SimpNote equivalent that can be added to a score, editied,
    # and rendered later, when an audio file is written:
    SimpNote(1,2,3,4)
    ```
    """
    if not callable(ins): raise TypeError(f"Not a function: {ins}")
    if not classname: 
        for n in f"{ins.__name__}_Note".split('_'):
            if n == '': continue
            classname += n.capitalize()
    # dictionary of function parameters with default values or None.
    params = {n: inspect.Parameter.empty if v.default==inspect._empty else v.default
              for n, v in inspect.signature(ins).parameters.items()}
    # define the init method for the new note class.
    def __init__(self, *args, **kwargs):
        ###print(f"args: {args}, kwargs: {kwargs}")
        ###print(f"params: {self.params}")
        # cache the list of function parameter names
        self._params = list(params)
        # define an attribute for each instrument parameter and initialize
        # it to the parameter's default value or None
        for p in params.items():
            setattr(self, p[0], p[1])
        # keep a record of how many times each arg receives a value
        counts = {p:0 for p in params}
        ###print(f'counts: {counts}')
        # collect ordered list of insturment's parameter names (strings)
        names = list(params)
        ###print(f'names: {names}')
        # parse the positional arguments, signal error if more arguments than parameters,
        # create the attribute and increment arg's count.
        for index, value in enumerate(args):
            if index == len(params): 
                raise TypeError(f"{classname}() takes {len(params)} positional arguments but {len(args)} were given.")
            name = names[index]
            setattr(self, name, value)
            counts[name] += 1            
        # parse the keyword arguments, signal error if the keyword parameter
        # was already set by a positional argument, or keyword is not value.
        # set the attribute and increment arg's count.
        for name, value in kwargs.items():
            if name in names:
                if counts[name] > 0:
                    raise TypeError(f"{classname}() parameter '{name}' assigned more than once.")
                setattr(self, name, value)
                counts[name] += 1
            else:
                raise TypeError(f"{classname}() got an unexpected keyword argument '{name}'.")
        # for any parameter that was not assigned set to default value or None.
        unassigned = []
        for name, count in counts.items():
            if count == 0:
                if params[name] is not inspect.Parameter.empty:
                    setattr(self, name, params[name])
                    counts[name] += 1
                else:
                    unassigned.append(name)
            elif count > 1:
                raise TypeError(f"{classname}() parameter '{name}' assigned more that once.")
        # one or more parameters do not have values.
        if unassigned:
            l = len(unassigned)
            p = "parameters" if l > 1 else "parameter"
            unassigned = ", ".join(unassigned)
            raise TypeError(f"{classname}() has {l} unassigned {p}: {unassigned}.")
        # First argument to note must be the start time value....
        # Event.__init__(self, getattr(self, params[0][0]))
        self.time = getattr(self, names[0])
    
    # repr() and str() will print like an instrument call, floats will be
    #    trucated to 3 places.
    def __repr__(self):
        """
        Both repr() and str() print like an instrument call. To save space floats are
        rounded to three places and lists of more than 10 elements are elided. To see
        exact values in the object use it's self.params() method.
        """
        def paramstr(val):
            if isinstance(val, float):
                #return f"{val:.3f}"
                return f"{round(val,3)}"
            if isinstance(val, list):
                val = [paramstr(v) for v in val]      
                if len(val) > 10:
                    val = val[:4] + ["..."] + val[-4:]
                return "[" + ", ".join(val) + "]"
            return f"{val}"

        text = self.__class__.__name__
        #return text + '(' + ", ".join(f"{getattr(self,p)}" for p in self.params) + ')'
        return text + '(' + ", ".join(f"{paramstr(getattr(self,p))}"
                                      for p in self._params) + ')'
    
    def __eq__(self, other):
        '''
        Returns True if parameter values in two instances are all equal (==).
        '''
        if type(self) is not type(other):
            return False
        for p in self._params:
            if getattr(self, p) != getattr(other, p):
                return False
        return True

    def _write(self):
        '''
        Internal function called by AudioFile().write() to render
        audio samples inside a 'with Sound:' construct.
        '''
        args = [getattr(self, p) for p in self._params]
        #print(f"{ins} writing args: {args}")
        ins(*args)

    def parameters(self):
        """Returns an ordered dictionary of the note's attributes and their values."""
        return {p: getattr(self, p) for p in self._params}

    return type(classname, (), {"__init__": __init__,
                                "__repr__": __repr__,
                                "__str__": __repr__,
                                # ARRRG caching instrument in an instance attr doesn't work
                                #"ins": ins, 
                                "__eq__": __eq__,
                                "_write": _write,
                                "parameters": parameters
                                })

    
if __name__ == '__main__':
    pass
    # from musx import Seq, Score, between

    # def simp(start, dur, freq, amp=.5):
    #     #print(f"simp: start={start}, dur={dur}, freq={freq}, amp={amp}")
    #     start = CLM.seconds2samples(start)
    #     end = start + CLM.seconds2samples(dur) 
    #     osc = CLM.make_oscil(freq)
    #     for i in range(start, end):
    #         CLM.outa(i, amp * CLM.oscil(osc))

    # SimpNote = AudioNote(simp)

    # def playsimp(score, num, rate, dur, low, high, amp):
    #     for _ in range(num):
    #         freq = between(low, high)
    #         score.add(SimpNote(score.now, dur, freq, amp)) 
    #         yield rate           

    # score = Score(out=Seq())
    # score.compose(playsimp(score, 10, .3, .3, 200, 440, .2))
    # score.out.print()
    # file = AudioFile("test.wav", score.out) #.write(play=True)
    # print(f"Writing {file}")
    # file.write(play=True)

    #======================================================== 
    # def testnote(*args, **kwargs):
    #     def printargs(*args, **kwargs):
    #         a = ', '.join(str(a) for a in args)
    #         k = ', '.join(f"{k}={v}" for k,v in kwargs.items())
    #         if a and k: sig = a + ", " + k
    #         else: sig = a or k
    #         print(f'simp({sig})')
    #     printargs(*args, **kwargs)
    #     try: 
    #         n = SimpNote(*args,**kwargs)
    #         print(n)
    #     except Exception as e: 
    #         print(f'{type(e).__name__}: {e.args[0]}')
    # print("--------------------------------------------------")
    # testnote(1,2,3,4)
    # print("--------------------------------------------------")
    # testnote(amp=3,freq=2,dur=2,start=0)
    # print("--------------------------------------------------")
    # testnote(1,2,freq=2,amp=4)
    # print("--------------------------------------------------")
