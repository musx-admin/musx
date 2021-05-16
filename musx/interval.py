###############################################################################
"""
A class that implements musical intervals.

The Interval class supports the standard interval names and classification
system, including the notion of descending or ascending intervals and simple
or compound intervals.  Intervals can be numerically compared for their size
(span+quality) and can be used to transpose Pitches while preserving correct
accidental spelling."
"""

from .pitch import Pitch

class Interval:

    ## Private class constants representing spans. There are eight interval
    #  spans ranging 0-7: _Uni=Unison, _2nd=Second, _3rd=Third, ... _8va=Octave
    _Uni, _2nd, _3rd, _4th, _5th, _6th, _7th, _8va = (i for i in range(8))

    ## Private class constants representing qualities. There are thirteen
    #  qualities ranging 0-13: from quintuply-diminished intervals to
    #  quintuply-augmented intervals.
    _5dim, _4dim, _3dim, _2dim, _dim, _min, _perf, _maj, _aug, _2aug, _3aug, _4aug, _5aug \
        = (i for i in range(13))

    ## Private map of all possible interval quality names to their constants.
    #  Note that diminished can use either "o" or "d", and augmented
    #  can use "+" or "A".
    _qual_map = {"ooooo": _5dim, "oooo": _4dim, "ooo": _3dim, "oo": _2dim, "o": _dim,
                 "ddddd": _5dim, "dddd": _4dim, "ddd": _3dim, "dd": _2dim, "d": _dim,
                 "m": _min, "P": _perf, "M": _maj,
                 "+": _aug, "++": _2aug, "+++": _3aug, "++++": _4aug, "+++++": _5aug,
                 "A": _aug, "AA": _2aug, "AAA": _3aug, "AAAA": _4aug, "AAAAA": _5aug}

    ## Reverse map from quality constants 0-12 onto their canonical names.
    _qual_names = ["ooooo", "oooo", "ooo", "oo", "o",
                   "m", "P", "M",
                   "+", "++", "+++", "++++", "+++++"]

    ## Reverse map from span constants to span full names
    _span_full_names = ['unison', 'second', 'third', 'fourth', 'fifth', 'sixth',
                        'seventh', 'octave']

    ## Reverse map from quality constants to quality full names
    _qual_full_names = ['quintuply-diminished', 'quadruply-diminished',
                        'triply-diminished', 'doubly-diminished', 'diminished',
                        'minor', 'perfect', 'major', 'augmented',
                        'doubly-augmented', 'triply-augmented',
                        'quadruply-augmented', 'quintuply-augmented']

    ## Ordered list of all possible perfect interval span values.
    _perf_spans = [_Uni, _4th, _5th, _8va]

    ## Ordered list of all possible imperfect interval span values.
    _impf_spans = [_2nd, _3rd, _6th, _7th]

    ## Ordered list of all possible imperfect interval qualities.
    _impf_quals = [_5dim, _4dim, _3dim, _2dim, _dim, _min, _maj, _aug, _2aug, _3aug, _4aug, _5aug]

    ## Ordered list of all possible perfect interval qualities.
    _perf_quals = [_5dim, _4dim, _3dim, _2dim, _dim, _perf, _aug, _2aug, _3aug, _4aug, _5aug]

    ## Reverse map from (diatonic) span values to their semitone content.
    _diatonic_semitones = [0, 2, 4, 5, 7, 9, 11, 12]

    ## A 2D map that returns the semitones for a given quality and span value.
    _semitones_map = {
        _min:  {_2nd: 1,  _3rd:  3,  _6th:  8, _7th: 10},
        _maj:  {_2nd: 2,  _3rd:  4,  _6th:  9, _7th: 11},
        _perf: {_Uni: 0,  _4th:  5,  _5th:  7, _8va: 12},
        _dim:  {_Uni: -1, _2nd:  0,  _3rd:  2, _4th:  4, _5th:  6, _6th: 7,  _7th: 9,  _8va: 11},
        _2dim: {_Uni: -2, _2nd: -1,  _3rd:  1, _4th:  3, _5th:  5, _6th: 6,  _7th: 8,  _8va: 10},
        _3dim: {_Uni: -3, _2nd: -2,  _3rd:  0, _4th:  2, _5th:  4, _6th: 5,  _7th: 7,  _8va:  9},
        _4dim: {_Uni: -4, _2nd: -3,  _3rd: -1, _4th:  1, _5th:  3, _6th: 4,  _7th: 6,  _8va:  8},
        _5dim: {_Uni: -5, _2nd: -4,  _3rd: -2, _4th:  0, _5th:  2, _6th: 3,  _7th: 5,  _8va:  7},
        _aug:  {_Uni:  1, _2nd:  3,  _3rd:  5, _4th:  6, _5th:  8, _6th: 10, _7th: 12, _8va: 13},
        _2aug: {_Uni:  2, _2nd:  4,  _3rd:  6, _4th:  7, _5th:  9, _6th: 11, _7th: 13, _8va: 14},
        _3aug: {_Uni:  3, _2nd:  5,  _3rd:  7, _4th:  8, _5th: 10, _6th: 12, _7th: 14, _8va: 15},
        _4aug: {_Uni:  4, _2nd:  6,  _3rd:  8, _4th:  9, _5th: 11, _6th: 13, _7th: 15, _8va: 16},
        _5aug: {_Uni:  5, _2nd:  7,  _3rd:  9, _4th: 10, _5th: 12, _6th: 14, _7th: 16, _8va: 17},
    }

    ## A 2D map that returns the interval quality for a given span and semitonal value.
    _span_semi_qual_map = {
        _Uni: {-5: _5dim, -4: _4dim, -3: _3dim, -2: _2dim, -1: _dim, 0: _perf,
               1: _aug, 2: _2aug, 3: _3aug, 4: _4aug, 5: _5aug},
        _2nd: {-4: _5dim, -3: _4dim, -2: _3dim, -1: _2dim, 0: _dim, 1: _min,
               2: _maj, 3: _aug, 4: _2aug, 5: _3aug, 6: _4aug, 7: _5aug},
        _3rd: {-2: _5dim, -1: _4dim, 0: _3dim, 1: _2dim, 2: _dim, 3: _min,
               4: _maj, 5: _aug, 6: _2aug, 7: _3aug, 8: _4aug, 9: _5aug},
        _4th: {0: _5dim, 1: _4dim, 2: _3dim, 3: _2dim, 4: _dim, 5: _perf,
               6: _aug, 7: _2aug, 8: _3aug, 9: _4aug, 10: _5aug},
        _5th: {2: _5dim, 3: _4dim, 4: _3dim, 5: _2dim, 6: _dim, 7: _perf,
               8: _aug, 9: _2aug, 10: _3aug, 11: _4aug, 12: _5aug},
        _6th: {3: _5dim, 4: _4dim, 5: _3dim, 6: _2dim, 7: _dim, 8: _min,
               # 9: _maj, 10: _aug, 11: _2aug, 12: _3aug, 13: _4aug, 14: _5aug},
               9: _maj, 10: _aug, 11: _2aug, 12: _3aug, 1: _4aug, 2: _5aug},
        _7th: {5: _5dim, 6: _4dim, 7: _3dim, 8: _2dim, 9: _dim, 10: _min,
               # 11: _maj, 12: _aug, 13: _2aug, 14: _3aug, 15: _4aug, 16: _5aug,
               11: _maj, 12: _aug, 1: _2aug, 2: _3aug, 3: _4aug, 4: _5aug},
        _8va: {7:  _5dim, 8: _4dim, 9: _3dim, 10: _2dim, 11: _dim, 12: _perf,
               # 13: _aug, 14: _2aug, 15: _3aug, 16: _4aug, 17: _5aug,
               1:  _aug,  2: _2aug,  3: _3aug,  4: _4aug,  5: _5aug}
     }


    def __init__(self, arg, other=None):
        """
        Creates an Interval from a string, list, or two Pitches.

        Calling signatures:

        * Interval(string) - creates an Interval from a pitch string.
        * Interval([s, q, x, s]) - creates a Pitch from a list of four
        integers: a span, quality, extra octaves and sign. (see below).
        * Interval(pitch1, pitch2) - creates an Interval from two Pitches.

        The format of a Interval string is:

        ```py
        interval  = ["-"] , <quality> , <span>
        <quality> = <diminished> | <minor> | <perfect> | <major> | <augmented>
        <diminished> = <5d> , <4d> , <3d> , <2d> , <1d> ;
        <5d> = "ooooo" | "ddddd"
        <4d> = "oooo" | "dddd"
        <3d> = "ooo" | "ddd"
        <2d> = "oo" | "dd"
        <1d> = "o" | "d"
        <minor> = "m"
        <perfect> = "P"
        <major> = "M"
        <augmented> = <5a>, <4a>, <3a>, <2a>, <1a>
        <5d> = "+++++" | "aaaaa"
        <4d> = "++++" | "aaaa"
        <3d> = "+++" | "aaa"
        <2d> = "++" | "aa"
        <1d> = "+" | "a"
        <span> = "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ...
        ```
       
        The __init__ function should check to make sure the arguments are either a string, a
        list of four integers, or two pitches.  If the input is a string then __init__ should
        pass the string to the the private _init_from_string() method (see below).  If the
        input is a list of four ints, __init__ will pass them to the private _init_from_list()
        method (see below). If the input is two pitches they will be passed to the private
        _init_from_pitches() method (see below).  

        Parameters
        ----------
        arg : string | list
            If only arg is specified it should be either an
            interval string or a list of four interval indexes.  If both
            arg and other are provided, both should be a Pitch.
        other : Pitch
            A Pitch if arg is a Pitch, otherwise None.

        Raises
        ------
        TypeError if the input is not a string, list of four integers, or two pitches.
        """

        if other is None:
            if isinstance(arg, str):
                self._init_from_string(arg)
            elif isinstance(arg, list):
                if len(arg) == 4 and all(isinstance(a, int) for a in arg):
                    self._init_from_list(*arg)
                else:
                    raise TypeError(f'{arg} is an invalid interval list.')
            else:
                raise TypeError(f'{arg} is an invalid interval reference.')
        elif isinstance(arg, Pitch) and isinstance(other, Pitch):
            self._init_from_pitches(arg, other)
        else:
            raise TypeError(f"Invalid interval specification: {arg} and {other}.")


    def _init_from_list(self, span, qual, xoct, sign):
        """
        A private method that checks four integer values (span, qual, xoct, sign) to make sure
        they are valid index values for the span, qual, xoct and sign attributes. Legal values
        are: span 0-7, qual 0-12, xoct 0-10, sign -1 or 1. If any value is out of range the
        method will raise a ValueError for that value. If all values are legal the method will
        make the following 'edge case' tests:

        * span and quality values cannot produce negative semitones, i.e. an interval
          whose 'top' would be lower that its 'bottom'. Here are the smallest VALID
          interval for each span that could cause this: perfect unison, diminished-second,
          triply-diminished third.
        * Only the span of a fifth can be quintuply diminished.
        * Only the span of a fourth can be quintuply augmented.
        * No interval can surpass 127 semitones, LOL. The last legal intervals are: 'P75'
         (a 10 octave perfect 5th), and a 'o76' (a 10 octave diminished 6th).
        * If a user specifies an octave as a unison span with 1 extra octave, e.g. [0,*,1,*],
        it should be converted to an octave span with 0 extra octaves, e.g. [7,*,0,*]
        
        Only if all the edge case checks pass then _init_from_list() should assign
        the four values to the attributes, e.g. self.span=span, self.qual=qual, and
        so on. Otherwise if any edge case fails the method should raise a ValueError.
        
        NOTE: The _init_from_list() method should be the only method in your implementation
        that assign values to self.letter, self.accidental and self.octave.
        """
        
        if 0 <= span <= 7:
            if 0 <= qual <= 12:
                if 0 <= xoct:
                    if sign in (1, -1):
                        if span in self._perf_spans:
                            if qual in [self._min, self._maj]:
                                qn = self._qual_full_names[qual]
                                sn = self._span_full_names[span]
                                raise ValueError(f"Span '{sn}' is not compatible with quality '{qn}'.")
                        else:
                            if qual is self._perf:
                                qn = self._qual_full_names[qual]
                                sn = self._span_full_names[span]
                                raise ValueError(f"Span '{sn}' is not compatible with quality '{qn}'.")
                        # only 4ths and fifths can be quintuply diminished/augmented
                        if qual == self._5dim and span != self._5th:
                            raise ValueError(f'{self._span_full_names[span]}s cannot be quintuply diminished.')
                        if qual == self._5aug and span != self._4th:
                            raise ValueError(f'{self._span_full_names[span]}s cannot be quintuply augmented.')
                        # check semitones to make sure the interval will not be negative or greater than 127
                        semi = self._semitones_map[qual][span] + (xoct*12)
                        # print('init from list: span=', span, 'qual=', qual, 'semi=', semi, 'xoct=', xoct)
                        if semi < 0:
                            qn = self._qual_full_names[qual]
                            sn = self._span_full_names[span]
                            raise ValueError(f"A '{qn}-{sn}' would be negative"
                                             ", perhaps you want a descending interval?")
                        if semi > 127:
                            raise ValueError("Intervals cannot span more than 127 semitones.")
                        # respell unisons with 1 extra octave as octaves.
                        if span == 0 and xoct > 0:
                            span, xoct = self._8va, xoct - 1
                        self.span, self.qual, self.xoct, self.sign = span, qual, xoct, sign
                    else:
                        raise(ValueError(f"'{sign}' is not an interval sign value 1 or -1."))
                else:
                    raise(ValueError(f"'{xoct}' is not a compound octave value 0-10."))
            else:
                raise(ValueError(f"'{qual}' is not an interval quality 0-12."))
        else:
            raise(ValueError(f"'{span}' is not an interval span 0-7."))


    def _init_from_string(self, name):
        """
        A private method that accepts an interval string and parses it into four
        integer values: span, qual, xoct, sign. If all four values can be parsed
        from the string they should be passed to the _init_from_list() method to
        check the values and assign them to the instance's attributes. A ValueError
        should be raised for any value that cannot be parsed from the string. See:
        _init_from_list().
        """
        
        if len(name) < 2:
            raise ValueError(f"'{name}' is not a valid interval name.")
        start = 0
        if name[0] == '-':
            sign = -1  # -1 is descending interval
            start = 1
        else:
            sign = 1  # 1 is ascending interval
        strlen = len(name)
        index = start
        # Find extent of quality chars.
        while index < strlen and name[index] in "odmMP+A":
            index += 1
        # Split string into quality and size substrings.
        qual = name[start:index]
        digi = name[index::]
        # digi string must be digits!
        if not digi.isdigit():
            raise ValueError(f"'{name}' is not a valid interval name.")
        # Set the interval's "span" value, i.e. the number
        # of lines and spaces it spans (0=Unison...7=Octave).
        span = int(digi) - 1
        if span < 0:
            raise ValueError(f"'{name}' is not a valid interval name name.")
        # All intervals are simplified to lie within one octave and the
        # octave itself is a simple interval. Compound intervals
        # (intervals larger than an octave) are stored simply but have
        # their xoct (extra octaves) attribute set to a positive number.
        # So a M2 would be span=1 xoct=0 and a M9 would be span=1 xoct=1.
        xoct = 0
        while span > 7:
            span -= 7  # simplify span to 0-7
            xoct += 1  # sum number of extra octaves
        # Look up the quality value of the name.
        qual = self._qual_map.get(qual, None)
        if qual is None:
            raise ValueError(f"'{name}' is not a valid interval name.")
        self._init_from_list(span, qual, xoct, sign)


    def _init_from_pitches(self, pitch1, pitch2):
        """
        A private method that determines appropriate span, qual, xoct, sign
        values from two pitches. If pitch1 is lower than or equal to pitch2
        then an ascending interval is formed (sign=1) otherwise a descending
        interval is formed (sign=-1). Once values for sign, span, qual and
        xoct have been determined they should be passed to _init_from_list()
        to initialize the interval's attributes.
        """
        
        # (1) Determine the sign attribute value. If the left pitch is
        # less than or equal to pitch2 then the interval is ascending
        # and sign is 1. Otherwise its descending and sign is -1.
        sign = 1 if pitch1 <= pitch2 else -1
        # (2) Determine the span attribute value. Span measures the
        # distance between the two pitch letters (L1 and L2).  In an
        # ascending interval if L1<=L2 then the span will be L2-L1
        # otherwise it will be the complement of the positive distance:
        # 8va - (L1-L2). In a descending interval if L1>L2 then the
        # interval's span is the positive distance L1-L2 otherwise
        # its the complement: 8va - (L2-L1).  This can be calculated
        # by one expression. In ascending intervals L2-L1 will be
        # positive for ascending letters and negative for descending
        # letters so mod 7 will produce the complement of the negative
        # span.
        span = ((pitch2.letter - pitch1.letter) * sign) % 7
        # (3) If letters are the same (unison or octave) then use semitones to
        # distinguish between unison and octave. The smallest possible octave is 8 semitones so less
        # than that must be a unison.

        # multiplying semitone difference by sign will ensure
        # positive semitones. you cant use abs()
        # because that won't work for
        semi = (pitch2.keynum() - pitch1.keynum()) * sign
        if pitch1.letter == pitch2.letter:
            span = self._Uni if semi < 8 else self._8va
        # determine the number of extra octaves by subtracting
        # out octaves from semitones while semitones is greater
        # than an octave.
        xoct = 0
        while semi > 12:
            xoct += 1
            semi -= 12
        ## determining quality. the remainder of semitones
        qual = self._span_semi_qual_map[span].get(semi, None)
        if qual is None:
            raise ValueError(f"{pitch1.string()} and {pitch2.string()}: no quality found for span {span}"
                             f", semitones {semi} and xoct {xoct}.")
        # xoct cleanup for spans whose semitonal content was clipped
        # because it is larger than 12 but should not increase xoct.
        # For example: +[+++]8va, +[+]7th, ++++6th.
        if span == self._8va:
            if qual > self._perf:
                xoct -= 1
                semi += 12
        elif span == self._7th:
            if qual > self._aug:
                xoct -= 1
                semi += 12
        elif span == self._6th:
            if qual > self._3aug:
                xoct -= 1
                semi += 12
        # print('init from pitch: sign=', sign, ', span=', span, ', semi=', semi, ', xoct=', xoct)
        self._init_from_list(span, qual, xoct, sign)

    # REFERENCE IMPLEMENTATION
    # ## A private method that determines appropriate span, qual, xoct, sign
    # # from two pitches. If pitch2 is lower than pitch1 then a descending
    # # interval should be formed. The values should be passed to the
    # # _init_from_list() method to initialize the interval's attributes.
    # def _init_from_pitches(self, pitch1, pitch2):
    #     # if the left pitch (self) is higher than the right (other)
    #     # then its a descending interval.
    #     if pitch1 <= pitch2:  # EQUAL OR ASCENDING INTERVAL
    #         sign = 1
    #         semi = (pitch2.keynum() - pitch1.keynum()) * sign
    #         if pitch1.letter < pitch2.letter:
    #             # letter1 is less than letter2 so the span will be
    #             # the difference between them
    #             span = (pitch2.letter - pitch1.letter)
    #         elif pitch1.letter == pitch2.letter:
    #             # letter1 and letter2 are some kind of unison or octave.
    #             # the smallest possible octave is 8 semitones (e.g. C##4
    #             # to Cbb5) so if semi is less than that it has to be a unison.
    #             span = self._Uni if semi < 8 else self._8va
    #         else:
    #             # letter1 is higher than letter2 so the span will be
    #             # the complement of the distance between them
    #             span = 7 - (pitch1.letter - pitch2.letter)
    #     else:  # DESCENDING INTERVAL
    #         sign = -1
    #         semi = (pitch2.keynum() - pitch1.keynum()) * sign
    #         if pitch1.letter < pitch2.letter:
    #             span = 7 - (pitch2.letter - pitch1.letter)
    #         elif pitch1.letter == pitch2.letter:
    #             # letter1 and letter2 are some kind of unison or octave.
    #             # the smallest possible octave is 8 semitones (e.g. C##4
    #             # to Cbb5) so if semi is less than that it has to be a unison.
    #             span = self._Uni if semi < 8 else self._8va
    #         else:
    #             span = pitch1.letter - pitch2.letter
    #     xoct = 0
    #     while semi > 12:
    #         xoct += 1
    #         semi -= 12
    #     qual = self._span_semi_qual_map[span].get(semi, None)
    #     if qual is None:
    #         raise ValueError(f"{pitch1.string()} and {pitch2.string()}: no quality found for span {span}"
    #                          f", semitones {semi} and xoct {xoct}.")
    #     # xoct cleanup for spans whose semitonal content was clipped
    #     # because it is larger than 12 but should not increase xoct.
    #     # For example: +[+++]8va, +[+]7th, ++++6th.
    #     if span == self._8va:
    #         if qual > self._perf:
    #             xoct -= 1
    #             semi += 12
    #     elif span == self._7th:
    #         if qual > self._aug:
    #             xoct -= 1
    #             semi += 12
    #     elif span == self._6th:
    #         if qual > self._3aug:
    #             xoct -= 1
    #             semi += 12
    #     # print('init from pitch: sign=', sign, ', span=', span, ', semi=', semi, ', xoct=', xoct)
    #     self._init_from_list(span, qual, xoct, sign)

    def __str__(self):
        """
        Returns the print representation of the key. Information includes
        the the class name, the interval text, the span, qual, xoct and sign
        values, and the id of the object. See: string().
        
        Example
        -------
        `<Interval: oooo8 [7, 1, 0, 1] 0x1075bf6d0>`
        """
        
        return f'<Interval: {self.string()} ' \
               f'[{self.span}, {self.qual}, {self.xoct}, {self.sign}] {hex(id(self))}>'


    def __repr__(self):
        """
        The string the console prints shows the external form.
    
        Example
        -------
        `Interval("oooo8")`
        """
        
        return f'Interval("{self.string()}")'


    def __lt__(self, other):
        """
        Implements Interval < Interval.

        This method should call self.pos() and other.pos() to get the
        values to compare. See: pos().

        Parameters
        ----------
        other : Ratio
            The interval to compare with this interval.
    
        Returns
        -------
        True if this interval is less than other.

        Raises
        ------
        A TypeError if other is not an Interval.
        """
        
        return self.pos() < other.pos()


    def __le__(self, other):
        """
        Implements Interval <= Interval.

        This method should call self.pos() and other.pos() to get the
        values to compare. See: pos().

        Parameters
        ----------
        other : Ratio
            The interval to compare with this interval.

        Returns
        -------
        True if this interval is less than or equal to other.

        Raises
        ------
        A TypeError if other is not an Interval.
        """
        
        return self.pos() <= other.pos()


    def __eq__(self, other):
        """
        Implements Interval == Interval.

        This method should call self.pos() and other.pos() to get the
        values to compare. See: pos().

        Parameters
        ----------
        other : Ratio
            The interval to compare with this interval.

        Returns
        -------
        True if this interval is equal to other.

        Raises
        ------
        A TypeError if other is not an Interval.
        """
        
        return self.pos() == other.pos()


    def __ne__(self, other):
        """
        Implements Interval != Interval.

        This method should call self.pos() and other.pos() to get the
        values to compare. See: pos().

        Parameters
        ----------
        other : Ratio
            The interval to compare with this interval.
        
        Returns
        -------
        True if this interval is not equal to other.

        Raises
        ------
        A TypeError if other is not an Interval.
        """
        
        return self.pos() != other.pos()


    def __ge__(self, other):
        """
        Implements Interval >= Interval.

        This method should call self.pos() and other.pos() to get the
        values to compare. See: pos().

        Parameters
        ----------
        other : Ratio
            The interval to compare with this interval.

        Returns
        -------
        True if this interval is greater than or equal to other.

        Raises
        ------
        A TypeError if other is not an Interval.
        """
        
        return self.pos() >= other.pos()


    def __gt__(self, other):
        """
        Implements Interval > Interval.

        This method should call self.pos() and other.pos() to get the
        values to compare. See: pos().

        Parameters
        ----------
        other : Ratio
            The interval to compare with this interval.

        Returns
        -------
        True if this interval is greater than the other.

        Raises
        ------
        A TypeError if other is not an Interval.
        """
        
        if not isinstance(other, Interval):
            raise TypeError(f'{other} is not an Interval.')
        return self.pos() > other.pos()

  
    def pos(self):
        """
        Returns a numerical value for comparing the size of this interval to
        another. The comparison depends on the span, extra octaves, and quality
        of the intervals but not their signs. For two intervals, if the span of
        the first (including extra octaves) is larger than the second then the
        first interval is larger than the second regardless of the quality of
        either interval. If the interval spans are the same then the first is
        larger than the second if its quality is larger. This value can be
        encoded as a 16 bit integer: (((span + (xoct * 7)) + 1) << 8) + qual
        """
        
        return (((self.span + (self.xoct * 7)) + 1) << 8) + self.qual


    def string(self):
        """
        Returns a string containing the interval name.
        For example, Interval('-P5').string() would return '-P5'.
        """
        
        s = "-" if self.sign < 0 else ""
        s += self._qual_names[self.qual]
        s += str((self.span + (self.xoct * 7)) + 1)
        return s


    def full_name(self, *, sign=True):
        """
        Returns the full interval name, e.g. 'doubly-augmented third'
        or 'descending augmented sixth'

        Parameters
        ----------
        sign : bool
            If true then "descending" will appear in the name if it is a descending interval.
        """
        
        s = 'descending ' if sign and self.sign < 0 else ""
        s += self._qual_full_names[self.qual]
        s += ' '
        s += self._span_full_names[self.span]
        return s


    def span_name(self):
        """
        Returns the full name of the interval's span, e.g. a
        unison would return "unison" and so on.
        """
        
        return self._span_full_names[self.span]


    def quality_name(self):
        """
        Returns the full name of the interval's quality, e.g. a
        perfect unison would return "perfect" and so on.
        """
        
        return self._qual_full_names[self.qual]


    def matches(self, other):
        """
        Returns true if this interval and the other interval have the
        same span, quality and sign. The extra octaves are ignored.
        Parameters
        ----------
        """
        
        return self.span == other.span and self.qual == other.qual \
               and self.sign == other.sign


    def lines_and_spaces(self):
        """
        Returns the interval's number of lines and spaces, e.g.
        a unison will return 1.
        """
        
        return self.span + 1


    def _to_iq(self, name):
        """
        Returns a zero based interval quality from its external
        string name. Raises an assertion if the name is invalid.
        See:is_unison() and similar.
        """

        iq = self._qual_map.get(name)
        if iq is None:
            raise ValueError(f"'{name}' is not a valid interval quality.")
        return iq


    def to_list(self):
        """
        Returns the interval values as a list: [span, qual, xoct, sign]
        """

        return [self.span, self.qual, self.xoct, self.sign]


    def is_unison(self, qual=None):
        """
        Returns true if the interval is a unison otherwise false.

        Parameters
        ----------
        qual : string 
            If specified the predicate tests for that specific quality of unison, which can be
            any valid quality symbol, e.g. 'P', 'M' 'm' 'd' 'A' 'o' '+' and so on. See: _to_iq().
        """

        if self.span == self._Uni:
            return True if qual is None else self.qual == self._to_iq(qual)
        return False


    def is_second(self, qual=None):
        """
        Returns true if the interval is a second otherwise false.

        Parameters
        ----------
        qual : string
            If specified the predicate tests for that specific
            quality of second, which can be any quality symbol, e.g.
            'P', 'M' 'm' 'd' 'A' 'o' '+' and so on. See: _to_iq().
        """

        if self.span == self._2nd:
            return True if qual is None else self.qual == self._to_iq(qual)
        return False


    def is_third(self, qual=None):
        """
        Returns true if the interval is a third otherwise false.

        Parameters
        ----------
        qual : string
            If specified the predicate tests for that specific
            quality of third, which can be any quality symbol, e.g.
            'P', 'M' 'm' 'd' 'A' 'o' '+' and so on. See: _to_iq().
        """

        if self.span == self._3rd:
            return True if qual is None else self.qual == self._to_iq(qual)
        return False


    def is_fourth(self, qual=None):
        """
        Returns true if the interval is a fourth otherwise false.

        Parameters
        ----------
        qual : string
            If specified the predicate tests for that specific
            quality of fourth, which can be any quality symbol, e.g.
            'P', 'M' 'm' 'd' 'A' 'o' '+' and so on. See: _to_iq().
        """

        if self.span == self._4th:
            return True if qual is None else self.qual == self._to_iq(qual)
        return False


    def is_fifth(self, qual=None):
        """
        Returns true if the interval is a fifth otherwise false.

        Parameters
        ----------
        qual : string
            If specified the predicate tests for that specific
            quality of fifth, which can be any quality symbol, e.g.
            'P', 'M' 'm' 'd' 'A' 'o' '+' and so on. See: _to_iq().
        """

        if self.span == self._5th:
            return True if qual is None else self.qual == self._to_iq(qual)
        return False


    def is_sixth(self, qual=None):
        """
        Returns true if the interval is a sixth otherwise false.
 
        Parameters
        ----------
        qual : string
            If specified the predicate tests for that specific
            quality of sixth, which can be any quality symbol, e.g.
            'P', 'M' 'm' 'd' 'A' 'o' '+' and so on. See: _to_iq().
        """

        if self.span == self._6th:
            return True if qual is None else self.qual == self._to_iq(qual)
        return False


    def is_seventh(self, qual=None):
        """
        Returns true if the interval is a seventh otherwise false.

        Parameters
        ----------
        qual : string
            If specified the predicate tests for that specific
            quality of seventh, which can be any quality symbol, e.g.
            'P', 'M' 'm' 'd' 'A' 'o' '+' and so on. See: _to_iq().
        """

        if self.span == self._7th:
            return True if qual is None else self.qual == self._to_iq(qual)
        return False

    
    def is_octave(self, qual=None):
        """
        Returns true if the interval is an octave otherwise false.

        Parameters
        ----------
        qual : string
            If specified the predicate tests for that specific
            quality of octave, which can be any quality symbol, e.g.
            'P', 'M' 'm' 'd' 'A' 'o' '+' and so on. See: _to_iq().
        """

        if self.span == self._8va:
            return True if qual is None else self.qual == self._to_iq(qual)
        return False


    def is_diminished(self):
        """
        Returns a 'diminution count' 1-5 if the interval is diminished else False.
        For example, if the interval is doubly-diminished then 2 is returned.
        If the interval not diminished at all (e.g. is perfect, augmented, minor or
        major) then False is returned.
        """

        return self._dim - self.qual + 1 if self.qual <= self._dim else False

    def is_minor(self):
        """
        Returns true if the interval is minor, otherwise false.
        """

        return self.qual == self._min

    def is_perfect(self):
        """
        Returns true if the interval is perfect, otherwise false.
        """

        return self.qual == self._perf

    def is_major(self):
        """
        Returns true if the interval is major, otherwise false.
        """

        return self.qual == self._maj

    def is_augmented(self):
        """
        Returns a 'augmentation count' 1-5 if the interval is augmented else False.
        For example, if the interval is doubly-augmented then 2 is returned.
        If the interval not augmented at all (e.g. is perfect, diminished, minor or
        major) then False is returned.
        """

        return 5 + (self.qual - self._5aug) if self.qual >= self._aug else False

    def is_perfect_type(self):
        """
        Returns true if the interval belongs to the 'perfect interval'
        family, i.e. it is a Unison, 4th, 5th, or Octave.
        """

        return self.span in [self._Uni, self._4th, self._5th, self._8va]

    
    def is_imperfect_type(self):
        """
        Returns true if this interval belongs to the 'imperfect interval'
        family, i.e. it is a 2nd, 3rd, 6th, or 7th.
        """

        return not self.is_perfect_type()  # 2nd, 3rd, 6th, 7th

        
    def is_simple(self):
        """
        Returns true if this is a simple interval, i.e. its span is
        less-than-or-equal to an octave.
        """

        return self.xoct == 0  # simple means no extra octaves

        
    def is_compound(self):
        """
        Returns true if this is a compound interval, i.e. its span is
        more than an octave (an octave is a simple interval).
        """

        return not self.is_simple()

    
    def is_ascending(self):
        """
        Returns true if this interval's sign is 1.
        """

        return self.sign == 1

    
    def is_descending(self):
        """
        Returns true if this interval's sign is -1.
        """

        return self.sign == -1

    
    def is_consonant(self):
        """
        Returns true if the interval is a consonant interval otherwise False.
        The perfect fourth should be considered consonant.
        """

        if self.is_perfect_type():
            return self.qual == self._perf
        else:
            return self.span in [self._3rd, self._6th] \
                   and self.qual in [self._min, self._maj]

                   
    def is_dissonant(self):
        """
        Returns True if the interval is not a consonant interval otherwise False.
        """

        return not self.is_consonant()

    
    def complemented(self):
        """
        Returns a complemented copy of the interval. 
        
        To complement an interval you invert its span and quality. To invert
        the span, subtract it from the maximum span index (the octave index).
        To invert the quality subtract it from the maximum quality index 
        (quintuply augmented).
        """

        # new = copy.copy(self)
        # new.complement()
        # return new
        return Interval([self._8va-self.span, self._5aug-self.qual, self.xoct, self.sign])

    
    def semitones(self):
        """
        Returns the number of semitones in the interval. 

        It is possible to determine the number of semitones by looking at the span and
        quality indexes. For example, if the span is a perfect fifth
        (span index 4) and the quality is perfect (quality index 6)
        then the semitones will be 5 and augmented or diminished fifths
        will add or subtract semitones accordingly.
        
        The semitones will be negative for descending intervals otherwise positive.
        """
        semi = self._semitones_map[self.qual][self.span]
        return (semi + (self.xoct * 12)) * self.sign

    
    def add(self, other):
        """
        Adds a specified interval to this interval.

        Parameters
        ----------
        other : Interval
            The interval to add to this one.

        Returns
        -------
        A new interval expressing the total span of both intervals.

        Raises
        ------
        * A TypeError if other is not an interval. 
        * A NotImplementedError if either intervals are descending.
        """

        if self.sign < 1 or other.sign < 1:
            raise ValueError("Only ascending intervals may be added.")
        newspan = self.span + other.span
        newsemi = self.semitones() + other.semitones()
        newxoct = 0
        while newsemi > 12:
            newspan -= 7
            newsemi -= 12
            newxoct += 1
        # get newspan's number of semitones in the diatonic octave
        assert 0 <= newspan < len(self._diatonic_semitones),  f"invalid added span value: {newspan}."
        diasemi = self._diatonic_semitones[newspan]
        # Qualities of the diatonic spans -- Unison to Octave
        diaqual = [self._perf, self._maj, self._maj, self._perf, self._perf,
                   self._maj, self._maj, self._perf][newspan]
        # calculate the difference in semitones between the new interval and its diatonic version
        semidif = newsemi - diasemi
        # print('diasemi=', diasemi, 'diaqual=', diaqual, "semidif=", semidif)
        # add that difference to the diatonic quality to calculate the new quality
        if newspan in self._perf_spans:
            newqual = self._perf_quals[self._perf_quals.index(diaqual) + semidif]
        else:
            newqual = self._impf_quals[self._impf_quals.index(diaqual) + semidif]
        return Interval([newspan, newqual, newxoct, self.sign*other.sign])

    
    def transpose(self, p):
        """
        Transposes a Pitch or Pnum by the interval. Pnum transposition
        has no octave or direction so if the interval is negative its
        complement should be used and octaves should reduce to unisons
        without complementing.

        Parameters
        ----------
        p : Pitch | Pnum
            The Pitch or Pnum to transpose, otherwise the string name of a pitch or pnum (eg. 'Cb5' or 'Dff')

        Returns
        ----------
        The transposed Pitch or Pnum.

        Raises
        ------
        A TypeError if p is not a Pitch or Pnum.
        """

        if isinstance(p, str) and len(str) > 0:
            p = Pitch(p) if p[-1].isdigit() else Pitch.pnums[p]
        if isinstance(p, Pitch):
            return self._transpose_pitch(p)
        if isinstance(p, Pitch.pnums):
            return self._transpose_pnum(p)
        raise TypeError(f"'{p}' is not a Pitch or Pnum.")

    
    def _transpose_pnum(self, pnum):
        """
        from mus.interval import Interval, _test_intervals
        from mus.pitch import Pitch
        Interval('m7').transpose(Pitch.pnums.E)
        Interval('-M2').transpose(Pitch.pnums.E)
        """

        def let_to_name(let): return f"{['C', 'D', 'E', 'F', 'G', 'A', 'B'][let]}"
        def acc_to_name(acc): return f"{['bb', 'b', 'n', '#', '##', ][acc]}"
        def acc_to_size(acc): return acc - 2  # size of accidental (bb=-2)
        def size_to_acc(acc): return acc + 2
        def let_to_size(let): return self._diatonic_semitones[let]

        span = self.span
        qual = self.qual
        # semi will be negative for descending intervals
        semi = self.semitones()
        desc = self.is_descending()
        # pnum space has no octaves so collapse octaves to unisons
        if span == self._8va:
            # collapse octaves but preserve quality, so an augmented octave
            # becomes an augmented unison and NOT a diminished unison.
            span, qual = self._Uni, qual
            semi = self._semitones_map[qual][span]
        # complement descending interval including its negative semitones
        if desc:
            # print("descending! old semi=", semi, "new semi=", semi % 12)
            span, qual, semi = self._8va - span, self._5aug - qual, semi % 12
        old_let = (pnum.value & 0xF0) >> 4
        old_acc = (pnum.value & 0xF)
        # letter of new pitch
        new_let = (old_let + span) % self._8va
        # semitonal size between the natural (diatonic) letters
        nat_size = (let_to_size(new_let) - let_to_size(old_let)) % 12
        # semitonal size of the interval
        int_size = semi

        ### print(f'interval {self.string()}: span', span, 'qual', qual, 'sign', self.sign, 'semi', int_size)

        # semitonal shift of the old accidental (where b= -1, ##= 2 etc.)
        old_acc_siz = acc_to_size(old_acc)
        # adjust the semitonal size of the natural interval by the size of the old accident
        adj_nat_siz = nat_size - old_acc_siz
        # subtract the adjusted natural size from the interval size to determine the size
        # of the new accidental
        new_acc_size = int_size - adj_nat_siz

        ### print(f'old pitch {pnum.name}: old_let', old_let, f'({let_to_name(old_let)})', 'old_acc', old_acc,
        ###       f'({acc_to_name(old_acc)}))', 'old_acc_size', old_acc_siz, 'nat_size', nat_size,
        ###       'int_size', int_size, 'adj_nat_size', adj_nat_siz, 'new_acc_size', new_acc_size)

        # invalid size means an impossible transposition, e.g. shifting F## by +2
        if not (-2 <= new_acc_size <= 2):
            raise ValueError(f"Transposition of '{pnum.name}' by '{self.string()}': "
                             "no pitch spelling possible.")
        # adjust the size of the next accidental
        new_acc = size_to_acc(new_acc_size)
        new_pnum = Pitch.pnums(new_let << 4 | new_acc)

        ### print('new_acc', new_acc, f'({acc_to_name(new_acc)}))','new pitch', new_pnum, '\n')

        return new_pnum

    
    def _transpose_pitch(self, pitch):
        """
        """

        pitch_let = pitch.letter
        pitch_acc = pitch.accidental
        pitch_oct = pitch.octave
        # print('pitch_let', pitch_let, 'pitch_acc', pitch_acc, 'pitch_oct', pitch_oct)
        # get and transpose the pnum
        pnum = self._transpose_pnum(pitch.pnums(pitch_let << 4 | pitch_acc))
        trans_let = (pnum.value & 0xF0) >> 4
        trans_acc = (pnum.value & 0xF)
        # transposed keynum is original pitch + interval semitones
        trans_key = pitch.keynum() + self.semitones()
        trans_oct = trans_key // 12
        # decrement octave if note is B# or B##, increment if Cbb or Cb
        if trans_let == pitch._let_B and trans_acc in [pitch._acc_s, pitch._acc_2s]:
            trans_oct -= 1
        elif trans_let == pitch._let_C and trans_acc in [pitch._acc_f, pitch._acc_2f]:
            trans_oct += 1
        return Pitch([trans_let, trans_acc, trans_oct])


