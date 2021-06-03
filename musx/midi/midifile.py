################################################################################
"""
The midifile module provide support for reading and writing midi files.
"""


import os.path
from . import midimsg as mm
from . import midievent as me
from .gm import AcousticGrandPiano
from ..seq import Seq
from ..note import Note
from ..tools import rescale


class MidiFile:
    """
    A class for reading and writing midi files.

    A MidiFile is an iterable so its tracks can be iterated, sliced and 
    mapped.

    Parameters
    ----------
    path : string
        The pathname to the midi file on disk.
    tracks : list
        A list of one or more tracks, each track is a Seq.
    divs : int
        The midi file's ticks-per-quarter setting, defaults to 480.
    """

    level = 0
    """The MIDI level of the file, either 0, 1, or 2."""

    divisions = 0
    """The number of ticks per quarter note."""

    tracks = []
    """
    The tracks of the MidiFile. Each track is a Seq. Your first track
    (track 0 in the file) should start with a tempo message otherwise
    the data will be performed using the musx default tempo mm=60.
    """

    pathname = ""
    """The pathname of the MidiFile."""

    _running_status = 0

    def __init__(self, path, tracks=[], divs=480):

        if not isinstance(path, str) or len(path) == 0:
            raise TypeError(f"'{path}' is not a valid pathname string.")
        if not isinstance(tracks, list):
            tracks = [tracks]
        else:
            tracks = tracks.copy() # always copy user's list
        if any(not isinstance(t, Seq) for t in tracks):
            raise TypeError(f"{tracks} is not a valid list of midi tracks.")
        if not isinstance(divs, int) and divs > 0:
            raise ValueError(f"{divs} is not a valid divisions-per-quarter.")
        self.tracks = tracks
        self.divisions = divs
        self.pathname = path

    def clear(self):
        """Removes all the data from the MidiFile."""
        self.level = 0
        self.divisions = 0
        self.tracks = []
        self._running_status = 0
        self.pathname = ""

    @staticmethod
    def fileversion(pathname):
        """
        A static function that returns a version of pathname guaranteed to not
        reference an existing file. Use this function to ensure that you will
        not overwrite a previous version of the MidiFile already on disk.

        Parameters
        ----------
        pathname : string
            The pathname of the file to version.

        Returns
        -------
        A pathname string guaranteed to not overwrite an existing file on disk.

        Example
        -------
        In this example, the file "foo.mid" would go through the following 
        versioning until a version was found that did not reference an existing file:
        "foo.mid", "foo1.mid", "foo2.mid" ...
        ```py
        MidiFile(fileversion("/path/to/foo.mid"))
        ```
        """
        def nextversion(p):
            name, extn = os.path.splitext(p)
            vers = 1
            yield name + extn
            while True:
                yield f"{name}{vers}{extn}"
                vers += 1
        # check versions until not found.
        for f in nextversion(pathname):
            if not os.path.isfile(f):
                return f

    def read(self, secs=True):
        """
        Reads the file in MidiFile.pathname and collects the track data
        as a list of Seqs. Any existing tracks in the MidiFile will be
        cleared before reading.
        
        Parameters
        ----------
        time : 'secs' | 'ticks' | 'raw'
            The format to import midi time values as. 'secs' is seconds,
            'ticks' is time expressed in midi ticks, and 'raw' are the
            raw delta values that precede each event in the file. The
            default value is 'secs'.

        Returns
        -------
        The MidiFile.
        """
        pathname = self.pathname
        with open(pathname, "rb") as stream:
            self.clear()
            self.pathname = pathname # restore the pathname after clearing!
            length = self._read_chunk_length(stream, b'MThd')
            assert length == 6, "MThd chunk length 6 not found."
            self.level = self._bytes_to_int(stream.read(2))
            tracks = self._bytes_to_int(stream.read(2))
            # read divisions as a two byte signed quantity. if its positive
            # then it represents ticks per quarter. if its negative then its
            # smpte format where the upper byte contains -24, -25 or -30,
            # and the lower byte is positive subframes. Example: millisecond
            # smpte timing would be 0xE728 = -25 40 = 25*40 = 1000ms
            # see http://midi.teragonaudio.com/tech/midifile/mthd.htm
            self.divisions = self._bytes_to_int(stream.read(2), True)
            if self.divisions < 0:
                raise NotImplementedError("Cowardly refusing to import SMPTE format midi file.")
