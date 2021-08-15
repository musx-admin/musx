###############################################################################
"""
A class that represents a musical Voice in a Bar. One voice holds a single
timeline of notes; multiple voices represent parallel streams of notes.
"""

from fractions import Fraction
#from .durational import Durational


class Voice:

    def __init__(self, voiceid):
        """
        Initializes a Voice and its attributes self.id, self.notes,
        and self.bar. The attribute self.notes should be initialized
        to an empty list and self.bar to None.

        Parameters
        ----------
        voiceid : int
            The unique integer id for the voice's id attribute.
    
        See Also
        --------
        `Note`, `Rest`, `Chord`, `Bar`
        """
        ## The unique id of the voice in its Bar.
        self.id = voiceid
        ## The notes, rests, and chords in the voice. See: Durational.
        self.notes = []
        ## The voice's owning bar.
        self.bar = None

    def __str__(self):
        """
        Returns a string showing the voices's unique id and the hex id of the instance.

        Example
        -------
        ```text
        '<Voice: 2 0x109877c50>'
        ```
        """
        return f'<Voice: {self.id} {hex(id(self))}>'

    def __repr__(self):
        """
        Define __repr__ to be the same as __str__ except there is no hex id included.

        Example
        -------
        ```text
        '<Voice: 2>'
        ```
        """
        return f'<Voice: {self.id}>'

    def __iter__(self):
        """
        Implements Voice iteration by returning an iterator for the voices's notes.
      
        See Also
        --------
        Python's `iter()` function.
        """
        return iter(self.notes)

    def add_note(self, note):
        """
        Appends a Note, Chord or Rest to the voice's note list and assigns
        itself to that object's voice attribute.

        Parameters
        ----------
        note : Note
            The note, chord, or rest to append to the note list.
        
        Raises
        ------
        The method should raise a TypeError if object supplied is not a Durational.
        """
        if not isinstance(note, Durational):
            raise TypeError(f"'{note} is not a Note, Chord or Rest.")
        note.voice = self
        self.notes.append(note)


    def dur(self):
        """
        Returns a beat Fraction representing the total duration of the notes
        in the voice.
        """
        dur = Fraction(0, 1)
        for note in self.notes:
            dur += note.dur
        return dur


    def get_pvid(self):
        """
        Returns a 'part and voice' identifier of the voice, a string concatenation
        of the part's id with the voice's id: PARTID.VOICEID.

        Example
        -------
        ```text
        'P1.1'
        ```
        """
        return self.bar.staff.part.id + "." + str(self.id)

