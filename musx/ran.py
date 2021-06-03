import random
import math
from .tools import rescale

# moved: between, odds, pick to here

def between(a, b):
    """
    Returns a random value between a and b (exclusive).

    An int is returned if both a and b are ints,
    otherwise a float is returned. The a value can be
    less than, equal to, or greater than b.

    Parameters
    ----------
    a : int | float
        The lower bound for the random selection.
    b : int | float
        The upper bound for the random selection.

    Returns
    -------
        A randomly chosen value between a and b.
    """
    if (a < b):
        if isinstance(a, int) and isinstance(b, int):
            return random.randrange(a, b)
        else:
            return a + (random.random() * (b - a))
    if (a > b):
        if isinstance(a, int) and isinstance(b, int):
            return a - random.randrange(b)
        else:
            return a - (random.random() * (a - b))
    return a


def odds(prob, true=True, false=False):
    """
    Returns true value if a random choice is less than prob else returns
    the false.

    Parameters
    ----------
    prob : float | int
        A value between 0 and 1 inclusive.
    true : value
        If odds is true the true value is returned.
    false : value
        If odds is false the false value is returned.

    Returns
    -------
    Either the true value or the false value based on probability.
    """
    if 0 <= prob <= 1.0:
        return true if random.random() < prob else false
    raise ValueError(f"{prob} not a number between 0 and 1.")


def pick(*args):
    """
    Randomly picks one of its arguments to return.

    Parameters
    ----------
    *args : variadic
        A series of values from which one will be randomly selected.

    Returns
    -------
    One value from the argument list.
    """
    return args[random.randrange(len(args))]


def vary(value, variance, shift=None):
    """
    Returns a random number that deviates from value or list of the same by
    up to variance (1=100%) according to shift. 
    
    Parameters
    ----------
    value : number | list
        The value or list of values to vary.
    variance : number
        The maximum amount to vary the value by, e.g. 0.5 means the variance
        could be up to 50% of the input value.
    shift : None | "+" | "-"
        Specifies where the variance is placed. If None then then value is at the
        center of what could be returned. Shift "+" places value at the minimum
        of what could be returned and "-" means that value is the maximum possible
        value returned.
    """
    if isinstance(value, list):
        return [vary(v, variance, shift) for v in value]
    if value == 0 or variance == 0:
        return val
    r = abs(value * variance)
    v = random.random() * r
    if shift == None:
        return (value - (r * .5)) + v
    if shift == '+':
        return value + v
    if shift == '-':
        return value - v
    raise ValueError("shift should be None, '+', or '-' ({shift})")


def ransegs(num, mapto, rangen=None):
    """
    Returns a list of random number segments.

    Parameters
    ----------
    num : int
        The number of random values returned in the list.
    mapto : number | [low, high]
        If mapto is a number then the values retuned will sum to that number.
        If mapto is a list then the random values are sorted and scaled to
        lie proportionatly from low to high.
    rangen : None | function
        If function is provided it will be called to return random numbers,
        otherwise uniform random numbers between are generated.
    """
    #print(f"ransegs(num={num}, mapto={mapto})")
    segs = []
    rsum = 0
    if rangen == None:
        rangen = random.random
    for i in range(num):
        n = rangen()
        segs.append(n)
        rsum += n
    if isinstance(mapto, (list, tuple)):
        segs.sort()
        #print("raws", segs)        
        for i in range(num):
            segs[i] = rescale(segs[i], segs[0], segs[-1], mapto[0], mapto[1])
    else:
        #print("raws", segs)
        for i in range(num):
            segs[i] = rescale(segs[i], 0, rsum, 0, mapto)
    #print("segs", segs)
    return segs

#-----------------------------------------------------------------------------
# Random number functions with different distributions

def uniran():
    """
    Returns a uniformly chosen floating point value between 0.0 and 1.0.
    See also: lowran(), midran(), highran().
    """
    return random.random()


def lowran():
    """
    Returns a floating point value between 0.0 and 1.0 with lower 
    values more likely. See also: uniran(), midran(), highran().
    """
    return min(random.random(), random.random())


