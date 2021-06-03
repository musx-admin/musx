################################################################################
"""
The seq module provide support for reading and writing sequences of events that
are sorted by time.
"""


import sys
import time
import threading
from .note import Note
from .midi import midievent as me
from .midi import gm
from .tools import rescale


class Seq:
    
    def __init__(self, events=[]):
        """
        A time ordered sequence of Event objects, e.g. instances of
        Note, MidiEvent, or some other user defined subclass.

        A Seq is an iterable so its events can be iterated, sliced and 
        mapped.

        Parameters
        ----------
        events : list
            The initial list of events for the sequence, defaults to an
            empty list. An initial list will not be sorted so its events
            should already be in proper time order.
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

    def map(self, func):
        """
        Maps a function of one argument over all the events in the sequence
        and returns a list of the collected results.

        Parameters
        ----------
        func : Function | lambda
            A function or lambda of one argument, which will receive the
            current event being mapped. The results of calling the function
            will be returned as a list of values.
        """
        return [func(x) for x in self]

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
        for i in range(start, end):
            e = self.events[i]
            print(i, e.time, e, sep='\t')
        # col1 = len(str(end))
        # col2 = len(str(round(self.events[end-1].time, 3)))
        # fmat = "{:" + str(col1) + "} {:" + str(col2) + "} {}"
        # if hints:
        #     fmat += "\t# {}"
        #     for i in range(start, end):
        #         e = self.events[i]
        #         print(fmat.format(i, round(e.time, 3), e.message, e.hint()))
        # else:
        #     for i in range(start, end):
        #         e = self.events[i]
        #         print(fmat.format(i, round(e.time, 3), e.message))

    def append(self, ev):
        """Adds an event to the end of the sequence without checking time."""
        self.events.append(ev)

    def add(self, ev):
        """
        Adds an event to the sequence in time sorted order, with the event
        postioned after any other events with the same time stamp.
        """
        if self.endtime() <= ev.time:
            self.events.append(ev)
        else:
            i = 0; l = len(self.events)
            while i < l and self.events[i].time <= ev.time:
                i += 1
            self.events.insert(i, ev) 
    
#     def play(self, port, block=True):
#         """
#         Plays the midi messages in the sequence out an open rtmidi output port.
#         The midi data should only contain valid midi channel messages, i.e. no 
#         meta or sysex messages.

#         Parameters
#         ----------
#         port : rtmidi.MidiOut
#             An open rtimidi MidiOut object.
#         block : bool
#             If true then play() will block for the duration of the playback.
#         """
#         if not self.events:
#             raise ValueError(f"no midi events to play")
#         if not 'rtmidi' in sys.modules:
#             raise RuntimeError(f"module rtmidi is not loaded")
#         if not isinstance(port, sys.modules['rtmidi'].MidiOut):
#             raise TypeError(f"port is not an instance of rtmidi.MidiOut")
#         player = threading.Thread(target=_rtplayer, args=(self.events, port))#, daemon=True
#         player.start()
#         # block until playback  is done.
#         if block:
#             player.join()


# def _rtplayer(midi, port):
#     length = len(midi)
#     thistime = midi[0].time
#     nexttime = thistime
#     i = 0
#     while i < length:
#         if midi[i].time == thistime:
#             #print(f'playing {seq[i]}')
#             port.send_message(midi[i].message)
#             i += 1
#             continue
#         # if here then midi[i] is later than thistime so sleep
#         nexttime = midi[i].time
#         #print(f'waiting {nexttime-thistime}')
#         time.sleep(nexttime - thistime) 
#         thistime = nexttime
