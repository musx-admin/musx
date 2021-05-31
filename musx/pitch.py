###############################################################################
"""
Defines the equal tempered chromatic scale over 11 octaves and provides a 
mapping between alternate representations of pitch material:  Pitch instances,
hertz frequency, key numbers, and pitch names.

The Pitch class represent equal tempered pitches and returns information
in hertz, keynum, pitch class, Pnum and pitch name formats.  Pitches
can be compared using standard math relations and maintain proper spelling
when complemented or transposed by an Interval.

The keynum, pitch and hertz functions provide mapping between the three 
alternate representations of frequency: 

* `keynum()` : converts a pitch name or hertz value into a key number.
* `pitch()` : converts a hertz value, key number or pitch name into a Pitch.
* `hertz()` : converts a pitch name or key number into a hertz value.

The functions can map individual values, lists of values, and string 
sequences of values.

**Lists and string sequences:**

The three functions convert individual values, lists of values and string
sequences containing values. In a string sequence use spaces
to delimit the items:

* A string sequence of key numbers: '0 40 21 33 87 12'
* A string sequence of hertz values: '440 880 220.12'
* A string sequence of pitch names: 'c4 d4 eb4 f#4 g3'

In any string sequence you can repeat an item by appending
one or more commas to its rightside. For example, the motive of Beethoven's 5th Symphony
'G4 G4 G4 Eb4' can be written as a pitch sequence 'G4,, Eb4', 
a key number sequence '67,, 63', or a hertz sequence '392,, 311'. 

A string sequence of pitches also supports "sticky" octave numbers: once 
an octave number is provided it remains in effect until a different octave is given.
For example a diatonic scale from A3 to A4 is 'a3 b c4 d e f g a'.

**Rests:**

The special string name 'R' or 'r' represents a musical rest. The key number of
a rest is -1, its hertz value is 0.0 and its Pitch is an empty pitch: Pitch().
"""

__pdoc__ = {
    'parse_number_sequence': False,
    'parse_pitch_sequence': False,
    'chromatic_scale': False,
    'build_chromatic_scale': False
}

from enum import IntEnum
from collections import namedtuple
import math
from . import tools

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

    def __repr__(self):
        """
        Prints an external form that, if evaluated, will create
        a Pitch with the same content as this pitch.
        """
        s = self.string()
        if s:
            return f'Pitch("{s}")'
        return 'Pitch()'

        __str__ == __repr__

    # def __str__(self):
    #     """
    #     Returns a string displaying information about the pitch within angle
    #     brackets. Information includes the class name, the pitch text, and
    #     the id of the object. It is important that you implement the __str__ 
    #     method precisely. In particular, for __str__ you want to see 
    #     '<', '>', '0x' in your output string.  The format of your output 
    #     strings from your version of this function must look EXACTLY the
    #     same as in the two examples below.
        
    #     Example
    #     -------   
    #         >>> str(Pitch("C#6"))
    #         '<Pitch: C#6 0x7fdb17e2e950>'
    #         >>> str(Pitch())
    #         '<Pitch: empty 0x7fdb1898fa70>'
    #     """
    #     s = self.string()
    #     return f'<Pitch: {s if s else "empty"} {hex(id(self))}>'

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
        return 440.0 * math.pow(2, ((k - 69) / 12))

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

#  The chromatic scale and the functions pitch(), keynum() and hertz()

chromatic_scale = {}
"""
A hash table (dictionary) that maps between note names, midi key
numbers and hertz values. The table's dictionary keys consist of all 
integer midi key numbers and all string pitch spellings of all midi key
numbers. See build_chromatic_scale() for more information.
"""


