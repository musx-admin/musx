"""
A high-level midi class that automatically generates midi note on and off pairs from a
more general representation of time, duration, key number, and amplitude.   
"""

from .midi import midievent as me
from .midi import midimsg as mm
from math import modf
from .tools import quantize


class Note:

    def __init__(self, time=0.0, dur=1.0, key=60, amp=.5, chan=0, tuning=1, off=127):
        """
        Creates a MidiNote from its arguments.

        Parameters
        ----------
        time : int | float
            The start time of the midi message in seconds. Defaults to 0.0.
        dur : int | float
            The duration in seconds, defaults to 1.0.
        key : int | float 
            A key number 0 to 127, defaults to 60 (C4). This value can
            also be a floating point value kk.cc where kk is the midi
            key and cc is cents above the midi key's equal-tempered
            frequency. See the tuning parameter for more information.
        amp : int | float
            An amplitude 0.0 to 1.0, defaults to 0.5.
        chan : int
            A midi channel 0 to 15, defaults to 0.
        tuning : int
            A value 1 to 16 setting the divisions per semitone used for
            microtonal quantization of floating point keynums.  A value of
            1 (the default) means standard semitonal tuning, so no 
            microtones occur. A value of 2 claims successive pairs of 
            channels for quarter-tone tuning, and a value of 16 will use
            all 16 channels to quantize to 16 divisions per semitone 
            (6.25 cents), which is very close to the frequency limen.
            See Seq and the micro.py demo file for more information.
        off : int | float
            A note off velocity 0 to 127, defaults to 127.

        Raises 
        ------
        A ValueError if the tuning value is not a number between 1 and 16, inclusive.
        """
        self.time = time
        self.dur = dur
        self.key = key
        self.amp = amp
        self.chan = chan
        self.off = off

        if not (1 <= tuning <= 16):
            raise ValueError(f"not a valid microtuning value: {tuning}.")
        elif type(key) is float and key - int(key) > 0.0:
            self._microtune(tuning)

    @property
    def time(self):
        """
        The start time of the midi note in seconds. The default value is 0.0.

        Raises
        ------
        A ValueError if the time value is not a number >= 0.
        """
        return self._time

    @time.setter
    def time(self, val):
        if isinstance(val, (int, float)) and val >= 0:
            self._time = val
        else:
            raise ValueError(f"Invalid time value: {val}.")

    @property
    def dur(self):
        """
        The duration of the midi note in seconds. The default value is 1.0.
 
        Raises
        ------
        A ValueError if the duration value is not a number greater than 0.
        """
        return self._dur

    @dur.setter
    def dur(self, val):
        if isinstance(val, (int, float)) and val > 0:
            self._dur = val
        else:
            raise ValueError(f"Invalid duration value: {val}.")

    @property
    def key(self):
        """
        The midi key number of the midi note. The default value is 60.
 
        Raises
        ------
        A ValueError if the key number is not a number between 0 and 127 inclusive.
        """
        return self._key

    @key.setter
    def key(self, val):
        if isinstance(val, (int, float)) and 0 <= val <= 127:
            self._key = val
        else:
            raise ValueError(f"Invalid key number value: {val}.")

    @property
    def amp(self):
        """
        The amplitude of the midi note. The value can be a float between
        between 0 and 1.0, or a velocity value between 2 and 127 inclusive.
        Defaults to .5.

        Raises
        ------
        A ValueError if the amplitude value is a number less than 0 or greater than 127.
        """

        return self._amp

    @amp.setter
    def amp(self, val):
        if isinstance(val, (int, float)) and 0 <= val <= 127:
            self._amp = val if val <= 1 else (val / 127)
        else:
            raise ValueError(f"Invalid amplitude value: {val}.")

    @property
    def chan(self):
        """
        The midi channel 0-15 of the midi note. The default value is 0.
        
        Raises
        ------
        A ValueError if the channel is not a number between 0 and 15 inclusive.
        """
        return self._chan

    @chan.setter
    def chan(self, val):
        if isinstance(val, int) and 0 <= val < 16:
            self._chan = val
        else:
            raise ValueError(f"Invalid channel value: {val}.")

    @property
    def off(self):
        """
        The note off velocity. The default value is 127.
        
        Raises
        ------
        A ValueError if off is not a number between 0 and 127 inclusive.
        """
        return self._off

    @off.setter
    def off(self, val):
        if isinstance(val, int) and 0 <= val <= 127:
            self._off = val
        else:
            raise ValueError(f"Invalid note off velocity value: {val}.")

    def __str__(self):
        string = f'<Note: time={self.time}, dur={self._dur}, key={self._key}, amp={self._amp}, chan={self._chan}'
        if self._off != 127:
            string += f', off={self._off}'
        string += f" {id(self)}>"
        return string

    def __repr__(self):
        string = f'Note({self._time}, {self._dur}, {self._key}, {self._amp}, {self._chan}'
        if self._off != 127:
            string += f', off={self._off}'
        string += ')'
        return string

    def _microtune(self, div):
        """
        Quantizes a floating point key number to div number of divisions
        per semitone. 
        """
        micro = 1.0 / div   # microtonal increment
        raw = self._key     # existing keynum
        key = int(raw)      # int version
        rem = raw - key     # float's fractional portion is microtones
        col = 0             # the microtonal channel to shift to
        for i in range(0, div+1):  # iterate number of divisions plus 1.
            if micro*i <= rem < micro*(i + 1): # found rem in this bucket!
                col = i     # offset to microtuned channel in midi file.
                break
        self._key = key     # convert floating point keynum to int
        self._chan += col   # shift note to microtuned channel
  
    def noteon(self):
        """Returns a note on MidiEvent for the note."""
        return me.MidiEvent([mm.kNoteOn | (self._chan & 0xf),
                             int(self._key), int(self._amp * 127)], self._time)

    def noteoff(self):
        """Returns a note off MidiEvent for the note."""
        return me.MidiEvent([mm.kNoteOff | (self._chan & 0xf),
                             int(self._key), self._off], self._time + self._dur)

if __name__ == '__main__':
    # from musx.midi.midinote import mtest
    # mtest()
    def mtest(raw, div):
        micro = 1.0 / div
        key = int(raw)
        rem = raw - key
        col=0
        # find the bucket that rem is in, this will be the channel increment.
        for i in range(0, div+1):
            if micro*i <= rem < micro*(i + 1):
                col = i
                break
        print([micro*d for d in range(div)]+[micro*div]) 
        print("raw=", raw, "div=", div, "micro", micro, "key=", key, "rem=", rem, "col=", col)
