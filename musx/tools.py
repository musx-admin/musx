###############################################################################
"""
An assortmant of tools for working with envlopes, randomness, rescaling, 
arithmetic, etc.
"""

import types
import math
import random
import subprocess
from functools import reduce

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


def interp(x, *xys, mode='lin', mul=None, add=None):
    """
    A function that interpolates a y value for a given x in a
    series of x,y coordinate pairs. If x is not within bounds
    then the first or last y value is returned.

    Parameters
    ----------
    x : int | float
        The x value to interpolate in the sequence of x y values. 
    xys : series of int or float | list
        Either a series of in-line x, y values representing the envelope
        or a single list of x y coordinate pairs.
    mode : 'lin' | 'cos' | 'exp' | '-exp'
        A string that specifies the type of interpolation performed;
        'lin' is linear, 'cos' is cosine, 'exp' is exponential and 
        '-exp' is inverted exponential. The default is 'lin'. Note
        that if specified the value must provided as an explicit
        keyword arg, e.g. mode='cos'.
    mul : None | number
        A value to multiply the result by.
    add : None | number
        A value to add to the result after any multiplication.
    Returns
    -------
    The interpolated value of x.
    """
    if len(xys) == 1 and isinstance(xys[0], (tuple,list)):
        xys = xys[0]
    if not xys or len(xys) & 1:
        raise ValueError(f"coordinates not x y pairs: {xys}.")
    # find the segment in the coordinates that contains the given x
    xr,yr = xys[0:2]
    xl,yl = xr,yr
    # iterate remaining pairs of x y values stepping by 2
    for wx,wy in zip(xys[2::2], xys[3::2]):
        if xr > x: break
        xl,yl = xr,yr
        xr,yr = wx,wy
    # print(x, xl, xr, yl, yr, mode)
    val = rescale(x, xl, xr, yl, yr, mode)
    if mul: val *= mul
    if add: val += add
    return val


def rescale_env(env, newxmin=None, newxmax=None, newymin=None, newymax=None,*, mode=None):
    '''
    Rescales the current x and/or y envelope coordinates of the given envelope to proportional
    values lying between the given new minima and maxima. If newxmin or newxmax are unspecified
    they inherit the current x minimum and maximum values. The same is true for y values.
    If mode is specfied it is applied to the y values only. See
    `rescale()` for information about mode.

    Parameters:
    -----------
    env : list 
        A list of x y coordinate values: [x1,y1,x2,y2,...xn,yn] where
        x values are monotoniclly increasing values from left to right.
    newxmin : int | float | None
        The new minimum x value. If None it defaults to the current minimum x value.
    newxmax : int | float | None
        The new maximum x value. If None it defaults to the current maximum x value.
    newymin : int | float | None
        The new minimum y value. If None it defaults to the current minimum y value.
    newymax : int | float | None
        The new maximum y value. If None it defaults to the current maximum y value.
    mode : string
        See `rescale()` for possible mode values.

    Returns
    -------
    A rescaled x,y envelope.
    '''
    #print(f"env:  {env}")
    if len(env) % 2 != 0:
        raise ValueError(f"env {env} does not have an even number of values.")
    xdata, ydata = env[::2], env[1::2]
    #print(f"xdata: {xdata}, ydata: {ydata}")
    for x1,x2 in zip(xdata,xdata[1:]):
        if x2<x1:
            raise ValueError(f"x value {x2} out of order in xdata: {xdata}.")
    oldxmin, oldxmax = xdata[0], xdata[-1]
    ##print(f"oldxmin: {oldxmin}, oldxmax: {oldxmax}")
    if newxmin is None: newxmin = oldxmin
    if newxmax is None: newxmax = oldxmax
    if not newxmin < newxmax:
        raise ValueError(f"newxmin value {newxmin} is not less than newxmax value {newxmax}.")
    #print(f"oldxmin: {oldxmin}, oldxmax: {oldxmax}, newxmin: {newxmin} newxmax: {newxmax}")
    oldymin = reduce(lambda a, b: a if a < b else b, ydata)
    oldymax = reduce(lambda a, b: a if a > b else b, ydata)
    ##print(f"oldymin: {oldymin}, oldymax: {oldymax}")
    if newymin is None: newymin = oldymin
    if newymax is None: newymax = oldymax
    if mode is None: mode = "lin"
    #print(f"oldymin: {oldymin}, oldymax: {oldymax}, newymin: {newymin}, newymax: {newymax}")
    res = []
    for x,y in zip(xdata,ydata):
       res.extend([rescale(x, oldxmin, oldxmax, newxmin, newxmax),
                   rescale(y, oldymin, oldymax, newymin, newymax, mode)])
    return res