def keynum(ref, filt=round):
    """
    Returns key numbers from a pitch name, hertz value, a list
    of the same, or a string sequence of the same.

    Parameters
    ----------
    ref : string | int | float | list
        A pitch name, hertz value, list of the same, or a string
        containing a sequence of the same separated by spaces.
    filt : function | None
        A function of one argument maps a floating point key number
        to an integer. The default is math.round, but math.floor and
        math.ceil could also be used. If filt is None then a floating
        point key number is returned. In a floating point key number, the 
        first two digits of the fractional portion are interpreted as
        the number of cents above the integer midi value.
    
    Returns 
    -------
    If ref is a pitch its hash table value is returned.

    If ref is a hertz value its key number is calculated, filtered
    and returned (see the filt parameter).

    If ref is a python list of pitch names or hertz values 
    then a list of key numbers is returned.
    
    If ref is a string of hertz values
    delimited by spaces then a list of key numbers is returned. 

    If ref is a string of pitch names then a list of key numbers
    are returned. Items in the list can be directly repeated by 
    appending ',' to an item for each repetition. If the items are
    pitch names then if a pitch does not contain an explicit octave
    then it inherits the previous octave number in the list.
    If no octave number is provided the the middle C octave (4)
    is used as the inital octave.

    Raises
    ------
    ValueError if ref is not a pitch name, hertz value or list of the same.

    Examples
    --------
    ```python
    >>> keynum('C#4')
    61
    >>> keynum(100)
    43
    >>> keynum(['Cb4', 'D#6'])
    [59, 87]
    >>> keynum([100, 200, 300])
    [43, 55, 62]
    >>> keynum('cs4 d e,, f g3 a b')
    [61, 62, 64, 64, 64, 65, 55, 57, 59]
    >>> keynum('100, 200, 300')
    [43, 43, 55, 55, 62]
    ```
    """
    if isinstance(ref, str):
        ref = ref.strip() # remove whitespace from start and end
        if ref:
            if ref[0].isalpha():  # should be a pitch
                try: # try to return a single keynum
                    return chromatic_scale[ref][0] 
                except KeyError:
                    # ref was not a single pitch. if ref contains a 
                    # space then take it to be a list of pitch names
                    # otherwise its an error
                    if ' ' in ref:
                        ref = parse_pitch_sequence(ref)
            elif ref[0].isdigit():  # should be hertz
                    # if ref contains a space then take it to be a list
                    # of hertz values otherwise convert to a float.
                    if ' ' in ref:
                        ref = parse_number_sequence(ref)
                    else:
                        ref = float(ref) 
    # ref is hertz and so not in the hashtable
    if isinstance(ref, (float, int)):
        keyn = 69 + math.log2(ref / 440.0) * 12
        if filt:
            keyn = filt(keyn)
        if 0 <= keyn < 128:
            return keyn  #filt(keyn) if filt else keyn
    if isinstance(ref, list):
        return [keynum(x, filt) for x in ref]
    raise ValueError(f"invalid keynum input: '{ref}'.")


def hertz(ref, filt=round):
    """
    Returns hertz values from a pitch name, key number, a list
    of the same, or a string sequence of the same.

    Parameters
    ----------
    ref : string, int or float
        A pitch name or midi key number to convert to a hertz value.
    filt : function | None
        A function of one argument maps a floating point key number
        to an integer.

    Returns 
    -------
    If ref is a pitch name or key number its hertz hash table
    value is returned.

    If ref is a python list of pitch names or key numbers 
    then a list of hertz values is returned.
    
    If ref is a string of key numbers
    delimited by spaces then a list of hertz values is returned. 

    If ref is a string of pitch names then a list of hertz values
    are returned. Items in this list can be directly repeated by appending
    ','  to an item for each repetition. If the items are pitch names then
    if a pitch does not contain an explicit octave then it inherits the
    previous octave number in the list. If no octave number is provided the
    the middle C octave (4) is used as the inital octave.

    Raises
    ------
    ValueError if ref is not a pitch name, key number or list of the same.

    Examples
    --------
    ```python
    >>> hertz('C#4')
    277.1826309768721
    >>> hertz(100)
    2637.02045530296
    >>> hertz(['Cb4', 'D#6'])
    [246.94165062806206, 1244.5079348883237]
    >>> hertz([48, 60, 72])
    [130.8127826502993, 261.6255653005986, 523.2511306011972]
    >>> hertz('cs4 d b3')
    [277.1826309768721, 293.6647679174076, 246.94165062806206]
    >>> hertz('48, 60')
    [130.8127826502993, 130.8127826502993, 261.6255653005986]
    ```
    """
    if isinstance(ref, str):
        ref = ref.strip()
        if ref:
            if ref[0].isalpha():  # should be a pitch
                try:  # try common case of a single pitch
                    return chromatic_scale[ref][1] # try to returning a single hertz
                except KeyError:  # keep going if string isnt a pitch
                    pass
                ref = parse_pitch_sequence(ref)
            elif ref[0].isdigit():  # should be a keynum
                ref = parse_number_sequence(ref)
    if isinstance(ref, float):
        ref = filt(ref) if filt else int(ref)
    if isinstance(ref, int):
        return chromatic_scale[ref][1]  # KeyError if int isnt valid keynum
    if isinstance(ref, list):
        return [hertz(x, filt) for x in ref]
    raise ValueError(f"invalid hertz input: '{ref}'.")


