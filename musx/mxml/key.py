###############################################################################
"""
The Key class represents the complete chromatic set of keys in western music.
"""


__pdoc__ = {
    'Key.__init__': True, 'Key.__str__': True, 'Key.__repr__': True
}


from ..pitch import Pitch
from .mode import Mode
from ..interval import Interval


class Key:
    """
    A key consists of an integer 'signum' representing the number of sharps or
    flats in the key's signature, and a Mode (Enum). Keys can return Pnums
    representing their tonic note and diatonic scale degrees.
    See: https://en.wikipedia.org/wiki/Key_(music)
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

    def __init__(self, signum, mode, staffnum):
        """
        Creates a Key from an integer key signature identifier and mode.
        
        Parameters
        ----------
        signum : int
            A value -7 to 7 representing the number of flats (negative) or sharps (positive).
        mode : Mode
            A Mode enum, or its case-insensitive string name.

        Raises 
        ------
        A TypeError if signum is not an integer or if mode is not a Mode or string.<br>
        A ValueError if the signum integer or the mode string is invalid.
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
        self.staffnum = staffnum

    def __str__(self):
        """
        Returns the print representation of the key.
        """
        staff = "all" if self.staffnum == 0 else self.staffnum
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

    # def __repr__(self):
    #     """
    #     Returns the external representation of the Key including the
    #     constructor name, signum, and the capitalized version of the
    #     mode's name.
        
    #     Examples
    #     --------
    #     'Key(4, "Dorian")'<br>
    #     'Key(-1, "Major")'
    #     """
    #     return f'Key({self.signum}, "{self.mode.name.capitalize()}")'

    # def string(self):
    #     """
    #     Returns a string containing the name of the tonic Pnum, a
    #     hyphen, and the capitalized version of the mode's name.
    
    #     Examples
    #     --------
    #     'Fs-Dorian',<br>
    #     'Bf-Phrygian',<br>
    #     'B-Major'
    #     """
    #     return f'{self.tonic().name}-{self.mode.name.capitalize()}'

    def tonic(self):
        """
        Returns a Pnum representing the key's tonic. The tonic can
        be calculated by transposing the Major tonic (Pnum) by the
        interval distance of the mode above the major. The
        transposition can be performed using that interval's transpose()
        method. The interval distances of Major up to Locrian are:
        P1, M2, M3, P4, P5, M6, M7.
        
        Examples
        --------
        Key(0, "lydian").tonic() is Pnum F.<br>
        Key(2, "dorian").tonic() is Pnum E.<br>
        Key(-6, "phrygian").tonic() is Pnum Bf.<br>
        """
        ton = self._tonics[self.signum]
        if self.mode is Mode.MAJOR:
            return ton
        return Interval(self._transp[self.mode]).transpose(ton)

    def scale(self):
        """
        Returns a list of Pnums representing the unique pitches of the key's
        diatonic scale. The octave completion should NOT be included in the list.
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


def _test_keys():
    # for s in range(-7, 8):
    #     for m in ['Major', 'Minor', "Dorian", "Phrygian", "Mixolydian",
    #               "Aeolian", "Locrian"]:
    #         print(f'assert \'Key({s}, "{m}")\'', "==", f"Key({s}, '{m}').__repr__()")

    # for s in range(-7, 8):
    #     for m in ['Major', 'Minor', "Dorian", "Phrygian", "Mixolydian",
    #               "Aeolian", "Locrian"]:
    #         print(f"assert '{Key(s, m).tonic().name}'", "==", f"Key({s}, '{m}').tonic().name")

    # for s in range(-7, 8):
    #     for m in ['Major', 'Minor', "Dorian", "Phrygian", "Mixolydian",
    #               "Aeolian", "Locrian"]:
    #         print(f"assert '{Key(s, m).scale()[-1].name}'", "==", f"Key({s}, '{m}').scale()[-1].name")

    print('Testing key.py ... ', end='')
    assert 'Key(-7, "Major")' == Key(-7, 'Major').__repr__()
    assert 'Key(-7, "Minor")' == Key(-7, 'Minor').__repr__()
    assert 'Key(-7, "Dorian")' == Key(-7, 'Dorian').__repr__()
    assert 'Key(-7, "Phrygian")' == Key(-7, 'Phrygian').__repr__()
    assert 'Key(-7, "Mixolydian")' == Key(-7, 'Mixolydian').__repr__()
    assert 'Key(-7, "Minor")' == Key(-7, 'Aeolian').__repr__()
    assert 'Key(-7, "Locrian")' == Key(-7, 'Locrian').__repr__()
    assert 'Key(-6, "Major")' == Key(-6, 'Major').__repr__()
    assert 'Key(-6, "Minor")' == Key(-6, 'Minor').__repr__()
    assert 'Key(-6, "Dorian")' == Key(-6, 'Dorian').__repr__()
    assert 'Key(-6, "Phrygian")' == Key(-6, 'Phrygian').__repr__()
    assert 'Key(-6, "Mixolydian")' == Key(-6, 'Mixolydian').__repr__()
    assert 'Key(-6, "Minor")' == Key(-6, 'Aeolian').__repr__()
    assert 'Key(-6, "Locrian")' == Key(-6, 'Locrian').__repr__()
    assert 'Key(-5, "Major")' == Key(-5, 'Major').__repr__()
    assert 'Key(-5, "Minor")' == Key(-5, 'Minor').__repr__()
    assert 'Key(-5, "Dorian")' == Key(-5, 'Dorian').__repr__()
    assert 'Key(-5, "Phrygian")' == Key(-5, 'Phrygian').__repr__()
    assert 'Key(-5, "Mixolydian")' == Key(-5, 'Mixolydian').__repr__()
    assert 'Key(-5, "Minor")' == Key(-5, 'Aeolian').__repr__()
    assert 'Key(-5, "Locrian")' == Key(-5, 'Locrian').__repr__()
    assert 'Key(-4, "Major")' == Key(-4, 'Major').__repr__()
    assert 'Key(-4, "Minor")' == Key(-4, 'Minor').__repr__()
    assert 'Key(-4, "Dorian")' == Key(-4, 'Dorian').__repr__()
    assert 'Key(-4, "Phrygian")' == Key(-4, 'Phrygian').__repr__()
    assert 'Key(-4, "Mixolydian")' == Key(-4, 'Mixolydian').__repr__()
    assert 'Key(-4, "Minor")' == Key(-4, 'Aeolian').__repr__()
    assert 'Key(-4, "Locrian")' == Key(-4, 'Locrian').__repr__()
    assert 'Key(-3, "Major")' == Key(-3, 'Major').__repr__()
    assert 'Key(-3, "Minor")' == Key(-3, 'Minor').__repr__()
    assert 'Key(-3, "Dorian")' == Key(-3, 'Dorian').__repr__()
    assert 'Key(-3, "Phrygian")' == Key(-3, 'Phrygian').__repr__()
    assert 'Key(-3, "Mixolydian")' == Key(-3, 'Mixolydian').__repr__()
    assert 'Key(-3, "Minor")' == Key(-3, 'Aeolian').__repr__()
    assert 'Key(-3, "Locrian")' == Key(-3, 'Locrian').__repr__()
    assert 'Key(-2, "Major")' == Key(-2, 'Major').__repr__()
    assert 'Key(-2, "Minor")' == Key(-2, 'Minor').__repr__()
    assert 'Key(-2, "Dorian")' == Key(-2, 'Dorian').__repr__()
    assert 'Key(-2, "Phrygian")' == Key(-2, 'Phrygian').__repr__()
    assert 'Key(-2, "Mixolydian")' == Key(-2, 'Mixolydian').__repr__()
    assert 'Key(-2, "Minor")' == Key(-2, 'Aeolian').__repr__()
    assert 'Key(-2, "Locrian")' == Key(-2, 'Locrian').__repr__()
    assert 'Key(-1, "Major")' == Key(-1, 'Major').__repr__()
    assert 'Key(-1, "Minor")' == Key(-1, 'Minor').__repr__()
    assert 'Key(-1, "Dorian")' == Key(-1, 'Dorian').__repr__()
    assert 'Key(-1, "Phrygian")' == Key(-1, 'Phrygian').__repr__()
    assert 'Key(-1, "Mixolydian")' == Key(-1, 'Mixolydian').__repr__()
    assert 'Key(-1, "Minor")' == Key(-1, 'Aeolian').__repr__()
    assert 'Key(-1, "Locrian")' == Key(-1, 'Locrian').__repr__()
    assert 'Key(0, "Major")' == Key(0, 'Major').__repr__()
    assert 'Key(0, "Minor")' == Key(0, 'Minor').__repr__()
    assert 'Key(0, "Dorian")' == Key(0, 'Dorian').__repr__()
    assert 'Key(0, "Phrygian")' == Key(0, 'Phrygian').__repr__()
    assert 'Key(0, "Mixolydian")' == Key(0, 'Mixolydian').__repr__()
    assert 'Key(0, "Minor")' == Key(0, 'Aeolian').__repr__()
    assert 'Key(0, "Locrian")' == Key(0, 'Locrian').__repr__()
    assert 'Key(1, "Major")' == Key(1, 'Major').__repr__()
    assert 'Key(1, "Minor")' == Key(1, 'Minor').__repr__()
    assert 'Key(1, "Dorian")' == Key(1, 'Dorian').__repr__()
    assert 'Key(1, "Phrygian")' == Key(1, 'Phrygian').__repr__()
    assert 'Key(1, "Mixolydian")' == Key(1, 'Mixolydian').__repr__()
    assert 'Key(1, "Minor")' == Key(1, 'Aeolian').__repr__()
    assert 'Key(1, "Locrian")' == Key(1, 'Locrian').__repr__()
    assert 'Key(2, "Major")' == Key(2, 'Major').__repr__()
    assert 'Key(2, "Minor")' == Key(2, 'Minor').__repr__()
    assert 'Key(2, "Dorian")' == Key(2, 'Dorian').__repr__()
    assert 'Key(2, "Phrygian")' == Key(2, 'Phrygian').__repr__()
    assert 'Key(2, "Mixolydian")' == Key(2, 'Mixolydian').__repr__()
    assert 'Key(2, "Minor")' == Key(2, 'Aeolian').__repr__()
    assert 'Key(2, "Locrian")' == Key(2, 'Locrian').__repr__()
    assert 'Key(3, "Major")' == Key(3, 'Major').__repr__()
    assert 'Key(3, "Minor")' == Key(3, 'Minor').__repr__()
    assert 'Key(3, "Dorian")' == Key(3, 'Dorian').__repr__()
    assert 'Key(3, "Phrygian")' == Key(3, 'Phrygian').__repr__()
    assert 'Key(3, "Mixolydian")' == Key(3, 'Mixolydian').__repr__()
    assert 'Key(3, "Minor")' == Key(3, 'Aeolian').__repr__()
    assert 'Key(3, "Locrian")' == Key(3, 'Locrian').__repr__()
    assert 'Key(4, "Major")' == Key(4, 'Major').__repr__()
    assert 'Key(4, "Minor")' == Key(4, 'Minor').__repr__()
    assert 'Key(4, "Dorian")' == Key(4, 'Dorian').__repr__()
    assert 'Key(4, "Phrygian")' == Key(4, 'Phrygian').__repr__()
    assert 'Key(4, "Mixolydian")' == Key(4, 'Mixolydian').__repr__()
    assert 'Key(4, "Minor")' == Key(4, 'Minor').__repr__()
    assert 'Key(4, "Locrian")' == Key(4, 'Locrian').__repr__()
    assert 'Key(5, "Major")' == Key(5, 'Major').__repr__()
    assert 'Key(5, "Minor")' == Key(5, 'Minor').__repr__()
    assert 'Key(5, "Dorian")' == Key(5, 'Dorian').__repr__()
    assert 'Key(5, "Phrygian")' == Key(5, 'Phrygian').__repr__()
    assert 'Key(5, "Mixolydian")' == Key(5, 'Mixolydian').__repr__()
    assert 'Key(5, "Minor")' == Key(5, 'Minor').__repr__()
    assert 'Key(5, "Locrian")' == Key(5, 'Locrian').__repr__()
    assert 'Key(6, "Major")' == Key(6, 'Major').__repr__()
    assert 'Key(6, "Minor")' == Key(6, 'Minor').__repr__()
    assert 'Key(6, "Dorian")' == Key(6, 'Dorian').__repr__()
    assert 'Key(6, "Phrygian")' == Key(6, 'Phrygian').__repr__()
    assert 'Key(6, "Mixolydian")' == Key(6, 'Mixolydian').__repr__()
    assert 'Key(6, "Minor")' == Key(6, 'Aeolian').__repr__()
    assert 'Key(6, "Locrian")' == Key(6, 'Locrian').__repr__()
    assert 'Key(7, "Major")' == Key(7, 'Major').__repr__()
    assert 'Key(7, "Minor")' == Key(7, 'Minor').__repr__()
    assert 'Key(7, "Dorian")' == Key(7, 'Dorian').__repr__()
    assert 'Key(7, "Phrygian")' == Key(7, 'Phrygian').__repr__()
    assert 'Key(7, "Mixolydian")' == Key(7, 'Mixolydian').__repr__()
    assert 'Key(7, "Minor")' == Key(7, 'Aeolian').__repr__()
    assert 'Key(7, "Locrian")' == Key(7, 'Locrian').__repr__()

    assert 'Cf' == Key(-7, 'Major').tonic().name
    assert 'Af' == Key(-7, 'Minor').tonic().name
    assert 'Df' == Key(-7, 'Dorian').tonic().name
    assert 'Ef' == Key(-7, 'Phrygian').tonic().name
    assert 'Gf' == Key(-7, 'Mixolydian').tonic().name
    assert 'Af' == Key(-7, 'Aeolian').tonic().name
    assert 'Bf' == Key(-7, 'Locrian').tonic().name
    assert 'Gf' == Key(-6, 'Major').tonic().name
    assert 'Ef' == Key(-6, 'Minor').tonic().name
    assert 'Af' == Key(-6, 'Dorian').tonic().name
    assert 'Bf' == Key(-6, 'Phrygian').tonic().name
    assert 'Df' == Key(-6, 'Mixolydian').tonic().name
    assert 'Ef' == Key(-6, 'Aeolian').tonic().name
    assert 'F' == Key(-6, 'Locrian').tonic().name
    assert 'Df' == Key(-5, 'Major').tonic().name
    assert 'Bf' == Key(-5, 'Minor').tonic().name
    assert 'Ef' == Key(-5, 'Dorian').tonic().name
    assert 'F' == Key(-5, 'Phrygian').tonic().name
    assert 'Af' == Key(-5, 'Mixolydian').tonic().name
    assert 'Bf' == Key(-5, 'Aeolian').tonic().name
    assert 'C' == Key(-5, 'Locrian').tonic().name
    assert 'Af' == Key(-4, 'Major').tonic().name
    assert 'F' == Key(-4, 'Minor').tonic().name
    assert 'Bf' == Key(-4, 'Dorian').tonic().name
    assert 'C' == Key(-4, 'Phrygian').tonic().name
    assert 'Ef' == Key(-4, 'Mixolydian').tonic().name
    assert 'F' == Key(-4, 'Aeolian').tonic().name
    assert 'G' == Key(-4, 'Locrian').tonic().name
    assert 'Ef' == Key(-3, 'Major').tonic().name
    assert 'C' == Key(-3, 'Minor').tonic().name
    assert 'F' == Key(-3, 'Dorian').tonic().name
    assert 'G' == Key(-3, 'Phrygian').tonic().name
    assert 'Bf' == Key(-3, 'Mixolydian').tonic().name
    assert 'C' == Key(-3, 'Aeolian').tonic().name
    assert 'D' == Key(-3, 'Locrian').tonic().name
    assert 'Bf' == Key(-2, 'Major').tonic().name
    assert 'G' == Key(-2, 'Minor').tonic().name
    assert 'C' == Key(-2, 'Dorian').tonic().name
    assert 'D' == Key(-2, 'Phrygian').tonic().name
    assert 'F' == Key(-2, 'Mixolydian').tonic().name
    assert 'G' == Key(-2, 'Aeolian').tonic().name
    assert 'A' == Key(-2, 'Locrian').tonic().name
    assert 'F' == Key(-1, 'Major').tonic().name
    assert 'D' == Key(-1, 'Minor').tonic().name
    assert 'G' == Key(-1, 'Dorian').tonic().name
    assert 'A' == Key(-1, 'Phrygian').tonic().name
    assert 'C' == Key(-1, 'Mixolydian').tonic().name
    assert 'D' == Key(-1, 'Aeolian').tonic().name
    assert 'E' == Key(-1, 'Locrian').tonic().name
    assert 'C' == Key(0, 'Major').tonic().name
    assert 'A' == Key(0, 'Minor').tonic().name
    assert 'D' == Key(0, 'Dorian').tonic().name
    assert 'E' == Key(0, 'Phrygian').tonic().name
    assert 'G' == Key(0, 'Mixolydian').tonic().name
    assert 'A' == Key(0, 'Aeolian').tonic().name
    assert 'B' == Key(0, 'Locrian').tonic().name
    assert 'G' == Key(1, 'Major').tonic().name
    assert 'E' == Key(1, 'Minor').tonic().name
    assert 'A' == Key(1, 'Dorian').tonic().name
    assert 'B' == Key(1, 'Phrygian').tonic().name
    assert 'D' == Key(1, 'Mixolydian').tonic().name
    assert 'E' == Key(1, 'Aeolian').tonic().name
    assert 'Fs' == Key(1, 'Locrian').tonic().name
    assert 'D' == Key(2, 'Major').tonic().name
    assert 'B' == Key(2, 'Minor').tonic().name
    assert 'E' == Key(2, 'Dorian').tonic().name
    assert 'Fs' == Key(2, 'Phrygian').tonic().name
    assert 'A' == Key(2, 'Mixolydian').tonic().name
    assert 'B' == Key(2, 'Aeolian').tonic().name
    assert 'Cs' == Key(2, 'Locrian').tonic().name
    assert 'A' == Key(3, 'Major').tonic().name
    assert 'Fs' == Key(3, 'Minor').tonic().name
    assert 'B' == Key(3, 'Dorian').tonic().name
    assert 'Cs' == Key(3, 'Phrygian').tonic().name
    assert 'E' == Key(3, 'Mixolydian').tonic().name
    assert 'Fs' == Key(3, 'Aeolian').tonic().name
    assert 'Gs' == Key(3, 'Locrian').tonic().name
    assert 'E' == Key(4, 'Major').tonic().name
    assert 'Cs' == Key(4, 'Minor').tonic().name
    assert 'Fs' == Key(4, 'Dorian').tonic().name
    assert 'Gs' == Key(4, 'Phrygian').tonic().name
    assert 'B' == Key(4, 'Mixolydian').tonic().name
    assert 'Cs' == Key(4, 'Aeolian').tonic().name
    assert 'Ds' == Key(4, 'Locrian').tonic().name
    assert 'B' == Key(5, 'Major').tonic().name
    assert 'Gs' == Key(5, 'Minor').tonic().name
    assert 'Cs' == Key(5, 'Dorian').tonic().name
    assert 'Ds' == Key(5, 'Phrygian').tonic().name
    assert 'Fs' == Key(5, 'Mixolydian').tonic().name
    assert 'Gs' == Key(5, 'Aeolian').tonic().name
    assert 'As' == Key(5, 'Locrian').tonic().name
    assert 'Fs' == Key(6, 'Major').tonic().name
    assert 'Ds' == Key(6, 'Minor').tonic().name
    assert 'Gs' == Key(6, 'Dorian').tonic().name
    assert 'As' == Key(6, 'Phrygian').tonic().name
    assert 'Cs' == Key(6, 'Mixolydian').tonic().name
    assert 'Ds' == Key(6, 'Aeolian').tonic().name
    assert 'Es' == Key(6, 'Locrian').tonic().name
    assert 'Cs' == Key(7, 'Major').tonic().name
    assert 'As' == Key(7, 'Minor').tonic().name
    assert 'Ds' == Key(7, 'Dorian').tonic().name
    assert 'Es' == Key(7, 'Phrygian').tonic().name
    assert 'Gs' == Key(7, 'Mixolydian').tonic().name
    assert 'As' == Key(7, 'Aeolian').tonic().name
    assert 'Bs' == Key(7, 'Locrian').tonic().name

    assert 'Bf' == Key(-7, 'Major').scale()[-1].name
    assert 'Gf' == Key(-7, 'Minor').scale()[-1].name
    assert 'Cf' == Key(-7, 'Dorian').scale()[-1].name
    assert 'Df' == Key(-7, 'Phrygian').scale()[-1].name
    assert 'Ff' == Key(-7, 'Mixolydian').scale()[-1].name
    assert 'Gf' == Key(-7, 'Aeolian').scale()[-1].name
    assert 'Af' == Key(-7, 'Locrian').scale()[-1].name
    assert 'F' == Key(-6, 'Major').scale()[-1].name
    assert 'Df' == Key(-6, 'Minor').scale()[-1].name
    assert 'Gf' == Key(-6, 'Dorian').scale()[-1].name
    assert 'Af' == Key(-6, 'Phrygian').scale()[-1].name
    assert 'Cf' == Key(-6, 'Mixolydian').scale()[-1].name
    assert 'Df' == Key(-6, 'Aeolian').scale()[-1].name
    assert 'Ef' == Key(-6, 'Locrian').scale()[-1].name
    assert 'C' == Key(-5, 'Major').scale()[-1].name
    assert 'Af' == Key(-5, 'Minor').scale()[-1].name
    assert 'Df' == Key(-5, 'Dorian').scale()[-1].name
    assert 'Ef' == Key(-5, 'Phrygian').scale()[-1].name
    assert 'Gf' == Key(-5, 'Mixolydian').scale()[-1].name
    assert 'Af' == Key(-5, 'Aeolian').scale()[-1].name
    assert 'Bf' == Key(-5, 'Locrian').scale()[-1].name
    assert 'G' == Key(-4, 'Major').scale()[-1].name
    assert 'Ef' == Key(-4, 'Minor').scale()[-1].name
    assert 'Af' == Key(-4, 'Dorian').scale()[-1].name
    assert 'Bf' == Key(-4, 'Phrygian').scale()[-1].name
    assert 'Df' == Key(-4, 'Mixolydian').scale()[-1].name
    assert 'Ef' == Key(-4, 'Aeolian').scale()[-1].name
    assert 'F' == Key(-4, 'Locrian').scale()[-1].name
    assert 'D' == Key(-3, 'Major').scale()[-1].name
    assert 'Bf' == Key(-3, 'Minor').scale()[-1].name
    assert 'Ef' == Key(-3, 'Dorian').scale()[-1].name
    assert 'F' == Key(-3, 'Phrygian').scale()[-1].name
    assert 'Af' == Key(-3, 'Mixolydian').scale()[-1].name
    assert 'Bf' == Key(-3, 'Aeolian').scale()[-1].name
    assert 'C' == Key(-3, 'Locrian').scale()[-1].name
    assert 'A' == Key(-2, 'Major').scale()[-1].name
    assert 'F' == Key(-2, 'Minor').scale()[-1].name
    assert 'Bf' == Key(-2, 'Dorian').scale()[-1].name
    assert 'C' == Key(-2, 'Phrygian').scale()[-1].name
    assert 'Ef' == Key(-2, 'Mixolydian').scale()[-1].name
    assert 'F' == Key(-2, 'Aeolian').scale()[-1].name
    assert 'G' == Key(-2, 'Locrian').scale()[-1].name
    assert 'E' == Key(-1, 'Major').scale()[-1].name
    assert 'C' == Key(-1, 'Minor').scale()[-1].name
    assert 'F' == Key(-1, 'Dorian').scale()[-1].name
    assert 'G' == Key(-1, 'Phrygian').scale()[-1].name
    assert 'Bf' == Key(-1, 'Mixolydian').scale()[-1].name
    assert 'C' == Key(-1, 'Aeolian').scale()[-1].name
    assert 'D' == Key(-1, 'Locrian').scale()[-1].name
    assert 'B' == Key(0, 'Major').scale()[-1].name
    assert 'G' == Key(0, 'Minor').scale()[-1].name
    assert 'C' == Key(0, 'Dorian').scale()[-1].name
    assert 'D' == Key(0, 'Phrygian').scale()[-1].name
    assert 'F' == Key(0, 'Mixolydian').scale()[-1].name
    assert 'G' == Key(0, 'Aeolian').scale()[-1].name
    assert 'A' == Key(0, 'Locrian').scale()[-1].name
    assert 'Fs' == Key(1, 'Major').scale()[-1].name
    assert 'D' == Key(1, 'Minor').scale()[-1].name
    assert 'G' == Key(1, 'Dorian').scale()[-1].name
    assert 'A' == Key(1, 'Phrygian').scale()[-1].name
    assert 'C' == Key(1, 'Mixolydian').scale()[-1].name
    assert 'D' == Key(1, 'Aeolian').scale()[-1].name
    assert 'E' == Key(1, 'Locrian').scale()[-1].name
    assert 'Cs' == Key(2, 'Major').scale()[-1].name
    assert 'A' == Key(2, 'Minor').scale()[-1].name
    assert 'D' == Key(2, 'Dorian').scale()[-1].name
    assert 'E' == Key(2, 'Phrygian').scale()[-1].name
    assert 'G' == Key(2, 'Mixolydian').scale()[-1].name
    assert 'A' == Key(2, 'Aeolian').scale()[-1].name
    assert 'B' == Key(2, 'Locrian').scale()[-1].name
    assert 'Gs' == Key(3, 'Major').scale()[-1].name
    assert 'E' == Key(3, 'Minor').scale()[-1].name
    assert 'A' == Key(3, 'Dorian').scale()[-1].name
    assert 'B' == Key(3, 'Phrygian').scale()[-1].name
    assert 'D' == Key(3, 'Mixolydian').scale()[-1].name
    assert 'E' == Key(3, 'Aeolian').scale()[-1].name
    assert 'Fs' == Key(3, 'Locrian').scale()[-1].name
    assert 'Ds' == Key(4, 'Major').scale()[-1].name
    assert 'B' == Key(4, 'Minor').scale()[-1].name
    assert 'E' == Key(4, 'Dorian').scale()[-1].name
    assert 'Fs' == Key(4, 'Phrygian').scale()[-1].name
    assert 'A' == Key(4, 'Mixolydian').scale()[-1].name
    assert 'B' == Key(4, 'Aeolian').scale()[-1].name
    assert 'Cs' == Key(4, 'Locrian').scale()[-1].name
    assert 'As' == Key(5, 'Major').scale()[-1].name
    assert 'Fs' == Key(5, 'Minor').scale()[-1].name
    assert 'B' == Key(5, 'Dorian').scale()[-1].name
    assert 'Cs' == Key(5, 'Phrygian').scale()[-1].name
    assert 'E' == Key(5, 'Mixolydian').scale()[-1].name
    assert 'Fs' == Key(5, 'Aeolian').scale()[-1].name
    assert 'Gs' == Key(5, 'Locrian').scale()[-1].name
    assert 'Es' == Key(6, 'Major').scale()[-1].name
    assert 'Cs' == Key(6, 'Minor').scale()[-1].name
    assert 'Fs' == Key(6, 'Dorian').scale()[-1].name
    assert 'Gs' == Key(6, 'Phrygian').scale()[-1].name
    assert 'B' == Key(6, 'Mixolydian').scale()[-1].name
    assert 'Cs' == Key(6, 'Aeolian').scale()[-1].name
    assert 'Ds' == Key(6, 'Locrian').scale()[-1].name
    assert 'Bs' == Key(7, 'Major').scale()[-1].name
    assert 'Gs' == Key(7, 'Minor').scale()[-1].name
    assert 'Cs' == Key(7, 'Dorian').scale()[-1].name
    assert 'Ds' == Key(7, 'Phrygian').scale()[-1].name
    assert 'Fs' == Key(7, 'Mixolydian').scale()[-1].name
    assert 'Gs' == Key(7, 'Aeolian').scale()[-1].name
    assert 'As' == Key(7, 'Locrian').scale()[-1].name

    # ERRORS
    msg1, msg2 = "Received wrong type of exception.", \
                 "Expected exception did not happen."

    # TYPE ERRORS
    err = TypeError

    try: Key(1.0, "major")
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Key(0, .4)
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    # TYPE ERRORS
    err = ValueError

    try: Key(-7, "foo")
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try:  Key(-7, "")
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Key(-8, "lydian")
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Key(10, "major")
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Key(0, " major ")
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    print('Done!')


if __name__ == '__main__':
    _test_keys()

