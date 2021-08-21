"""
Defines a base Event class for musical events, a generic Note class to
represent time, duration, pitch, and amplitude, and a Chord class to
bundle Notes with a common start time and duration. Notes are automatically
converted to whatever format is requred by a specific back ends, e.g. MIDI,
Csound, or MusicXml.
"""

from .midi import midievent as me
from .midi import midimsg as mm
from .tools import quantize
from .pitch import Pitch
from fractions import Fraction

class Event:
    """
    A base class for defining musical events. Any subclass of Event can
    be added to a `Seq` object.

    Parameters
    ----------
    time : int | float
        The onset time in seconds, defaults to 0.0.  For ways to specify
        time and duration metrically, see `rhythm()` and `intempo()`.
    """
      
    def __init__(self, time):
        self.time = time

    @property
    def time(self):
        """
        The start time of the event in seconds, defaults to 0.0.  For ways
        to specify time metrically, see `rhythm()` and `intempo()`.

        Raises
        ------
        ValueError if the time value is not a number >= 0.
        """
        return self._time

    @time.setter
    def time(self, val):
        if isinstance(val, (int, float, Fraction)) and val >= 0:
            self._time = val
        else:
            raise ValueError(f"Invalid Note time: {val}.")


class Note (Event):
    """
    Creates a Note instance from its arguments. A Note is a sound event
    that can be used in different contexts. For example, if a Note is
    passed to methods in the MIDI or Csound modules the note data will
    be automatically converted to the format supported by the module.

    Parameters
    ----------
    time : int | float | Fraction
        The onset time in seconds, defaults to 0.0.  For ways to specify
        time and duration metrically, see `rhythm()` and `intempo()`.
    duration : int | float | Fraction
        The duration in seconds, defaults to 1.0. For ways to specify
        duration and time metrically, see `rhythm()` and `intempo()`.
    pitch : int | float | Pitch
        An int or float key number 0 to 127, or a `Pitch` object. 
        Defaults to 60 (C4). If pitch is a float *kkk.cc* then
        *kkk* is the midi key number and *cc* is cents above that midi
        key's equal tempered frequency. See `MidiFile.metatrack()`
        for more information.
    amplitude : int | float
        An amplitude 0.0 to 1.0, defaults to 0.5.
    instrument : value
        An instrument designation of some kind, defaults to 0. If you are
        generating midi then this value should be a channel integer 
        0 to 15, inclusive. 
    """
    def __init__(self, time=0.0, duration=1.0, pitch=60, amplitude=.5, instrument=0):
        super().__init__(time)
        self.duration = duration
        # # If the note contains more than one pitch the first is assigned to self._pitch
        # # and the others are cached in the _otherpitches attribute.
        # self._otherpitches = []
        # # self.pitch is a setter: if pitch is a list the first pitch will be assigned 
        # # to self._pitch and the remaining pitches are cached in _otherpitches
        self.pitch = pitch
        self.amplitude = amplitude
        self.instrument = instrument
        self._children = []

    @property
    def time(self):
        """
        The start time of the note in seconds, defaults to 0.0.  For ways
        to specify metric time, see: `rhythm()` and `intempo()`.

        Raises
        ------
        ValueError if the time value is not a number >= 0.
        """
        return self._time

    @time.setter
    def time(self, val):
        if isinstance(val, (int, float, Fraction)) and val >= 0:
            self._time = val
        else:
            raise ValueError(f"Invalid Note time: {val}.")

    @property
    def duration(self):
        """
        The duration of the note in seconds, defaults to 1.0. For ways
        to specify metric durations, see: `rhythm()` and `intempo()`.
 
        Raises
        ------
        ValueError if the duration value is not a number greater than 0.
        """
        return self._duration

    @duration.setter
    def duration(self, val):
        if isinstance(val, (int, float, Fraction)) and val > 0:
            self._duration = val
        else:
            raise ValueError(f"Invalid Note duration: {val}.")

    @property
    def pitch(self):
        """
        A `Pitch` object or an int or float key number, defaults to 60. If you output
        a note to midi, pitch will be automatically scaled to an int or float keynum.
 
        Raises
        ------
        ValueError if the pitch is not a Pitch or a number between 0 and 127 inclusive.
        """
        return self._pitch

    @pitch.setter
    def pitch(self, val):
        self._pitch = val
        # def checkpitch(p):
        #     if (isinstance(p, (int, float)) and (0 <= p <= 127)) or isinstance(p, Pitch):
        #         return p
        #     raise ValueError(f"Invalid Note pitch: {p}.")    
        # # if isinstance(val, list) and len(val)>0:
        # #     self._pitch = checkpitch(val[0])
        # #     for v in val[1:]:
        # #         self._otherpitches.append(checkpitch(v))
        # # else:
        #     self._pitch = checkpitch(val)

    @property
    def amplitude(self):
        """
        A value between 0.0 and 1.0 inclusive, defaults to 0.5. If you output
        a note to midi, amplitude will be automatically scaled to 0-127 inclusive.

        Raises
        ------
        ValueError if the amplitude value is not a number between 0 and 1 inclusive.
        """
        return self._amplitude

    @amplitude.setter
    def amplitude(self, val):
        if isinstance(val, (int, float)) and 0 <= 1.0:
            self._amplitude = val
        else:
            raise ValueError(f"Invalid Note amplitude: {val}.")

    @property
    def instrument(self):
        """
        A value designating the note's instrument, defalts to 0. For midi output
        the instrument must be a midi channel value 0 to 15 inclusive.
        """
        return self._instrument

    @instrument.setter
    def instrument(self, val):
        self._instrument = val

    @property
    def tag(self):
        """
        Either 'note', 'rest' or 'chord' depending the note's current state: if the note has
        any children the tag is 'chord', else if the pitch of the note is empty the tag is 'rest'
        else the tag is 'note'.
        """
        if self._children:
            return 'chord'
        if self.pitch.is_empty():
            return 'rest'
        return 'note'

    def add_child(self, note):
        """
        Adds a child note and tags this note as a chord.
        """
        if isinstance(note, Note):
            # Not sure if I want or need to do this...
            if self._children and self._children[0].time != note.time:
                raise ValueError(f'Conflicting note onset times in chord: {self._children[0].time} and {note.time}.')
            # if self._children and self._children[0].duration != note.duration:
            #     raise ValueError(f'Conflicting note durations in chord: {self._children[0].duration} and {note.duration}.')
            self._children.append(note)
        else:
            raise ValueError(f'Invalid child: {note}.')

    def is_rest(self):
        """
        Returns true if the note's pitch is empty, e.g. a Pitch().
        """
        return isinstance(self._pitch, Pitch) and self._pitch.is_empty()

    def is_chord(self):
        """
        Returns true if the note contains any children.
        """
        return len(self._children) > 0

    def chord(self):
        """Returns a list containing this note and any childen."""
        notes = [self]
        notes.extend(self._children)
        return notes

    def __iter__(self):
        """
        Iterates the children of this note.
        """
        return iter(self._children)

    def __len__(self):
        """
        Returns the number of children this note contains.
        """
        return len(self._children)

    def __str__(self):
        name = "Chord" if self.is_chord() else "Note"
        pstr = ":".join([str(c.pitch) for c in self.chord()]) if self.is_chord() else str(self.pitch)
        return f"<{name}: {self._time}, {self._duration}, {pstr}, {self._amplitude}, {self._instrument}>"

    # No special repr() method for now...
    __repr__ = __str__

    # def __repr__(self):
    #     if self.is_rest():
    #         return f"Note({repr(self.time)}, {repr(self.duration)}, Pitch())"
    #     # if self.is_chord():
    #     #     return f"Note({repr(self.time)}, {repr(self.duration)}, {repr(self.pitches())}, {repr(self._amplitude)}, {repr(self._instrument)})"
    #     return f"Note({repr(self._time)}, {repr(self._duration)}, {repr(self._pitch)}, {repr(self._amplitude)}, {repr(self._instrument)})"

    def _pitchtokey(self):
        if isinstance(self._pitch, Pitch):
            return self._pitch.keynum()
        return self._pitch