def pitch(ref, filt=round, *, hz=False, acc=[]):
    """
    Returns the pitch name from a hertz value, key number, a 
    list of the same, or a string sequence of the same.
    
    Parameters
    ----------
    ref : int or float
        A key number or hertz value, depending on the value of the
        hz parameter.
    filt : function | None
        A function of one argument that maps a floating point key number
        to an integer.
    hz : True | False
        If True then ref is accepted as a hertz value otherwise it is
        assumed to be a key number. The default value is False.
    acc :  int | list
        An ordered preference list of accidentals to use in the pitch spelling.
        Values range from -2 (double flat) to 2 (double sharp) with 0 being
        no accidental.

    Returns 
    -------
    If ref is a key number its hash table value is returned.

    If ref is a hertz value its key number is calculated, filtered
    to an int value and its hash table value is returned.

    If ref is a python list of key numbers their hash values are returned.

    If ref is a python list of hertz values they are converted to
    key numbers and then processed as described in the previous point.
    
    If ref is a string sequence of hertz values or key numbers they are
    converted to a python list and treated as described above.

    Examples
    --------
    >>> pitch(60)
    Pitch("C4")
    >>> pitch(60, acc=[1])
    Pitch("B#3")
    >>> pitch(60, acc=[-2])
    Pitch("Dbb4")
    >>> pitch(440*3/2, hz=True)
    Pitch("E5")
    >>> pitch([48, 60, 72])
    [Pitch("C3"), Pitch("C4"), Pitch("C5")]
    >>> pitch("67,, 63")
    [Pitch("G4"), Pitch("G4"), Pitch("G4"), Pitch("Eb4")]
    """
    #print('** in pitch: ',ref)
    # if parsing hertz first convert to keynum or list of keynums
    if hz:
        ref = keynum(ref)
    # ref is float keynum, convert to int
    if isinstance(ref, float):
        ref = filt(ref)
    # ref is an integer keynum, look up the pitch
    if isinstance(ref, int):
        try:
            data = chromatic_scale[ref]
            if data:
                if not acc:
                    # default prefers sharps for C# and F# otherwise flats.
                    acc = [2, 3, 1, 4, 0] if ref % 12 in [1, 6] else [2, 1, 3, 0, 4]
                else:
                    if not isinstance(acc,list):
                        acc = [acc]
                    acc = [a + 2 for a in acc]  # convert -2..2 to 0..4
                try:
                    return next(data[0][i] for i in acc if data[0][i])
                except StopIteration as err:
                    raise ValueError("No pitch for accidentals {acc}.") from err
        except KeyError as err:
            raise ValueError(f"no table entry for midi note {ref}.") from err
    # ref is a string sequence of keynums, a string sequence 
    # of pitch names, or a pitch name.
    if isinstance(ref, str):
        #print('** is str, ref=', ref)
        ref = ref.strip()
        if ref:
            if ref[0].isalpha():  # should be a pitch
                try: 
                    #print('** trying')
                    ##return chromatic_scale[ref][1] # try to return a single pitch
                    return chromatic_scale[ref][2] # try to return a single pitch
                except KeyError:
                    pass
                #print('** parse pitch seq')
                ref = parse_pitch_sequence(ref)
            elif ref[0].isdigit():  # should be a hertz
                #print('** parse number seq')
                ref = parse_number_sequence(ref)
    # ref is a list of keynums or a list of pitch names
    if isinstance(ref, list):
        #print('** processing list:', ref)
        return [pitch(x, filt, hz=False, acc=acc) for x in ref]

    raise ValueError(f"invalid keynum input: '{ref}'.")


