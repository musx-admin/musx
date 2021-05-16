###############################################################################
"""
An assortmant of music composition tools for working with randomness, 
rescaling, arithmetic, etc.
"""

import types
import math
import random
import subprocess

__pdoc__ = {
    'parse_string_sequence': False
}

def isgen(x):
    """Returns True if x is a generator."""
    return isinstance(x, types.GeneratorType)


def isfunc(x):
    """Returns True if x is a function."""
    return isinstance(x, types.FunctionType)


def isseq(x):
    """Returns True if x is a list or tuple."""
    return isinstance(x, (list, tuple))


def isnum(x, others=None):
    """
    Returns True if x is an int or float of one of the
    other number types passed in (e.g. Fraction, complex).
    """
    if isinstance(x, (int, float)):
        return True
    if others:
        return isinstance(x, others)
    return False


def rescale(x, x1, x2, y1, y2, mode='lin'):
    """
    Maps the value x ranging between x1 and x2 into a proportional value
    between y1 and y2.
    
    Parameters
    ----------
    x : int | float
        The value to rescale.
    x1 : int | float
        The lower limit of input range.
    x2 : int | float
        The upper limit of input range.
    y1 : int | float
        The lowest limit of output range.
    y2 : int | float
        The upper limit of output range.
    mode : string
        If mode is 'lin' then linear scaling occurs, 'cos' produces cosine
        scaling, 'exp' produces exponential scaling, and '-exp' produces 
        inverted exponential.

    Returns
    -------
    The rescaled value.
    """
    if x > x2: return y2
    if x <= x1: return y1
    # as x moves x1 to x2 mu moves 0 to 1
    mu = (x - x1) / (x2 - x1)
    if mode == 'lin':
        #return (((y2 - y1) / (x2 - x1)) * (x - x1)) + y1
        return (y1 * (1 - mu) + (y2 * mu))
    elif mode == 'cos':
        mu2 = (1 - math.cos(mu * math.pi)) / 2
        return (y1 * (1 - mu2) + y2 * mu2)
    elif mode in ['exp','-exp']:
        # # http://www.pmean.com/10/ExponentialInterpolation.html
        # if y1==0: y1=0.00001
        # return y1 * ((y2/y1) ** (mu))
        # #https://docs.fincad.com/support/developerfunc/mathref/Interpolation.htm
        # if y1==0: y1=0.00001
        # m = math.log(y2 / y1) / (x2 - x1)
        # k = y1 * math.pow(math.e, -m * x1)
        # return k * math.pow(math.e, m * x)

        # a base that yields a slope that is not too steep or shallow...
        b = 512
        if mode == 'exp':
            return y1 + ( ((y2 - y1) / b) * math.pow(b, mu) )
        b = 1/b
        return y1 + ( ((y2 - y1) / (b - 1)) * (math.pow(b, mu) - 1) )
    raise ValueError(f"mode {mode} is not 'lin', 'cos', 'exp', or '-exp'.")


def frange(start, stop=None, step=None):
    """
    Returns an iterator produceing a series of floats from start (inclusive)
    to stop (exclusive) by step.

    Parameters
    ----------
    frange can be called with one, two or three arguments:
    
    * frange(stop)
    * frange(start, stop)
    * frange(start, stop, step)

    start : int | float
        The starting value of the sequence.

    stop : int | float
        The exclusive upper (or lower) bounds of the iteration.

    step : int | float
        The increment (or decrement) to move by. Defaults to 1.

    Returns
    -------
    Values ranging from start to stop (exclusive).
    """
    if stop is None:
        stop = start
        start = 0.0
    else:
        start += 0.0

    if step is None:
        step = 1.0
    else:
        step += 0.0
    i = 1
    init = start # initial start value (offset)
    # no iteration if step is 0 or reversed direction of start -> stop.
    while step != 0:
        if step > 0 and start >= stop:
            break
        if step < 0 and start <= stop:
            break
        yield start
        # start += step   # arrg! cumulative addition yields wonky numbers
        start = (step * i) + init  # scale by step and shift to start
        i += 1


