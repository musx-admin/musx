################################################################################
"""
Functions and classes for working with microtonality, the harmonic series, and
spectra.  For examples of generating microtonal music using midi see the demos
micro.py, gamelan.py, fm.py, and rm.py.
"""

import math
import fractions
from .pitch import keynum
from .tools import quantize


try:
    from scipy.special import jn as bes_jn
except ModuleNotFoundError:
    def bes_jn(a,b):
        raise ModuleNotFoundError("\nfmspectrum(): module scipy.special not found.")


def harmonics(h1, h2, fund=1, reverse=False):
    """
    Returns the harmonic series ratios between harmonic number
    h1 to h2 inclusive.

    If 0 < h1 < h2 then the ratios will produce the overtone series, 
    otherwise (0 > h1 > h2) will produce undertones.  If reverse is
    False then the overtone ratios are ascending and undertones are
    decending.

    Parameters
    ----------
    h1 : int
        The starting harmonic. If positive, overtones are produced
        otherwise negative undertones are produced.
    h2 : int
        The ending harmonic (inclusive). If positive it must be
        equal to or greater than h1. If negativ it must be equal
        to or less than h1.
    fund : int | float
        The fundamental of the series, defaults to 1. If fund is an int
        then exact Faction harmonics are produced. If fund is a float
        then the series will be floats as well.
    reverse : bool
        If true then overtones are returned reversed order.
    
    Returns
    -------
    The list of harmonic ratios between h1 and h2 inclusive.
    """

    if not isinstance(h1, int):
        TypeError(f"not an integer harmonic number: {h1}.")
    if not isinstance(h2, int):
        TypeError(f"not an integer harmonic number: {h2}.")
    utones = False
    harms = []
    if (0 < h1 < h2):
        pass
    elif (0 > h1 > h2):
        utones = True
    else:
        raise ValueError(f"harmonic numbers out of order: {h1} {h2}.")
    h1 = fractions.Fraction(abs(h1),1)
    h2 = fractions.Fraction(abs(h2),1)
    h = h1
    f = None
    while h <= h2:
        # utones collect the reciprocal
        f = fund/(h/h1) if utones else fund*(h/h1)
        harms.append(f)
        h += 1
    if reverse:
        harms.reverse()
    return harms


def temper(ratio, div=12):
    """
    Converts a frequency ratio into a tempered interval.

    Parameters
    ----------
    ratio : int | float | Fraction | list
        The ratio to convert. The value can be an integer, float,
        Fraction, or a list of the same.
    div : int
        The divisions per octave. 12 will convert to
        semitones and 1200 will convert to cents.
    Returns
    -------
    The tempered interval.
    """

    func = lambda r,s: math.log(r)/math.log(2.0) * s
    if type(ratio) is list:
        return [func(r, div) for r in ratio]
    return func(ratio, div)


def untemper(interval, div=12):
    """
    Converts a tempered interval into a frequency ratio.

    Parameters
    ----------
    interval : int | float
        The interval to convert. The value can be an integer, float,
        or a list of the same.
    div : int
        The divisions per octave. 12 will convert from
        semitones and 1200 will convert from cents.
    Returns
    -------
    The untempered frequency ratio
    """

    func = lambda i,d: math.pow(2.0, i/d)
    if type(interval) is list:
        return [func(i, div) for i in interval]
    return func(interval, div)


