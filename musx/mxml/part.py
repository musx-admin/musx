"""
A class that represents a musical part in a `musx.mxml.notation.Notation`.
"""

class Part():
    """
    A class that represents a musical part in a `musx.mxml.notation.Notation`.

    A part that has been added to a notation contains a backpointer
    to its owning notation.

    Parameters
    ----------
    id : string
        A string part identifier from the MusicXml file.
    """
    def __init__(self, id, measures=[]):
        self.id = id
        """The string part id from the MusicXml file."""
        self.measures = []
        """The list of measures in the part."""
        for m in measures:
            self.add_measure(m)

    def __iter__(self):     
        return iter(self.measures)

    def __str__(self):
        text = self.id
        return f'<Part: {text}>' #  {hex(id(self))}

    __repr__ = __str__ 

    def add_measure(self, measure):
        """
        Adds a measure to part. Once added, the measure will have a
        backpointer to its owning part.
        """
        measure.part = self  # back link from measure to its part
        self.measures.append(measure)