def rand(limit):
    """
    Returns a generator that produces uniform random numbers below limit.

    Parameters
    ----------
    limit : int | float
        Sets the exlusive upper bound for random selection. If limit
        is an integer then integer values are returned otherwise float
        values are returned.
    """
    if isinstance(limit, int):
        def irand():
            while True:
                yield random.randrange(limit)
        return irand()
    elif isinstance(limit, float):
        def frand():
            while True:
                yield random.random() * limit
        return frand()
    raise TypeError("limit not an int or float: {limit}.")


def quantize(number, stepsize):
    """Quantizes number to a given step size."""
    return math.floor( (number/stepsize) + .5) * stepsize


def deltas(numbers):
    """
    Returns the changes between consecutive numbers in a list of numbers.

    Example: deltas([1,5,3])  ->  [4, -2]

    Parameters
    ----------
    numbers : list
        The list of numbers to process.

    Returns
    -------
    A list containing the differences between a series of numbers.
    """
    return [l - r for l,r in zip(numbers[1:], numbers[:])]


def _expl(powr, y0, y1, base):
    if powr < 0:
        powr=0.0
    elif powr > 1: 
        powr = 1.0
    if base == 1.0:
        return y0 + (powr * (y1 - y0))
    return y0 + ( ( (y1 - y0) / (base - 1.0) ) * ((base ** powr) - 1.0) )


def _explseg(i, length, summ, powr):
    if i >= length:
        i += -1
    x1 = (i+1) / length
    x2 = i / length
    f1 = _expl(x1, 0.0, 1.0, powr)
    f2 = 0.0 if (i <= 0) else _expl( x2, 0.0, 1.0, powr)
    return summ * (f1 - f2)


def explsegs(num, summ, base=2):
    segs = []
    for i in range(num):
        segs.append(_explseg(i, num, summ, base))
    return segs


def _geoseg( i, length, summ, base):
    if length == 0:
        return 0.0
    a = summ * ((1.0 - base) / (1.0 - (base ** length)))
    return  a * (base ** i)


def geosegs(num, summ, base=2):
    segs = []
    for i in range(num):
        segs.append(_geoseg(i, num, summ, base))
    return segs


def _map_lists(func, left, right):
    if type(left) is list:
        if type(right) is list:
            assert len(left) == len(right), "lists are different lengths."
            return [func(l,r) for l,r in zip(left,right)]
        else:
            return [func(l,right) for l in left]
    else:
        if type(right) is list:
            return [func(left,r) for r in right]
        else:
            return func(left,right)
    

def multiply(left, right):
    """
    List-aware multiplication.
    
    Left and right can be numbers or lists, if both are lists
    they must be of the same length.
    """
    return _map_lists(lambda l,r: l*r, left, right)


def add(left, right):
    """
    List-aware addition.
    
    Left and right can be numbers or lists, if both are lists
    they must be of the same length.
    """
    return _map_lists(lambda l,r: l+r, left, right)


def subtract(left, right):
    """
    List-aware subtraction.
    
    Left and right can be numbers or lists, if both are lists
    they must be of the same length.
    """
    return _map_lists(lambda l,r: l-r, left, right)


def divide(left, right):
    """
    List-aware division.
    
    Left and right can be numbers or lists, if both are lists
    they must be of the same length.
    """
    return _map_lists(lambda l,r: l/r, left, right)


def _rem(x,y):
    #return math.copysign(x % y, x)
    mod = x % y
    res = math.copysign(mod, x)
    return int(res) if isinstance(mod, int) else res