class Spectrum (list):

    def __new__(cls, pairs):
        """
        Creates a Spectrum out of a list of frequency/amplitude pairs.

        Parameters
        ----------
        pairs : list
            A sorted list of [frequency, amplitude] pairs with lower
            frequency pairs to the left.

        Returns:
        A Spectrum.
        """
        z = 0
        for t in pairs:
            if not isinstance(t, list) or len(t) != 2: 
                raise TypeError(f"not a tuple (frequency, amplitude): {t}.")
            if not isinstance(t[0], (int, float)):
                raise TypeError(f"invalid frequency: {t[0]}.")
            if not isinstance(t[1], (int, float)):
                raise TypeError(f"invalid amplitude: {t[0]}.")
            if not t[0] > z:
                raise ValueError(f"invalid frequency: {t[0]} not greater than {z}.")
            # if not t[1] > 0:
            #     raise ValueError(f"invalid amplitude {t[1]} not greater than 0.")
        return super(Spectrum, cls).__new__(cls, pairs)

    def size(self):
        return len(self)

    def freqs(self):
        """Returns a list of the frequency components in the spectrum."""
        return [t[0] for t in self]

    def amps(self):
        """Returns a list of the amplitude components in the spectrum."""
        return [t[1] for t in self]

    def pairs(self):
        """Returns a list of frequency and amplitude pairs."""
        return list(self)

    def maxfreq(self):
        """Returns the maximum frequency in the spectrum."""
        return self[-1][0]

    def minfreq(self):
        """Returns the minimum frequency in the spectrum."""
        return self[0][0]

    def minamp(self):
        """Returns the minimum amplitude in the spectrum."""
        mina = None
        for t in self:
            if not mina or t[1] < mina:
                 mina = t[1]
        return mina

    def maxamp(self):
        """Returns the minimum amplitude in the spectrum."""
        maxa = None
        for t in self:
            if not maxa or t[1] > maxa:
                 maxa = t[1]
        return maxa

    def __str__(self):
        return f'<Spectrum: {len(self)} {hex(id(self))}>'

    __repr__ = __str__

    def keynums(self, quant=None, unique=None, minkey=0, maxkey=127, thresh=0):
        """
        Returns a list of the frequency components of spectrum converted to key
        numbers. 

        Parameters
        ----------
        quant : int | float | function | None
            If quant is a number then the key numbers returned are quantized to
            that semitonal value, e.g. quant .5 returns key numbers quantized
            to the nearest quarter-tone and quant 1 returns key numbers rounded
            to the nearest semitone. Quant can also be a function, e.g. round,
            ceil, or floor.
        unique : bool
            If unique is True then no duplicate key numbers will be returned. 
        minkey : int | None
            If a minkey number is specified then spectral values lower than that will be octave 
            shifted upward until they equal or exceed it.
        maxkey : int | None
            If a maxkey number is specified then spectral values higher than that will be octave 
            shifted downward until they equal or lower than it.
        thresh : float | None
            The minimum amplitude that a frequency must possess in order to be
             returned as keys.

        Returns
        -------
        A list of key number from the spectrum.
        """
        if not (minkey < maxkey):
            raise TypeError("minkey {minkey} not less than {maxkey}.")
        if callable(quant) or quant is None:
            func = quant
        elif isinstance(quant, (int, float)):
            func = lambda x: quantize(x, quant)
        else:
            raise TypeError("quant value not a callable, number, or None: {quant}.")
        keys = [keynum(x[0], func) for x in self if x[1] >= thresh]
        for i in range(len(keys)):
            while keys[i] < minkey: keys[i] += 12
            while keys[i] > maxkey: keys[i] -= 12
            if not minkey <= keys[i] <= maxkey:
                raise ValueError(f"key {keys[i]} outside bounds {minkey} to {maxkey}.")
        if unique:
            keys = list(dict.fromkeys(keys))
        return sorted(keys)

    def add(self, freq, amp):
        """
        Updates the amplitude of an existing [freq,amp] pair or inserts a new
        pair if freq is not yet in the spectrum.  
        
        Warning: add alters the existing spectrum by adding or updating 
        components.

        Parameters
        ----------
        freq : int | float
            The frequency to add or update.
        amp : int | float
            The amplitude to add or update.
        """

        index = 0
        while index < len(self):
            if self[index][0] == freq:
                self[index][1] += amp   # update existing entry
                return
            elif self[index][0] > freq: # insert before this one
                break
            index += 1
        #print("insert freq", freq, "at index", index, "in", spec)
        self.insert(index, [freq, amp]) # add new entry


def fmspectrum(carrier, mratio, index):
    """
    Returns a spectrum generated by Frequency Modulation.
    
    Parameters
    ---------- 
    carrier : int | float 
        The FM carrier frequency, in hertz.
    mratio : int | float
        The carrier-to-modulator ratio. 1 means the carrier and modulator
        are the same frequency, 2 means the modulator frequency is twice
        the carrier.
    index : int | float
        The index of modulation. The number of FM sidebands (spectral
        components) will be 2*index+1.
    
    Returns
    -------
    A Spectrum created by frequency modulation.
    """

    mfreq = carrier * mratio
    sides = round(index) +  1
    spectrum = {}
    frq = 0
    amp = 0
    for s in range(-sides, sides+1):
        frq = carrier + (mfreq * s)
        amp = bes_jn(s, index)
        if not (amp == 0.0 or frq == 0.0):
            if frq < 0:
                frq = abs(frq)
                amp = -amp
            if spectrum.get(frq):
                spectrum[frq] += amp
            else:
                spectrum[frq] = amp
    return Spectrum( sorted( [f, round(abs(a), 3)] for f,a in spectrum.items()) )


