###############################################################################
"""
An enumeration of all the 7-tone modes: MAJOR, MINOR, IONIAN, DORIAN,
PHRYGIAN, LYDIAN, MIXOLYDIAN, AEOLIAN, and LOCRIAN. The value for each mode
should be a number index 0-6 representing its diatonic scale degree C-B.
For example, MAJOR will be 0 (C), MINOR is 5 (A) and Dorian is 1 (D).
Define IONIAN and AEOLIAN as synonyms for MAJOR and MINOR by assigning
them their corresponding enum value.
"""

__pdoc__ = {
    'Mode.__init__': False
}

from enum import IntEnum


class Mode (IntEnum):

    MAJOR = 1
    IONIAN = MAJOR
    DORIAN = 2
    PHRYGIAN = 3
    LYDIAN = 4
    MIXOLYDIAN = 5
    MINOR = 6
    AEOLIAN = MINOR
    LOCRIAN = 7
    
    # def short_name(self):
    #     """
    #     Returns only the first three characters of the mode's name.
    #     """
    #     return self.name[:3]
    
    def tonic_degree(self):
        """
        Returns the integer degree number representing the starting
        scale degree of the mode. Thus IONIAN and MAJOR are 0,
        DORIAN is 1, LOCRIAN is 6 and so on.
        """
        return self.value - 1

if __name__ == '__main__':
    def _test_modes():
        print('Testing mode.py ... ', end='')
        assert 1 == Mode['MAJOR']
        assert 2 == Mode['DORIAN']
        assert 3 == Mode['PHRYGIAN']
        assert 4 == Mode['LYDIAN']
        assert 5 == Mode['MIXOLYDIAN']
        assert 6 == Mode['MINOR']
        assert 7 == Mode['LOCRIAN']
        assert 7 == len(Mode)
        assert Mode['IONIAN'] is Mode['MAJOR']
        assert Mode['AEOLIAN'] is Mode['MINOR']
        print('Done!')
    _test_modes()
