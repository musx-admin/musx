"""
An enumeration of music clefs: Treble, Soprano, MezzoSoprano, Alto, Tenor,
Baritone, Bass, Treble8va, Bass8va, Treble15ma, Bass15ma, TenorTreble, 
BaritoneF, SubBass, FrenchViolin, Percussion. 
"""

from enum import Enum

# Line-Space unit Constants, where BOTTOM_LINE is 0 and TOP_LINE is 8.
_TOP_LINE = 8
_SPACE_BELOW_TOP_LINE = 7
_LINE_ABOVE_MIDDLE_LINE = 6
_SPACE_ABOVE_MIDDLE_LINE = 5
_MIDDLE_LINE = 4
_SPACE_BELOW_MIDDLE_LINE = 3
_LINE_BELOW_MIDDLE_LINE = 2
_SPACE_ABOVE_BOTTOM_LINE = 1
_BOTTOM_LINE = 0

class Clef:
    """
    To create a Clef don't call the constructor directly, call one of the class
    factory methods listed below.
    """
    def __init__(self, staffnum, ident, linespace, transpostion):
        self.staffnum = staffnum
        self.ident = ident
        self.linespace = linespace
        self.transpostion = transpostion

    @classmethod
    def Alto(cls, staffnum=None):
        """
        Parameters
        ----------
        staffnum : int
            The MusicXml staff number of the clef. If zero then the clef is attached
            to all staffs.
        """
        return cls(staffnum, 3, _MIDDLE_LINE, 0)
        
    @classmethod
    def Treble(cls, staffnum=None):
        return cls(staffnum, 0, _LINE_BELOW_MIDDLE_LINE, 0)

    @classmethod
    def Soprano(cls, staffnum=None):
        return cls(staffnum, 1, _BOTTOM_LINE, 0)

    @classmethod
    def MezzoSoprano(cls, staffnum=None):
        return cls(staffnum, 2, _LINE_BELOW_MIDDLE_LINE, 0)


    @classmethod
    def Tenor(cls, staffnum=None):
        return cls(staffnum, 4, _LINE_ABOVE_MIDDLE_LINE, 0)

    @classmethod
    def Baritone(cls, staffnum=None):
        return cls(staffnum, 5, _TOP_LINE, 0)

    @classmethod
    def Bass(cls, staffnum=None):
        return cls(staffnum, 6, _LINE_ABOVE_MIDDLE_LINE, 0)

    @classmethod
    def Treble8va(cls, staffnum=None):
        return cls(staffnum, 7, _LINE_BELOW_MIDDLE_LINE, 8)

    @classmethod
    def Bass8va(cls, staffnum=None):
        return cls(staffnum, 8, _LINE_ABOVE_MIDDLE_LINE, -8)

    @classmethod
    def Treble15ma(cls, staffnum=None):
        return cls(staffnum, 9, _LINE_BELOW_MIDDLE_LINE, 15)

    @classmethod        
    def Bass15ma(cls, staffnum=None):
        return cls(staffnum, 10, _LINE_ABOVE_MIDDLE_LINE, -15)

    @classmethod
    def TenorTreble(cls, staffnum=None):
        return cls(staffnum, 11, _LINE_BELOW_MIDDLE_LINE, -8)

    @classmethod
    def BaritoneF(cls, staffnum=None):
        return cls(staffnum, 12, _MIDDLE_LINE, 0)

    @classmethod
    def SubBass(cls, staffnum=None):
        return cls(staffnum, 13, _TOP_LINE, 0)

    @classmethod
    def FrenchViolin(cls, staffnum=None):
        return cls(staffnum, 14, _BOTTOM_LINE, 0)

    @classmethod
    def Percussion(cls, staffnum=None):
        return cls(staffnum, 15, _MIDDLE_LINE, 0)

    _names = {
            0: "Treble", 1: "Soprano", 2: "MezzoSoprano", 3: "Alto",
            4: "Tenor",  5: "Baritone", 6: "Bass", 7: "Treble8va", 
            8: "Bass8va", 9: "Treble15ma", 10: "Bass15ma", 11: "TenorTreble", 
            12: "BaritoneF", 13: "SubBass", 14: "FrenchViolin", 15: "Percussion"
        }

    def __str__(self):
        staff = "all" if self.staffnum == 0 else self.staffnum
        return f'<Clef: {type(self)._names[self.ident]} staff={staff}>' #  {hex(id(self))}

    __repr__ = __str__




