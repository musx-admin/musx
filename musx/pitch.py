###############################################################################
"""
A class that implements musical pitches.

The Pitch class represent equal tempered pitches and returns information
in hertz, keynum, pitch class, Pnum and pitch name formats.  Pitches
can be compared using standard math relations and maintain proper spelling
when complemented or transposed by an Interval.
"""

from enum import IntEnum
from math import pow
from collections import namedtuple


PitchBase = namedtuple('PitchBase', ['letter', 'accidental', 'octave'])
PitchBase.__doc__ = """Base class for the immutable implementation of Pitch."""


class Pitch (PitchBase):
    """
    Creates a Pitch from a string or list, if neither is provided
    an empty Pitch is returned. The legal constructor forms are:
    
    * Pitch(string) - creates a Pitch from a pitch name string.
    * Pitch([l, a, o]) - creates a Pitch from a three element
    pitch list containing a letter, accidental and octave index
    (see below).
    * Pitch() - creates an empty Pitch.

    The format of a Pitch name string is:

    ```
    <pitch> :=  <letter>, [<accidental>], <octave>
    <letter> := 'C' | 'D' | 'E' | 'F' | 'G' | 'A' | 'B' |
                'c' | 'd' | 'e' | 'f' | 'g' | 'a' | 'b'
    <accidental> := <2flat> | <flat> | <natural> | <sharp> | <2sharp>
    <2flat> := 'bb' | 'ff'
    <flat> := 'b' | 'f'
    <natural> := ''
    <sharp> := '#' | 's'
    <2sharp> := '##' | 'ss'
    <octave> := '00' | '0' | '1' | '2' | '3' | '4' | '5' |
                 '6' | '7' | '8' | '9'
    ```

    Parameters
    ----------
    arg : string | list | None
        A pitch name string, a list of three pitch indexes, or None.

    Returns
    -------
    A new Pitch instance.

    Raises
    ------
    * TypeError if arg is a invalid pitch list.
    * TypeError if arg is an invalid pitch.
    """

    # Pitch letter constants (0-6).
    _let_C, _let_D, _let_E, _let_F, _let_G, _let_A, _let_B = range(7)

    # Maps pitch-letter names onto zero based indexes.
    _letter_map = {"C": _let_C, "D": _let_D, "E": _let_E, "F": _let_F,
                   "G": _let_G, "A": _let_A, "B": _let_B,
                   "c": _let_C, "d": _let_D, "e": _let_E, "f": _let_F,
                   "g": _let_G, "a": _let_A, "b": _let_B
                   }

    # Octave constants for code readability.
    _oct_00, _oct_0, _oct_1, _oct_2, _oct_3, _oct_4, _oct_5, _oct_6, _oct_7, _oct_8, _oct_9 = range(11)

    # Maps octave names onto zero based indexes.
    _octave_map = {"00": _oct_00, "0": _oct_0, "1": _oct_1, "2": _oct_2, "3": _oct_3, "4": _oct_4,
                   "5": _oct_5, "6": _oct_6, "7": _oct_7, "8": _oct_8, "9": _oct_9}

    # Accidental constants for code readability.
    _acc_2f, _acc_f, _acc_n, _acc_s, _acc_2s = range(5)

    # Maps accidental names onto zero based indexes.
    _accidental_map = {"bb": _acc_2f, "b": _acc_f,  "": _acc_n, "#": _acc_s, "##": _acc_2s,
                       "ff": _acc_2f, "f": _acc_f, "n": _acc_n, "s": _acc_s, "ss": _acc_2s}

    _enharmonic_map = [{_acc_s:  'B#',  _acc_n: 'C',  _acc_2f: 'Dbb'},
                       {_acc_2s: 'B##', _acc_s: 'C#', _acc_f:  'Db'},
                       {_acc_2s: 'C##', _acc_n: 'D',  _acc_2f: 'Ebb'},
                       {_acc_s:  'D#',  _acc_f: 'Eb', _acc_2f: 'Fbb'},
                       {_acc_2s: 'D##', _acc_n: 'E',  _acc_f:  'Fb'},
                       {_acc_s:  'E#',  _acc_n: 'F',  _acc_2f: 'Gbb'},
                       {_acc_2s: 'E##', _acc_s: 'F#', _acc_f:  'Gb'},
                       {_acc_2s: 'F##', _acc_n: 'G',  _acc_2f: 'Abb'},
                       {_acc_s:  'G#',  _acc_f: 'Ab'},
                       {_acc_2s: 'G##', _acc_n: 'A',  _acc_2f: 'Bbb'},
                       {_acc_s:  'A#',  _acc_f: 'Bb', _acc_2f: 'Cbb'},
                       {_acc_2s: 'A##', _acc_n: 'B',  _acc_f:  'Cb'}]

    # Reverse map of pitch indexes 0-6 onto their canonical names.
    _letter_names = ['C', 'D', 'E', 'F', 'G', 'A', 'B']

    # Reverse map of accidental indexes 0-4 onto their symbolic names.
    _accidental_names = ['bb', 'b', '', '#', '##']

    # Reverse map of pitch indexes 0-4 onto their safe names.
    _accidental_safe_names = ['ff', 'f', '', 's', 'ss']

    # Reverse map of pitch indexes 0-10 onto their canonical names.
    _octave_names = ['00', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    # Diatonic letter distances in semitones.
    _letter_spans = [0, 2, 4, 5, 7, 9, 11]

    # ## The minimum pnum identifier value.
    # _min_pcid = (_let_C << 4 | _acc_2f)
    #
    # ## The maximum pnum identifier value.
    # _max_pcid = (_let_B << 4 | _acc_2s)

 
    pnums = IntEnum('Pnum',
                    [(lj + aj, ((li << 4) + ai))
                     for li, lj in enumerate(["C", "D", "E", "F", "G", "A", "B"])
                     for ai, aj in enumerate(["ff", "f", "", "s", "ss"])])
    """
    A class variable that holds an IntEnum of all possible letter-and-accidental
    combinations Cff up to Bss.  (Since the accidental character # is illegal as a
    python enum name pnums use the 'safe versions' of the accidental
    names: 'ff' upto 'ss'. 
    
    A pnum value is a one byte integer 'llllaaaa', where 'llll' is its 
    letter index 0-6, and 'aaaa' is its accidental index 0-4. Pnums can be 
    compared using regular math relations.
    """

    def __new__(cls, arg=None):
        # Check for valid types and lengths up front.
        if arg is None:
            return cls._values_to_pitch(arg, arg, arg)
        if isinstance(arg, list):
            if len(arg) == 3 and all(isinstance(a, int) for a in arg):
                return cls._values_to_pitch(*arg)
            else:
                raise TypeError(f'{arg} is an invalid pitch list.')
        if isinstance(arg, str) and len(arg) >= 2:
            return cls._string_to_pitch(arg)
        raise TypeError(f"'{arg}' is an invalid pitch.")

    @classmethod
    def _string_to_pitch(cls, arg):
        """
        A private method that accepts a pitch string and parses it into three
        integer index values: letter, accidental, and octave. If all three values can
        be parsed from the string they should then passed to the _values_to_pitch()
        method to assign them to the instance's attributes. A ValueError
        should be raised for any value that cannot be parsed from the string. See:
        _values_to_pitch().

        Parameter
        ---------
        arg : string
            The string to convert to a pitch.
        
        Returns
        -------
        A new Pitch instance.

        Raises
        ------
        * ValueError is arg is not a valid pitch name.
        """
        strlen = len(arg)
        index = 0
        letter = cls._letter_map.get(arg[index].upper())
        if letter is None:
            raise ValueError(f"'{arg}' is not a valid pitch name.")
        while index < strlen and not arg[index].isdigit():
            index += 1
        if index == strlen:
            raise ValueError(f"'{arg}' is not a valid pitch name.")
        octave = cls._octave_map.get(arg[index::])
        if octave is None:
            raise ValueError(f"'{arg}' is not a valid pitch name.")
        accidental = cls._acc_n  # default accidental natural
        if index > 1:
            accidental = cls._accidental_map.get(arg[1:index])
            if accidental is None:
                raise ValueError(f"'{arg}' is not a valid pitch name.")
        return cls._values_to_pitch(letter, accidental, octave)

    @classmethod
    def _values_to_pitch(cls, let, acc, ova):
        """
        A private method that checks three values (letter, accidental and octave) to make
        sure they are either valid index values for the letter, accidental and octave
        attributes or they are None. The valid integer values are:
        
        * A letter index 0-6 corresponding to the pitch letter names ['C', 'D', 'E', 'F', 'G', 'A', 'B'].
        * An accidental index 0-4 corresponding to symbolic accidental names ['bb', 'b', '', '#', '##']
          or 'safe' accidental names ['ff', 'f', 'n', 's', 'ss'].
        * An octave index 0-10 corresponding to the pitch octave names ['00', '0', '1', '2', '3',
          '4', '5', '6', '7', '8', '9'].
        
        If any value is out of range the method will raise a ValueError for that value. If
        all values are legal the method will make the following 'edge case' tests:
        
        * Values cannot produce a pitch below midi key number 0 (lowest pitch is 'C00')
        * Values cannot produce a pitch above midi key number 127 (highest pitches are 'G9' and 'Abb9')
        
        If all the edge case checks pass then _values_to_pitch() should call the super's __new()__ method:

            super(Pitch, cls).__new__(cls, let, acc, ova)

        otherwise it should raise a ValueError for the offending values. NOTE: _values_to_pitch
        should be the only method in your implementation that calls the super method.

        Parameter
        ---------
        let : string
            The pitch letter string to convert to a pitch.
        
        acc : string
            The accidental string to convert to a pitch.
        
        ova : string
            The octave string to convert to a pitch.
        
        Returns
        -------
        A new Pitch instance.

        Raises
        ------
        * ValueError is arg is not a valid pitch name.
        """
        if let is None:
            return super(Pitch, cls).__new__(cls, None, None, None)
        if 0 <= let <= 6:
            if 0 <= acc <= 4:
                if 0 <= ova <= 10:
                    if ova == 0 and let == cls._let_C and acc < cls._acc_n:
                        nam = cls._letter_names[let] + cls._accidental_names[acc] + cls._octave_names[ova]
                        raise ValueError(f"Pitch '{nam}': midi number below 0.")
                    if ova == 10 and cls._letter_spans[let] + acc-2 > 7:
                        nam = cls._letter_names[let] + cls._accidental_names[acc] + cls._octave_names[ova]
                        raise ValueError(f"Pitch '{nam}': midi number exceeds 127.")
                    return super(Pitch, cls).__new__(cls, let, acc, ova)
                else:
                    raise ValueError(f"'{ova}' is not a valid pitch octave 0-10.")
            else:
                raise ValueError(f"'{acc}' is not a valid pitch accidental 0-4.")
        else:
            raise ValueError(f"'{let}' is not a valid pitch letter.")

    def __str__(self):
        """
        Returns a string displaying information about the pitch within angle
        brackets. Information includes the class name, the pitch text, and
        the id of the object. It is important that you implement the __str__ 
        method precisely. In particular, for __str__ you want to see 
        '<', '>', '0x' in your output string.  The format of your output 
        strings from your version of this function must look EXACTLY the
        same as in the two examples below.
        
        Example
        -------   
            >>> str(Pitch("C#6"))
            '<Pitch: C#6 0x7fdb17e2e950>'
            >>> str(Pitch())
            '<Pitch: empty 0x7fdb1898fa70>'
        """
        s = self.string()
        return f'<Pitch: {s if s else "empty"} {hex(id(self))}>'

    def __repr__(self):
        """
        Prints the external form of the Pitch that, if evaluated, would create
        a Pitch with the same content as this pitch.
        
        Note: It is the __repr__ (not the __str__) function that the autograder
        uses to compare results. So it is very important that you implement this
        method precisely. In particular, for __repr__ you want to see double
        quotes inside single quotes and NOT the other way around. The format of
        your output strings from your version of this function must look 
        EXACTLY the same as in the two examples below.

        Example
        -------
            >>> str(Pitch("C#6"))
            '<Pitch: C#6 0x7fdb17e2e950>'

            >>> repr(Pitch("Bbb3"))
            'Pitch("Bbb3")'
        """
        s = self.string()
        if s:
            return f'Pitch("{s}")'
        return 'Pitch()'

    def __lt__(self, other):
        """
        Implements Pitch < Pitch.

        This method should call self.pos() and other.pos() to get the two 
        values to compare.

        Parameters
        ----------
        other : Pitch
            The pitch to compare with this pitch.

        Returns
        -------
        True if this Pitch is less than the other.

        Raises
        ------
        * TypeError if other is not a Pitch.
        """
        if isinstance(other, Pitch):
            return self.pos() < other.pos()
        raise TypeError(f'{other} is not a Pitch.')

    def __le__(self, other):
        """
        Implements Pitch <= Pitch.

        This method should call self.pos() and other.pos() to get the values
        to compare.

        Parameters
        ----------
        other : Pitch
            The pitch to compare with this pitch.

        Returns
        -------
        True if this Pitch is less than or equal to the other.

        Raises
        ------
        * TypeError if other is not a Pitch.
        """
        if isinstance(other, Pitch):
            return self.pos() <= other.pos()
        raise TypeError(f'{other} is not a Pitch.')

    def __eq__(self, other):
        """
        Implements Pitch == Pitch.

        This method should call self.pos() and other.pos() to get the values
        to compare.

        Parameters
        ----------
        other : Pitch
            The pitch to compare with this pitch.

        Returns
        -------
        True if this Pitch is equal to the other.

        Raises
        ------
        * TypeError if other is not a Pitch.
        """
        if isinstance(other, Pitch):
            return self.pos() == other.pos()
        raise TypeError(f'{other} is not a Pitch.')

    def __ne__(self, other):
        """
        Implements Pitch != Pitch.

        This method should call self.pos() and other.pos() to get the values
        to compare.

        Parameters
        ----------
        other : Pitch
            The pitch to compare with this pitch.

        Returns
        -------
        True if this Pitch is not equal to the other.

        Raises
        ------
        * TypeError if other is not a Pitch.
        """
        if isinstance(other, Pitch):
            return self.pos() != other.pos()
        raise TypeError(f'{other} is not a Pitch.')

    def __ge__(self, other):
        """
        Implements Pitch >= Pitch.

        This method should call self.pos() and other.pos() to get the values
        to compare.

        Parameters
        ----------
        other : Pitch
            The pitch to compare with this pitch.

        Returns
        -------
        True if this Pitch is greater than or equal to the other.

        Raises
        ------
        * TypeError if other is not a Pitch.
        """
        if isinstance(other, Pitch):
            return self.pos() >= other.pos()
        raise TypeError(f'{other} is not a Pitch.')

    def __gt__(self, other):
        """
        Implements Pitch > Pitch.

        This method should call self.pos() and other.pos() to get the values
        to compare.

        Parameters
        ----------
        other : Pitch
            The pitch to compare with this pitch.

        Returns
        -------
        True if this Pitch is greater than the other.

        Raises
        ------
        * TypeError if other is not a Pitch.
        """
        if isinstance(other, Pitch):
            return self.pos() > other.pos()
        raise TypeError(f'{other} is not a Pitch.')

    def pos(self):
        """
        Returns a unique integer representing this pitch's position in
        the octave-letter-accidental space. The expression to calculate
        this value is `(octave<<8) + (letter<<4) + accidental`.
        """
        return (self.octave << 8) + (self.letter << 4) + self.accidental

    def is_empty(self):
        """
        Returns true if the Pitch is empty. A pitch is empty if its letter,
        accidental and octave attributes are None. Only one of these attributes
        needs to be checked because __new__ will only  create a Pitch if all
        three are legal values or all three are None.
        """
        return self.letter is None

    def string(self):
        """
        Returns a string containing the pitch name including the letter,
        accidental, and octave.  For example, Pitch("C#7").string() would
        return 'C#7'.
        """
        if self.is_empty():
            return ''
        s = self._letter_names[self.letter]
        s += self._accidental_names[self.accidental]
        s += self._octave_names[self.octave]
        return s

    def keynum(self):
        """Returns the midi key number of the Pitch."""
        deg = self._letter_spans[self.letter]
        # convert accidental index into semitone shift, e.g. double flat == -2.
        acc = self.accidental - 2
        return (12 * self.octave) + deg + acc

    def pnum(self):
        """
        Returns the pnum (pitch class enum) of the Pitch. Pnums enumerate and
        order the letter and accidental of a Pitch so they can be compared,
        e.g.: C < C# < Dbb. See also: `pnums`.
        """
        return self.pnums((self.letter << 4) + self.accidental)
    
    def pc(self):
        """Returns the pitch class (0-11) of the Pitch."""
        return self.keynum() % 12

    def hertz(self):
        """Returns the hertz value of the Pitch."""
        k = self.keynum()
        return 440.0 * pow(2, ((k - 69) / 12))

    @classmethod
    def from_keynum(cls, keynum, acci=None):
        """
        A class method that creates a Pitch for the specified midi key number.

        Parameters
        ----------
        keynum : int 
            A valid keynum 0-127.
        acci : string
            The accidental to use. If no accidental is provided a default is
            chosen from `C C# D Eb F F# G Ab A Bb B`
        
        Returns
        -------
        A new Pitch with an appropriate spelling.
        
        Raises
        ------
        A ValueError if the midi key number is invalid or if the pitch requested does not support the specified accidental.
        """
        if not (isinstance(keynum, int) and 0 <= keynum <= 127):
            raise ValueError(f"Invalid midi key number: {keynum}.")
        o, i = divmod(keynum, 12)
        if acci is None:
            acci = ['', '#', '', 'b', '', '', '#', '', 'b', '', 'b', ''][i]
        a = cls._accidental_map.get(acci)
        if a is None:
            raise ValueError(f"'{acci}' is not a valid accidental.")
        # s = cls._enharmonic_map[i][a]
        s = cls._enharmonic_map[i].get(a)
        if s is None:
            raise ValueError(f'No pitch for keynum {keynum} and accidental {acci}')
        if s in ['B#', 'B##']:
            o -= 1
        elif s in ['Cb', 'Cbb']:
            o += 1
        return Pitch(s + cls._octave_names[o])


# from mus.pitch import Pitch, _test_pitches
def _test_pitches():
    print('Testing pitch.py  ...')

    assert 'Pitch()' == Pitch().__repr__()
    assert 'Pitch("C4")' == Pitch('C4').__repr__()
    assert 'Pitch("A8")' == Pitch('A8').__repr__()
    assert 'Pitch("F##2")' == Pitch('F##2').__repr__()
    assert 'Pitch("G#8")' == Pitch('Gs8').__repr__()
    assert 'Pitch("Bb3")' == Pitch('Bb3').__repr__()
    assert 'Pitch("Fbb4")' == Pitch('fff4').__repr__()
    assert 'Pitch("Bbb0")' == Pitch('bbb0').__repr__()
    assert 'Pitch("C00")' == Pitch('cn00').__repr__()
    assert 'Pitch("Abb9")' == Pitch('Abb9').__repr__()
    assert 'Pitch("C#5")' == Pitch([0, 3, 6]).__repr__()
    assert 'Pitch("D2")' == Pitch([1, 2, 3]).__repr__()
    assert 'Pitch("A##2")' == Pitch([5, 4, 3]).__repr__()

    assert Pitch('C4') < Pitch('A4')
    assert Pitch('C4') <= Pitch('A4')
    assert not Pitch('C4') > Pitch('A4')
    assert not Pitch('C4') >= Pitch('A4')
    assert not Pitch('C4') == Pitch('A4')
    assert Pitch('C4') != Pitch('A4')
    assert not Pitch('C4') < Pitch('A3')
    assert not Pitch('C4') <= Pitch('A3')
    assert Pitch('C4') > Pitch('A3')
    assert Pitch('C4') >= Pitch('A3')
    assert not Pitch('C4') == Pitch('A3')
    assert Pitch('C4') != Pitch('A3')
    assert not Pitch('C4') < Pitch('Cb4')
    assert not Pitch('C4') <= Pitch('Cb4')
    assert Pitch('C4') > Pitch('Cb4')
    assert Pitch('C4') >= Pitch('Cb4')
    assert not Pitch('C4') == Pitch('Cb4')
    assert Pitch('C4') != Pitch('Cb4')
    assert Pitch('E##3') < Pitch('Fbb3')
    assert Pitch('E##3') <= Pitch('Fbb3')
    assert not Pitch('E##3') > Pitch('Fbb3')
    assert not Pitch('E##3') >= Pitch('Fbb3')
    assert not Pitch('E##3') == Pitch('Fbb3')
    assert Pitch('E##3') != Pitch('Fbb3')
    assert Pitch('B#5') < Pitch('C6')
    assert Pitch('B#5') <= Pitch('C6')
    assert not Pitch('B#5') > Pitch('C6')
    assert not Pitch('B#5') >= Pitch('C6')
    assert not Pitch('B#5') == Pitch('C6')
    assert Pitch('B#5') != Pitch('C6')
    assert not Pitch('B#5') < Pitch('C5')
    assert not Pitch('B#5') <= Pitch('C5')
    assert Pitch('B#5') > Pitch('C5')
    assert Pitch('B#5') >= Pitch('C5')
    assert not Pitch('B#5') == Pitch('C5')
    assert Pitch('B#5') != Pitch('C5')
    assert not Pitch('B#5') < Pitch('B#5')
    assert Pitch('B#5') <= Pitch('B#5')
    assert not Pitch('B#5') > Pitch('B#5')
    assert Pitch('B#5') >= Pitch('B#5')
    assert Pitch('B#5') == Pitch('B#5')
    assert not Pitch('B#5') != Pitch('B#5')
    assert Pitch('Fss4') == Pitch([3, 4, 5])

    assert 69 == Pitch('A4').keynum()
    assert 70 == Pitch('A#4').keynum()
    assert 71 == Pitch('A##4').keynum()
    assert 68 == Pitch('Ab4').keynum()
    assert 67 == Pitch('Abb4').keynum()
    assert 0 == Pitch('Dbb00').keynum()
    assert 0 == Pitch('Cn00').keynum()
    assert 127 == Pitch('Abb9').keynum()
    assert 127 == Pitch('G9').keynum()

    assert Pitch.pnums.C == Pitch('C00').pnum()
    assert Pitch.pnums.Cs == Pitch('C#1').pnum()
    assert Pitch.pnums.Css == Pitch('C##8').pnum()
    assert Pitch.pnums.Cf == Pitch('Cb0').pnum()
    assert Pitch.pnums.Cff == Pitch('Cbb2').pnum()

    assert 11 == Pitch('B7').pc()
    assert 0 == Pitch('B#7').pc()
    assert 1 == Pitch('B##7').pc()
    assert 10 == Pitch('Bb7').pc()
    assert 9 == Pitch('Bbb7').pc()

    assert 1318.5102276514797 == Pitch('E6').hertz()
    assert 1396.9129257320155 == Pitch('E#6').hertz()
    assert 1479.9776908465376 == Pitch('E##6').hertz()
    assert 1244.5079348883237 == Pitch('Eb6').hertz()
    assert 1174.6590716696303 == Pitch('Ebb6').hertz()

    assert 'Pitch("F#4")' == Pitch.from_keynum(66).__repr__()
    assert 'Pitch("C5")' == Pitch.from_keynum(72).__repr__()
    assert 'Pitch("B#3")' == Pitch.from_keynum(60, '#').__repr__()
    assert 'Pitch("Dbb7")' == Pitch.from_keynum(96, 'bb').__repr__()
    assert 'Pitch("Ab5")' == Pitch.from_keynum(80).__repr__()
    assert 'Pitch("Ab5")' == Pitch.from_keynum(80, 'b').__repr__()
    assert 'Pitch("G#5")' == Pitch.from_keynum(80, '#').__repr__()
    assert 'Pitch("Bb4")' == Pitch.from_keynum(70).__repr__()
    assert 'Pitch("Bb4")' == Pitch.from_keynum(70, 'b').__repr__()
    assert 'Pitch("Cbb5")' == Pitch.from_keynum(70, 'bb').__repr__()

    # ERRORS
    msg1, msg2 = "Received wrong type of exception.", "Expected exception did not happen."

    # TYPE ERRORS
    err = TypeError

    try: Pitch(1)
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Pitch(1.0)
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Pitch([])
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Pitch('')
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Pitch([1, 2, 3, 4])
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Pitch('F')
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    # VALUE ERRORS
    err = ValueError

    try: Pitch('Cf00')
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Pitch([0, 0, 0])
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Pitch([-1, 0, 0])
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Pitch([0, -1, 0])
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Pitch([0, 0, -1])
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Pitch([7, 0, 0])
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Pitch([0, 5, 0])
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Pitch([0, 0, 11])
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Pitch([6, 6, 6])
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Pitch([-1, -1, -1])
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Pitch('C#s4')
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Pitch('Hb5')
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Pitch('cFF')
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Pitch('Cb00')
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Pitch('Ab9')
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Pitch('C10')
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Pitch('C-1')
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Pitch('X11')
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Pitch('B3b')
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Pitch('D##10')
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Pitch('Cxx3')
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Pitch('F#')
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Pitch('HighC')
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Pitch.from_keynum(48, '##')
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Pitch.from_keynum(84, 'b')
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Pitch.from_keynum(80, '')
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Pitch.from_keynum(80, 'bb')
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Pitch.from_keynum(80, '##')
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Pitch.from_keynum(70, '')
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Pitch.from_keynum(70, 'bbb')
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    print('Done!')


if __name__ == '__main__':
    _test_pitches()
