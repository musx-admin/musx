###############################################################################
"""
Adds methods to python's Fraction class for representing exact time, mensural tuples,  
tuning ratios, etc. 
"""

from fractions import Fraction
   
def dotted(self, dots=1):
    """
    Returns the 'dotted' value of the fraction, e.g. 1/4 with
    one dot is 1/4 + 1/8 = 3/8, e.g. the time value of a dotted quarter.

    Parameters
    ----------
    dots : int
        The number of dots to apply, each dot adds half the previous 
        value of the fraction.

    Returns
    -------
    A new fraction representing the dotted value.
    """
    if isinstance(dots, int) and dots > 0:
        return self * (2 - Fraction(1, 2**dots))
    raise ValueError(f"Dots value is not a positive integer: {dots}.")


def tuplets(self, num, intimeof=1):
    """
    Returns a list of num sub-divisions (metric 'tuples') that sum to
    value of fraction * num.
    
    Parameters
    ----------
    num : int
        The number of tuples to return.  
    intimeof : int
        A number that, when multiplied by the fraction itself,
        represents the sum of all the tuplets in the list.

    Examples
    --------
    >>> Fraction(1, 4).tuplets( 3)
    [Fraction(1, 12), Fraction(1, 12), Fraction(1, 12)]
    >>> Fraction(1, 4).tuplets(3, 2)
    [Fraction(1, 6), Fraction(1, 6), Fraction(1, 6)]
    """
    tup = Fraction(intimeof, num)
    one = self * tup
    return [one for _ in range(num)]


def tup(self, num):
    """
    Returns the fraction representing num divisions of the current fraction.

    Parameters
    ----------
    num : int
        The number to divide this fraction by.

    Examples
    --------
    >>> Fraction(1, 4).tup(5)
    Fraction(1, 20)
    """
    if isinstance(num, int) and num > 0:
        return Fraction(self._numerator, (self._denominator * num))
    raise ValueError(f"Invalid tup divisor: {num}.")


def seconds(self, tempo=60, beat=None):
    """
    Converts a fraction to floating point seconds according to a
    given tempo and beat.
    
    Parameters
    ----------
    tempo : int
        The tempo in beats per minute. Defaults to 60.
    beat : Fraction
        A fraction representing the beat. Defaults to 1/4 (quarter note).

    Examples
    --------
    >>> Fraction(1,4).seconds(tempo=120)
    0.5

    Returns
    -------
    A floating point value in seconds.
    """
    if beat is None:
        beat = Fraction(1, 4)
    elif isinstance(beat, int):
        beat = Fraction(beat, 1)
    if isinstance(beat, Fraction):
        return (beat._denominator / beat._numerator) * (self._numerator / self._denominator) * (60 / tempo)
    raise TypeError(f'Invalid beat: {beat}.')


# this adds the extensions to python's Fraction class.

Fraction.dotted = dotted
Fraction.tuplets = tuplets
Fraction.tup = tup
Fraction.seconds = seconds


if __name__ == "__main__":
    pass