def parse_pitch_sequence(string):
    seq = tools.parse_string_sequence(string)
    oct = '4'
    for i,p in enumerate(seq):
        if not (p[0] in 'CcDdEeFfGgAaBbRr'):
            raise ValueError(f"invalid pitch: '{p}'.")
        # o holds octave number, or '' if no octave
        o = p[len(p.rstrip('0123456789')):]
        if o: 
            oct = o         # update octave to carry forward
        else: 
            seq[i] = p+oct  # add octave to pitch 
    return seq


def parse_number_sequence(string):
    seq = tools._sequence(string)
    for i,p in enumerate(seq):
        if not p[0] in '0123456789+-.':
            raise ValueError(f"invalid numeric: '{p}'.")
        seq[i] = float(p) if ('.' in p) else int(p)
    return seq


def scale(start, length, *steps, fit=None):
    """
    Returns a list of key numbers beginning on start and incremented by
    successive interval increments. The step values loop if the
    length of the scale is greater than the number of intervals in steps.

    Parameters
    ----------
    start : int | float
        The initial key number that starts the scale.
    length : int
        The length of the scale including the start.
    steps : ints | floats | list | tuple
        An in-line (variadic) series of increments defining the
        intervals beween the key numbers in the scale. This series
        can also be specified as a single list or tuple of increments.
    fit : None | [lb, ub, mode]
        Limits placed on the range of the scale. If the value is None there
        are no limits. Otherwise fit should be a list or tuple of 3 
        elements containing a lower bound, upper bound and string mode.
        See: `musx.tools.fit()` for more information.

    Returns
    -------
    A list of key numbers defining the scale.

    Examples
    --------
    ```python
    # 16 note (3 octave) pentatonic scale on C#4
    >>> scale(61, 16, 2, 3, 2, 2, 3)
    [60, 62, 65, 67, 69, 72, 74, 77, 79, 81, 84, 86, 89, 91, 93, 96]
    # one octave of the octotonic scale
    >>> scale(60, 9, 1, 2)
    [60, 61, 63, 64, 66, 67, 69, 70, 72]
    # interval cycle
    >>> scale(60, 12, (1, 2, 3, 4, 5))
    [60, 61, 63, 66, 70, 75, 76, 78, 81, 85]
    # cycle of fifths compressed to one octave
    >>> pitch(scale(0, 12, 7, fit=[60, 72, 'wrap']))
    ['C5', 'G4', 'D4', 'A4', 'E4', 'B4', 'F#4', 'C#4', 'Ab4', 'Eb4', 'Bb4', 'F4']
    ```
    """
    series = [start]
    numsteps = len(steps)
    if fit:
        fit = list(fit) # copy it
        series[0] = tools.fit(series[0], *fit)
    # the variadic steps is a list of values or a list of one list.
    if numsteps == 1 and isinstance(steps[0], (list, tuple)):
        steps = steps[0]
        numsteps = len(steps)
    for i in range(0, length-1):
        knum = series[-1] + steps[i % numsteps]
        if fit:
            knum = tools.fit(knum, *fit)
        series.append(knum)
    return series