# from mus.interval import Interval, _test_intervals
def _test_intervals():
    print('Testing interval.py ... ', end='')

    assert (Interval('M3') < Interval('o4'))
    assert (Interval('M3') <= Interval('A3'))
    assert (Interval('M3') <= Interval('M3'))
    assert not (Interval('M3') > Interval('M3'))
    assert (Interval('oo4') > Interval('M3'))
    assert not (Interval('m3') != Interval('m3'))

    assert 0 == Interval('P1').semitones()
    assert 1 == Interval('+1').semitones()
    assert 2 == Interval('++1').semitones()
    assert 3 == Interval('+++1').semitones()
    assert 4 == Interval('++++1').semitones()

    assert 4 == Interval('M3').semitones()
    assert 3 == Interval('m3').semitones()
    assert 2 == Interval('o3').semitones()
    assert 1 == Interval('oo3').semitones()
    assert 0 == Interval('ooo3').semitones()

    assert 0 == Interval('o2').semitones()
    assert 1 == Interval('m2').semitones()
    assert 2 == Interval('M2').semitones()
    assert 3 == Interval('+2').semitones()
    assert 4 == Interval('++2').semitones()
    assert 5 == Interval('+++2').semitones()
    assert 6 == Interval('++++2').semitones()

    assert 12 == Interval('P8').semitones()
    assert 11 == Interval('o8').semitones()
    assert 10 == Interval('oo8').semitones()
    assert 9 == Interval('ooo8').semitones()
    assert 8 == Interval('oooo8').semitones()

    assert 13 == Interval('+8').semitones()
    assert 14 == Interval('++8').semitones()
    assert 15 == Interval('+++8').semitones()
    assert 16 == Interval('++++8').semitones()

    assert 9  == Interval('oooo9').semitones()
    assert 10 == Interval('ooo9').semitones()
    assert 11 == Interval('oo9').semitones()
    assert 12 == Interval('o9').semitones()
    assert 13 == Interval('m9').semitones()
    assert 14 == Interval('M9').semitones()
    assert 15 == Interval('+9').semitones()
    assert 16 == Interval('++9').semitones()
    assert 17 == Interval('+++9').semitones()
    assert 18 == Interval('++++9').semitones()

    assert Interval('P8').is_simple()
    assert Interval('+8').is_simple()
    assert Interval('++8').is_simple()
    assert Interval('+++8').is_simple()
    assert Interval('++++8').is_simple()

    assert Interval('m9').is_compound()
    assert Interval('o9').is_compound()
    assert Interval('oo9').is_compound()
    assert Interval('ooo9').is_compound()
    assert Interval('oooo9').is_compound()

    assert Interval("P1").is_perfect()
    assert not Interval("A1").is_perfect()
    assert Interval("+1").is_perfect_type()
    assert not Interval("P1").is_imperfect_type()

    assert Interval("P4").is_perfect()
    assert not Interval("A4").is_perfect()
    assert Interval("+++++4").is_perfect_type()
    assert not Interval("P4").is_imperfect_type()

    assert Interval("P5").is_perfect()
    assert not Interval("A5").is_perfect()
    assert Interval("ddddd5").is_perfect_type()
    assert not Interval("P5").is_imperfect_type()

    assert Interval("P8").is_perfect()
    assert not Interval("o8").is_perfect()
    assert Interval("oooo8").is_perfect_type()
    assert not Interval("P8").is_imperfect_type()

    assert 1 == Interval("+8").is_augmented()
    assert 3 == Interval("+++3").is_augmented()
    assert 1 == Interval("o8").is_diminished()
    assert 3 == Interval("ooo3").is_diminished()
    assert 5 == Interval("ddddd5").is_diminished()
    assert 4 == Interval("AAAA5").is_augmented()

    assert not Interval("P5").is_diminished()
    assert not Interval("AAAA5").is_diminished()
    assert not Interval("P5").is_augmented()
    assert not Interval("oooo5").is_augmented()

    assert Interval('P1').is_consonant()
    assert Interval('P4').is_consonant()
    assert Interval('P5').is_consonant()
    assert Interval('P8').is_consonant()
    assert Interval('m3').is_consonant()
    assert Interval('M6').is_consonant()

    assert not Interval('+1').is_consonant()
    assert not Interval('+++++4').is_consonant()
    assert not Interval('ooooo5').is_consonant()
    assert not Interval('o8').is_consonant()
    assert not Interval('oo3').is_consonant()
    assert not Interval('+6').is_consonant()

    assert not Interval('P1').is_dissonant()
    assert not Interval('P4').is_dissonant()
    assert not Interval('P5').is_dissonant()
    assert not Interval('P8').is_dissonant()
    assert not Interval('m3').is_dissonant()
    assert not Interval('M6').is_dissonant()

    assert Interval('+1').is_dissonant()
    assert Interval('+++++4').is_dissonant()
    assert Interval('ooooo5').is_dissonant()
    assert Interval('o8').is_dissonant()
    assert Interval('oo3').is_dissonant()
    assert Interval('+6').is_dissonant()

    assert Interval('P1').is_unison()
    assert Interval('+1').is_unison()
    assert Interval('+1').is_unison('A')
    assert Interval('+1').is_unison('+')
    assert not Interval('+1').is_unison('o')
    assert not Interval('P8').is_unison()
    assert not Interval('m2').is_unison()

    assert Interval('+8').is_octave()
    assert Interval('+8').is_octave('A')
    assert Interval('+8').is_octave('+')
    assert not Interval('+8').is_octave('P')
    assert not Interval('P1').is_octave()
    assert not Interval('m2').is_octave()

    assert Interval('+2').is_second('A')
    assert Interval('+2').is_second('+')
    assert not Interval('+2').is_second('m')
    assert Interval('m2').is_second()
    assert Interval('M2').is_second()
    assert Interval('ddd9').is_second()
    assert not Interval('m3').is_second()

    assert Interval('+3').is_third('A')
    assert Interval('+3').is_third('+')
    assert not Interval('+3').is_third('++')
    assert Interval('m3').is_third()
    assert Interval('M3').is_third()
    assert Interval('++10').is_third()
    assert not Interval('m2').is_third()

    assert Interval('+4').is_fourth('A')
    assert Interval('+4').is_fourth('+')
    assert not Interval('+4').is_fourth('oo')
    assert Interval('P4').is_fourth()
    assert Interval('d11').is_fourth()
    assert not Interval('m2').is_fourth()

    assert Interval('+5').is_fifth('A')
    assert Interval('+5').is_fifth('+')
    assert not Interval('+5').is_fifth('oo')
    assert Interval('P5').is_fifth()
    assert Interval('A12').is_fifth()
    assert not Interval('m3').is_fifth()

    assert Interval('M6').is_sixth('M')
    assert Interval('+6').is_sixth('+')
    assert not Interval('+6').is_sixth('oo')
    assert Interval('+6').is_sixth()
    assert Interval('m13').is_sixth()
    assert not Interval('+5').is_sixth()

    assert Interval('m7').is_seventh('m')
    assert Interval('+7').is_seventh('+')
    assert not Interval('+7').is_seventh('oo')
    assert Interval('+7').is_seventh()
    assert Interval('+++14').is_seventh()
    assert not Interval('+3').is_seventh()

    # SHOULD BE OK
    assert 'Interval("-M2")' == Interval(Pitch("Cs4"), Pitch("B3")).__repr__()
    assert 'Interval("m7")' == Interval(Pitch("Cs4"), Pitch("B4")).__repr__()
    assert 'Interval("-M2")' == Interval(Pitch('E4'), Pitch('D4')).__repr__()
    assert 'Interval("-m2")' == Interval(Pitch('E4'), Pitch('D#4')).__repr__()
    assert 'Interval("-M2")' == Interval(Pitch("Cs4"), Pitch("B3")).__repr__()
    assert 'Interval("m7")' == Interval(Pitch("Cs4"), Pitch("B4")).__repr__()
    assert 'Interval("-M9")' == Interval(Pitch("Cs4"), Pitch("B2")).__repr__()
    assert 'Interval("m14")' == Interval(Pitch("Cs4"), Pitch("B5")).__repr__()
    assert 'Interval("-o14")' == Interval(Pitch("Bb5"), Pitch("Cs4")).__repr__()

    assert 'Interval("P1")' == Interval(Pitch("B3"), Pitch("B3")).__repr__()
    assert 'Interval("P8")' == Interval(Pitch("B3"), Pitch("B4")).__repr__()
    assert 'Interval("-P8")' == Interval(Pitch("B3"), Pitch("B2")).__repr__()
    assert 'Interval("+1")' == Interval(Pitch("B3"), Pitch("Bs3")).__repr__()
    assert 'Interval("-+1")' == Interval(Pitch("B3"), Pitch("Bb3")).__repr__()
    assert 'Interval("-o2")' == Interval(Pitch('Eb4'), Pitch('D#4')).__repr__()

    assert 'Interval("ooo3")' == Interval(Pitch("B##3"), Pitch("Db4")).__repr__()
    assert 'Interval("o2")' == Interval(Pitch("B#3"), Pitch("C4")).__repr__()
    assert 'Interval("-+1")' == Interval(Pitch("B3"), Pitch("Bb3")).__repr__()

    assert 'Interval("-o2")' == Interval(Pitch('Eb4'), Pitch('D#4')).__repr__()
    assert 'Interval("+7")' == Interval(Pitch('Eb4'), Pitch('D#5')).__repr__()
    assert 'Interval("++7")' == Interval(Pitch('Ef3'), Pitch('D##4')).__repr__()

    assert 'Interval("+8")' == Interval(Pitch("C4"), Pitch("C#5")).__repr__()
    assert 'Interval("++8")' == Interval(Pitch("C4"), Pitch("C##5")).__repr__()
    assert 'Interval("+++8")' == Interval(Pitch("Cb4"), Pitch("C##5")).__repr__()
    assert 'Interval("++++8")' == Interval(Pitch("Cbb4"), Pitch("C##5")).__repr__()
    assert 'Interval("++++15")' == Interval(Pitch("Cbb4"), Pitch("C##6")).__repr__()

    assert 'Interval("-+8")' == Interval(Pitch("C#5"), Pitch("C4")).__repr__()
    assert 'Interval("-++8")' == Interval(Pitch("C##5"), Pitch("C4")).__repr__()
    assert 'Interval("-+++8")' == Interval(Pitch("C##5"), Pitch("Cb4")).__repr__()
    assert 'Interval("-++++8")' == Interval(Pitch("C##5"), Pitch("Cbb4")).__repr__()
    assert 'Interval("-++++15")' == Interval(Pitch("C##5"), Pitch("Cbb3")).__repr__()

    assert 'Interval("m7")' == Interval(Pitch("E4"), Pitch("D5")).__repr__()
    assert 'Interval("M7")' == Interval(Pitch("E4"), Pitch("D#5")).__repr__()
    assert 'Interval("+7")' == Interval(Pitch("E4"), Pitch("D##5")).__repr__()
    assert 'Interval("++7")' == Interval(Pitch("Eb4"), Pitch("D##5")).__repr__()
    assert 'Interval("+++7")' == Interval(Pitch("Ebb4"), Pitch("D##5")).__repr__()

    assert 'Interval("M6")' == Interval(Pitch("F4"), Pitch("D5")).__repr__()
    assert 'Interval("+6")' == Interval(Pitch("F4"), Pitch("D#5")).__repr__()
    assert 'Interval("++6")' == Interval(Pitch("F4"), Pitch("D##5")).__repr__()
    assert 'Interval("+++6")' == Interval(Pitch("Fb4"), Pitch("D##5")).__repr__()
    assert 'Interval("++++6")' == Interval(Pitch("Fbb4"), Pitch("D##5")).__repr__()

    assert 'Interval("+4")' == Interval(Pitch("F4"), Pitch("B4")).__repr__()
    assert 'Interval("++4")' == Interval(Pitch("F4"), Pitch("B#4")).__repr__()
    assert 'Interval("+++4")' == Interval(Pitch("F4"), Pitch("B##4")).__repr__()
    assert 'Interval("++++4")' == Interval(Pitch("Fb4"), Pitch("B##4")).__repr__()
    assert 'Interval("+++++4")' == Interval(Pitch("Fbb4"), Pitch("B##4")).__repr__()
    assert 'Interval("-++++4")' == Interval(Pitch("B#4"), Pitch("Fbb4")).__repr__()

    assert 'Interval("o5")' == Interval(Pitch("B4"), Pitch("F5")).__repr__()
    assert 'Interval("ooo5")' == Interval(Pitch("B4"), Pitch("Fbb5")).__repr__()
    assert 'Interval("oooo5")' == Interval(Pitch("B#4"), Pitch("Fbb5")).__repr__()
    assert 'Interval("ooooo5")' == Interval(Pitch("B##4"), Pitch("Fbb5")).__repr__()
    assert 'Interval("-ooooo5")' == Interval(Pitch("Fbb5"), Pitch("B##4")).__repr__()

    assert 'Interval("P75")' == Interval(Pitch("C00"), Pitch("G9")).__repr__()
    assert 'Interval("++74")' == Interval(Pitch("C00"), Pitch("F##9")).__repr__()
    assert 'Interval("o76")' == Interval(Pitch("C00"), Pitch("Abb9")).__repr__()

    assert [7, 6, 0, 1] == Interval([0, 6, 1, 1]).to_list()  # oct written as unison + 1 xoct.
    assert [7, 6, 1, 1] == Interval([0, 6, 2, 1]).to_list()  # oct written as unison + 1 xoct.

    assert Pitch.pnums.Bss == Interval("M7").transpose(Pitch.pnums.Css)
    assert Pitch.pnums.Cff == Interval("m2").transpose(Pitch.pnums.Bff)
    assert Pitch.pnums.Css == Interval("+1").transpose(Pitch.pnums.Cs)
    assert Pitch.pnums.Gf == Interval("m3").transpose(Pitch.pnums.Ef)
    assert Pitch.pnums.As == Interval("+6").transpose(Pitch.pnums.C)
    assert Pitch.pnums.Bff == Interval("M7").transpose(Pitch.pnums.Cff)

    # WORKING
    assert 'Fff' == Interval('P1').transpose(Pitch.pnums.Fff).name
    assert 'Ff' == Interval('+1').transpose(Pitch.pnums.Fff).name
    assert 'F' == Interval('++1').transpose(Pitch.pnums.Fff).name
    assert 'Fs' == Interval('+++1').transpose(Pitch.pnums.Fff).name
    assert 'Fss' == Interval('++++1').transpose(Pitch.pnums.Fff).name
    # EXPLICITLY DISALLOWED
    # Interval('P1').transpose(Pitch.pnums.Fss)
    # Interval('o1').transpose(Pitch.pnums.Fss)
    # Interval('oo1').transpose(Pitch.pnums.Fss)
    # Interval('ooo1').transpose(Pitch.pnums.Fss)
    # Interval('oooo1').transpose(Pitch.pnums.Fss)
    assert 'Fff' == Interval('P8').transpose(Pitch.pnums.Fff).name
    assert 'Ff' == Interval('+8').transpose(Pitch.pnums.Fff).name
    assert 'F' == Interval('++8').transpose(Pitch.pnums.Fff).name
    assert 'Fs' == Interval('+++8').transpose(Pitch.pnums.Fff).name
    assert 'Fss' == Interval('++++8').transpose(Pitch.pnums.Fff).name
    assert 'Fss' == Interval('P8').transpose(Pitch.pnums.Fss).name
    assert 'Fs' == Interval('o8').transpose(Pitch.pnums.Fss).name
    assert 'F' == Interval('oo8').transpose(Pitch.pnums.Fss).name
    assert 'Ff' == Interval('ooo8').transpose(Pitch.pnums.Fss).name
    assert 'Fff' == Interval('oooo8').transpose(Pitch.pnums.Fss).name
    assert 'Fs' == Interval('A8').transpose(Pitch.pnums.F).name
    assert 'Fs' == Interval('-A8').transpose(Pitch.pnums.F).name

    assert 'Pitch("G4")' == Interval("M2").transpose(Pitch('F4')).__repr__()
    assert 'Pitch("F4")' == Interval("P1").transpose(Pitch('F4')).__repr__()
    assert 'Pitch("F5")' == Interval("P8").transpose(Pitch('F4')).__repr__()
    assert 'Pitch("F3")' == Interval("-P8").transpose(Pitch('F4')).__repr__()
    assert 'Pitch("F#5")' == Interval("A8").transpose(Pitch('F4')).__repr__()
    assert 'Pitch("Fb5")' == Interval("d8").transpose(Pitch('F4')).__repr__()

    # BUG!!! THIS DOES NOT WORK. MAYBE THE
    # Interval('-A1').transpose(Pitch.pnums.F)
    # ERRORS
    msg1, msg2 = "Received wrong type of exception.", \
                 "Expected exception did not happen."

    # TYPE ERRORS
    err = TypeError

    try: Interval([])
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Interval([0, 6])
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Interval([0, 6, 0])
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Interval(123.0)
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Interval((3, 6, 0, 1))
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Interval(Pitch("c4"), 1.0)
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Interval(1.0, Pitch("c4"))
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    # VALUE ERRORS
    err = ValueError

    try: Interval('M0')
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Interval('1')
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Interval('X1')
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Interval("+++")
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Interval("+-+5")
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Interval("M1")
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Interval("M4")
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Interval("M5")
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Interval("M8")
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Interval("m1")
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Interval("m4")
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Interval("m5")
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Interval("m8")
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Interval('o1')
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Interval('oo2')
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Interval('oooo3')
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Interval('oooo3')
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Interval(Pitch("C00"), Pitch("G#9"))
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Interval(Pitch("B#3"), Pitch("Cb4"))
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Interval(Pitch("B##3"), Pitch("Cbb4"))
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Interval(Pitch("B##3"), Pitch("Cbb4"))
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Interval(Pitch("B##3"), Pitch("Dbb4"))
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Interval([0, 6, 0, 0])
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Interval([8, 0, 0, 1])
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Interval([0, 13, 0, 1])
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Interval([0, 6, -1, 1])
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Interval([0, 6, 11, 1])
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Interval([0, 1, 0, 1])
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Interval([0, 2, 0, 1])
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Interval([0, 4, 0, 1])
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Interval([5, 6, 10, 1])
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Interval([4, 6, 11, 1])
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Interval("m7").transpose(Pitch.pnums.Cff)
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    # try: XXX
    # except err: pass
    # except: assert False, msg1
    # else: assert False, msg2

    print('Done!')


if __name__ == '__main__':
    _test_intervals()

'''
from random import randint, choice
from mus import Pitch, Interval
def rand():
    s = randint(0, 7)
    q = choice([4, 6, 8]) if s in [0, 3, 4, 7] else choice([4, 5, 7, 8])
    return [s, q, 0, 1]
y=rand()

for s in [1,4,5,8]:
    for q in ["ooooo", "oooo", "ooo", "oo", "o", "P", "+", "++", "+++", "++++", "+++++"]:
        x = Interval(q+str(s))
        y = x.semitones()
        z = x.semitones2()
        print(y,z)
        assert y == z , "OOPS"

for s in [2,3,6,7]:
    for q in ["ooooo", "oooo", "ooo", "oo", "o", "m", "M", "+", "++", "+++", "++++", "+++++"]:
       x = Interval(q+str(s))
       y = x.semitones()
       z = x.semitones2()
       print(y,z)
       assert y == z , "OOPS"

for s in [2,3,6,7]:
    for q in ["ooooo", "oooo", "ooo", "oo", "o", "m", "M", "+", "++", "+++", "++++", "+++++"]:
        print(Interval(q+str(s)))    


'''