def rmspectrum(freqs1, freqs2, asfreqs=False):
    """
    Returns a spectrum generated by ring modulation, where freq1 and freq2
    can be frequencies, lists of frequencies, or Spectrum objects.
    
    Ring moduluation produces a spectrum consiting of the sum and difference
    tones between all pairs of frequencies in freqs1 and freqs2.

    Parameters
    ----------
    freqs1 : int | float | list | Spectrum
        A hertz value, list of the same, or Spectrum.
    freqs2 : int | float | list | Spectrum
        A hertz value, list of the same, or Spectrum.
    asfreqs : bool
        If true the spectrum's frequency values are returned as a
        list, otherwise the specturm is returned.

    Returns
    -------
    A Spectrum or list containing the pairwise sum and difference tones
    of freqs1 and freqs2.
    """
    if isinstance(freqs1, Spectrum) or isinstance(freqs2, Spectrum):
        raise NotImplementedError("Spectrum input not yet implemented. :(")
    if not isinstance(freqs1, list):
        freqs1 = [freqs1]
    if not isinstance(freqs2, list):
        freqs2 = [freqs2]
    spec = Spectrum([])  # create empty spectrum
    for f1 in freqs1:
        for f2 in freqs2:
            if not f1 == f2:
                spec.add(abs(f1+f2), 0.0)
                spec.add(abs(f1-f2), 0.0)
    return [p[0] for p in spec] if asfreqs else spec

"""
from musx.spectral import fmspectrum
fmspectrum(100, 1.4, 3)
"""

def _read_spear_frame(fstr):
    data = fstr.split(" ")
    time = float(data.pop(0))
    size = int(data.pop(0))
    # omit null frames
    if not data:
        return None
    spec = []
    for i in range(size):
        data.pop(0) # flush partial num
        f = float(data.pop(0)) # read freq
        a = float(data.pop(0)) # read amp
        spec.append([f, a])
    spec.sort(key=lambda a: a[0]) # sort by freq
    return Spectrum(spec)


def import_spear_frames(filename):
    """Imports the contents of a Spear frame data file as a list of Spectrum objects."""
    def rhdr(f):
        l = f.readline()
        if l == '':
            raise ValueError(f"Reached EOF while parsing file header of {filename}")
        return l[:-1]
    
    file = open(filename, 'r')
    line = rhdr(file)
    if not line ==  "par-text-frame-format":
        raise ValueError(f"Expected 'par-text-frame-format' but got '{line}'")
    line = rhdr(file)
    if not line ==  "point-type index frequency amplitude":
        raise ValueError(f"Expected 'point-type index frequency amplitude' but got '{line}'")

    # flush remaining header lines
    while True:
        if line == "frame-data":
            break
        line = rhdr(file)

    # file now at frame-data, read spectra till eof
    frames = []
    line = file.readline()
    while (line):
        spec = _read_spear_frame(line[:-1])
        if spec:
            frames.append(spec)
        line = file.readline()
    return frames

def import_spear_partials(filename):
    """Imports the contents of a Spear partials data file as a list of Spectrum objects."""
    raise NotImplementedError("not implemented yet :(")

if __name__ == '__main__':
    
    from fractions import Fraction
    # print("harmonics(1,8) =>", harmonics(1, 8))
    # print("harmonics(-1,-8) =>",harmonics(-1, -8))
    # print("harmonics(8,16) =>",harmonics(8, 16))
    # print("harmonics(-8,-16) =>",harmonics(-8, -16))
    # print("harmonics(8,16,100) =>",harmonics(8, 16, fund=100))
    # print("harmonics(-8,-16, 100) =>",harmonics(-8, -16, fund=100))
    # print("harmonics(8,16,100) =>",harmonics(8, 16, fund=100.0))
    # print("harmonics(-8,-16, 100) =>",harmonics(-8, -16, fund=100.0))
    import musx
    x=musx.fmspectrum(100, 1.4, 3) 
    x.keynums()