def build_chromatic_scale():
    """
    Returns a hash table (dictionary) with entries that map between
    pitch names, Pitch instances, midi key numbers, and hertz values. The hash keys
    are all possible MIDI key numbers 0 to 127 and all possible pitch
    names for each MIDI key number. See module documentation for more information.

    For a dictionary key that is a pitch name, its dictionary value will
    be a two element list containing the pitch's integer keynum and its hertz
    value:

    `<pitch_name>: [<keynum>, <hertz>, <Pitch>]`

    For a dictionary key that is an integer midi key number, its dictionary value
    will be a two element list:

    `<keynum> : [[<Pitch_bb>, <Pitch_b>, <Pitch>, <Pitch_#>, <Pitch_##>], <hertz>]`

    The first element in the list is a sublist of length five containing all
    possible Pitch objects for the given key number. The five list
    locations represent accidental ordering from double-flat to double-sharp
    spellings: if a pitch spelling uses one sharp it would be added at index 3,
    and if a pitch spelling is not possible for a given accidental position that
    position will hold an empty string. The second element in the value list is
    the key number's hertz value.

    To calculate a hertz value from a key number use the formula:

    `hertz = 440.0 * 2 ** ((keynum - 69) / 12)`

    To calculate a key number from a hertz value use the reverse formula:
    
    `keynum = 69 + log(hertz / 440, 2) * 12`  
    """
    # letter names for note entries
    letter_names = ["C", "D", "E", "F", "G", "A", "B"]
    # symbolic accidental names for notes, "" is for a diatonic note without accidental
    accidental_names = ["bb", "b", "", "#", "##"]
    # safe accidental name variants
    accidental_safe_name = {"bb": "ff", "b": "f", "": "", "#": "s", "##": "ss"}
    # lowest octave name is 00 instead of -1.
    octave_names = ["00", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    # semi-tone shifts applied to diatonic notes within the octave
    letter_steps = [0, 2, 4, 5, 7, 9, 11]
    # semi-tone shift applied to diatonic notes for notes with accidentals
    accidental_steps = [-2, -1, 0, 1, 2]
    # init table with midi keys, each holding a note array and frequency.
    # the note array will hold all chromatic note names for the midi key.
    table = {key: [['','','','',''], 440.0 * 2 ** ((key-69.0)/12)] for key in range(128)}
    # iterate all the octave for midi key numbers 0-127.
    for octave_index, octave_name in enumerate(octave_names):
        # starting key number for notes in the octave
        octave_midi = octave_index * 12
        # iterate all the diatonic letter names for notes.
        for letter_index, letter_name in enumerate(letter_names):
            # the midi key number of the diatonic note
            letter_midi = octave_midi + letter_steps[letter_index]
            # iterate the accidentals and create all possible note names for the letter
            for accidental_index, accidental_name in enumerate(accidental_names):
                # get the semitone amount to shift the letter note by
                accidental_step = accidental_steps[accidental_index]
                # calculate the midi key number for the note
                note_midi = letter_midi + accidental_step
                # stop notes outside of midi range (there are only a few)
                if 0 <= note_midi <= 127:
                    accidental_name = accidental_names[accidental_index]
                    # create the official note name
                    note_name1 = letter_name + accidental_name + octave_name
                    # create the Pitch for the official name.
                    note_pitch = Pitch(note_name1)
                    # create variants (lower case letter names, safe accidental names)
                    note_name2 = letter_name.lower() + accidental_name + octave_name
                    note_name3 = letter_name + accidental_safe_name[accidental_name] + octave_name
                    note_name4 = letter_name.lower() + accidental_safe_name[accidental_name] + octave_name
                    # fetch the midi data from the table
                    midi_data = table[note_midi]
                    # add the note to the note array
                    ##midi_data[0][accidental_index] = note_name1
                    midi_data[0][accidental_index] = note_pitch
                    # get the frequency from the midi data and add it to the note data.
                    note_freq = table[note_midi][1]
                    # add the hash entry for the note name
                    ##table[note_name1] = [note_midi, note_freq]
                    table[note_name1] = [note_midi, note_freq, note_pitch]
                    # add the variants (lower case letter, safe accidentals)
                    table[note_name2] = table[note_name1]
                    table[note_name3] = table[note_name1]
                    table[note_name4] = table[note_name1]
    # add entries for musical rests
    r = Pitch()
    table['R'] = [-1, 0.0, r]
    table['r'] = table['R']
    #table[-1] = [[r,r,r,r,r], 0.0]
    return table


# Build the hash table
chromatic_scale = build_chromatic_scale()