# class ClefType (Enum):
#     TREBLE = (0, LINE_BELOW_MIDDLE_LINE, 0)
#     SOPRANO = (1, BOTTOM_LINE, 0)
#     MEZZO_SOPRANO = (2, LINE_BELOW_MIDDLE_LINE, 0)
#     ALTO = (3, MIDDLE_LINE, 0)
#     TENOR = (4, LINE_ABOVE_MIDDLE_LINE, 0)
#     BARITONE = (5, TOP_LINE, 0)
#     BASS = (6, LINE_ABOVE_MIDDLE_LINE, 0)
#     TREBLE_8VA = (7, LINE_BELOW_MIDDLE_LINE, 8)
#     BASS_8VA = (8, LINE_ABOVE_MIDDLE_LINE, -8)
#     TREBLE_15MA = (9, LINE_BELOW_MIDDLE_LINE, 15)
#     BASS_15MA = (10, LINE_ABOVE_MIDDLE_LINE, -15)
#     TENOR_TREBLE = (11, LINE_BELOW_MIDDLE_LINE, -8)
#     BARITONE_F = (12, MIDDLE_LINE, 0)
#     SUB_BASS = (13, TOP_LINE, 0)
#     FRENCH_VIOLIN = (14, BOTTOM_LINE, 0)
#     PERCUSSION = (15, MIDDLE_LINE, 0)


#     def linespace(self):
#         """Returns the linespace attachment value of the clef."""
#         return self.value[1]


#     def transposition(self):
#         """Returns the transposition level of the clef."""
#         return self.value[2]


# def _test_clefs():
#     print('Testing clef.py ... ', end='')
#     assert 16 == len(Clef)
#     assert Clef['TREBLE']
#     assert Clef['SOPRANO']
#     assert Clef['MEZZO_SOPRANO']
#     assert Clef['ALTO']
#     assert Clef['TENOR']
#     assert Clef['BARITONE']
#     assert Clef['BASS']
#     assert Clef['TREBLE_8VA']
#     assert Clef['BASS_8VA']
#     assert Clef['TREBLE_15MA']
#     assert Clef['BASS_15MA']
#     assert Clef['TENOR_TREBLE']
#     assert Clef['BARITONE_F']
#     assert Clef['SUB_BASS']
#     assert Clef['FRENCH_VIOLIN']
#     assert Clef['PERCUSSION']
#     assert (0, LINE_BELOW_MIDDLE_LINE, 0) == Clef['TREBLE'].value
#     assert (1, BOTTOM_LINE, 0) == Clef['SOPRANO'].value
#     assert (2, LINE_BELOW_MIDDLE_LINE, 0) == Clef['MEZZO_SOPRANO'].value
#     assert (3, MIDDLE_LINE, 0) == Clef['ALTO'].value
#     assert (4, LINE_ABOVE_MIDDLE_LINE, 0) == Clef['TENOR'].value
#     assert (5, TOP_LINE, 0) == Clef['BARITONE'].value
#     assert (6, LINE_ABOVE_MIDDLE_LINE, 0) == Clef['BASS'].value
#     assert (7, LINE_BELOW_MIDDLE_LINE, 8) == Clef['TREBLE_8VA'].value
#     assert (8, LINE_ABOVE_MIDDLE_LINE, -8) == Clef['BASS_8VA'].value
#     assert (9, LINE_BELOW_MIDDLE_LINE, 15) == Clef['TREBLE_15MA'].value
#     assert (10, LINE_ABOVE_MIDDLE_LINE, -15) == Clef['BASS_15MA'].value
#     assert (11, LINE_BELOW_MIDDLE_LINE, -8) == Clef['TENOR_TREBLE'].value
#     assert (12, MIDDLE_LINE, 0) == Clef['BARITONE_F'].value
#     assert (13, TOP_LINE, 0) == Clef['SUB_BASS'].value
#     assert (14, BOTTOM_LINE, 0) == Clef['FRENCH_VIOLIN'].value
#     assert (15, MIDDLE_LINE, 0) == Clef['PERCUSSION'].value
#     print('Done!')


# if __name__ == '__main__':
#     _test_clefs()



