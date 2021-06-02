###############################################################################
"""
The midievent module provides object oriented support for working with midi
messages. To represent basic midi on and off data you should use a `Note` 
object because it provides a more flexible represention that will automatically
convert to on and off messages when written to files and ports.
"""


from . import midimsg as mm
from . import gm
from ..note import Event


class MidiEvent (Event):
    """
    A class that wraps lists of midi message bytes so they can be treated 
    as time stamped objects. Unless you know what you are doing you should
    probably not call this constructor directly and use the class message
    constructors to create defined below.

    Parameters
    ----------
    message : list
        The list of message byte values. The constructor does not check these values!
    time : number
        The time to give the midi message. The units for this are application-specific.
    """

    def __init__(self, message, time=0.0):

        super().__init__(time)
        self.message = message
        # self.time = time

    def __str__(self):
        """The print() string shows the raw data."""
        return self.tostring()

    def __repr__(self):
        """The string the console prints shows the external form."""
        return self.toextern()

    @staticmethod
    def _check_range(val, a, b=None):
        """
        Raises a TypeError if val not in range(a,b), or range(0,a) if 
        b is not provided.
        """
        if b is None:
            b, a = a, 0
        if not a <= val < b:
            raise ValueError(f"midi value {val} not in range({a},{b}).")
        return val

    @staticmethod
    def _check_int_range(val, a, b=None):
        """Raises an assertion if val is not an int or not in range(a,b)."""
        if not isinstance(val, int):
            raise TypeError(f"value {val} is not an int.")
        return MidiEvent._check_range(val, a, b)

    @staticmethod
    def _rescale(value, oldmin, oldmax, newmin, newmax):
        """Rescales value to new linear range."""
        return (((newmax - newmin) / (oldmax - oldmin)) * (value - oldmin)) + newmin

    def status(self):
        """Returns the status byte of a MidiEvent."""
        return mm.status(self.message)

    def channel(self):
        """
        Returns the channel of a midi channel event or -1
        if the message is not a channel event.
        """
        if mm.is_channel_message(self.message):
            return mm.channel(self.message)
        return -1

    @classmethod
    def note_off(cls, channel, keynum, velocity, time=0.0):
        """
        Creates a midi note off event.

        Parameters
        ----------
        channel : 0-15
            The channel number of the midi event.
        keynum : byte
            A midi key number 0 to 127.
        velocity : byte
            A velocity value 0 to 127.
        time : number
            The time to give the midi message. The units for this are application-specific.

        Raises
        ------
        * A TypeError if a value is not an integer.
        * A ValueError if the value is out of range.
        """
        channel = cls._check_int_range(channel, 16)
        keynum = cls._check_int_range(keynum, 128)
        velocity = cls._check_int_range(velocity, 128)
        return cls(mm.note_off(channel, keynum, velocity), time)


    def is_note_off(self):
        """Returns true if the event is a note off."""
        return self.status() == mm.kNoteOff

    @classmethod
    def note_on(cls, channel, keynum, velocity, time=0.0):
        """
        Creates a midi note on event.

        Parameters
        ----------
        channel : 0-15
            The channel number of the midi event.
        keynum : byte
            A midi key number 0 to 127.
        velocity : byte
            A velocity value 0 to 127.
        time : number
            The time to give the midi message. The units for this are application-specific.

        Raises
        ------
        * A TypeError if a value is not an integer.
        * A ValueError if the value is out of range.
        """
        channel = cls._check_int_range(channel, 16)
        keynum = cls._check_int_range(keynum, 128)
        velocity = cls._check_int_range(velocity, 128)
        return cls(mm.note_on(channel, keynum, velocity), time)

    def is_note_on(self):
        """Returns true if the message is a note on."""
        return self.status() == mm.kNoteOn

    def is_note_on_or_off(self):
        """Returns true if the message is a note on or off."""
        return mm.kNoteOff <= self.status() <= mm.kNoteOn

    def keynum(self):
        """
        Returns a key number value 0 to 127, or -1 if the
        event is not a note on, off, or aftertouch.
        """
        if self.status() in [mm.kNoteOff, mm.kNoteOn, mm.kAftertouch]:
            return mm.keynum(self.message)
        return -1

    def velocity(self):
        """
        Returns a velocity value 0 to 127, or -1 if the message is not
        a note on or off.
        """
        if self.is_note_on_or_off():
            return mm.velocity(self.message)
        return -1

    @classmethod
    def aftertouch(cls, chan, keynum, press, time=0.0):
        """
        Creates a midi aftertouch event.

        Parameters
        ----------
        chan : 0-15
            The channel number of the midi event.
        keynum : byte
            A midi key number 0 to 127.
        press : byte
            A pressure value 0 to 127.
        time : number
            The time to give the midi message. The units for this are application-specific.

        Raises
        ------
        * A TypeError if a value is not an integer.
        * A ValueError if the value is out of range.
        """
        chan = cls._check_int_range(chan, 16)
        keynum = cls._check_int_range(keynum, 128)
        press = cls._check_int_range(press, 128)
        return cls(mm.aftertouch(chan, keynum, press), time)

    def is_aftertouch(self):
        """Returns true if the midi event is an an aftertouch."""
        return self.status() == mm.kAftertouch

    def touch(self):
        """
        Return a pressure value 0 127, or -1 if the event is not an aftertouch.
        """
        if self.is_aftertouch():
            return mm.touch(self.message)
        return -1

    @classmethod
    def control_change(cls, chan, ctrl, val, time=0.0):
        """
        Creates a control change event.

        Parameters
        ----------
        chan : 0-15
            The channel number of the midi event.
        ctrl : byte
            A controller number 0 to 127.
        val : byte
            A controller value 0 to 127.
        time : number
            The time to give the midi message. The units for this are application-specific.

        Raises
        ------
        * A TypeError if a value is not an integer.
        * A ValueError if the value is out of range.
        """
        chan = cls._check_int_range(chan, 16)
        ctrl = cls._check_int_range(ctrl, 128)
        val = cls._check_int_range(val, 128)
        return cls(mm.control_change(chan, ctrl, val), time)

    def is_control_change(self):
        """Returns true if the message is a control change event."""
        return self.status() == mm.kCtrlChange

    def controller(self):
        """
        Returns a controller value 0 to 127, or -1 if the event
        is not a control change.
        """
        if self.is_control_change():
            return mm.controller(self.message)
        return -1

    def is_controller_of_type(self, contype):
        """
        Returns true if the event is a control change message and
        its controller is the specified type.
        """
        return self.is_control_change() and self.controller() == contype

    def control(self):
        """
        Returns a control value 0 127, or -1 if the event is
        not a control change.
        """
        if self.is_control_change():
            return mm.control(self.message)
        return -1

    @classmethod
    def program_change(cls, chan, prog, time=0.0):
        """
        Creates a midi program change event.

        Parameters
        ----------
        chan : 0-15
            The channel number of the midi event.
        prog : byte
            A midi program number 0 to 127.
        time : number
            The time to give the midi message. The units for this are application-specific.

        Raises
        ------
        * A TypeError if a value is not an integer.
        * A ValueError if the value is out of range.
        """
        chan = cls._check_int_range(chan, 16)
        prog = cls._check_int_range(prog, 128)
        return cls(mm.program_change(chan, prog), time)

    def is_program_change(self):
        """Returns true if the event is a program change."""
        return self.status() == mm.kProgChange

    def program(self):
        """
        Returns a progam change value 0 127, or -1 if the event is
        not a program change.
        """
        if self.status() == mm.kProgChange:
            return mm.program(self.message)
        return -1

    @classmethod
    def channel_pressure(cls, chan, press, time=0.0):
        """
        Creates a midi channel pressure event.

        Parameters
        ----------
        chan : 0-15
            The channel number of the midi event.
        press : byte
            A midi pressure number 0 to 127.
        time : number
            The time to give the midi message. The units for this are application-specific.

        Raises
        ------
        * A TypeError if a value is not an integer.
        * A ValueError if the value is out of range.
        """
        chan = cls._check_int_range(chan, 16)
        press = cls._check_int_range(press, 128)
        return cls(mm.channel_pressure(chan, press), time)

    def is_channel_pressure(self):
        """Returns true if the event is a channel pressure."""
        return self.status() == mm.kChanPress

    def pressure(self):
        """
        Returns a pressure value 0 127, or -1 if the event is not
        a channel pressure.
        """
        if self.is_channel_pressure():
            return mm.pressure(self.message)
        return -1

    @classmethod
    def pitch_bend(cls, chan, bend, time=0.0):
        """
        Creates a pitch bend event.

        Parameters
        ----------
        chan : int
            The channel number, 0 to 15.
        bend : int
            A pitch bend value, 0 to 16383. See: bendvalue().
        time  : int | float
            A score time to give the midi message. The units for this are
            application-specific.
        """
        chan = cls._check_int_range(chan, 16)
        bend = cls._check_int_range(bend, 16384)  # 14 bit value 0-16383
        return cls(mm.pitch_bend(chan, bend), time)

    def is_pitch_bend(self):
        """Returns true if the event is a pitch bend."""
        return self.status() == mm.kPitchBend

    def bend(self):
        """
        Returns a bend value 0 to 16383 or -1 if the event is not a pitch bend.
        """
        if self.status() == mm.kPitchBend:
            return mm.bend(self.message)
        return -1

    @staticmethod
    def bend_value(semibend, semirange):
        """
        Converts a pitchbend value in semitones into a midi pitch bend value.

        Parameters
        --------
        semibend : number
            The bend value expressed in floating point semitones.
        semirange : float 
            A device dependant maximum pitch bend range expressed in floating point semitones.        
        """
        return int(MidiEvent._rescale(semibend, -semirange, semirange, 0, 16383))

    @classmethod
    def all_notes_off(cls, chan, time=0.0):
        """
        Creates a midi all notes off event.

        Parameters
        ----------
        chan : 0-15
            The channel number of the midi event.
        time : number
            The time to give the midi message. The units for this are application-specific.

        Raises
        ------
        * A TypeError if a value is not an integer.
        * A ValueError if the value is out of range.
        """
        chan = cls._check_int_range(chan, 16)
        return cls(mm.control_change(chan, 123, 0), time)

    @classmethod
    def all_sound_off(cls, chan, time=0.0):
        """
        Creates a midi all sound off event.

        Parameters
        ----------
        chan : 0-15
            The channel number of the midi event.
        time : number
            The time to give the midi message. The units for this are application-specific.

        Raises
        ------
        * A TypeError if a value is not an integer.
        * A ValueError if the value is out of range.
        """
        chan = cls._check_int_range(chan, 16)
        return cls(mm.control_change(chan, 120, 0), time)

    ## Creates a midi all controllers off message.
    #  @param chan  a channel number, 0 to 15.
    #  @param time  a time to give the midi message. The units
    #  for this are application-specific.
    @classmethod
    def all_controllers_off(cls, chan, time=0.0):
        """
        Creates a midi note off event.

        Parameters
        ----------
        channel : 0-15
            The channel number of the midi event.
        keynum : byte
            A midi key number 0 to 127.
        velocity : byte
            A velocity value 0 to 127.
        time : number
            The time to give the midi message. The units for this are application-specific.

        Raises
        ------
        * A TypeError if a value is not an integer.
        * A ValueError if the value is out of range.
        """
        chan = cls._check_int_range(chan, 16)
        return cls(mm.control_change(chan, 121, 0), time)


    # Midi Meta Messages. These are only valid in midi files.


    def is_meta(self, typ=None):
        """
        Returns true if the event is a meta event.

        If typ is not specifed the function returns true if the event is any
        type of meta message, otherwise the event must be the specied type between
        kDevName and kSeqEvent.

        Parameters
        ----------
        typ : metatype | None
            The midi meta message type or None.
        """
        meta = self.status() == mm.kMetaMsg and len(self.message) >= 3
        if not meta or typ is None:
            return meta
        return self.message[1] == typ

    @classmethod
    def meta_seq_number(cls, num, time=0.0):
        """
        Creates a midi sequence number meta event.

        Parameters
        ----------
        num : int
            A sequence number max 2 bytes.
        time : number
            The time to give the midi message. The units for this are application-specific.

        Raises
        ------
        * A TypeError if a value is not an integer.
        * A ValueError if the value is out of range.
        """
        if isinstance(num, int) and num >= 0:
            return cls(mm.meta_seq_number(num), time)
        raise ValueError(f"invalid sequence number: '{num}'.")

    @classmethod
    def _textmeta(cls, mtype, text, time=0.0):
        if isinstance(mtype, int) and mm.kText <= mtype <= mm.kDevName:
            if isinstance(text, str) and len(text) > 0:
                return cls(mm.text_meta_message(mtype, text), time)
            else:
                raise TypeError(f"text value '{text}' is not a string.")
        else:
            raise TypeError(f"value '{text}' is not valid midi meta type.")

    @classmethod
    def meta_text(cls, text, time=0.0):
        """
        Creates a midi text meta event.

        Parameters
        ----------
        text : string
            The text string for the message.
        time : number
            The time to give the midi message. The units for this are application-specific.

        Raises
        ------
        * A TypeError if the value is not a string.
        """
        return cls._textmeta(mm.kText, text, time)

    @classmethod
    def meta_copyright(cls, text, time=0.0):
        """
        Creates a midi copyright meta event.

        Parameters
        ----------
        text : string
            The text string for the message.
        time : number
            The time to give the midi message. The units for this are application-specific.

        Raises
        ------
        * A TypeError if the value is not a string.
        """
        return cls._textmeta(mm.kCopyRight, text, time)

    @classmethod
    def meta_track_name(cls, text, time=0.0):
        """
        Creates a midi track name meta event.

        Parameters
        ----------
        text : string
            The text string for the message.
        time : number
            The time to give the midi message. The units for this are application-specific.

        Raises
        ------
        * A TypeError if the value is not a string.
        """
        return cls._textmeta(mm.kTrackName, text, time)

    @classmethod
    def meta_instrument_name(cls, text, time=0.0):
        """
        Creates a midi instrument name meta event.

        Parameters
        ----------
        text : string
            The text string for the message.
        time : number
            The time to give the midi message. The units for this are application-specific.

        Raises
        ------
        * A TypeError if the value is not a string.
        """
        return cls._textmeta(mm.kInstName, text, time)

    @classmethod
    def meta_lyric(cls, text, time=0.0):
        """
        Creates a midi lyric meta event.

        Parameters
        ----------
        text : string
            The text string for the message.
        time : number
            The time to give the midi message. The units for this are application-specific.

        Raises
        ------
        * A TypeError if the value is not a string.
        """
        return cls._textmeta(mm.kLyric, text, time)

    @classmethod
    def meta_marker(cls, text, time=0.0):
        """
        Creates a midi marker meta event.

        Parameters
        ----------
        text : string
            The text string for the message.
        time : number
            The time to give the midi message. The units for this are application-specific.

        Raises
        ------
        * A TypeError if the value is not a string.
        """
        return cls._textmeta(mm.kMarker, text, time)

    @classmethod
    def meta_cue_point(cls, text, time=0.0):
        """
        Creates a midi cue point meta event.

        Parameters
        ----------
        text : string
            The text string for the message.
        time : number
            The time to give the midi message. The units for this are application-specific.

        Raises
        ------
        * A TypeError if the value is not a string.
        """
        return cls._textmeta(mm.kCuePoint, text, time)

    @classmethod
    def meta_program_name(cls, text, time=0.0):
        """
        Creates a midi program name meta event.

        Parameters
        ----------
        text : string
            The text string for the message.
        time : number
            The time to give the midi message. The units for this are application-specific.

        Raises
        ------
        * A TypeError if the value is not a string.
        """
        return cls._textmeta(mm.kProgName, text, time)

    @classmethod
    def meta_device_name(cls, text, time=0.0):
        """
        Creates a midi device name meta event.

        Parameters
        ----------
        text : string
            The text string for the message.
        time : number
            The time to give the midi message. The units for this are application-specific.

        Raises
        ------
        * A TypeError if the value is not a string.
        """
        return cls._textmeta(mm.kDevName, text, time)


    def text(self):
        """
        Returns the text string from a meta text event or
        an empty string if the event is not a text event.
        """
        if self.is_meta():
            if mm.kText <= self.message[1] <= mm.kDevName:
                return mm.text(self.message)
        return ''

    @classmethod
    def meta_channel_prefix(cls, chan, time=0.0):
        """
        Creates a midi channel prefix meta event.

        Parameters
        ----------
        chan : 0-15
            A midi channel number 0 to 15.
        time : number
            The time to give the midi message. The units for this are application-specific.

        Raises
        ------
        * A TypeError if a value is not an integer.
        * A ValueError if the value is out of range.
        """
        chan = cls._check_int_range(chan, 16)
        return cls(mm.meta_chan_prefix(chan), time)

    @classmethod
    def meta_midi_port(cls, port, time=0.0):
        """
        Creates a midi port meta event.

        Note: **This meta event is depreciated in the midi spec.**

        Parameters
        ----------
        port : byte
            A midi port number 0 to 127.
        time : number
            The time to give the midi message. The units for this are application-specific.

        Raises
        ------
        * A TypeError if a value is not an integer.
        * A ValueError if the value is out of range.
        """
        port = cls._check_int_range(port, 127)
        return cls(mm.meta_port(port), time)

    @classmethod
    def meta_eot(cls, time=0.0):
        """
        Creates a midi end-of-track meta event.

        Parameters
        ----------
        time : number
            The time to give the midi message. The units for this are application-specific.

        Raises
        ------
        * A TypeError if a value is not an integer.
        * A ValueError if the value is out of range.
        """
        return cls(mm.meta_eot(), time)

    @classmethod
    def meta_tempo(cls, quarter, time=0.0):
        """
        Creates a midi tempo meta event.

        Parameters
        ----------
        tempo : int
            The rate of a quarter note expressed as either a 
            metronome value (208 or less) or microseconds 
            (e.g. tempo 120 is 500000).
        time : float | int
            A time to give the midi message. The units for this are 
            application-specific.
        """
        if isinstance(quarter, int) and quarter > 0:
            if quarter <= 208:
                quarter = int((60 / quarter) * 1000000)
            return cls(mm.meta_tempo(quarter), time)
        raise ValueError(f"invalid tempo value: '{quarter}'.")

    def tempo(self, units='usec'):
        """
        Returns the tempo from a meta tempo event or 0 if the event is not a 
        tempo event.

        Parameters
        ----------
        units : 'usec' | 'bpm'
            A string indicating if the tempo should returned as microseconds or beats per minute.
        """
        if self.is_meta(mm.kTempo):
            if units == 'usec':
                return mm.tempo(self.message)
            elif units == 'bpm':
                return int(60 * (1000000 / mm.tempo(self.message)))
        return 0

    # HKT FIXME: 4 4 yields  
    # 1 0.0 [255, 88, 4, 2, 24, 8]	# time signature: 2/16777216
    # should be
    # 1 0.0 [255, 88, 4, 4, 2, 1, 96]	# time signature: 4/4
    @classmethod
    def meta_time_signature(cls, top, bot, clocks=24, tsecs=8, time=0.0):
        """
        Creates a midi time signature meta event.

        Parameters
        ----------
        top : byte
            The top number of the time signature.
        bot : byte
            The power of 2 of the bottom number: 0 is top/1, 2 is top/4, etc.
        clocks : byte
            The number of MIDI clocks between metronome clicks.
        tsecs : byte
            the number of 32nds in a quarter note (usually 8).

        Raises
        ------
        * A TypeError if a value is not an integer.
        * A ValueError if the value is out of range.
        """
        for x in [top, bot, clocks, tsecs]:
            if not isinstance(x, int):
                raise ValueError(f"parameter value {x} not an integer. ")
        pow2 = [1, 2, 4, 8, 16, 32, 64, 128]
        if bot not in pow2:
            raise ValueError(f"denominator value {x} not a power of 2. ")
        # timesig stores bot as exponent of 2, which is the same as the
        # index of bot in list :) examp: bot of 8 is 2^3 so 3 is stored.
        bot = pow2.index(bot)
        return cls(mm.meta_time_sig(top, bot, clocks, tsecs), time)

    @classmethod
    def meta_key_signature(cls, sf, mode, time=0.0):
        """
        Creates a midi key signature meta event.

        Parameters
        ----------
        sf :  -7 to 7 
            The number of flats (negative) or sharps.
        mode : 0 or 1
            Specify 0 for a major key and 1 for minor.
        time : number
            The time to give the midi message. The units for this are application-specific.

        Raises
        ------
        * A TypeError if a value is not an integer.
        * A ValueError if the value is out of range.
        """
        sf = cls._check_int_range(sf, -7, 8)
        num = cls._check_int_range(sf, 0, 2)
        return cls(mm.meta_key_sig(sf, num), time)

    @classmethod
    def meta_seq_event(cls, data, time=0.0):
        """
        Creates a midi sequence meta event.

        Parameters
        ----------
        data : list
            A list of data bytes to send to the sequencer.
        time : number
            The time to give the midi message. The units for this are application-specific.

        Raises
        ------
        * A TypeError if a value is not an integer.
        * A ValueError if the value is out of range.
        """
        for b in data:
            if b < 0 or b > 0xFF:
                raise ValueError(f"Invalid data byte: {b} is > 0xFF")
        return cls(mm.meta_seq_event(data), time)


    # System Common Messages. These are not valid in midi files.


    @classmethod
    def sysex(cls, data, time=0.0):
        """
        Creates a midi sysex event from the specified list of data
        adding a terminal EOE byte if necessary.

        Parameters
        ----------
        data : list
            A list of data bytes to send to the sequencer.
        time : number
            The time to give the midi message. The units for this are application-specific.

        Raises
        ------
        * A TypeError if a value is not an integer.
        * A ValueError if the value is out of range.
        """
        for d in data:
            cls._check_int_range(d, 127)
        return cls(mm.sysex(data), time)

    def is_sysex(self):
        """Returns true if the message is a sysex event."""
        return self.status() == mm.kSysEx

    def sysex_data(self):
        """
        Returns the data list of the sysex event (without the EOE byte) or
        an empty list if it is not a sysex event.
        """
        if self.status() == mm.kSysEx:
            return self.message[1::-1]
        return []

    @classmethod
    def time_code(cls, typ, val, time=0.0):
        """
        Creates a midi time code event.

        Parameters
        ----------
        typ : 0-15
            The time code type.
        val : byte
            The type code value.
        time : number
            The time to give the midi message. The units for this are application-specific.

        Raises
        ------
        * A TypeError if a value is not an integer.
        * A ValueError if the value is out of range.
        """
        typ = cls._check_int_range(typ, 8)
        val = cls._check_int_range(val, 16)
        return cls(mm.midi_time_code(typ, val), time)

    @classmethod
    def song_position(cls, pos, time=0.0):
        """
        Creates a midi song position event.

        Parameters
        ----------
        pos : int
            A 14 bit song pointer position.
        time : number
            The time to give the midi message. The units for this are application-specific.

        Raises
        ------
        * A TypeError if a value is not an integer.
        * A ValueError if the value is out of range.
        """
        pos = cls._check_int_range(pos, 1 << 14)
        return cls(mm.midi_song_position(pos), time)

    @classmethod
    def song_select(cls, song, time=0.0):
        """
        Creates a midi song select event.

        Parameters
        ----------
        song : byte
            The song number to set.
        time : number
            The time to give the midi message. The units for this are application-specific.

        Raises
        ------
        * A TypeError if a value is not an integer.
        * A ValueError if the value is out of range.
        """
        song = cls._check_int_range(song, 128)
        return cls(mm.midi_song_select(song), time)

    @classmethod
    def tune_request(cls, time=0.0):
        """
        Creates a midi tune request event.

        Parameters
        ----------
        time : number
            The time to give the midi message. The units for this are application-specific.

        Raises
        ------
        * A TypeError if a value is not an integer.
        * A ValueError if the value is out of range.
        """
        return cls(mm.midi_tune_request(), time)


    # System Realtime Messages. These are not valid in midi files.


    @classmethod
    def midi_clock(cls, time=0.0):
        """
        Creates a midi clock message.
        
        Parameters
        ----------
        time : number
            The time to give the midi message. The units for this are application-specific.
        """
        return cls(mm.midi_clock(), time)

    def is_midi_clock(self):
        """Returns true if the event is a midi clock event."""
        return self.status() == mm.kTimingClock

    @classmethod
    def midi_start(cls, time=0.0):
        """
        Creates a midi start message.

        Parameters
        ----------
        time : number
            The time to give the midi message. The units for this are application-specific.
        """
        return cls(mm.midi_start(), time)

    def is_midi_start(self):
        """Returns true if the event is a midi start event."""
        return self.status() == mm.kStart

    @classmethod
    def midi_continue(cls, time=0.0):
        """
        Creates a midi continue event.

        Parameters
        ----------
        time : number
            The time to give the midi message. The units for this are application-specific.
        """
        return cls(mm.midi_continue(), time)

    def is_midi_continue(self):
        """Returns true if the event is a midi continue event."""
        return self.status() == mm.kContinue

    @classmethod
    def midi_stop(cls, time=0.0):
        """
        Creates a midi stop event.

        Parameters
        ----------
        time : number
            The time to give the midi message. The units for this are application-specific.
        """
        return cls(mm.midi_stop(), time)

    def is_midi_stop(self):
        """Returns true if the event is a midi stop event."""
        return self.status() == mm.kStop

    @classmethod
    def active_sensing(cls, time=0.0):
        """
        Creates a midi active sensing event.

        Parameters
        ----------
        time : number
            The time to give the midi message. The units for this are application-specific.
        """
        return cls(mm.active_sensing(), time)

    def is_active_sensing(self):
        """Returns true if the event is a midi active sensing event."""
        return self.status() == mm.kActiveSens

    @classmethod
    def midi_reset(cls, time=0.0):
        """
        Creates a midi reset event.

        Parameters
        ----------
        time : number
            The time to give the midi message. The units for this are application-specific.
        """
        return cls(mm.midi_reset(), time)

    def is_midi_reset(self):
        """Returns true if the event is a midi reset event."""
        return self.status() == mm.kReset

    # Support code.

    def tostring(self, hint=False):
        text = f"{self.message}"
        if hint:
            text += " # " + self.hint()
        return text

    def hint(self):
        stat = self.status()
        if stat < mm.kSysEx:  # channel message
            text = self._print_table[stat][0][1] + ": "
            if stat == mm.kCtrlChange:
                text += (gm.controller_names[self.message[1]] + " ")
            elif stat == mm.kProgChange:
                text += (gm.instrument_names[self.message[1]] + " ")
            text += "chan " + str(self.channel())
        elif stat == mm.kMetaMsg:  # meta or reset
            if len(self.message) > 1:  # is a meta message
                stat = self.message[1]  # status now meta type
                text = MidiEvent._print_table[stat][0][1] + ": "
                if mm.kText <= stat <= mm.kDevName:
                    msg = self.text()
                    if len(msg) > 16:
                        msg = msg[:16] + "..."
                    text += msg
                elif stat == mm.kTempo:
                    text += str(self.tempo('bpm')) + ' bpm'
                elif stat == mm.kTimeSig:
                    text += str(self.message[3]) + "/" + str(2**self.message[4])
                elif stat == mm.kKeySig:
                    # the key is stored as a twos-complement value -7...7
                    # key = int.from_bytes(bytes([self.message[3]]), 'big', signed=True)
                    k = self.message[3]
                    key = k if k < 128 else (256 - k) * (-1)
                    text += MidiEvent._key_table[key+7] + ["-major", "-minor"][self.message[4]]
            else:
                text = MidiEvent._print_table[stat][0][1]
        else:  # system common or realtime
            text = MidiEvent._print_table[stat][0][1]
        return text

    def toextern(self):
        stat = self.status()
        if stat == mm.kReset:  # NB: midi makes kReset status same as kMetaMsg
            if self.is_meta():
                stat = self.message[1]
        e = MidiEvent._print_table[stat]
        s = e[0][0] + "("
        for i in range(1, len(e)):
            if i > 1: s += ", "
            x = e[i][1](self)
            s += "\'" + x + "\'" if isinstance(x, str) else str(x)
        s += ")"
        return s

    _key_table = ['Cb', 'Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F', 'C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#']
    _print_table = {
        # Channel Events
        mm.kNoteOff: [["note_off", "note off"], ["chan", channel], ["key", keynum], ["vel", velocity]],
        mm.kNoteOn: [["note_on", "note on"], ["chan", channel], ["key", keynum], ["vel", velocity]],
        mm.kAftertouch: [["aftertouch", "after touch"], ["chan", channel], ["touch", touch]],
        mm.kCtrlChange: [["control_change", "controller"], ["chan", channel], ["controller", controller], ["control", control]],
        mm.kProgChange: [["program_change", "program"], ["chan", channel], ["program", program]],
        mm.kChanPress: [["channel_pressure", "channel pressure"], ["chan", channel], ["pressure", pressure]],
        mm.kPitchBend: [["pitch_bend", "pitch bend"], ["chan", channel], ["bend", bend]],
        # Meta Events
        mm.kSeqNumber: [["meta_seq_number", "sequence number"], ["num", lambda e: mm.meta_seq_number(e.message)]],
        mm.kText: [["meta_text", "text"], ["text", text]],
        mm.kCopyRight: [["meta_copyright", "copyright"], ["text", text]],
        mm.kTrackName: [["meta_track_name", "track name"], ["text", text]],
        mm.kInstName: [["meta_instrument_name", "instrument name"], ["text", text]],
        mm.kLyric: [["meta_lyric", "lyric"], ["text", text]],
        mm.kMarker: [["meta_marker", "marker"], ["text", text]],
        mm.kCuePoint: [["meta_cue_point", "cue point"], ["text", text]],
        mm.kProgName: [["meta_program_name", "program name"], ["text", text]],
        mm.kDevName: [["meta_device_name", "device name"], ["text", text]],
        mm.kChanPrefix: [["meta_channel_prefix", "channel prefix"], ["chan", lambda ev: ev.message[3]]],
        mm.kMidiPort: [["meta_midi_port", "midi port"], ["port", lambda ev: ev.message[3]]],
        mm.kEOT: [["meta_eot", "end of track"]],
        mm.kTempo: [["meta_tempo", "tempo"], ["usecs", tempo]],
        mm.kSMPTEOff: [["smptemeta", "SMPTE"]],
        mm.kTimeSig: [["meta_time_signature", "time signature"]],
        mm.kKeySig: [["meta_key_signature", "key signature"]],
        mm.kSeqEvent: [["meta_seq_event", "sequencer data"]],
        # System Common Messages
        mm.kSysEx: [["sysex", "system exclusive"]],
        mm.kTimeCode: [["time_code", "time code"]],
        mm.kSongPos: [["song_position", "song position"]],
        mm.kSongSel: [["song_select", "song select"]],
        mm.kTuneReq: [["tune_request", "tune request"]],
        # System Real Time
        mm.kTimingClock: [["midi_clock", "midi clock"]],
        mm.kStart: [["midi_start", "midi start"]],
        mm.kContinue: [["midi_continue", "midi continue"]],
        mm.kStop: [["midi_stop", "midi stop"]],
        mm.kActiveSens: [["active_sensing", "active sensing"]],
        mm.kReset: [["midi_reset", "midi reset"]],
    }





