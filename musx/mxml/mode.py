"""
An enumeration of the diatonc modes: MAJOR, MINOR, IONIAN, DORIAN,
PHRYGIAN, LYDIAN, MIXOLYDIAN, AEOLIAN, and LOCRIAN. IONIAN and AEOLIAN
are synonyms for MAJOR and MINOR
"""

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
    
    def tonic_degree(self):
        """
        Returns the integer scale degree number representing the starting
        scale degree of the mode. Thus IONIAN and MAJOR are 0, DORIAN is
        1, LOCRIAN is 6 and so on.
        """
        return self.value - 1
