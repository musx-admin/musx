###############################################################################
"""
The paint.py module provides two high-level generators that can produce a wide
variety of interesting textures and music when scheduled as composer functions.
The `brush()` composer outputs MidiNotes in sequential order, similar to how a 
paint brush makes lines on a canvas. In contrast, the `spray()` composer 
generates MidiNotes by applying random selection to its input parameters.

For examples of using paint.py see gamelan.py, blues.py and messiaen.py in
the demos directory.
"""


from musx.generators import cycle, choose
from musx.midi import MidiNote


def brush(sco, *, len=None, end=None, rhy=.5, dur=None, key= 60, amp=.5, chan=0, tuning=1):
    """
    Outputs MidiNotes in sequential order, automatically looping parameter
    list values until the algorithm stops.

    Parameters
    ----------
    sco : Score
        The MidiNotes that are generated will be added to this score.
    len : number
        The number of MIDI events to generate. Either len or end must be
        specified.
    end : number
        An end time after which no more events will be generated.
        Either end or len must be specified.
    rhy : number | list
        A rhythm or list of rhythms that specify the amount of time to wait
        between MIDI events. Negative rhythm values are interpreted as musical
        rests, i.e. events are not output but time advances. The default value
        is 0.5.
    dur : number | list
        A duration or list of durations that specify the amount of time each 
        MIDI event lasts. The default value is the current rhythm.
    key : number | list
        A MIDI key number or list of key numbers to play. The list can contain
        sublists of key numbers; in this case each sublist is treated as a 
        chord (the key numbers in the sublist are performed simultaneously.)
    amp : number | list
        A value or list of values between 0.0 and 1.0 for determining the 
        loudness of the MIDI events.
    chan: number | list
        A MIDI channel number (zero based) or list of channel numbers for MIDI
        events. Channel value 9 will send events to the synthesizer's drum map
        for triggering various percussion sounds.
    tuning: int 
        A value 1 to 16 setting the divisions per semitone used for microtonal
        quantization of floating point keynums. See MidiNote, MidiSeq and the
        micro.py demo file for more information. 
    """
    # user must specify either len or end parameter
    # NB: 'len' is a parameter, for the built-in 'len' use obj.__len__() !
    counter = 0
    if len:
        if end: raise TypeError("specify either leng or end, not both.")
        stopitr = len
        thisitr = (lambda: counter)
    else:
        if not end: raise TypeError("specify either leng or end.")
        stopitr = end
        thisitr = (lambda: sco.elapsed)
    #max( (x.__len__() if type(x) is list else 1) for x in [rhy,dur,key,amp,chan])
    # (lambda: counter < stopitr or sco.now < stopitr)
    # convert all values into cycles
    cyc = (lambda x: cycle(x if type(x) is list else [x]))
    rhy = cyc(rhy)
    dur = cyc(dur)
    key = cyc(key)
    amp = cyc(amp)
    chan = cyc(chan)
    while (thisitr() < stopitr):
        t = sco.now
        #print("counter=", counter, "now=", t)
        r = next(rhy)
        d = next(dur)
        k = next(key)
        a = next(amp)
        c = next(chan)
        if r > 0:
            if not d: d = r
            if type(k) is list:
                for j in k: 
                    m = MidiNote(time=t, dur=d, key=j, amp=a, chan=c, tuning=tuning)
                    sco.add(m)
            else:
                m = MidiNote(time=t, dur=d, key=k, amp=a, chan=c, tuning=tuning)
                sco.add(m)
        counter += 1
        yield abs(r)


def spray(sco, *, len=None, end=None, rhy=.5, dur=None, key= 60, band=0, amp=.5, chan=0, tuning=1):
    """
    Generates MidiNotes using discrete random selection. Most parameters allow
    lists of values to be specified, in which case elements are randomly selected
    from the lists every time an event is output.

    Parameters
    ----------
    Parameters are the same as brush() except for these changes or additions:

    key : number | list
        A MIDI key number or list of key numbers to play. If a list is specified
        a key number is randomly selected from the list for each midi event.

    band : number | list
        A number is treated as a half-step range on either side of the current
        key choice from which the next key number will be chosed.  If a list of
        intervals is specified then randomly selected intervals are added
        added to the current key number to determine the key number played.
        The list can also contain sublists of intervals, in which case each
        sublist is treated as a chord, i.e. the intervals in the sublist are
        added to the current key and performed simultaneously.
    """ 
    # user must specify either len or end parameter
    # NB: 'len' is a parameter, for the built-in 'len' use obj.__len__() !
    counter = 0
    if len:
        if end: raise TypeError("specify either leng or end, not both.")
        stopitr = len
        thisitr = (lambda: counter)
    else:
        if not end: raise TypeError("specify either leng or end.")
        stopitr = end
        thisitr = (lambda: sco.elapsed)
    # convert each param into a chooser pattern.
    ran = (lambda x: choose(x if type(x) is list else [x]))
    rhy = ran(rhy)
    dur = ran(dur)
    key = ran(key)
    amp = ran(amp)
    chan = ran(chan)
    band = choose( [i for i in range(-band, band+1)] if type(band) is int else band )
    while (thisitr() < stopitr):
        t = sco.now
        #print("counter=", counter, "now=", t)
        r = next(rhy)
        d = next(dur)
        k = next(key)
        a = next(amp)
        c = next(chan)
        b = next(band)
        if type(b) is list:
            k = [k+i for i in b]
        else:
            k = k + b
        #print("key=", k, end=" ")
        if r > 0:
            if not d: d = r
            if type(k) is list:
                for j in k:
                    m = MidiNote(time=t, dur=d, key=j, amp=a, chan=c, tuning=tuning)
                    sco.add(m)
            else:
                m = MidiNote(time=t, dur=d, key=k, amp=a, chan=c, tuning=tuning)
                sco.add(m)
        counter += 1
        yield abs(r)