"""
from midi import MidiEvent, MidiSeq, MidiFile
MidiEvent.chanprefixmeta(12)
MidiEvent.textmeta(midi.mm.kText, "hello rick!")
MidiEvent.chanprefixmeta(12)
"""

"""
from midi import MidiEvent, MidiSeq
m = MidiEvent.noteon(11,60,100)
m.tostring()
MidiEvent.chanprefixmeta(12)
MidiEvent.noteon(0,60, 90)

from ..seq import Seq
from midi import MidiEvent, MidiFile
m = MidiFile()
m.read_file("/Users/taube/Classes/205/Resources/reich.mid")
m.track(0)

for e in m.track(0): print(e, True)
"""

if __name__ == '__main__':
    def test():
        args = [6, 60, 127, 1.0]
        ev = MidiEvent.note_off(*args)
        assert ev.is_note_off(), "isnoteoff() failed."
        vals = [ev.channel(), ev.keynum(), ev.velocity(), ev.time]
        assert args == vals, f"args {args} not same as vals {vals}."
        ev.is_note_on_or_off(), f"isnoteonoroff() failed."
        print("notoff ok.")

        args = [6, 60, 127, 1.0]
        ev = MidiEvent.note_on(*args)
        assert ev.is_note_on(), "isnoteon() failed."
        vals = [ev.channel(), ev.keynum(), ev.velocity(), ev.time]
        assert args == vals, f"args {args} not same as vals {vals}."
        ev.is_note_on_or_off(), f"isnoteonoroff() failed"
        print("noteon ok.")

        args = [6, 60, 100, 100.0]
        ev = MidiEvent.aftertouch(*args)
        assert ev.is_aftertouch(), "isnoteon() failed."
        vals = [ev.channel(), ev.keynum(), ev.touch(), ev.time]
        assert args == vals, f"args {args} not same as vals {vals}."
        print("aftertouch ok.")

        args = [6, 60, 100, 100.0]
        ev = MidiEvent.control_change(*args)
        assert ev.is_control_change(), "iscontrolchange() failed."
        vals = [ev.channel(), ev.controller(), ev.control(), ev.time]
        assert args == vals, f"args {args} not same as vals {vals}."
        assert ev.is_controller_of_type(args[1]), f"controller not of type {args[1]}."
        print("controlchange ok.")

        args = [11, 44, 1.0]
        ev = MidiEvent.program_change(*args)
        ev.is_program_change()
        vals = [ev.channel(), ev. program(), ev.time]
        assert args == vals, f"args {args} not same as vals {vals}."
        print("programchange ok.")

        args = [15, 55, 0.0]
        ev = MidiEvent.channel_pressure(*args)
        ev.is_channel_pressure()
        vals = [ev.channel(), ev.pressure(), ev.time]
        assert args == vals, f"args {args} not same as vals {vals}."
        print("channelpressure ok.")

        args = [15, 55, 0.0]
        ev = MidiEvent.pitch_bend(*args)
        ev.is_pitch_bend()
        vals = [ev.channel(), ev.bend(), ev.time]
        assert args == vals, f"args {args} not same as vals {vals}."
        print("pitchbend ok.")

        args = [11, 300.0]
        ev = MidiEvent.all_notes_off(*args)
        assert ev.is_controller_of_type(123), f"controller not of type {123}."
        vals = [ev.channel(), ev.time]
        assert args == vals, f"args {args} not same as vals {vals}."
        print("allnotesoff ok.")

        args = [11, 300.0]
        ev = MidiEvent.all_sound_off(*args)
        assert ev.is_controller_of_type(120), f"controller not type {120}."
        vals = [ev.channel(),  ev.time]
        assert args == vals, f"args {args} not same as vals {vals}."
        print("allsoundoff ok.")

        args = [11, 300.0]
        ev = MidiEvent.all_controllers_off(*args)
        assert ev.is_controller_of_type(121), f"controller not type {121}."
        vals = [ev.channel(), ev.time]
        assert args == vals, f"args {args} not same as vals {vals}."
        print("allcontrollersoff ok.")

        args = [mm.kCopyRight, "Illiacsoftware, Inc"]
        ev = MidiEvent.meta_copyright(args[1])
        assert ev.is_meta(args[0]), f"meta message not of type {args[0]}."
        assert ev.text() == args[1], f"text {ev.text()} is not {args[1]}."
        print("meta Copyright ok.")
