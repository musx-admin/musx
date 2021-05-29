################################################################################
"""
The midifile module provide support for reading and writing midi files.
"""


import os.path
from . import midimsg as mm
from . import midievent as me
from ..seq import Seq


class MidiFile:

    level = 0
    """The MIDI level of the file, either 0, 1, or 2."""

    divisions = 0
    """The number of ticks per quarter note."""

    tracks = []
    """
    The tracks of the MidiFile. Each track is a Seq. Your first track
    should start with a tempo message otherwise the file will be performed
    at the midi default tempo of mm=120.
    """

    pathname = ""
    """The pathname of the MidiFile."""

    _running_status = 0

    def __init__(self, path, tracks=[], divs=480):
        """
        A class for reading and writing midi files.

        A MidiFile is an iterable so its tracks can be iterated, sliced and 
        mapped, e.g. `for tr in midifile: print(tr)`.

        Parameters
        ----------
        path : string
            The pathname to the midi file on disk.
        tracks : list
            A list of one or more tracks, each track is a Seq.
        divs : int
            The midi file's ticks-per-quarter setting, defaults to 480.
        """
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
        MidiFile(fileversion("/path/to/foo.mid"))`
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

    ## Converts integer value into the specified number of bytes.
    @staticmethod
    def int_to_bytes(val, num):
        return val.to_bytes(num, 'big')

    ## Returns integer value of bytes.
    @staticmethod
    def bytes_to_int(bytez, sign=False):
        return int.from_bytes(bytez, 'big', signed=sign)

    def read_chunk_length(self, stream, ident):
        assert stream.read(4) == ident, f"Chunk {ident} not found."
        return self.bytes_to_int(stream.read(4))

    def write_chunk_length(self, stream, ident, length):
        stream.write(ident)
        stream.write(self.int_to_bytes(length, 4))

    ## Reads a variable length quantity and returns its integer value.
    def read_varlen_value(self, stream):
        value = self.bytes_to_int(stream.read(1))
        if value & 0x80:   # value's top bit is 1 so keep reading
            value &= 0x7F  # its actual value is the lower 7 bits
            while True:
                value <<= 7  # left shift to make room for next byte
                other = self.bytes_to_int(stream.read(1))
                value += other & 0x7F
                if not other & 0x80:  # done if upper bit is not 1
                    break
        return value

    ## Writes integer value as variable length quantity.
    @staticmethod
    def write_varlen_value(stream, val):
        vlq = []
        for i in range(21, 0, -7):
            if val >= (1 << i):
                vlq.append(((val >> i) & 0x7F) | 0x80)
        vlq.append(val & 0x7F)
        #print("val=", val, "vlq=", vlq)
        #stream.write(bytes(vlq))
        for b in vlq:
            stream.write(MidiFile.int_to_bytes(b, 1))

    def read_meta_message(self, stream):
        metatype = self.bytes_to_int(stream.read(1))
        length = self.read_varlen_value(stream)
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
        raise NotImplementedError(f"read_meta_message: unhandled metatype {hex(metatype)}.")

    def read_channel_message(self, stream, status):
        stat = status & 0xF0
        if mm.kNoteOff <= stat < mm.kProgChange or stat > mm.kChanPress:
            # two data bytes: note off, note on, aftertouch, controller, and pitchbend
            val1 = self.bytes_to_int(stream.read(1))
            val2 = self.bytes_to_int(stream.read(1))
            return [status, val1, val2]
        else:
            # one data byte:  program change, channel pressure
            val1 = self.bytes_to_int(stream.read(1))
            return [status, val1]

    def read_sysex_message(self, stream, status):
        # Note: the length includes the terminal EOE
        length = self.read_varlen_value(stream)
        return [status, length, stream.read(length)]

    def read_message(self, stream):
        # [:1] because peek can return more than one byte
        status = self.bytes_to_int(stream.peek(1)[:1])
        if status & 0x80:
            # have a channel message
            if status < mm.kSysEx:
                self._running_status = status
            stream.read(1)
        else:
            status = self._running_status
            assert status & 0x80, "status byte not found."

        if status < mm.kSysEx:  # a channel message
            return self.read_channel_message(stream, status)
        elif status == mm.kSysEx or status <= mm.kEOE:  # a sysex message
            self._running_status = 0
            return self.read_sysex_message(stream, status)
        elif status == mm.kMetaMsg:  # a meta message
            self._running_status = 0
            return self.read_meta_message(stream)
        else:
            raise NotImplementedError(f"channel status {hex(status)} unsupported.")

    @staticmethod
    def write_message(stream, message):
        status = message[0]
        if status < mm.kSysEx:
            #print("writing", message)
            for b in message:
                stream.write(MidiFile.int_to_bytes(b, 1))
            #stream.write(bytes(message))
        elif status == mm.kMetaMsg:
            stream.write(MidiFile.int_to_bytes(status, 1))
            meta = message[1]
            stream.write(MidiFile.int_to_bytes(meta, 1))
            if mm.kText <= meta <= mm.kDevName or meta == mm.kSeqEvent:
                MidiFile.write_varlen_value(stream, message[2])
                stream.write(message[3])  # a bytes struct
            else:
                for b in message[2:]:
                    stream.write(MidiFile.int_to_bytes(b, 1))
                # stream.write(bytes(message[2:]))
        elif status == mm.kSysEx or status == mm.kEOE:
            stream.write(status)
            MidiFile.write_varlen_value(stream, message[1])
            stream.write(message[2])  # a bytes struct
        else:
            raise NotImplementedError(f"Unsupported message: {message}.")

    def read_track(self, stream, tosecs):
        abs_delta = 0
        # read the length of the track. since this is not dependable we
        # ignore it and use the required EOT message to stop the track.
        self.read_chunk_length(stream, b'MTrk')
        self._running_status = 0
        trk = []
        while True:
            delta = self.read_varlen_value(stream)
            abs_delta += delta
            msg = self.read_message(stream)
            # print(delta, msg)
            # break on EOT, which is required by the midifile spec.
            if mm.is_meta_message_type(msg, mm.kEOT):  # mm.is_meta_eot(msg):
                break
            time = abs_delta / self.divisions if tosecs else abs_delta
            trk.append(me.MidiEvent(msg, time))
        # add the track as a sequence in the midi file
        self.tracks.append(Seq(trk))


    def write_track(self, stream, track, divs, force_tempo=False):
        self.write_chunk_length(stream, b'MTrk', 0)
        # save the begin position of this track.
        track_beg = stream.tell()
        previous_time = 0
        # If force_tempo is True then this is the first track
        # and the user did not provide a tempo marking. In
        # this case write an initial tempo message for mm=60
        if force_tempo:
            MidiFile.write_varlen_value(stream, 0)
            MidiFile.write_message(stream, mm.meta_tempo(1000000))
        for ev in track:
            # convert absolute time to time in ticks.
            delta = int((ev.time - previous_time) * divs)
            #print(delta, "\t", ev.message)
            MidiFile.write_varlen_value(stream, delta)
            MidiFile.write_message(stream, ev.message)
            previous_time = ev.time
        # add a 0 delta and EOT
        MidiFile.write_varlen_value(stream, 0)
        MidiFile.write_message(stream, mm.meta_eot())
        # calculate the length of the track we just wrote
        track_end = stream.tell()
        track_len = track_end - track_beg
        # go to track header's 4-byte length field and write the length
        stream.seek(track_beg - 4)
        stream.write(self.int_to_bytes(track_len, 4))
        # reposition back here to write the next track
        stream.seek(track_end)

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
            length = self.read_chunk_length(stream, b'MThd')
            assert length == 6, "MThd chunk length 6 not found."
            self.level = self.bytes_to_int(stream.read(2))
            tracks = self.bytes_to_int(stream.read(2))
            # read divisions as a two byte signed quantity. if its positive
            # then it represents ticks per quarter. if its negative then its
            # smpte format where the upper byte contains -24, -25 or -30,
            # and the lower byte is positive subframes. Example: millisecond
            # smpte timing would be 0xE728 = -25 40 = 25*40 = 1000ms
            # see http://midi.teragonaudio.com/tech/midifile/mthd.htm
            self.divisions = self.bytes_to_int(stream.read(2), True)
            if self.divisions < 0:
                raise NotImplementedError("Cowardly refusing to import SMPTE format midi file.")
#            print("level=", level, "tracks=", tracks, "divisions=", divisions)
            # process all the tracks in the file
            for _ in range(tracks):
                self.read_track(stream, secs)
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
            self.write_chunk_length(stream, b'MThd', 6)
            stream.write(self.int_to_bytes(level, 2))
            stream.write(self.int_to_bytes(trnum, 2))
            stream.write(self.int_to_bytes(divs, 2))
            force_tempo = False
            # if the first event in the first track is not a
            # tempo event then force tempo==60.
            if not self.tracks[0][0].is_meta(mm.kTempo):
                force_tempo = True
            for t in self.tracks:
                self.write_track(stream, t, divs, force_tempo)
                force_tempo = False

            #self.pathname = pathname
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
    
    # def time_format_type(self):
    #     if self.time_format == 0:
    #         return "beats"
    #     if self.time_format < 0:
    #         return "smpte"
    #     return "ticks"

    # def convert_to_beats(self):
    #     if self.time_format == 0:
    #         return False
    #     scaler = 1 / self.time_format
    #     for s in self.tracks:
    #         for e in s.events:
    #             e.time = e.time * scaler
    #     self.time_format = 0
    #     return True

    # def convert_to_ticks(self, ticks=480):
    #     scaler = ticks if self.time_format == 0 else ticks / self.time_format
    #     for s in self.tracks:
    #         for e in s.events:
    #             e.time = int(e.time * scaler) # FIXME: check Grace to see if it rounds.
    #     self.time_format = ticks
    #     return True

    # def ticks_to_beats(self, val):
    #     return val / self.time_format

    # def beats_to_ticks(self, val):
    #     return int(val * self.time_format)

"""
m = midi.MidiFile()
m = midi.MidiFile("/Users/taube/Classes/205/Resources/reich.mid").read()
m = midi.MidiFile("/Users/taube/Classes/205/Resources/jimmy.mid").read()
m = midi.MidiFile("/Users/taube/Classes/205/Resources/messiaen.mid").read()
m = midi.MidiFile("/Users/taube/Classes/205/Resources/samba.mid").read()
m = midi.MidiFile("/Users/taube/Classes/205/Resources/castles.mid").read()
m = midi.MidiFile("/Users/taube/Classes/205/Resources/tam-tam-1.aiff").read()
"""
