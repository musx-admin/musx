"""
Defines a base Event class for musical events and a generic Note class to
represent time, duration, pitch, and amplitude. Notes are automatically
converted to whatever format is requred by a specific back end, e.g. midi
or csound.
"""

from .midi import midievent as me
from .midi import midimsg as mm
from .tools import quantize
from .pitch import Pitch

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
        if isinstance(val, (int, float)) and val >= 0:
            self._time = val
        else:
            raise ValueError(f"Invalid time value: {val}.")


class Note (Event):
    """
    Creates a Note instance from its arguments. A Note is a sound event
    that can be used in different contexts. For example, if a Note is
    passed to methods in the midi or csound modules the note data will
    be automatically converted to the format supported by the module.

    Parameters
    ----------
    time : int | float
        The onset time in seconds, defaults to 0.0.  For ways to specify
        time and duration metrically, see `rhythm()` and `intempo()`.
    duration : int | float
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
        self.pitch = pitch
        self.amplitude = amplitude
        self.instrument = instrument

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
        if isinstance(val, (int, float)) and val >= 0:
            self._time = val
        else:
            raise ValueError(f"Invalid time value: {val}.")

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
        if isinstance(val, (int, float)) and val > 0:
            self._duration = val
        else:
            raise ValueError(f"Invalid duration value: {val}.")

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
        if isinstance(val, Pitch) or (isinstance(val, (int, float)) and 0 <= val <= 127):
            self._pitch = val
        else:
            raise ValueError(f"Invalid pitch value: {val}.")

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
            raise ValueError(f"Invalid amplitude value: {val}.")

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

    def __repr__(self):
        return f'Note({self._time}, {self._duration}, {self._pitch}, {self._amplitude}, {self._instrument})'

    __str__ = __repr__

    def _pitchtokey(self):
        if isinstance(self._pitch, Pitch):
            return self._pitch.keynum()
        return self._pitch

