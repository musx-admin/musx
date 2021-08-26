
"""
An enumeration of measure barlines: Regular, Dotted, Dashed, Tick, Short, Heavy, 
HeavyHeavy, HeavyLight, InteriorDouble, FinalDouble, BackwardRepeat, ForwardRepeat,
DoubleRepeat.
"""

class Barline:
    """
    To create a Barline don't call the constructor directly, call one of the class
    factory methods listed below. 
    """

    def __init__(self, ident, location):
        self.ident = ident
        self.location = location

    @classmethod
    def BackwardRepeat(cls, location):
        """
        Parameters
        ----------
        location: str
            Either "left", "right" or "both".
        """
        return cls(11, location)

    @classmethod
    def Dashed(cls, location):
        return cls(3, location)

    @classmethod
    def Dotted(cls, location):
        return cls(2, location)

    @classmethod
    def DoubleRepeat(cls, location):
        return cls(13, location)

    @classmethod
    def FinalDouble(cls, location):
        return cls(10, location)

    @classmethod
    def ForwardRepeat(cls, location):
        return cls(12, location)

    @classmethod
    def Heavy(cls, location):
        return cls(6, location)

    @classmethod
    def HeavyHeavy(cls, location):
        return cls(7, location)

    @classmethod
    def HeavyLight(cls, location):
        return cls(8, location)

    @classmethod
    def InteriorDouble(cls, location):
        return cls(9, location)

    @classmethod
    def Regular(cls, location):
        return cls(1, location)

    @classmethod
    def Short(cls, location):
        return cls(5, location)

    @classmethod
    def Tick(cls, location):
        return cls(4, location)

    _names = {
            1: "Regular", 2: "Dotted", 3: "Dashed", 4: "Tick",  5: "Short", 6: "Heavy",
            7: "HeavyHeavy", 8: "HeavyLight", 9: "InteriorDouble", 10: "FinalDouble", 
            11: "BackwardRepeat", 12: "ForwardRepeat", 13: "DoubleRepeat"
        }

    def __str__(self):
        return f'<Barline: {type(self)._names[self.ident]} pos={self.location}>' #  {hex(id(self))}

    __repr__ = __str__


 