def exp_env(segments = 10, base = 2, flip = False, reverse = False, scaler=1, offset=0):
    """
    Returns a normalized exponential envelope, e.g. both axes range 0 to 1.
    As x goes from 0 to segments, y is assigned 1/base**x
    
    Parameters
    ----------
    segments : int
        The number of segments in the envelope, defaults to 10.
    base : int | float
        The base for the exponential, defaults to 2. 
    flip : boolean
        If flip is true y values are inverted.
    reverse : boolean
        If reverse is true x values are retrograded.
    
    Returns
    -------
    An exponential x,y envelope with both axes ranging 0 -> 1.
    """
    xvalues = [x/segments for x in range(0, segments+1, 1)]
    #print("xvalues:", xvalues)
    yvalues = [1/(base**(x)) for x in range(segments+1)]
    if flip:
        for i in range(len(yvalues)):
            yvalues[i] = 1 - yvalues[i]
    if reverse:
        for i in range(len(xvalues)):
            xvalues[i] = 1 - xvalues[i]
    #yvalues[-1] = 0.0
    #print("yvalues:", yvalues)
    env = []
    for x,y in zip(xvalues, yvalues):
        env.extend([x,y * scaler + offset])
    #print("expenv:", env)
    return env


def segment_env(env, dur, attack, release=[]):
    '''
    Returns a version of env with attack and (optionally) decay segments lasting specific amounts of time.

    Parameters
    ----------
    env : list
        The x,y envelope.
    dur : int | float
        The total duration in seconds of the envelope.
    attack : [ _attack_x, attack_dur_ ]
        The ending x coordinate and duration of the attack segment. 
    release : [ _release_x, release_dur_ ] | []
        The starting x coordinate and duration of the release segment.
    '''    
    # maximum x value in envelope.
    x_max = env[-2]
    # get the index positions of the attack and release segments.
    # divides by 2 because x_values will be half the length of env.
    try: 
        attack_index = int(env.index(attack[0])/2)
        attack_dur = attack[1]
    except ValueError as e: 
        raise Exception(f"Attack coordinate {attack[0]} is not in {env}.") from e
    if release:
        try: 
            release_index = int(env.index(release[0])/2)
            release_dur = release[1]
        except ValueError as e:
            raise Exception(f"Release coordinate {release[0]} is not in {env}.") from e     
    # split x and y coords into separate lists with x_values converted to time.
    x_values, y_values = [(x / x_max) * dur for x in env[::2]], env[1::2]
    # rescale x coords from index 0 to att_index to fit in attack_dur time.
    for i in range(0, attack_index+1):
         x_values[i] = rescale(x_values[i], x_values[0], x_values[attack_index], x_values[0], attack_dur)
    # rescale backwards for release values.
    if release:
        end_time = x_values[-1]
        for i in range(len(x_values)-1, release_index-1, -1):
             x_values[i] = rescale(x_values[i], x_values[release_index], end_time, end_time - release_dur, end_time)
    # return new envelope with durations converted back to user's original coordinates.
    env = []
    for x,y in zip(x_values, y_values):
        env.extend([(x / dur) * x_max, y])
    return env


def frange(start, stop=None, step=None):
    """
    Returns an iterator producing a series of floats from start (inclusive)
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

# musx.tools.parse_string_sequence("e*3")
# musx.tools.parse_string_sequence("e fs*3")
#musx.pitch("a4, g3*3 e f")  $ BUG (RECURSION)

def parse_string_sequence(string):
    # split string at blank spaces, by
    # repeated value, check for dangling and undelimited repeats.
    seq = []
    for raw in string.split():
        pos = raw.rfind('*')
        if pos > -1:    # string has * somewhere
            split = raw.split('*')
            if '' in split or len(split) != 2:
                raise SyntaxError(f"Invalid expansion  '{raw}'.")
            sym, rep = split[0], split[1]
            try:
                val = int(rep)
            except Exception as ve:
                ve.args = (f"Invalid expansion factor '{rep}' in '{raw}'.",)
                raise
            if val < 1 or val > 32:
                raise ValueError(f"Expansion factor '{val}' is not between 1 and 32.")
            else:
                for _ in range(val):
                    seq.append(sym)
        else:
            seq.append(raw)
    return seq


def histo(data):
    """
    Returns a dictionary containing a histogram of the input data.
    
    Parameters
    ----------
    data : list
        The list of data to analyze.
    
    Example
    -------
    >>> histo([3,4,1,1,2,1,5,6,5])
    {3: 1, 4: 1, 1: 3, 2: 1, 5: 2, 6: 1}
    """
    if isinstance(data, list):
        hist = {}
        for d in data:
            try: hist[d] += 1
            except: hist[d] = 1
        return hist
    raise TypeError ("Histogram data is not a list.")
