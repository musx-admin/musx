###############################################################################

"""
A class representing standard musical meters.
"""

from fractions import Fraction


class Meter:

    def __init__(self, num, den, staffnum):
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
        ## The numerator number of the meter.
        self.num = num
        ## The denominator number of the meter.
        self.den = den
        # The staff number of the meter (0=All)
        self.staffnum = staffnum

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
        Returns a Fraction representing the meter's beat. For example,
        4/4 returns a beat of 1/4, 6/8 meter returns the beat 3/8,
        and 3/2 returns a beat of 1/2. The method should raise
        a NotImplementedError If the meter is not simple or compound.
        See: Fraction.
        """
        if self.is_simple():
            return Fraction(1, self.den)
        elif self.is_compound():
            return Fraction(1, self.den) * 3
        else:
            raise NotImplementedError('Ooops! Odd meter beats not implemented.')


    def measure_dur(self):
        """
        Returns a Fraction representing the meter's total measure duration, in beats.
        For example, 4/4 returns a duration Fraction of 1/1, 6/8 meter returns 3/4,
        and 3/2 returns a duration of 3/2. See: Fraction.
        """
        return Fraction(1, self.den) * self.num


'''
from mus.meter import Meter
from mus.Fraction import Fraction
'''


def _test_meters():
    assert Fraction("1/2") == Meter(1, 2).measure_dur()
    assert Fraction("1/16") == Meter(2, 32).measure_dur()
    assert Fraction("3/2") == Meter(3, 2).measure_dur()
    assert Fraction("1/4") == Meter(4, 16).measure_dur()
    assert Fraction("5/8") == Meter(5, 8).measure_dur()
    assert Fraction("3/2") == Meter(6, 4).measure_dur()
    assert Fraction("7/8") == Meter(7, 8).measure_dur()
    assert Fraction("4/1") == Meter(8, 2).measure_dur()
    assert Fraction("9/4") == Meter(9, 4).measure_dur()
    assert Fraction("10/4") == Meter(10, 4).measure_dur()
    assert Fraction("11/16") == Meter(11, 16).measure_dur()
    assert Fraction("12/1") == Meter(12, 1).measure_dur()
    assert Fraction("13/2") == Meter(13, 2).measure_dur()
    assert Fraction("7/2") == Meter(14, 4).measure_dur()
    assert Fraction("15/32") == Meter(15, 32).measure_dur()
    assert Fraction("1/1") == Meter(16, 16).measure_dur()

    assert Fraction("1/2") == Meter(1, 2).beat()
    assert Fraction("1/32") == Meter(2, 32).beat()
    assert Fraction("1/2") == Meter(3, 2).beat()
    assert Fraction("1/16") == Meter(4, 16).beat()
    assert Fraction("3/4") == Meter(6, 4).beat()
    assert Fraction("1/8") == Meter(4, 8).beat()
    assert Fraction("3/4") == Meter(9, 4).beat()
    assert Fraction("3/1") == Meter(12, 1).beat()
    assert Fraction("3/32") == Meter(15, 32).beat()
    assert Fraction("3/1") == Meter(12, 1).beat()

    assert Meter(15, 32).is_compound()
    assert Meter(12, 4).is_compound()
    assert Meter(9, 16).is_compound()
    assert Meter(6, 2).is_compound()

    assert Meter(2, 32).is_simple()
    assert Meter(1, 4).is_simple()
    assert Meter(4, 16).is_simple()
    assert Meter(3, 2).is_simple()

    assert Meter(2, 32).is_duple()
    assert Meter(2, 32).is_duple()
    assert not Meter(4, 16).is_duple()
    assert not Meter(3, 2).is_duple()

    assert Meter(3, 32).is_triple()
    assert Meter(3, 32).is_triple()
    assert not Meter(4, 16).is_triple()
    assert Meter(3, 2).is_triple()

    assert not Meter(2, 2).is_quadruple()
    assert not Meter(7, 4).is_quadruple()
    assert Meter(4, 2).is_quadruple()
    assert Meter(12, 1).is_quadruple()

    assert Meter(5, 2).is_quintuple()
    assert not Meter(7, 4).is_quintuple()
    assert Meter(5, 2).is_quintuple()
    assert Meter(5, 2).is_quintuple()

    assert Meter(7, 32).is_septuple()
    assert not Meter(11, 2).is_septuple()
    assert not Meter(13, 8).is_septuple()
    assert not Meter(15, 2).is_septuple()

    assert Meter(7, 32).is_complex()
    assert Meter(8, 8).is_complex()
    assert Meter(10, 2).is_complex()
    assert Meter(11, 8).is_complex()
    assert Meter(14, 2).is_complex()
    assert not Meter(15, 2).is_complex()

    # TypeError

    msg1, msg2 = "Received wrong type of exception.", \
                 "Expected exception did not happen."

    # TYPE ERRORS
    err = TypeError
    try: Meter(4, 4.0)
    except err: pass
    except: assert False, msg1
    else: assert False, msg2


    # VALUE ERRORS
    err = ValueError

    try: Meter(4, 5)
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Meter(0, 4)
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    try: Meter(0, 4)
    except err: pass
    except: assert False, msg1
    else: assert False, msg2

    err = NotImplementedError

    try: Fraction("5/8") == Meter(5, 8).beat()
    except err: pass
    except: assert False, msg1
    else: assert False, msg2
