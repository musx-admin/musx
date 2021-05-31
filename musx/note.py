"""
A high-level event class that automatically generates midi note on and off pairs from a
more general representation of time, duration, pitch, and amplitude.   
"""

from .midi import midievent as me
from .midi import midimsg as mm
from .tools import quantize
from .pitch import Pitch

class Event:
    """
    A base class for defining musical events.

    Parameters
    ----------
    time : int | float
        The onset time in seconds, defaults to 0.0.  For ways to specify
        time and duration metrically, see: `rhythm()` and `intempo()`.
    """
      
    def __init__(self, time):
        self.time = time

    @property
    def time(self):
        """
        The start time of the note in seconds, defaults to 0.0.  For ways
        to specify time metrically, see: `rhythm()` and `intempo()`.

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

    def __init__(self, time=0.0, duration=1.0, pitch=60, amplitude=.5, instrument=0, microdivs=1):
        """
        Creates Note from its arguments.

        Parameters
        ----------
        time : int | float
            The onset time in seconds, defaults to 0.0.  For ways to specify
            time and duration metrically, see: `rhythm()` and `intempo()`.
        duration : int | float
            The duration in seconds, defaults to 1.0. For ways to specify
            duration and time metrically, see: `rhythm()` and `intempo()`.
        pitch : int | float | Pitch
            An int or float key number 0 to 127, or a Pitch object. 
            Defaults to 60 (C4). If pitch is a float kkk.cc then
            kkk is the midi key number and cc is cents above that midi
            key's equal tempered frequency. See microdivs for more information.
        amplitude : int | float
            An amplitude 0.0 to 1.0, defaults to 0.5.
        instrument : value
            An instrument designation of some kind. If you are generating midi
            events then the value should be a channel integer 0 to 15, inclusive.
        microdivs : int
            Specifies the microtonal divisions per semitone when pitch is a floating
            point key number. The default value is 1, so semitone/1 = semitone. 
            A value of 2 means semitone/2 = 50 cents, e.g quartertone tuning. 
            When used with midi output and `Seq.metaseq()`, this triggers channel
            tuning, where microdivs of 2 claims successive pairs of channels for 
            quarter-tone tuning, and a value of 16 will use all 16 channels to 
            quantize to 16 divisions per semitone, or 6.25 cents, which is very 
            close to the frequency limen. For more information see: `Seq.metaseq()`
            and the micro.py demo file.

        Raises 
        ------
        ValueError if the microdivs value is not a number between 1 and 16, inclusive.
        """
        #self.time = time
        super().__init__(time)
        self.duration = duration
        self.pitch = pitch
        self.amplitude = amplitude
        self.instrument = instrument

        if not (1 <= microdivs <= 16):
            raise ValueError(f"not a valid microtuning value: {microdivs}.")
        elif type(pitch) is float and pitch - int(pitch) > 0.0:
            self._microtune(microdivs)

    @property
    def time(self):
        """
        The start time of the note in seconds, defaults to 0.0.  For ways
        to specify time metrically, see: `rhythm()` and `intempo()`.

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
        to specify time metrically, see: `rhythm()` and `intempo()`.
 
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
        A Pitch object or an int or float key number, defaults to 60.
 
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
        A value between 0.0 and 1.0 inclusive, defaults to 0.5.

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

    def _microtune(self, div):
        """
        Quantizes a floating point key number to div number of divisions
        per semitone. 
        """
        micro = 1.0 / div   # microtonal increment
        raw = self._pitchtokey()     # existing keynum
        key = int(raw)      # int version
        rem = raw - key     # float's fractional portion is microtones
        col = 0             # the microtonal channel to shift to
        for i in range(0, div+1):  # iterate number of divisions plus 1.
            if micro*i <= rem < micro*(i + 1): # found rem in this bucket!
                col = i     # offset to microtuned channel in midi file.
                break
        self._pitch = key     # convert floating point keynum to int
        self._instrument += col   # shift note to microtuned instrumentnel
  
    def noteon(self):
        """Returns a note on MidiEvent for the note."""
        return me.MidiEvent([mm.kNoteOn | (self._instrument & 0xf),
                             int(self._pitchtokey()), int(self._amplitude * 127)], self._time)

    def noteoff(self):
        """Returns a note off MidiEvent for the note."""
        return me.MidiEvent([mm.kNoteOff | (self._instrument & 0xf),
                             int(self._pitchtokey()), 127], self._time + self._duration)

# if __name__ == '__main__':
#     # from musx.midi.midinote import mtest
#     # mtest()
#     def mtest(raw, div):
#         micro = 1.0 / div
#         key = int(raw)
#         rem = raw - key
#         col=0
#         # find the bucket that rem is in, this will be the channel increment.
#         for i in range(0, div+1):
#             if micro*i <= rem < micro*(i + 1):
#                 col = i
#                 break
#         print([micro*d for d in range(div)]+[micro*div]) 
#         print("raw=", raw, "div=", div, "micro", micro, "key=", key, "rem=", rem, "col=", col)