#            print("level=", level, "tracks=", tracks, "divisions=", divisions)
            # process all the tracks in the file
            for _ in range(tracks):
                self._read_track(stream, secs)
        return self

    def write(self, secs=True):
        """
        Writes the MidiFile's track data to the file in MidiFile.pathname.
        
        Parameters
        ----------
        secs : bool
            If true the MidiEvents in the track data contain time in seconds
            andthis is converted to midi ticks. Otherwise the tracks should 
            contain tick data.

        Returns
        -------
        The MidiFile.
        """
        trnum = len(self.tracks)
        if trnum == 0:
            raise ValueError("no tracks to write.")
        level = 0 if trnum == 1 else 1
        divs = self.divisions
        pathname = self.pathname # self.fileversion(pathname)
        with open(pathname, "wb") as stream:
            self._write_chunk_length(stream, b'MThd', 6)
            stream.write(self._int_to_bytes(level, 2))
            stream.write(self._int_to_bytes(trnum, 2))
            stream.write(self._int_to_bytes(divs, 2))
            force_tempo = False
            # if the first event in the first track is not a
            # tempo event then force tempo==60.
            if not isinstance(self.tracks[0][0], me.MidiEvent) or not self.tracks[0][0].is_meta(mm.kTempo):
                force_tempo = True
            microdivs = 0
            if hasattr(self.tracks[0], "metatrack"):
                microdivs = self.tracks[0].microdivs 
            # write the tracks
            for t in self.tracks:
                self._write_track(stream, t, divs, microdivs, force_tempo)
                force_tempo = False

            self.format = level
            self.divisions = divs
        return self

    def addtrack(self, seq):
        """
        Appends a Seq to the midi file's track list.
        
        Parameters
        ----------
        seq : Seq
            The Seq to append to the current tracks in the MidiFile.
        """
        self.tracks.append(seq)

    def print(self, tracks=True, hints=True):
        """
        Prints the track contents of the MidiFile.

        Parameters
        ----------
        tracks : bool | int | list
            Specifies which tracks to print. If tracks is True
            then all tracks are printed, if tracks is an integer
            then that track number is printed, otherwise tracks
            is a list of integers and only those tracks
            are printed. Track numbers are 0 based, and track
            0 is often a "meta track" of a midi file.
        hints : bool
            If true then hints are printed in the printed listing,
            otherwise they are not. 

        Returns
        -------
        The MidiFile.
        """
        for i, t in enumerate(self.tracks):
            if tracks is True or t is i or i in tracks:
                t.print()

    @classmethod
    def metatrack(cls, tempo=60, timesig=[4,4], keysig=[0,0], ins={}, microdivs=1):
        """
        Returns a sequence containing a series of midi meta events that 
        define the contents for a midi file's track 0, including its tempo,
        time signature, key signature, instrument assignments (program changes)
        and micro tuning setup using channel tuning. This meta data can then
        be assigned as track 0 in a level 1 midifile, or the initial contents
        of a level 0 midi file.

        Parameters
        ----------
        tempo : int
            The quarter-note metronome tempo of midi notes in the file.
            Note that musx's tempo defaults to 60 bmp not 120 bpm.
        timesig : [num, den]
            A list of two integers indicating the numerator and denominator
            of a midi time signature, with den being a power of 2.
        keysig : [sharpflats, mode]
            A list of two integers indicating a key signature and mode. 
            sharpflats is an integer -7 to 7  where negative numbers are
            flats keys, 0 is C and 1 to 7 are sharp keys. The mode 
            value should be 0 for major and 1 for minor.
        ins : {chan: instrument, ...}
            A dictionary of upto 16 channel numbers 0 to 15 and their
            general midi program asignment. See musx.midi.gm for the 
            list of midi instument constants.
        microdivs : int 1 to 16
            Specifies microtonal divisions per semitone (semitone/microdivs).
            The default value is 1, so semitone/1 = semitone and no microtonal
            output will occur. If microdivs is 2 then semitone/2 = 50 cent
            quantization, e.g. quartertone tuning. musx uses channel tuning
            to procuce microtones. This means that when microdivs is 2 musx
            will claim successive pairs of channels for quarter-tone tuning
            so the channels available for different instuments is 0, 2, 4,
            6, 8, 10, 12, and 14.
            The maxmimum number of microdivs is 16, or 6.25 cents, which is very 
            close to the frequency limen. This will claim all 16 channels in 
            order to produce microtone so the only channel available for
            instrument assignment is channel 0. For more information see the 
            micro.py demo file.
        """
        tempo = me.MidiEvent.meta_tempo(tempo)
        if not len(timesig) == 2 and all(isinstance(n, int) for n in timesig):
            raise TypeError(f"invalid timesig: {timesig}.")
        timesig = me.MidiEvent.meta_time_signature(timesig[0], timesig[1])
        insts = {i: AcousticGrandPiano for i in range(16)}
        for c,p in ins.items():
            if not isinstance(c, int) and 0 <= c <= 15:
                raise TypeError("invalid midi channel: {c}.")
            if not isinstance(p, int) and 0 <= p <= 127:
                raise TypeError("invalid gm instrument: {p}.")
            insts[c] = p
        if not len(keysig) == 2 and all(isinstance(n, int) for n in keysig):
            raise ValueError(f"invalid timesig: {keysig}.")
        keysig = me.MidiEvent.meta_key_signature(keysig[0], keysig[1])
        meta = [tempo, timesig, keysig]
        meta += [me.MidiEvent.program_change(c,p) for c,p in insts.items()]
        if not (1 <= microdivs <= 16):
            raise ValueError(f"invalid microtuning value: {microdivs}.")
        if microdivs > 1:
            values = cls._channel_tuning(microdivs)
            for c,v in enumerate(values):
                # calculate the pitch bend value
                b = round(rescale(v, -2,  2,  0, 16383))
                meta.append(me.MidiEvent.pitch_bend(c, b))
        metaseq = Seq()
        metaseq.events = meta
        # mark this seq as being a midi meta track and add the microdivs value
        metaseq.metatrack = True
        metaseq.microdivs = microdivs if microdivs > 1 else 0
        return metaseq

    def __str__(self):
        return f"<MidiFile: '{self.pathname}' {hex(id(self))}>"

    __repr__ = __str__

    def __iter__(self):
        """Impelements the iterator protocol."""
        return iter(self.tracks)

    def __getitem__(self, index):
        """Impelements the iterator protocol."""
        return self.tracks[index]  # index can be slice

    def __len__(self):
        """Impelements the iterator protocol."""
        return len(self.tracks)

    @staticmethod
    def _int_to_bytes(val, num):
        """Converts integer value into the specified number of bytes."""
        return val.to_bytes(num, 'big')

    @staticmethod
    def _bytes_to_int(bytez, sign=False):
        """Returns integer value of bytes."""
        return int.from_bytes(bytez, 'big', signed=sign)

    def _read_chunk_length(self, stream, ident):
        assert stream.read(4) == ident, f"Chunk {ident} not found."
        return self._bytes_to_int(stream.read(4))

    def _write_chunk_length(self, stream, ident, length):
        stream.write(ident)
        stream.write(self._int_to_bytes(length, 4))

    def _read_varlen_value(self, stream):
        """Reads a variable length quantity and returns its integer value."""
        value = self._bytes_to_int(stream.read(1))
        if value & 0x80:   # value's top bit is 1 so keep reading
            value &= 0x7F  # its actual value is the lower 7 bits
            while True:
                value <<= 7  # left shift to make room for next byte
                other = self._bytes_to_int(stream.read(1))
                value += other & 0x7F
                if not other & 0x80:  # done if upper bit is not 1
                    break
        return value

    @staticmethod
    def _write_varlen_value(stream, val):
        """Writes integer value as variable length quantity."""
        vlq = []
        for i in range(21, 0, -7):
            if val >= (1 << i):
                vlq.append(((val >> i) & 0x7F) | 0x80)
        vlq.append(val & 0x7F)
        #print("val=", val, "vlq=", vlq)
        #stream.write(bytes(vlq))
        for b in vlq:
            stream.write(MidiFile._int_to_bytes(b, 1))

    def _read_meta_message(self, stream):
        metatype = self._bytes_to_int(stream.read(1))
        length = self._read_varlen_value(stream)
        if mm.kText <= metatype <= mm.kDevName:
            return [0xFF, metatype, length, stream.read(length)]
        if metatype in [mm.kChanPrefix, mm.kMidiPort, mm.kTempo,
                        mm.kSMPTEOff, mm.kTimeSig, mm.kKeySig,
                        mm.kSeqNumber]:
            msg = [0xFF, metatype, length]
            for n in stream.read(length):
                msg.append(n)
            return msg
        if metatype == mm.kEOT:
            return [0xFF, metatype, length]
        if metatype == mm.kSeqEvent:
            return [0xFF, metatype, length, stream.read(length)]
        raise NotImplementedError(f"_read_meta_message: unhandled metatype {hex(metatype)}.")

    def _read_channel_message(self, stream, status):
        stat = status & 0xF0
        if mm.kNoteOff <= stat < mm.kProgChange or stat > mm.kChanPress:
            # two data bytes: note off, note on, aftertouch, controller, and pitchbend
            val1 = self._bytes_to_int(stream.read(1))
            val2 = self._bytes_to_int(stream.read(1))
            return [status, val1, val2]
        else:
            # one data byte:  program change, channel pressure
            val1 = self._bytes_to_int(stream.read(1))
            return [status, val1]

    def _read_sysex_message(self, stream, status):
        # Note: the length includes the terminal EOE
        length = self._read_varlen_value(stream)
        return [status, length, stream.read(length)]

    def _read_message(self, stream):
        # [:1] because peek can return more than one byte
        status = self._bytes_to_int(stream.peek(1)[:1])
        if status & 0x80:
            # have a channel message
            if status < mm.kSysEx:
                self._running_status = status
            stream.read(1)
        else:
            status = self._running_status
            assert status & 0x80, "status byte not found."

        if status < mm.kSysEx:  # a channel message
            return self._read_channel_message(stream, status)
        elif status == mm.kSysEx or status <= mm.kEOE:  # a sysex message
            self._running_status = 0
            return self._read_sysex_message(stream, status)
        elif status == mm.kMetaMsg:  # a meta message
            self._running_status = 0
            return self._read_meta_message(stream)
        else:
            raise NotImplementedError(f"channel status {hex(status)} unsupported.")

    @staticmethod
    def _write_message(stream, message):
        status = message[0]
        if status < mm.kSysEx:
            #print("writing", message)
            for b in message:
                stream.write(MidiFile._int_to_bytes(b, 1))
            #stream.write(bytes(message))
        elif status == mm.kMetaMsg:
            stream.write(MidiFile._int_to_bytes(status, 1))
            meta = message[1]
            stream.write(MidiFile._int_to_bytes(meta, 1))
            if mm.kText <= meta <= mm.kDevName or meta == mm.kSeqEvent:
                MidiFile._write_varlen_value(stream, message[2])
                stream.write(message[3])  # a bytes struct
            else:
                for b in message[2:]:
                    stream.write(MidiFile._int_to_bytes(b, 1))
                # stream.write(bytes(message[2:]))
        elif status == mm.kSysEx or status == mm.kEOE:
            stream.write(status)
            MidiFile._write_varlen_value(stream, message[1])
            stream.write(message[2])  # a bytes struct
        else:
            raise NotImplementedError(f"Unsupported message: {message}.")

    def _read_track(self, stream, tosecs):
        abs_delta = 0
        # read the length of the track. since this is not dependable we
        # ignore it and use the required EOT message to stop the track.
        self._read_chunk_length(stream, b'MTrk')
        self._running_status = 0
        trk = []
        while True:
            delta = self._read_varlen_value(stream)
            abs_delta += delta
            msg = self._read_message(stream)
            # print(delta, msg)
            # break on EOT, which is required by the midifile spec.
            if mm.is_meta_message_type(msg, mm.kEOT):  # mm.is_meta_eot(msg):
                break
            time = abs_delta / self.divisions if tosecs else abs_delta
            trk.append(me.MidiEvent(msg, time))
        # add the track as a sequence in the midi file
        self.tracks.append(Seq(trk))

    def _write_track(self, stream, track, divs, microdivs, force_tempo=False):
        ##print("write_track------------------------------")
        #track.print()
        self._write_chunk_length(stream, b'MTrk', 0)
        # save the begin position of this track.
        track_beg = stream.tell()
        # the previous time, used to calculate delta times between events.
        prev_time = 0
        # If force_tempo is True then this is the first track
        # and the user did not provide a tempo marking. In
        # this case write an initial tempo message for mm=60
        if force_tempo:
            MidiFile._write_varlen_value(stream, 0)
            MidiFile._write_message(stream, mm.meta_tempo(1000000))
        # pending queue of note offs, used if the track contains Note objects.
        off_queue = []
        # write out all the events in the track
        ##foo = 0
        for ev in track:
            ##print(foo,"\t", ev); foo += 1
            # write out any pending offs <= ev.time
            prev_time = MidiFile._write_offs(stream, off_queue, ev.time, prev_time, divs)
            # if we encounter a Note object, enqueue a note off and write a note on immediately.
            if isinstance(ev, Note):
                chan = ev.instrument
                key = ev._pitchtokey()
                vel = int(ev.amplitude * 127)
                if isinstance(key, float):
                    if not key.is_integer() and microdivs > 1:
                        chan, key = MidiFile._microtune(chan, key, microdivs)
                    else:
                        key = int(key)
                noteon  = me.MidiEvent([mm.kNoteOn | chan, key, vel], ev.time)
                noteoff = me.MidiEvent([mm.kNoteOff | chan, key, 127], ev.time+ev.duration)
                MidiFile._enqueue_off(noteoff, off_queue)
                ev = noteon
            #print("ev.message", ev.message)
            delta = int((ev.time - prev_time) * divs)
            MidiFile._write_varlen_value(stream, delta)
            MidiFile._write_message(stream, ev.message)
            prev_time = ev.time
        # flush any remaining note offs.
        MidiFile._write_offs(stream, off_queue, prev_time, prev_time, divs, True)   
        # add a 0 delta and EOT
        MidiFile._write_varlen_value(stream, 0)
        MidiFile._write_message(stream, mm.meta_eot())
        # calculate the length of the track we just wrote
        track_end = stream.tell()
        track_len = track_end - track_beg
        # go to track header's 4-byte length field and write the length
        stream.seek(track_beg - 4)
        stream.write(self._int_to_bytes(track_len, 4))
        # reposition back here to write the next track
        stream.seek(track_end)

    @staticmethod
    def _enqueue_off(off, queue):
        """Adds a note off to the note off queue at the latest possible position."""
        i = 0; l = len(queue)
        while i < l and queue[i].time <= off.time:
            i += 1
        queue.insert(i, off)

    @staticmethod
    def _write_offs(stream, queue, time, prev, divs, all=False):
        """Writes offs <= current time, returns updated previous time."""
        while (queue and (all or (queue[0].time <= time))):
            MidiFile._write_varlen_value(stream, int((queue[0].time - prev) * divs))
            MidiFile._write_message(stream, queue[0].message)
            prev = queue.pop(0).time
        return prev 

    @staticmethod
    def _microtune(channel, floatkey, microdivs):
        """
        Quantizes a floating point key number to div number of divisions
        per semitone. 
        """
        microincr = 1.0 / microdivs        # microtonal increment
        keynumber = int(floatkey)          # int version
        remainder = floatkey - keynumber   # float's fractional portion is microtones
        microchan = 0                      # the microtonal channel to shift to
        for i in range(0, microdivs +1 ):  # iterate number of divisions plus 1.
            if microincr * i <= remainder < microincr * (i + 1): # found rem in this bucket!
                microchan = i              # offset to microtuned channel in midi file.
                break
        channel += microchan               # shift note to microtuned channel
        return channel, keynumber

    @staticmethod
    def _channel_tuning(microdivs):
        """
        Internal function that converts the microdivs value 
        (the number of divisions per semitone) into a 
        sequence of cent values above the standard midi
        key number and then repeatedly assigns the sequence
        across all 16 midi channels.

        Example: if microdivs is 2, then the semitone is divided
        into two 50 cent steps [0, .5], this pattern is then
        repeated eight times over the sixteen midi channels
        [0, .5, 0, .5, ... 0, .5] yielding eight pairs of channels
        at indexes 0, 2, 4, ... 14 tuned for quarter tones.

        Parameters
        ----------
        microdivs : int 
            The number of divisions per semitone, 1 is semitone,
            2 is quarter tone, etc.

        Returns
        -------
        A sequence of microdivs adjustments for all 16 channels.
        """
        microdivs = max(1, min(16, microdivs))
        cents = [0.0]
        for i in range(1, microdivs):
            cents.append(1.0 * i/microdivs)
        # return a row of 16 repeating cent values
        return [cents[i % len(cents)] for i in range(16)]
    