def fit(num, lb, ub, mode='wrap'):
    """
    Forces a number to lie between a lower and upper bound according to mode. 

    Parameters
    ----------
    num : int | float
        The number to fit.
    lb : int | float
        The lower bound.
    ub : int | float
        The upper bound.
    mode : 'reflect' | 'limit' | 'wrap'
        If mode is 'reflect' then the min and max boundaries reflect the value back into range.\
        If mode is 'wrap' then num will be the remainder of num % boundaries.

    Returns
    -------
    The value of num coerced to lie within the range lb to ub.

    Raises
    ------
    ValueError if mode is not one of the supported modes.

    Examples
    --------
    ```python
    [fit(i, 0, 10) for i in range(-20, 21, 5)]
    ```
    """
    if lb > ub:
        ub, lb = lb, ub
    if lb <= num <= ub:
        return num
    b = ub if num > ub else lb
    if mode == 'limit':
        return b
    rng = ub - lb
    if mode == 'reflect':
        # shift num to 0 to compare with range
        # limit num to rng*2 (rising/reflecting)
        num = _rem(num - b, (rng * 2))
        if abs(num) > rng:   # in range2
            if num >= 0:
                num = num - (rng * 2)
            else:
                num = num + (rng * 2)
        else:
            num = -num
        return num + b
    if mode == 'wrap':
        return (lb if b == ub else ub) + _rem(num - b, rng)
    raise ValueError(f"{mode} not one of ['reflect', 'limit', 'wrap'].")

'''
(defun fit (number lb ub &optional (mode :reflect))
  (when (> lb ub) (rotatef lb ub))
  (if (<= lb number ub)
      number
      (let ((b (if (> number ub) ub lb)) (r (- ub lb)))
        (case mode
          ((:limit) b)
          ((:reflect)
           (let* ((2r (* 2 r)) 
                  (v (rem (- number b) 2r)))
             (+ (if (> (abs v) r)
                    (funcall (if (>= v 0) #'- #'+) v 2r)
                    (- v))
                b)))
          ((:wrap) (+ (if (= b ub) lb ub) (rem (- number b) r)))
          (t (error "~s is not :limit, :reflect or :wrap" mode))))))
'''

midiextensions = ('.mid', '.midi')
"""
A tuple of allowable midi file extensions. Defaults to ('.mid', '.midi').
"""

midiplayer = ''


def setmidiplayer(command):
    """
    Assign a shell command (string) that will play a midi file.

    Parameter
    ---------
    command : string
        The shell command that will play a midi file.

    Example
    -------
    setmidiplayer('fluidsynth -iq -g1 /Users/taube/SoundFonts/MuseScore_General.sf2')
    """    
    
    global midiplayer
    midiplayer = command


audioextensions = ('.aiff', '.wav', '.mp3', '.mp4')
"""
A tuple of allowable audio file extensions. 
Defaults to ('.aiff', '.wav', '.mp3', '.mp4').
"""


audioplayer = ''
"""
A shell command (string) that accepts one argument,
a pathname (file) to play. See: setaudioplayer().
"""


def setaudioplayer(command):
    """
    Assign a shell command (string) that will play an audio file.

    Parameter
    ---------
    command : string
        The shell command that will play an audio file.

    Example
    -------
    setaudioplayer('afplay')
    """    
    
    global audioplayer
    audioplayer = command


def playfile(file, wait=False):
    """
    Plays a midi or audio file using the shell commands you have specified
    for midiplayer and audioplayer. See: setaudioplayer, setmidiplayer.

    Parameters
    ----------
    file : string
        The file to play.
    wait : bool
        If true playfile waits until the file has finished playing
        before returning, otherwise playfile returns immediately.
    """
    args = []
    kind = ''
    if file.endswith(midiextensions):
        kind = 'midi'
        if midiplayer:
            args = midiplayer.split() + [file]
    elif file.endswith(audioextensions):
        kind = 'audio'
        if audioplayer:
            args = audioplayer.split() + [file] 
    if args:
        p = subprocess.Popen(args)
        if wait:
            p.wait()
    else:
        help = f"playfile(): Don't know how to play '{file}':"
        if kind:
            help += f" use musx.set{kind}player() to set a shell command to play {kind} files."
        else:
            help += f" file type not found in musx.midiextensions or musx.audioextensions."
        print(help)


def parse_string_sequence(string):
    # split string at blank spaces, replace each repeat token ',' by
    # repeated value, check for dangling and undelimited repeats.
    seq = []
    for raw in string.split():
        tok = raw.rstrip(',')
        if tok:
            if ',' not in tok:
                for _ in range(len(raw) - len(tok) + 1):
                    seq.append(tok)
            else:
                raise SyntaxError(f"undelimited ',' in '{tok}'.")
        else:
            raise SyntaxError(f"dangling repeat ',' in '{string}'.")
    return seq