def midran():
    """
    Returns a floating point value between 0.0 and 1.0 with midrange
    values more likely. See also: uniran(), lowran(), highran().
    """
    return (random.random() + random.random()) / 2.0


def highran():
    """
    Returns a floating point value between 0.0 and 1.0 with higher 
    values more likely. See also: uniran(), lowran(), midran().
    """
    return max(random.random(), random.random())


def beta(alpha=.5, beta=.5):
    """
    Returns value between 0 and 1 from the beta distribution (https://en.wikipedia.org/wiki/Beta_distribution).
    When a=b=1 the distribution is uniform. When alpha=beta, the distribution is 
    symmetric around .5. When alpha<1 and beta<1 then the density of larger and
    smaller numbers increases. When alpha>1 and beta>1, density is similar to the
    gaussian distribution.
    """
    ra = 1.0 / alpha
    rb = 1.0 / beta
    while True:
        r1 = random.random()
        r2 = random.random()
        y1 = r1 ** ra
        y2 = r2 ** rb
        y3 = y1 + y2
        if y3 <= 1.0:
            return (y1 / y3)


def gamma(alpha=1):
    """
    Returns value greater than 0 from the gamma distribution 
    (https://en.wikipedia.org/wiki/Gamma_distribution).
    Parameter alpha controls the distribution's shape and should be a positive integer
    (if a non-integer is provided, the value is rounded.) When alpha=1, the 
    distribution is the same as exponential. As its value increases, the 
    probability density function becomes a curve with mean=alpha and standard 
    deviation = sqrt(alpha).
    """
    r = 1.0
    n = round(alpha)
    for i in range(n):
        r = r * (1 - random.random())
    return - math.log(r)


def poisson(alpha=1):
    """
    Returns value greater than 0 from the poisson distribution
    (https://en.wikipedia.org/wiki/Poisson_distribution).
    Returns positive integer values, theoretically unbounded but practically
    limited by the alpha parameter. Parameter alpha controls the distribution's 
    shape and must be positive: the mean is a and the standard deviation is sqrt(a).
    """
    b = math.exp( - alpha)
    n = 0
    p = 1.0
    while True:
        p = p * random.random()
        n += 1
        if p < b:
            return n


def expran(alpha=1):
    """
    Returns a value greater than 0 from the exponential distribution
    (https://en.wikipedia.org/wiki/Exponential_distribution) with stretching factor alpha.
    Increasing alpha "prefers" smaller numbers. The distribution is unbounded but when 
    alpha=1 then %99.9 of the time the value returned will be than 6.9077554, i.e. -log(.001).
    The distribution density is f(x)=(exp -x) with a mean of 1.0.
    """
    return (- math.log(1.0 - random.random())) / alpha


def gauss(sigma=1, mu=0):
    """
    Returns unbounded value from the normal distribution
    (https://en.wikipedia.org/wiki/Normal_distribution) with standard deviation
    sigma and mean mu.  The spread (standard deviation) is 1.0 centered at 0, 
    so 68.26% of the results are between -1 and 1 inclusive and 99.74% of the
    results are between -3 and 3 inclusive.
    """
    while True:
        x = -1 + 2 * random.random()
        y = -1 + 2 * random.random()
        r2 = (x * x) + (y * y)
        if not ((r2 > 1.0) or (r2 == 0)):
            break
    return (sigma * y * math.sqrt(-2.0 * math.log(r2) / r2)) + mu


def cauchy(alpha=False):
    """
    Returns an unbounded value from the Cauchy distribution
    (https://en.wikipedia.org/wiki/Cauchy_distribution).
    The density function is a bell shaped curve centered at 0 similar to a
    normal distribution but with more values at the extremes. The mean and
    standard deviation of the Cauchy distribution are undefined. If parameter
    alpha is True then only positive values are returned. Density is f(x)=1/(pi(1 + x^2)).
    """
    #return math.tan( math.pi * 2 * (random.random() - 0.5))
    r = (1.5707964 if alpha else math.pi) * random.random()
    return sin(r) / cos(r)

