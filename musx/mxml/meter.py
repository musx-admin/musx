"""
A class representing standard musical meters.
"""

from fractions import Fraction


class Meter:
    """
    Returns a meter with integer attributes num and den set.

    Parameters
    ----------
    num : int
        The numerator, an integer between 1 and 16 inclusive.
    den : int
        The denominator, a power of 2 between 1 and 32 inclusive.
    staffnum : int
        The staff number of the meter, 0 if meter applies to all staffs. 
    """
    def __init__(self, num, den, staffnum):
        if not isinstance(num, int):
            raise TypeError(f"Invalid meter numerator: {num}.")
        if not 1 <= num <= 16:
            raise ValueError(f"Invalid meter numerator: {num}.")
        if not isinstance(den, int):
            raise TypeError(f"Invalid meter denominator: {den}.")
        if not (den in [1, 2, 4, 8, 16, 32]):
            raise ValueError(f"Invalid meter denominator: {den}.")
        if not isinstance(staffnum, int):
            raise ValueError(f"Invalid staff number: {num}")
        self.num = num
        """The numerator number of the meter."""
        self.den = den
        """The denominator number of the meter."""   
        self.staffnum = staffnum
        """The staff number of the meter (0=All)."""

    def __str__(self):
        """
        Returns the print representation of the meter.
        """
        staff = "all" if self.staffnum == 0 else self.staffnum
        return f"<Meter: {self.num}/{self.den} staff={staff}>" # {hex(id(self))

    def __repr__(self):
        """
        Returns the external representation of the meter.
        """
        return f'Meter({self.num}, {self.den} , {self.staffnum})'

    # def string(self):
    #     """
    #     Returns the string name of the meter, e.g. '6/8'
    #     """
    #     return f'{self.num}/{self.den}'

    def is_compound(self):
        """
        Returns true if the meter is compound (numerator 6, 9, 12, or 15).
        """
        return self.num in [6, 9, 12, 15]

    def is_simple(self):
        """
        Returns true if the meter is simple (numerator 1, 2, 3, or 4).
        """
        return self.num in [1, 2, 3, 4]
    
    def is_complex(self):
        """
        Returns true if the meter is complex (numerator 5, 7, 8, 10, 11, 13, or 14).
        """
        return self.num in [5, 7, 8, 10, 11, 13, 14]

    def is_duple(self):
        """
        Returns true if the meter is duple (numerator 2 or 6).
        """
        return self.num in [2, 6]

    def is_triple(self):
        """
        Returns true if the meter is triple (numerator 3 or 9).
        """
        return self.num in [3, 9]

    def is_quadruple(self):
        """
        Returns true if the meter is quadruple (numerator 4 or 12).
        """
        return self.num in [4, 12]
    
    def is_quintuple(self):
        """
        Returns true if the meter is quintuple (numerator 5 or 15).
        """
        return self.num in [5, 15]

    def is_septuple(self):
        """
        Returns true if the meter is a septuple (numerator 7).
        """
        return self.num in [7]

    def beat(self):
        """
        Returns a Fraction representing the meter's beat duration. For
        example, 4/4 returns a beat of 1/4, 6/8 meter returns the beat 3/8,
        and 3/2 returns a beat of 1/2.
        """
        if self.is_simple():
            return Fraction(1, self.den)
        elif self.is_compound():
            return Fraction(1, self.den) * 3
        else:
            raise NotImplementedError('Ooops! Odd meter beats not implemented.')


    def measure_dur(self):
        """
        Returns a Fraction representing the meter's total measure duration, in
        beats. For example, 4/4 returns a duration Fraction of 1/1, 6/8 meter
        returns 3/4, and 3/2 returns a duration of 3/2. See: Fraction.
        """
        return Fraction(1, self.den) * self.num

