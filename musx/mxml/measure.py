"""
A class that represents a measure of music in a Part.
"""

from ..note import Event, Note

class Measure:

    def __init__(self, id):
        """
        A class that represents a measure of music in a Part. A Measure
        contains Notes (tagged as either Note, Chord or Rest) as well as 
        notational objects such as Key, Clef, Meter, Barline, etc. 

        Parameters
        ----------
        id : The measure's unique integer identifier in its owning Part.
        """
        # The measure's integer identifier in its owning Part.
        self.id = id
        # The measure's elements, in MusicXml order.
        self.elements = []
        # If true the measure is an incomplete (pickup) measure.
        self.partial = False

    def add_element(self, element):
        """
        Adds a measure element to the measure in the same order as occurring
        in the MusicXml score file.  The element can be a Note (which will be
        tagged as either 'note', 'rest' or 'chord'), or an mxml notational
        object such as a Clef, Key, Meter, Barline, etc. 
        """
        self.elements.append(element)

    def voices(self):
        """
        Returns a dictionary whose keys are the Measure's voice ids and whose
        values are the time ordered Notes that belong to that voice.
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
