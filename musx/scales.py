###############################################################################
"""
Defines the equal tempered chromatic scale over 11 octaves and provides a 
mapping between three alternate representations of pitch material:  hertz
frequency, key numbers, Pitch instances, and pitch names.

Hertz values are integer or floating point numbers greater than 0.

MIDI key numbers are integers 0 to 127 representing equal tempered pitches C00
to G#9, with C4 (middle C) assigned to MIDI key number 60. Floating point key
numbers are also possible where a value *kkk.cc* is interpreted as a frequency
*cc* cents above the integer key number *kkk*. For example, 60.5 represents a 
frequency 50 cents (a quarter tone) above Middle C.

Pitch names are strings containing a pitch letter, optional accidental, and
octave number. Pitch letters can be upper or lower case, and accidentals can
be "symbolic" (bb, b, '', #, ##) or "python safe" (ff, f, '', s, ss). See
documentation on `Pitch` for more information.

**The mapping functions:**

The following functions map between the three alternate representations
of frequency: 

* `keynum()` : converts a pitch name or hertz value into a key number.
* `pitch()` : converts a hertz value, key number or pitch name into a Pitch.
* `hertz()` : converts a pitch name or key number into a hertz value.

All three functions can map individual values, lists of values,
and string sequences of values.

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


import math
import musx.tools
from musx.pitch import Pitch
from musx.tools import parse_string_sequence

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
    seq = parse_string_sequence(string)
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
    seq = parse_string_sequence(string)
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
        series[0] = musx.tools.fit(series[0], *fit)
    # the variadic steps is a list of values or a list of one list.
    if numsteps == 1 and isinstance(steps[0], (list, tuple)):
        steps = steps[0]
        numsteps = len(steps)
    for i in range(0, length-1):
        knum = series[-1] + steps[i % numsteps]
        if fit:
            knum = musx.tools.fit(knum, *fit)
        series.append(knum)
    return series


def build_chromatic_scale(GRADING=False):
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
                    note_pitch = musx.Pitch(note_name1) if not GRADING else note_name1
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
    r = musx.Pitch() if not GRADING else 'R'
    table['R'] = [-1, 0.0, r]
    table['r'] = table['R']
    #table[-1] = [[r,r,r,r,r], 0.0]
    return table


# Build the hash table
chromatic_scale = build_chromatic_scale()

if __name__ == '__main__':
    grading_scale = build_chromatic_scale(GRADING=True)
    chromatic_scale = grading_scale
    def _print_table(table):
        """Prints all the entries in the table."""
        for key, val in table.items():
            print(key, val)
    # _print_table(grading_scale)

    #==========================================================================

        # local copies since these may not be in student files
    myoctavename_map = ['00', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    myenharmonic_map = [{1: 'B#', 0: 'C', -2: 'Dbb'},
                      {2: 'B##', 1: 'C#', -1: 'Db'},
                      {2: 'C##', 0: 'D', -2: 'Ebb'},
                      {1: 'D#', -1: 'Eb', -2: 'Fbb'},
                      {2: 'D##', 0: 'E', -1: 'Fb'},
                      {1: 'E#', 0: 'F', -2: 'Gbb'},
                      {2: 'E##', 1: 'F#', -1: 'Gb'},
                      {2: 'F##', 0: 'G', -2: 'Abb'},
                      {1: 'G#', -1: 'Ab'},
                      {2: 'G##', 0: 'A', -2: 'Bbb'},
                      {1: 'A#', -1: 'Bb', -2: 'Cbb'},
                      {2: 'A##', 0: 'B', -1: 'Cb'}]
    # create a data set to test using valid input. each element in
    # the list is a tuple containing (keynum, pitch, pc, accidental)
    testdata = []
    for k in range(128):
        o, s = divmod(k, 12)
        d = myenharmonic_map[s]
        for (_, p) in d.items():
            oo = o
            if p in ['B#', 'B##']:
                oo += -1
            elif p in ['Cb', 'Cbb']:
                oo += 1
            if oo < 0:
                continue
            testdata.append((k, p + myoctavename_map[oo], s, p[1:]))
    print(testdata)      
    for t in testdata:
        # t is: (midi, pitch, pc, accidental)
        # test midi->hertz->midi
        m = t[0]
        h = hertz(t[0])
        k = keynum(h)
        assert t[0] == k, f"midi -> hertz -> midi: keys {t[0]} and {k} not the same."
        # test midi->pitch->midi
        p = pitch(t[0])
        k = keynum(p)
        assert m == k, f"midi -> pitch - >midi: {t[0]} and {k} not the same."
        # test midi->pitch with a specified accidental to use
        print(t)
        p = pitch(t[0], acc= {'bb': -2, 'b': -1, '': 0, '#': 1, '##': 2}[t[3]])
        assert t[1] == p,  f"midi to pitch: {t[0]} and {t[3]} not {t[1]}."

    # Test some edge cases (things that should fail)

    testdata = ['', '5', '#', 'Ab',  'Xbb', 'X#4', 'Bb#5', 'Cb00', 'A9', 'E5#', 'Bbbb1', 'F000']
    for x in testdata:
        try:
            keynum(x)
        except Exception:
            pass
        else:
             assert False, f'pitch_to_midi() fail for bad pitch \'{x}\' did not happen.'

    testdata = [-1,  128]
    for x in testdata:
        try:
             hertz(x)
        except Exception:
            pass
        else:
            assert False, f'hertz() fail for bad midi \'{x}\' did not happen.'

    testdata = [-1, 0, 440.0 * math.pow(2, ((128-69)/12))]
    for x in testdata:
        try:
            keynum(x)
        except Exception:
             pass
        else:
             assert False, f'keynum(x) fail for bad hertz \'{x}\' did not happen.'

    testdata = "Cb4 C00 C4 D E F G A B C##5"
    authority = [59, 0, 60, 62, 64, 65, 67, 69, 71, 74]
    assert authority == keynum(testdata), f"note string failed"
        
    testdata = ["f3 g bf c4 ef b e5",  "f3 g bf c4 e a d5"]
    authority = [[53, 55, 58, 60, 63, 71, 76], [53, 55, 58, 60, 64, 69, 74]]
    assert authority == keynum(testdata), f"list of note strings failed"

    testdata = "a3, c#4, e, c# d, b3, g#, e   a, cs4, ff4, b##3 g##4, ef, e"
    authority = [57, 57, 61, 61, 64, 64, 61, 62, 62, 59, 59, 56, 56, 52, 57, 57, 61, 61, 64, 64, 61, 69, 69, 63, 63, 64]
    assert authority == keynum(testdata), f"twinkle twinkle little star failed"

    print('OK!')

    
