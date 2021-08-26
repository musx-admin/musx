"""
A class that represents a key signature and mode.
"""

from ..pitch import Pitch
from .mode import Mode
from ..interval import Interval


class Key:
    """
    A key consists of an integer 'signum' representing the number of sharps or
    flats in the key's signature, and a `musx.mxml.mode.Mode`.
 
    Parameters
    ----------
    signum : int
        A value -7 to 7 representing the number of flats (negative) or sharps (positive)
        in the key signature.
    mode : Mode
        A Mode enum, or its case-insensitive string name.
    staffid : int
        The staff number to which the Key will be associated. If the
        value is 0 the key is associated will all staffs.
    """
    # Private map of key signature numbers (-7 to 7) to Pitch.pnums
    # representing the tonic notes of the major keys in the cycle of
    # fifths. For example, the signum -1 maps to Pitch.pnum.F, the
    # tonic of F major.
    _tonics = {i-7: v for i, v in enumerate([
        Pitch.pnums.Cf, Pitch.pnums.Gf, Pitch.pnums.Df, Pitch.pnums.Af,
        Pitch.pnums.Ef, Pitch.pnums.Bf, Pitch.pnums.F, Pitch.pnums.C,
        Pitch.pnums.G, Pitch.pnums.D, Pitch.pnums.A, Pitch.pnums.E,
        Pitch.pnums.B, Pitch.pnums.Fs, Pitch.pnums.Cs])}

    # Private map returns a transposition interval for the key's tonic
    # Pnum. Major is not included because it involves no transposition.
    _transp = {Mode.MINOR: 'M6', Mode.DORIAN: 'M2',
               Mode.PHRYGIAN: 'M3', Mode.LYDIAN: 'P4', Mode.MIXOLYDIAN: 'P5',
               Mode.LOCRIAN: 'M7'}

    def __init__(self, signum, mode, staffid):
        """
        Creates a Key from an integer key signature identifier and mode.
        """
        if isinstance(signum, int):
            if -7 <= signum <= 7:
                if isinstance(mode, str):
                    m = mode
                    mode = Mode.__dict__.get(m.upper())
                    if mode is None:
                        raise ValueError(f"'{m}' is an invalid mode name.")
                elif not isinstance(mode, Mode):
                    raise TypeError(f'{signum} is not a Mode or mode name.')
            else:
                raise ValueError(f'{signum} is not a key signature between -7 and 7.')
        else:
            raise TypeError(f'{signum} is not a key signature between -7 and 7.')
        # The the number of flats or sharp, -7 to 7
        self.signum = signum
        # The Mode of the key.
        self.mode = mode
        # The staff number of the key (0=All)
        self.staffid = staffid

    def __str__(self):
        """
        Returns the print representation of the key.
        """
        staff = "all" if self.staffid == 0 else self.staffid
        if self.mode:
            # Force tonic pnum to display "#" and "b" as accidental.
            text = self.tonic().name
            text = text.replace('f', 'b') if 'f' in text else text.replace('s', '#')
            text += f'-{self.mode.name.capitalize()}'
        else:
            text = str(abs(self.signum)) + " "
            if abs(self.signum) > 1: 
                text += "sharps" if self.signum > 0 else "flats"
            elif self.signum == 0: 
                text += "accidentals"
            else: 
                text += "sharp" if self.signum == 1 else "flat"
        return f'<Key: {text} staff={staff}>' # {hex(id(self))}

    def tonic(self):
        """
        Returns a Pnum representing the key's tonic note. See `musx.pitch.Pitch`
        for documentation on Pnum.
        """
        ton = self._tonics[self.signum]
        if self.mode is Mode.MAJOR:
            return ton
        return Interval(self._transp[self.mode]).transpose(ton)

    def scale(self):
        """
        Returns a list of Pnums representing the pitches of the key's
        diatonic scale. The octave completion is not included in the list.
        """
        steps = [Interval('M2'), Interval('M2'), Interval('m2'),
                 Interval('M2'), Interval('M2'), Interval('M2'),
                 Interval('m2')]
        start = self.mode.tonic_degree()
        order = steps[start:] + steps[:start]
        tonic = self.tonic()
        scale = [tonic]
        for s in order[:-1]:
            tonic = s.transpose(tonic)
            scale.append(tonic)
        return scale
