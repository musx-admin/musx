###############################################################################
"""
The paint.py module provides two high-level composers that can produce a wide
variety of interesting textures and music. The `brush()` composer outputs Notes
in sequential order, similar to how a paint brush makes lines on a canvas. In
contrast, the `spray()` composer generates Notes by applying random selection
to its input parameters.

For examples of using paint.py see gamelan.py, blues.py and messiaen.py in
the demos directory.
"""


from musx import Note, cycle, choose


def brush(score, *, length=None, end=None, rhythm=.5, duration=None, pitch=60, amplitude=.5, instrument=0, microdivs=1):
    """
    Outputs Notes in sequential order, automatically looping parameter
    list values until the algorithm stops.

    Parameters
    ----------
    score : Score
        The Notes that are generated will be added to this score.
    length : number
        The number of MIDI events to generate. Either length or end must be
        specified.
    end : number
        An end time after which no more events will be generated.
        Either end or length must be specified.
    rhythm : number | list
        A rhythm or list of rhythms that specify the amount of time to wait
        between notes. Negative rhythm values are interpreted as musical
        rests, i.e. events are not output but time advances. The default value
        is 0.5.
    duration : number | list
        A duration or list of durations that specify the amount of time each 
        MIDI event lasts. The default value is the current rhythm.
    pitch : number | list
        A MIDI key number or list of key numbers to play. The list can contain
        sublists of key numbers; in this case each sublist is treated as a 
        chord (the key numbers in the sublist are performed simultaneously.)
    amplitude : number | list
        A value or list of values between 0.0 and 1.0 for determining the 
        loudness of the MIDI events.
    instrument : number | list
        A MIDI channel number 0 to 15, or a list of channel numbers. Channel 
        value 9 will send events to the synthesizer's drum map for triggering
        various percussion sounds.
    tuning : int 
        A value 1 to 16 setting the divisions per semitone used for microtonal
        quantization of floating point keynums. See Note, Seq and the
        micro.py demo file for more information. 
    """
    # user must specify either length or end parameter
    counter = 0
    if length:
        if end: raise TypeError("specify either length or end, not both.")
        stopitr = length
        thisitr = (lambda: counter)
    else:
        if not end: raise TypeError("specify either length or end.")
        stopitr = end
        thisitr = (lambda: score.elapsed)
    # convert all values into cycles
    cyc = (lambda x: cycle(x if type(x) is list else [x]))
    rhy = cyc(rhythm)
    dur = cyc(duration)
    key = cyc(pitch)
    amp = cyc(amplitude)
    chan = cyc(instrument)
    while (thisitr() < stopitr):
        t = score.now
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
                    m = Note(time=t, duration=d, pitch=j, amplitude=a, instrument=c)
                    score.add(m)
            else:
                m = Note(time=t, duration=d, pitch=k, amplitude=a, instrument=c)
                score.add(m)
        counter += 1
        yield abs(r)


def spray(score, *, length=None, end=None, rhythm=.5, duration=None, pitch= 60, band=0, amplitude=.5, instrument=0):
    """
    Generates Notes using discrete random selection. Most parameters allow
    lists of values to be specified, in which case elements are randomly selected
    from the lists every time an event is output.

    Parameters
    ----------
    Parameters are the same as brush() except for these changes or additions:

    pitch : number | list
        A MIDI key number or list of key numbers to play. If a list is specified
        a key number is randomly selected from the list for each midi event.

    band : number | list
        A number is treated as a half-step range on either side of the current
        key choice from which the next key number will be chosen.  If a list of
        intervals is specified then randomly selected intervals are added
        added to the current key number to determine the key number played.
        The list can also contain sublists of intervals, in which case each
        sublist is treated as a chord, i.e. the intervals in the sublist are
        added to the current key and performed simultaneously.
    """ 
    # user must specify either length or end parameter
    counter = 0
    if length:
        if end: raise TypeError("specify either leng or end, not both.")
        stopitr = length
        thisitr = (lambda: counter)
    else:
        if not end: raise TypeError("specify either length or end.")
        stopitr = end
        thisitr = (lambda: score.elapsed)
    # convert each param into a chooser pattern.
    ran = (lambda x: choose(x if type(x) is list else [x]))
    rhy = ran(rhythm)
    dur = ran(duration)
    key = ran(pitch)
    amp = ran(amplitude)
    chan = ran(instrument)
    band = choose( [i for i in range(-band, band+1)] if type(band) is int else band )
    while (thisitr() < stopitr):
        t = score.now
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
        #print("pitch=", k, end=" ")
        if r > 0:
            if not d: d = r
            if type(k) is list:
                for j in k:
                    m = Note(time=t, duration=d, pitch=j, amplitude=a, instrument=c)
                    score.add(m)
            else:
                m = Note(time=t, duration=d, pitch=k, amplitude=a, instrument=c)
                score.add(m)
        counter += 1
        yield abs(r)