#-----------------------------------------------------------------------------
# Noises white, brown and pink return sample values -1.0 to 1.0


def white(level=None):
    """
    Returns white (uniform) noise samples between -1.0 and 1.0.

    Parameters
    ----------
    level : None or int or float
        An optional scaler on the sample returned.
    """
    samp = random.random() * 2.0 - 1.0
    return samp * level if level else samp


# def _lowpass(current, previous, alpha):
#     """
#     The change from one filter output to the next is proportional to the
#     difference between the previous output and the next input.
#     """
#     return previous + (alpha * (current - previous))
#
# _brown = white()
# """ The previous brown sample, initialzed to a random number."""
#
# def brown(alpha=.02):
#     global _brown
#     samp = _lowpass(white(), _brown, alpha)
#     _brown = samp
#     return samp * 3.0  # boost the overall gain


_brown = 0.0

def brown():
    """
    Returns brownish (1/f**2) noise samples between -1 and 1.
    """
    # from http://vellocet.com/dsp/noise/VRand.h
    # but made to generate between -1 1
    global _brown
    while True:
        r = random.random() * 2 - 1
        _brown += r
        if (_brown < -16.0) or (_brown > 16.0):
            _brown -= r
        else:
            break
    # return interval -1 1.
    return _brown * 0.0625


_pow2 = 5
_pown = 32
_pinking = [0.0 for _ in range(_pown+1)]

def _one_over_f_aux(n, rarray, halfrange):
    s = 0.0
    for i in range(_pow2):
        p = 2.0 ** i
        if not ( (n / p) == ((n - 1) / p) ):
            rarray[i]=( (random.random() * 2 * halfrange) - halfrange)
        s += rarray[i]
    return s

_i = _pown

def pink():
    """
    Returns pinkish (1/f) noise samples between -1.0 and 1.0.  Based on Gardner
    (1978) and Dick Moore (1988?).
    """
    global _i
    if _i == _pown:
        r = [0.0 for _ in range(_pow2)]
        h = 1.0 / _pow2
        for n in range(_pown):
            _pinking[n]=_one_over_f_aux(n, r, h)
        _i = 0
    else:
        _i += 1
    return _pinking[_i]


if __name__ == '__main__':
    
    ransegs(num=5, mapto=10)
    ransegs(num=5, mapto=(0,4))
    ransegs(num=5, mapto=(-2,4))

    # x = 60
    # for i in range(20):
    #     print(x)
    #     x = drunk(x, width=2)
    # print(x)

   
    # for i in range(20):
    #     print(pink())

    # for i in range(20):
    #     print(brown())

    import numpy as np
    import matplotlib.pyplot as plt
    # beta(.3, .3)
    # x = [pink() for _ in range(10000)]
    # plt.hist(x, bins=20, facecolor="blue", alpha=0.5)
    # plt.show()

#     y = [expran(1.5) for _ in range(1000)]
#     plt.hist(y, bins=20, facecolor="blue", alpha=0.5)
#    #plt.plot(y)
#     plt.show()


    

    #ransegs(5, 2, 4)
    #ransegs(5, 0, 10)
    #ransegs(5, 0, 10)
    #ransegs(5, -10, 10)
    #ransegs(5, sumto=10)

 
        
    #x = ransegs(5, 10)
    #print("sum=", sum(x))









"""
(define (segs num sum)
  (let ((rgen ran)
        (args ()))
    (let* ((rsum (apply rgen args))
           (head (list rsum))
           (tail head))
      (print "rgen " rgen " rsum " rsum " args " args " head" head)
      (do ((i 1 (+ i 1))
           (n #f))
          ((not (< i num))
           (do ((tail head (cdr tail)))
               ((null? tail) head)
             (set-car! tail
                       (ffi_rescale (car tail) 0 rsum 0 sum 1))))
        (set! n (apply rgen args))
        (set-cdr! tail (list n))
        (set! tail (cdr tail))
        (set! rsum (+ rsum n))))
    ))
(let ((l (segs 7 2)))
  (print l)
  (apply + l))
"""
