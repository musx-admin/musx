"""
Defines a base Event class for musical events and a generic Note subclass to
represent time, duration, pitch, and amplitude. Notes can also represent chords`
and rests according to their attribute values. A note's attribute values are 
automatically converted to whatever format is required by a specific backend.
"""

from fractions import Fraction
from copy import copy, deepcopy
from .midi import midievent as me
from .midi import midimsg as mm
from .tools import quantize
from .pitch import Pitch

class Event:
    """
    A base class for defining musical events. Any subclass of Event can
    be added to a `musx.seq.Seq` object.

    Parameters
    ----------
    time : int | float
        The onset time in seconds, defaults to 0.0.  For ways to specify
        time and duration metrically, see `musx.rhythm.rhythm()` and
        `musx.rhythm.intempo()`.
    """
    def __init__(self, time):
        self.time = time

    @property
    def time(self):
        """
        The start time of the event in seconds, defaults to 0.0.  For ways
        to specify time metrically, see `musx.rhythm.rhythm()` and
        `musx.rhythm.intempo()`.
        """
        return self._time

    @time.setter
    def time(self, val):
        if isinstance(val, (int, float, Fraction)) and val >= 0:
            self._time = val
        else:
            raise ValueError(f"Invalid Note time: {val}.")

    def __str__(self):
        return f'<Event: {self.time} {hex(id(self))}>)'
    
    def __repr__(self):
        return f'Event({self.time})'