# class Chord(Event):
#     """
#     A class defining a musical chord. The onset time and duration of the chord
#     will be determined by the first note added to the chord, and all other notes
#     must agree with the time and duration of the first note.

#     Parameters
#     ----------
#     notes : A list of zero or more Notes, defaults to the empty list.
#     """
#     def __init__(self, notes=[]):
#         #super().__init__(time_)
#         if not isinstance(notes, list):
#             notes = [notes]
#         self._notes = []
#         for n in notes:
#             self.add_note(n)
#         self._voice = None

#     def __len__(self):
#         return len(self._notes)

#     def __iter__(self):
#         return iter(self._notes)

#     def __str__(self):
#         cstr = ":".join([str(n.pitch) for n in self.notes])
#         return f'<Chord: {str(self.time)} {str(self.duration)} {cstr}>'

#     def __repr__(self):
#         cstr = ", ".join([repr(n) for n in self.notes])
#         return f'Chord({cstr})'

#     @property
#     def time(self):
#         return self._notes[0].time if self._notes else None
    
#     @property
#     def duration(self):
#         return self._notes[0].duration if self._notes else None
    
#     @property
#     def notes(self):
#         return self._notes

#     def add_note(self, note):
#         """Appends a note to the chord."""
#         if isinstance(note, Note):
#             if self._notes and self._notes[0].time != note.time:
#                 raise ValueError(f'Conflicting note onset times in chord: {self._notes[0].time} and {note.time}.')
#             if self._notes and self._notes[0].duration != note.duration:
#                 raise ValueError(f'Conflicting note durations in chord: {self._notes[0].duration} and {note.duration}.')
#             self._notes.append(note)
#         else:
#             raise ValueError(f'Invalid chord note: {note}.')