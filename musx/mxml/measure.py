"""
A class that represents a measure of music in a Part.
"""

from ..note import Event, Note

class Measure:
    """
    A class that represents a measure of music in a `musx.mxml.part.Part`. A Measure
    contain notes -- tagged as either `note`, `chord` or `rest` -- as
    well as notational objects such as `musx.mxml.key.Key`, `musx.mxml.clef.Clef`, etc. 
        
    A Measure that has been added to a Part contains a backpointer to its owning part.

    Parameters
    ----------
    id : int
        The measure's unique integer identifier in its owning Part.
    """

    def __init__(self, id):
        self.id = id
        """The measure's integer identifier in its owning Part."""
        self.elements = []
        """The measure's elements, in MusicXml file order."""
        self.partial = False
        """If true the measure is an incomplete (pickup) measure."""
        self.onset = False
        """The onset time of the measure expressed as a fraction."""

    def add_element(self, element):
        """
        Adds a measure element in MusicXml order.  The element can be a
        `musx.note.Note` or a notational object such as a `musx.mxml.key.Key` 
        or `musx.mxml.clef.Clef`, etc. 
        """
        self.elements.append(element)

    def voices(self):
        """
        Returns a dictionary whose keys are the Measure's voice ids and whose
        values are the time ordered notes that belong to that voice.
        """
        voices = {}
        for e in self.elements:
            if isinstance(e, Note):
                v = e.get_mxml('voice',1)
                try: voices[v].append(e)
                except KeyError:
                    voices[v] = [e]
        return voices

    def __iter__(self):
        """
        Iterates the Measure's elements.
        """
        return iter(self.elements)

    def __str__(self):
        return f'<Measure: {self.id}>'

    __repr__ = __str__
