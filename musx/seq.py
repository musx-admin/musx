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
        Note, MidiEvent, or some other user defined Event subclass.

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
        and returns a list of the results returned by the function.

        Parameters
        ----------
        func : Function | lambda
            A function or lambda of one argument, which will receive the
            current event being mapped. The results of calling the function
            will be returned as a list of values.
        """
        return [func(x) for x in self]

    def print(self, start=0, end=None):
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
        _printer = self._midiprinter if isinstance(self.events[0], me.MidiEvent) else self._defaultprinter
        for i in range(start, end):
            e = self.events[i]
            _printer(i, e)

    @staticmethod
    def _defaultprinter(index, event):
        print(index, event.time, event, sep='\t')

    @staticmethod
    def _midiprinter(index, event):
        time = event.time
        str1 = f'{index:4}'    # index position of event in seq
        str2 = f'{time:7.3f}'  # seconds rounded to 3 places in a 7 character pad
        str3 = event.tostring(hint=True) # hint
        print(str1 + "  " + str2 + "  " + str3)


    def append(self, ev):
        """
        Adds an event to the end of the sequence without checking time.
        """
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

    def serialize(self, skiprests=True):
        """
        Iterator that yields consecutive notes, chord members, and optionally, rests.
        """
        for x in self.events:
            try:
                tag = x.tag
                if tag == 'rest' and skiprests:
                    continue
                yield x
                for c in x:
                    yield c
            except AttributeError:
                yield x