class Note (Event):
    """
    Creates a Note instance from its arguments. A Note is a generic sound
    event that can be used in different contexts. For example, if a Note
    is passed to methods in the MIDI or Csound backends the note data is
    automatically converted to the format supported by that module.

    In addition to single tones, Notes can have children, in which case 
    it is auto-tagged as a chord; if a Note contains an empty pitch 
    it is tagged as a rest. See Note.tag

    Parameters
    ----------
    time : int | float | Fraction
        The onset time in seconds, defaults to 0.0.  For ways to specify
        time and duration metrically, see `rhythm()` and `intempo()`.
    duration : int | float | Fraction
        The duration in seconds, defaults to 1.0. For ways to specify
        duration and time metrically, see `rhythm()` and `intempo()`.
    pitch : int | float | Pitch | list
        An int or float key number 0 to 127, or a `Pitch` object, or list
        of the same. Defaults to 60 (C4). If pitch is a float *kkk.cc* then
        *kkk* is the midi key number and *cc* is cents above that midi
        key's equal tempered frequency. If the pitch is an empty Pitch the
        note is tagged as a rest. If a list of pitches is provided the
        note will contain the first Pitch and the remaining pitches will
        be converted to child Notes, each child containing the same
        attribute values as the parent notw except for pitch.
    amplitude : int | float
        An amplitude 0.0 to 1.0, defaults to 0.5.
    instrument : value
        An instrument designation of some kind, defaults to 0. If you are
        generating midi then this value should be a channel integer 
        0 to 15, inclusive. 
    """
    def __init__(self, time=0.0, duration=1.0, pitch=60, amplitude=.5, instrument=0):
        # WARNING: if you add new attributes be sure to update copy() and
        # copy_at_tempo() as needed.
        super().__init__(time)
        self.duration = duration
        self.amplitude = amplitude
        self.instrument = instrument
        self._children = []
        self._mxml = {}
        self.pitch = pitch

    @property
    def time(self):
        """
        The start time of the note in seconds, defaults to 0.0.  For ways
        to specify metric time, see: `rhythm()` and `intempo()`.
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
        A `musx.pitch.Pitch` object or an int or float key number, or list of
        the same. Defaults to 60 (Middle C). If the pitch is assigned a list 
        of pitches, the note will keep the first pitch and the other pitches
        will be assigned to child notes of this note, which will then be 
        tagged as a chord.
        """
        return self._pitch

    @pitch.setter
    def pitch(self, val):
        def checkpitch(p):
            if (isinstance(p, (int, float)) and (0 <= p <= 127)) or isinstance(p, Pitch):
                return p
            raise ValueError(f"Invalid Note pitch: {p}.")    
        if isinstance(val, list) and len(val)>0:
            self._pitch = checkpitch(val[0])
            for p in val[1:]:
                self.add_child(Note(time=self.time, duration=self.duration, pitch=p,
                    amplitude=self.amplitude, instrument=self.instrument))
        else:
            self._pitch = checkpitch(val)

    @property
    def amplitude(self):
        """
        A value between 0.0 and 1.0 inclusive, defaults to 0.5. If you output
        a note to midi, amplitude will be automatically scaled to 0-127 inclusive.
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
        The value of tag is either 'note', 'rest' or 'chord' depending the
        note's current state: if the note has any children the tag is 'chord',
        else if the pitch of the note is empty the tag is 'rest' otherwise the
        tag is 'note'.
        """
        if self._children:
            return 'chord'
        if isinstance(self.pitch, Pitch) and self.pitch.is_empty():
            return 'rest'
        return 'note'

    def add_child(self, note):
        """
        Adds note as a child of this note and tags itself as a chord.
        """
        if isinstance(note, Note):
            # Not sure if I want to do this...
            if self._children and self._children[0].time != note.time:
                raise ValueError(f'Conflicting note onset times in chord: {self._children[0].time} and {note.time}.')
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
        Returns true if the note contains children.
        """
        return len(self._children) > 0

    def chord(self):
        """
        Returns a list containing this note and any childen.
        """
        notes = [self]
        notes.extend(self._children)
        return notes

    def get_mxml(self, key, default=None):
        """
        Returns the mxml value of the given key, or the default value if
        the key is not in the note's mxml dictionary.
        """
        return self._mxml.get(key, default)

    def set_mxml(self, key, value):
        """
        Assigns the mxml key and value to the note.
        """
        self._mxml[key] = value

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

    def _tagged_pitch_str(self):
        """
        Returns a tag-specific pitch string: if the Note's tag is 'note' then the pitch name is
        returned, if the tag is 'chord' then pitch names delimited by ":" are returned and if
        the tag is 'rest' the string 'R' is returned.
        """
        return ":".join([str(c.pitch) for c in self.chord()]) if self.is_chord() else str(self.pitch)

    def __str__(self):
        name = "Note" #"Chord" if self.is_chord() else "Note"
        pstr = self._tagged_pitch_str()
        mxml = ", ".join(f"{str(k)}={v}" for k,v in self._mxml.items())
        if mxml:
            mxml = " "+mxml
        return f"<{name}: {self._time}, {self._duration}, {pstr}, {self._amplitude}, {self._instrument}{mxml}>"

    # No special repr() method for now...
    __repr__ = __str__

    def _pitchtokey(self):
        if isinstance(self._pitch, Pitch):
            return self._pitch.keynum()
        return self._pitch

    # def __deepcopy__(self, memo):
    #     cls = self.__class__
    #     result = cls.__new__(cls)
    #     memo[id(self)] = result
    #     for k, v in self.__dict__.items():
    #         setattr(result, k, deepcopy(v, memo))
    #     return result

    def copy(self):
        # ARRRG! Tried __deepcopy__ but gave up for now...
        """
        Returns a deep copy of this Note and all its children.
        """
        cpy = Note() 
        cpy._time = self._time
        cpy._duration = self._duration
        cpy._amplitude = self._amplitude
        cpy._pitch = self._pitch
        cpy._instrument = self._instrument
        cpy._children = [c.copy() for c in self._children]
        cpy._mxml = self._mxml.copy()
        return cpy

    def copy_at_tempo(self, tempo_scalar):
        """
        Returns a copy of this note with its time and duration adjusted by
        tempo_scaler, a metronome value per quarter: 60.0 / (1/4 * tempo)
        """
        cpy = Note() 
        cpy._time = self._time * tempo_scalar
        cpy._duration = self._duration * tempo_scalar
        cpy._amplitude = self._amplitude
        cpy._pitch = self._pitch
        cpy._instrument = self._instrument
        cpy._children = [c.copy_at_tempo(tempo_scalar) for c in self._children]
        cpy._mxml = self._mxml.copy()     
        return cpy
        