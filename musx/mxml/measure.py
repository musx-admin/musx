###############################################################################
"""A class representing a measure of music."""

from .voice import Voice

class Measure:

    def __init__(self, id):
        """
        The initializer (__init__) sets the Measure attributes self.id, self.clef,
        self.key, self.meter, self.voices, self.barline, self.partial,
        and self.staff. Initialize self.voices to an empty list and self.staff to None.

        Parameters
        ----------

        bid : int
            An integer for the bar's id attribute.
        clef : Clef
            A Clef for the bar's clef attribute. Defaults to None.
        key : Key
            A Key for the bar's measure attribute.  Defaults to None.
        meter : Meter
            A Meter for the bar's meter attribute. Defaults to None.
        barline : Barline
            A Barline for the bar's barline attribute. Defaults to None.
        partial : boolean
            A boolean value for the bar's partial attribute. If true the bar
            is an incomplete (e.g. pickup) measure. Defaults to False.
        """
        # The measure's integer identifier in its owning Part.
        self.id = id
        # Optional Clef(s) for the measure.
        self.clefs = []
        # Optional Key(s) for the measure.
        self.keys = []
        # Optional Meter(s) for the measure.
        self.meters = []
        # The list of Voices in the measure.
        self.voices = []
        # The left/right Barlines for the measure.
        self.barlines = []
        # If true the measure is an incomplete (pickup) measure.
        self.partial = False
        # The bar's owning Staff.
        self.staff = None

    def __str__(self):
        text = f'<Measure: {self.id}'
        for c in self.clefs:
            text += " " + str(c)
        for k in self.keys:
            text += " " + str(k)
        for m in self.meters:
            text += " " + str(m)
        #print("*** barlines", len(self.barlines))
        for b in self.barlines:
            text += " " + str(b)
        text += ">"
        return text

    __repr__ = __str__

    def __iter__(self):
        """
        Implements Measure iteration
        """
        return iter(self.voices)

    def num_voices(self):
        """Returns the number of voices in the bar."""
        return len(self.voices)


if __name__ == "__main__":
    # add your testing code here.
    pass
