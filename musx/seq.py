################################################################################
"""
The seq module provide support for reading and writing sequences of Notes.
"""


from .note import Note
from .midi import midievent as me
from .midi import gm
from .tools import rescale
import sys
import time
import threading

class Seq:
    
    def __init__(self, events=[]):
        """
        A time ordered sequence of MidiEvents.

        A Seq is an iterable so its events can be iterated, sliced and 
        mapped, e.g. `for ev in midiseq: print(ev)`.

        Parameters
        ----------
        evs : list
            The initial list of events for the sequence. This intial list
            will not be sorted so its events should already be in proper
            time order.
        """
        # copy user's event list because addevent alters it!
        if isinstance(events, list):
            self.events = events.copy()
        else:
            raise ValueError(f"events is not a list ({events})")

    def __str__(self):
        return f"<Seq: len={len(self)}, endtime={self.endtime()} {hex(id(self))}>"

    __repr__ = __str__

    def __iter__(self):
        return iter(self.events)

    def __getitem__(self, index):
        return self.events[index]  # index can be slice

    def __len__(self):
        return len(self.events)

    def endtime(self):
        """Returns the time of the last event or 0 if there are none."""
        return self.events[-1].time if len(self.events) > 0 else 0

    def clear(self):
        """Removes the current contents of the sequence."""
        self.events = []

    def print(self, start=0, end=None, hints=True):
        """
        Prints the contents of the sequence to the standard output.
        
        Parameters
        ----------
        start : int
            The index of the first event to print.
        end : int
            The index (exclusive) at which to stop printing.
        hints : bool
            If true events are printed with message names.
        """
        if end is None:
            end = len(self.events)
        col1 = len(str(end))
        col2 = len(str(round(self.events[end-1].time, 3)))
        fmat = "{:" + str(col1) + "} {:" + str(col2) + "} {}"
        if hints:
            fmat += "\t# {}"
            for i in range(start, end):
                e = self.events[i]
                print(fmat.format(i, round(e.time, 3), e.message, e.hint()))
        else:
            for i in range(start, end):
                e = self.events[i]
                print(fmat.format(i, round(e.time, 3), e.message))

    def append(self, ev):
        """Adds an event to the end of the sequence without checking time."""
        self.events.append(ev)

    def add(self, e):
        """
        Adds a midi event to the sequence in time sorted order. If the added event
        is a MidiNote it is first converted into a NoteOn and NoteOff pair before
        being added.

        The sorting rules for adding midi events are:

        * an event later than the last event in the sequence is appended to the sequence.
        * a NoteOn is added after all other messages with the same time stamp.
        * a NoteOff is added before all other messages with the same time stamp.
        * all other events are added after NoteOff events with the same time stamp.

        Parameters
        ---------
        e : MidiEvent | MidiNote
            The MidiEvent or MidiNote
        """
        if isinstance(e, Note):
            on = e.noteon()
            off = e.noteoff()
            # print(f"adding noteon {on} to seq, time is {on.time}")
            self.add(on)
            # print(f"adding noteoff {off} to seq, time is {off.time}")
            self.add(off)
            return self
        if e.time > self.endtime():
            self.events.append(e)
            return self
        seqlen = len(self.events)
        if e.is_note_on():
            # note ons come after all other messages at the same time
            i = 0
            # stop when events[i] is stricty larger
            while i < seqlen and self.events[i].time <= e.time:
                i += 1
            # i == seqlen or i.time > e.time
            self.events.insert(i, e)  # inserting at len() ok
        elif e.is_note_off():
            # note offs come before all other messages at the same time
            i = 0
            # stop when events[i] is >= e.time
            while i < seqlen and self.events[i].time < e.time:
                i += 1
            # i == len or i.time == e.time or i.time > e.time
            self.events.insert(i, e)
        else:
            # other messages are inserted after any offs at the same time
            i = 0
            while i < seqlen and self.events[i].time < e.time:
                i += 1
            # i == len or i.time == e.time or i.time > e.time
            while i < seqlen and self.events[i] == e.time and self.events[i].isnoteoff():
                i += 1
            self.events.insert(i, e)
        return self
    
    @classmethod
    def metaseq(cls, tempo=60, timesig=[4,4], keysig=[0,0], ins={}, tuning=1):
        """
        Returns a sequence containing midi meta events declaring the midifile's
        tempo, time signature, key signature, instrument assignments, and 
        channel tuning setup. This meta data can be assigned as track 0
        in a level 1 midifile, or become the initial contents of track 0 
        in a level 0 midi file.

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
            general midi program asignment 0 to 127 (in musx channel and
            program values are zero based, not 1 based). See musx.midi.gm
            for the list of instument constants.
        tuning : int
            A value 1 to 16 setting the divisions per semitone used for
            microtonal quantization of floating point keynums. See MidiNote
            and the micro.py demo file for more information.
        """
        tempo = me.MidiEvent.meta_tempo(tempo)
        if not len(timesig) == 2 and all(isinstance(n, int) for n in timesig):
            raise TypeError(f"invalid timesig: {timesig}.")
        timesig = me.MidiEvent.meta_time_signature(timesig[0], timesig[1])
        insts = {i: gm.AcousticGrandPiano for i in range(16)}
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
        # channel tuning
        if 2 <= tuning <= 16:
            values = cls.channeltuning(tuning)
            for c,v in enumerate(values):
                # calculate the pitch bend value
                b = round(rescale(v, -2,  2,  0, 16383))
                meta.append(me.MidiEvent.pitch_bend(c, b))
        return Seq(meta)

    @staticmethod
    def channeltuning(tuning):
        """
        Internal funtion that converts the tuning value 
        (the number of divisions per semitone) into a 
        sequence of cent values above the standard midi
        key number and then repeatedly assigns the sequence
        across all 16 midi channels.

        Example: if tuning is 2, then the semitone is divided
        into two 50 cent steps [0, .5], this tuning is then
        repeated eight times over the sixteen midi channels
        [0, .5, 0, .5, ... 0, 5] yielding eight pairs of channels
        at indexes 0, 2, 4, ... 14 tuned for quarter tones.

        Parameters
        ----------
        tuning : int 
            The number of divisions per semitone, 1 is semitone,
            2 is quarter tone, etc.

        Returns
        -------
        A sequence of tuning adjustments for all 16 channels.
        """

        tuning = max(1, min(16, tuning))
        cents = [0.0]
        for i in range(1, tuning):
            cents.append(1.0 * i/tuning)
        # return a row of 16 repeating cent values
        return [cents[i % len(cents)] for i in range(16)]

    @staticmethod
    def sounds(insts, at=0):
        """
        Returns a list of up to 16 midi program changes with channel assignments
        starting from channel at.

        Parameters
        ----------
        insts : list
            A list of up to 16 General Midi instrument values.
        at : 0-15
            The starting channel to assign from.
        """
        maxi = len(insts) + at
        if maxi > 15:
            raise ValueError(f"midi channel assignment {maxi} is beyond 15.")
        return [musx.MidiEvent.program_change(c+at, p) for c, p in zip(range(16), insts)]

    @staticmethod   
    def tunings(divs):
        """
        Returns a list of up to 16 midi pitchbends for channel tuning.

        Parameters
        ----------
        divs : int
            An integer 1 to 16 specifying the number of division of the semitone the tuning has.
        """
        if not 1 <= divs <= 16:
            raise ValueError(f"tuning divisions not between 1 and 16 inclusive ({divs})")
        meta = []
        values = Seq.channeltuning(divs)
        for c,v in enumerate(values):
            # calculate the pitch bend value
            b = round(rescale(v, -2,  2,  0, 16383))
            meta.append(me.MidiEvent.pitch_bend(c, b))
        return meta

    def play(self, port, block=True):
        """
        Plays the midi messages in the sequence out an open rtmidi output port.
        The midi data should only contain valid midi channel messages, i.e. no 
        meta or sysex messages.

        Parameters
        ----------
        port : rtmidi.MidiOut
            An open rtimidi MidiOut object.
        block : bool
            If true then play() will block for the duration of the playback.
        """
        if not self.events:
            raise ValueError(f"no midi events to play")
        if not 'rtmidi' in sys.modules:
            raise RuntimeError(f"module rtmidi is not loaded")
        if not isinstance(port, sys.modules['rtmidi'].MidiOut):
            raise TypeError(f"port is not an instance of rtmidi.MidiOut")
        player = threading.Thread(target=_rtplayer, args=(self.events, port))#, daemon=True
        player.start()
        # block until playback  is done.
        if block:
            player.join()


def _rtplayer(midi, port):
    length = len(midi)
    thistime = midi[0].time
    nexttime = thistime
    i = 0
    while i < length:
        if midi[i].time == thistime:
            #print(f'playing {seq[i]}')
            port.send_message(midi[i].message)
            i += 1
            continue
        # if here then midi[i] is later than thistime so sleep
        nexttime = midi[i].time
        #print(f'waiting {nexttime-thistime}')
        time.sleep(nexttime - thistime) 
        thistime = nexttime
